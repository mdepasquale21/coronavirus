import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

#models
from sklearn.linear_model import LinearRegression

#import data
dataset = pd.read_csv('./dati/dpc-covid19-ita-andamento-nazionale.csv')

# prepare independent and dependent variables
days = [t[0] for t in enumerate(dataset['data'])]
x = [[days[i]] for i in range(len(days))] #make a 2-D array
log_y= np.log(dataset['totale_casi'])
y = dataset['totale_casi']

################################################################################################################################
#Building the linear regression model
regressor1 = LinearRegression()
regressor2 = LinearRegression()
regressor3 = LinearRegression()
regressor4 = LinearRegression()
regressor5 = LinearRegression()
regressor6 = LinearRegression()
regressor7 = LinearRegression()

regressors = (regressor1,regressor2,regressor3,regressor4,regressor5,regressor6,regressor7)

map = {1:30, 2:25, 3:20, 4:15, 5:10, 6:5, 7:None}

log_y_pred = []
scores = []
growths = []
n0s = []
for reg, i in zip(regressors, range(1, len(regressors)+1)):
    xx = x[:map[i]]
    yy = log_y[:map[i]]
    reg.fit(xx,yy)
    log_y_pred.append(reg.predict(x))
    scores.append(reg.score(x, log_y))  # R2 score
    growths.append(reg.coef_[0]) # coefficients reg.coef_ is an array in general, when fitting multidimensional X values
    n0s.append(reg.intercept_)  # intercepts

colors = ('orange', 'green', 'yellow', 'purple', 'brown', 'grey', 'blue')

#plot of fit vs data
plt.scatter(x,log_y,color = 'red')
for i in range(len(regressors)):
    plt.plot(x,log_y_pred[i],color = colors[i])
#plt.title('Epidemic curve vs Fit')
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Log of Total Cases')
#plt.legend((['fit (R2={:.3f})'.format(score) for score in scores], 'log data'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=4)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./FIT/fit_1_time.png', dpi=250)
plt.tight_layout()
plt.clf()
plt.close()

plt.scatter(x,y,color = 'red')
for i in range(len(regressors)):
    plt.plot(x,np.exp(log_y_pred[i]),color = colors[i])
#plt.title('Epidemic curve vs Fit')
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Total Cases')
#plt.legend((['fit (R2={:.3f})'.format(score) for score in scores], 'data'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=4)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig('./FIT/fit_2_time.png', dpi=250)
plt.clf()
plt.close()

################################################################################################################################
