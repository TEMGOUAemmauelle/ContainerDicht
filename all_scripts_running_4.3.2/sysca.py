import pandas as pd
df = pd.read_csv('syscall_track.csv')
#df2 = df.copy()

columns= ['syscall', 'time']
f = open('net100.txt','r')
donne = f.readlines()

for don in donne:
    if don.find("<") != -1 :
        sysc = don[:don.find("(")]
        if sysc != "sendto" :
            tim = don[don.find("<") + 1:-2]
            value =[sysc, tim]    
            df = pd.concat([df,pd.DataFrame([value], columns = columns)], ignore_index=True)
            df.to_csv('df_new.csv',index=False)
            print(sysc+"   "+tim)
