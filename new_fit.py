import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import seaborn as sns

#models
from sklearn.linear_model import LinearRegression
from lmfit.models import ExponentialModel
from lmfit.models import StepModel

#import data
dataset = pd.read_csv('./dati/dpc-covid19-ita-andamento-nazionale.csv')

################################################################################################################################
# features = [
# data, stato, ricoverati_con_sintomi, terapia_intensiva, totale_ospedalizzati, isolamento_domiciliare,
# totale_attualmente_positivi, nuovi_attualmente_positivi,
# dimessi_guariti, deceduti, totale_casi, tamponi
# ]
################################################################################################################################

# prepare independent and dependent variables
days = [t[0] for t in enumerate(dataset['data'])]
x = [[days[i]] for i in range(len(days))] #make a 2-D array
log_y= np.log(dataset['totale_casi'])
y = dataset['totale_casi']

################################################################################################################################
#Building the linear regression model
regressor = LinearRegression()

regressor.fit(x,log_y)
log_y_pred = regressor.predict(x) # useful for plot

score = regressor.score(x, log_y) # R2 score
growth = regressor.coef_[0] # coefficients reg.coef_ is an array in general, when fitting multidimensional X values
n0 = regressor.intercept_ # intercepts

#plot of fit vs data
plt.scatter(x,log_y,color = 'red')
plt.plot(x,log_y_pred,color = 'blue')
plt.title('Epidemic curve vs Fit')
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Log of Total Cases')
plt.legend(('fit (R2={:.3f})'.format(score), 'log data'),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./FIT/fit_1.png', dpi=250)
plt.clf()

plt.scatter(x,y,color = 'red')
plt.plot(x,np.exp(log_y_pred),color = 'blue')
plt.title('Epidemic curve vs Fit')
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Total Cases')
plt.legend(('fit (R2={:.3f})'.format(score), 'data'),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./FIT/fit_2.png', dpi=250)
plt.clf()
################################################################################################################################

#Building the exponential model
model_exp = ExponentialModel()
params_exp = model_exp.guess(y, x=days)
result_exp = model_exp.fit(y, params_exp, x=days)

#Building the logistic model
model_logistic = StepModel(form='logistic')
params_logistic = model_logistic.guess(y, x=days)
result_logistic = model_logistic.fit(y, params_logistic, x=days)

# plot exponential fit vs logistic fit
plt.scatter(days,y,color='red')
plt.plot(days,result_exp.best_fit,color='blue')
plt.plot(days,result_logistic.best_fit,color='black')
#plt.title('Epidemic curve vs Fit')
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Total Cases')
plt.legend((
"ExponentialModel $\chi^2 = {:.2E}$".format(result_exp.redchi),
"Logistic $\chi^2 = {:.2E}$".format(result_logistic.redchi),
'data'
),loc='upper right', bbox_to_anchor=(1.05, 1.17), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./FIT/fit_3.png', dpi=250)
plt.clf()
