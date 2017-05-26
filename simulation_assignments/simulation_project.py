import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
%matplotlib inline


###Simulate the shifted gamma pdf

s = 0.31
r = 0.41

raw_time = np.linspace(0.000001,15,200)

shifted_gamma = ((r**s)*np.exp(-r*(raw_time-1.0/120))*(raw_time-1.0/120)**(s-1))/gamma(s)

plt.xlim(0,15)
plt.xlabel("Flight times (in hours)")
plt.suptitle("PDF of $r^s(y^{s-1}e^{-ry})/\Gamma(s)$ with $r=0.41h^{-1}, s=0.31$", fontsize=16)
plt.plot(raw_time, shifted_gamma, lw=3)


###Normalize probabilties

probabilities= shifted_gamma
prob = sum(probabilities) 
c = (1.0)/prob 
probabilities = map(lambda x: c*x, probabilities)
flight_times = np.random.choice(raw_time, 1400, p=probabilities)


###Convert flight times into seconds
flight_times_sec = flight_times*3600
sorted_times = np.sort(flight_times_sec)

###Plot histogram of pseudo data
plt.xlabel("Flight times (in seconds)", fontsize=16)
plt.ylabel("Total number of flights", fontsize=16)
plt.suptitle("Pseudo data generated after sampling from PDF", fontsize=18)
plt.hist(sorted_times)

###Convert flight times into records
integer_times = [np.int(i)/10 for i in sorted_times]



###Function definitions that go into the integrals
def shift_gamma(x,rl,sl):
    return ((rl**sl)*np.exp(-rl*(x-1.0/120))*(x-1.0/120)**(sl-1))/gamma(sl)

def shift_gamma2(x,j,rl,sl):
    return (j-(x/10))*((rl**sl)*np.exp(-rl*(x-1.0/120))*(x-1.0/120)**(sl-1))/gamma(sl)

def shift_gamma3(x,j,rl,sl):
    return (x/10-j)*((rl**sl)*np.exp(-rl*(x-1.0/120))*(x-1.0/120)**(sl-1))/gamma(sl)

def shift_gamma4(x,j,rl,sl):
    return x*((rl**sl)*np.exp(-rl*(x-1.0/120))*(x-1.0/120)**(sl-1))/gamma(sl)


N = len(integer_times)


###Log-likelihood function
def calc_likelihood(integer_times,r,s):
    sum_multinomial = []
    for j in integer_times:

        sum_multinomial.append(np.log((integrate.quad(shift_gamma,10*(j-1),10*(j+1),args=(r,s))[0] - 
                            integrate.quad(shift_gamma2,10*(j-1),10*(j),args=(j,r,s))[0] - 
                            integrate.quad(shift_gamma3,10*(j),10*(j+1),args=(j,r,s))[0])))


    term_subtract = np.log(1- (4*integrate.quad(shift_gamma,30,40,args=(r,s))[0] - 
                                              0.1*integrate.quad(shift_gamma4,30,40,args=(j,r,s)[0]))
    #print(np.sum(sum_multinomial))
    #print(term_subtract)
    return N*(np.sum(sum_multinomial) - term_subtract)


###Define values of r & s to observe the behavior of function with respect to them
r_array = np.linspace(0.1/3600,1.3/3600,100)
s_array = np.linspace(0.1,1.9,100)

likelihood_wrt_r = []
likelihood_wrt_s = []

###Calculate funtion's behavior based on r and s values
for s_gl in s_array:
    likelihood_wrt_s.append(calc_likelihood(integer_times, 0.41/3600, s_gl))
    
for r_gl in s_array:
    likelihood_wrt_r.append(calc_likelihood(integer_times, r_gl, 0.31))


###Plot behavior
plt.xlabel("shape parameter $s$",fontsize=16)
plt.ylabel("$Log-likelihood: l(\ttheta|r)$",fontsize=16)
plt.suptitle("Behavior of likelihood function with respect to shape parameter", fontsize=14)
plt.plot(s_array, likelihood_values)

plt.xlabel("rate parameter $r$",fontsize=16)
plt.ylabel("$Log-likelihood: l(\ttheta|r)$",fontsize=16)
plt.suptitle("Behavior of likelihood function with respect to rate parameter", fontsize=14)
plt.plot(r_array, likelihood_values)



###Prediction of parameter values using statsmodel's GenericLikelihoodModel
from statsmodels.base.model import GenericLikelihoodModel
class Gamma(GenericLikelihoodModel):
    
    
    def __init__(self,endog):
         super(Gamma, self).__init__(endog)
        
    def loglike(self, params):
        rp = params[0]
        sp = params[1]
        return calc_likelihood(self.endog, rp, sp)
        
    def fit(self, start_params=np.array([0.11/3600,0.51])):
        return super(Gamma, self).fit(start_params=start_params)
        

model = Gamma(integer_times)
results = model.fit()


###Get parameters and print other info like std error and 95% CI
r1, s1 = results.params
print(r1, s1)
results.df_model = len(np.array([0.41/3600,0.31]))
results.df_resid = len(integer_times) - len(params)
results.df_resid = len(integer_times) - len(results.params)
results.summary()