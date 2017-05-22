########################################################
### This program takes a DNA (or any string) input #####
### and the length of kmer to find which kmer has  #####
### maximum frequency. In "ATAGGATGGAT", 2-mer "AT" #### 
### occurs maximum times, so that will be returned. ####
########################################################
def findkmer(string, k):
    stringfreq = {}
    for i in range(0, len(string)):
        tmp = string[i:i+k]
        if tmp in stringfreq:
            stringfreq[tmp] += 1
        else:
            stringfreq[tmp] = 1

    highest = max(stringfreq.values())
    maxstring = [key for key, v in stringfreq.items() if v == highest]
    if highest == 1:
        msg = "No most frequent " + str(k) + "mer found." \
                "All are of length 1 :( "
        return msg
    else:
        msg = "The most frequent " + str(k) + "mer" + \
                " are " + ', '.join(maxstring) + \
                ". They occur " + str(highest) + " times."
        return msg


input_str = raw_input("Paste the path of the string you would like to investigate."
                  "Ideally same path as this program: ")
kmer = input("What's the k in your kmer?")

with open(input_str, 'r') as mystr:
    content = mystr.read().replace('\n', '')

print(findkmer(content, kmer))
