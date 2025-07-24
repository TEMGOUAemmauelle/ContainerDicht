import pandas as pd

df1 = pd.read_csv('df_new.csv')
df2 = pd.read_csv('miki.csv')
columns= ['syscall', 'total_time', 'occur']

tot = 0

for x in df1['syscall'].unique() :
    val = df1[df1['syscall'] == x].time.sum()
    occ = df1[df1['syscall'] == x].time.count()
    value =[x, val, occ]
    df2 = pd.concat([df2,pd.DataFrame([value], columns = columns)], ignore_index=True)
    df2.to_csv('df_new_final.csv',index=False)
    tot = tot + val
    print(value)
    
    

print(tot)
      
