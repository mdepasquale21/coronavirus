import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

#models
from sklearn.linear_model import LinearRegression

matplotlib.rcParams.update({'font.size': 6})

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
regressor8 = LinearRegression()

regressors = (regressor1,regressor2,regressor3,regressor4,regressor5, regressor6, regressor7, regressor8)

map = {1:-49, 2:-42, 3:-35, 4:-28, 5:-21, 6:-14, 7:-7, 8:None}

log_y_pred = []
scores = []
growths = []
n0s = []
for reg, i in zip(regressors, range(1, len(regressors)+1)):
    xx = x[:map[i]]
    yy = log_y[:map[i]]
    reg.fit(xx,yy)
    log_y_pred.append(reg.predict(x))
    scores.append(reg.score(xx, yy))  # R2 score
    growths.append(reg.coef_[0]) # coefficients reg.coef_ is an array in general, when fitting multidimensional X values
    n0s.append(reg.intercept_)  # intercepts

colors = ('yellow','pink', 'orange', 'grey', 'green', 'purple', 'brown', 'blue')

#plot of fit vs data
plt.scatter(x,log_y,color = 'red')
for i in range(len(regressors)):
    plt.plot(x,log_y_pred[i],color = colors[i])
#plt.title('Epidemic curve vs Fit')
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Log of Total Cases')
plt.legend((
'7 weeks ago (R2={:.3f})'.format(scores[0]),
'6 weeks ago (R2={:.3f})'.format(scores[1]),
'5 weeks ago (R2={:.3f})'.format(scores[2]),
'4 weeks ago (R2={:.3f})'.format(scores[3]),
'3 weeks ago (R2={:.3f})'.format(scores[4]),
'2 weeks ago (R2={:.3f})'.format(scores[5]),
'1 week ago  (R2={:.3f})'.format(scores[6]),
'today (R2={:.3f})'.format(scores[7]),
'log data'),
loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=4)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./FIT2/fit_1_time.png', dpi=250)
plt.tight_layout()
plt.clf()
plt.close()

plt.scatter(x,y,color = 'red')
for i in range(len(regressors)):
    plt.plot(x,np.exp(log_y_pred[i]),color = colors[i])
#plt.title('Epidemic curve vs Fit')
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Total Cases')
plt.ylim([0,1000000])
plt.legend((
'7 weeks ago (R2={:.3f})'.format(scores[0]),
'6 weeks ago (R2={:.3f})'.format(scores[1]),
'5 weeks ago (R2={:.3f})'.format(scores[2]),
'4 weeks ago (R2={:.3f})'.format(scores[3]),
'3 weeks ago (R2={:.3f})'.format(scores[4]),
'2 weeks ago (R2={:.3f})'.format(scores[5]),
'1 week ago  (R2={:.3f})'.format(scores[6]),
'today (R2={:.3f})'.format(scores[7]),
'data'),
loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=4)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig('./FIT2/fit_2_time.png', dpi=250)
plt.clf()
plt.close()

################################################################################################################################

weeks = [i for i in range(len(regressors))]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.scatter(weeks, growths, s=85, c='orange')
for i, txt in enumerate(growths):
    #ax.annotate(txt, (weeks[i], growths[i]))
    ax.annotate('{:.3f}'.format(txt), (weeks[i], growths[i]))
plt.xlabel('Time (weeks after feb)')
plt.ylabel('Coefficient of LR')
plt.title('Exponential growth in time')
plt.savefig('./FIT2/time_vs_coeff.png', dpi = 250)
plt.clf()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.scatter(weeks, scores, s=85, c='yellow')
for i, txt in enumerate(scores):
    #ax.annotate(txt, (weeks[i], scores[i]))
    ax.annotate('{:.3f}'.format(txt), (weeks[i], scores[i]))
plt.xlabel('Time (weeks after feb)')
plt.ylabel('R2 Score')
plt.title('R2 score of exponential in time')
plt.savefig('./FIT2/time_vs_scores.png', dpi = 250)
plt.clf()
