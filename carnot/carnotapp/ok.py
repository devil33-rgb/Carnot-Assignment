# meet authentication 
#vne-vnkf-tzk
# 1st part stands for country 
# 2nd part stands for the data and time 
# 3rd part stands for permission 


def lcsubstr(str1,str2):
    ans = 0
    for i in range(len(str1)):
        for j in range(len(str2)):
            k=0
            while ((i+k)< len(str1) and (j+k)<len(str2) and str[i+k]==str[j+k]):
                k+=1
            ans = max(ans,k)
    return ans
        