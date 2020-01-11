import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np
import random
with open('data4000.data','w') as f:
    f.write('col_1:I,col_2:I,col_3:I,col_4:C,col_5:C,clo_6:T\n')
    for i in range(0,1000):
        if random.random()>0.95:
            i_1 = random.randint(1,1000)
            i_2 = random.randint(1,1000)
            i_3 = random.randint(1,1000)
            sym = random.choice(['v','o'])
            colors = random.choices(['RED','GREEN','BLUE','YELLOW'],k=4)
            label = 0
        else:
            label = 1
            i_1 = random.randint(i-20,i+20)
            i_2 = random.randint(i-20,i+20)
            i_3 = random.randint(i-20,i+20)
            if random.random()>0.95:
                sym = random.choice(['v','o'])
                label = 0 
            else:
                sym = "v" if i<500 else 'o'
            if random.random()>0.95:
                label =0
                colors = random.choices(['RED','GREEN','BLUE','YELLOW'],k=4)
            else:
                colors = ['RED','GREEN','BLUE','YELLOW']
            

        f.write('{col1},{col2},{col3},{col4},{col5},{col6}\n'.format(col1=i_1,col2=i_2,col3=i_3,col4=colors[0],col5=sym,col6=label))  
        f.write('{col1},{col2},{col3},{col4},{col5},{col6}\n'.format(col1=i_1,col2=1000-i_2,col3=i_3,col4=colors[1],col5=sym,col6=label)) 
        f.write('{col1},{col2},{col3},{col4},{col5},{col6}\n'.format(col1=i_1,col2=i_2,col3=1000-i_3,col4=colors[2],col5=sym,col6=label))
        f.write('{col1},{col2},{col3},{col4},{col5},{col6}\n'.format(col1=1000-i_1,col2=i_2,col3=i_3,col4=colors[3],col5=sym,col6=label))
    
data = pd.read_csv('data4000.data').values
x = data[:,0].astype(np.int)
y = data[:,1].astype(np.int)
z = data[:,2].astype(np.int)
color = data[:,3]
marker =data[:,4]
fig = plt.figure()
 
# 将二维转化为三维
axes3d = Axes3D(fig)
for i in range(len(x)):
    axes3d.scatter(x[i],y[i],z[i],c=color[i],marker=marker[i])

# 效果相同
