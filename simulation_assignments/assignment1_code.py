#Import all libraries
import os
import matplotlib.pyplot as plt
import numpy as np
import random

#Initialize all variables and parameters
M = 2048
a1= 1229
a2= 1231
c = 1
x0=7.0 
y0= (a1*x0+c)%M
 
#run the linear congruential generator 
def linear_generator():
    x0=7.0 
    y0= (a1*x0+c)%M
    table = []
    array1 = [x0/M]
    array2 = [y0/M]
    

    for i in range(1000):
        x1= (a1*x0 + c)%M
        y1= (a1*y0 + c)%M
        array1.append(x1/M)
        array2.append(y1/M)
        T = (1.0/M)*(x1 + (1.0/M)*y1)
        table.append(T)
        x0=x1
        y0=y1
    return array1, array2, table

#Store the arrays and the shuffle table spit out by linear congruential generator
x,y,table = linear_generator()



#random generator using python's random module
def random_generator_plot():
    x3= np.random.random(1000)
    x4= np.random.random(1000)
    
    covariance = np.cov(np.transpose(x3), np.transpose(x4))
    plt.plot(x3,x4, "bo") 
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.suptitle("plotting X and Y values received from python's random number generator", fontsize=16)
    plt.show()
    return covariance



#calculate the mean for x and y values
x_mean = np.mean(x)
y_mean = np.mean(y)



#seeds for next set of equations used for creating the shuffle table
xk = x[-1]
yk = y[-1]

w_table= []

def shuffler():
    z0= (a2*y0+c)%M
    for i in range(1000):
        z1= int((1231*z0 + c)%M)
        w= table[z1%1000]
        w_table.append(w/M)   
        xl= (1229*xk + c)%M
        yl= (1229*yk + c)%M
        T = (1.0/M)*(xl + (1.0/M)*yl)
        table[z1%1000]= T
        z0=z1
    return w_table 


#Create a plot of shuffle table values
def plot_w():
     w_array1 = []
     w_array2 = []
     sum = 0
     #calculating covariant using equations(without numpy)
     for i in range(1, len(w_table)):
        w_array1.append(w_table[i])
        w_array2.append(w_table[i-1])
     
     
     w1_mean = np.mean(w_array1)
     w2_mean = np.mean(w_array2)
    
     for i in range(0, len(w_array1)):
             sum += (w_array1[i] - w1_mean) * (w_array2[i] - w2_mean)
     
     covariance2 = sum/(len(w_array1)-1)

     #using np covariant function
     #covariance2 = np.cov(np.transpose(w_table[0:len(w_table)-1]), np.transpose(w_table[1:]))

     plt.plot(w_table[0:len(w_table)-1],w_table[1:], "bo") 
     plt.xlabel("W(i) values")
     plt.ylabel("W(i-1) values")
     plt.suptitle("plotting w(i) and w(i-1) after using shuffle table", fontsize=18)
     plt.show()
     return covariance2
 
#funtion that finds covariance
def find_covariance(x,y):
    sum = 0
    for i in range(0, len(x)):
        sum += (x[i] - x_mean) * (y[i] - y_mean)

    covariance = sum/(len(x)-1)
    return covariance



#plot the x and y values

#plt.plot(x, y, "bo")
#plt.xlabel("X values")
#plt.ylabel("Y values")
#plt.suptitle("plotting x and y values without shuffle table", fontsize=18)
#plt.show()



#Store shuffle table values(w0,w1...) and run the shuffle table plot
#w_table= shuffler()
covariance_w = plot_w()
print(covariance_w)

#Plot the values received from python's r.n.g
#covariance_rn = random_generator_plot()
#print covariance_rn[0]
