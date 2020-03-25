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
plt.tight_layout()
plt.clf()
plt.close()

plt.scatter(x,y,color = 'red')
plt.plot(x,np.exp(log_y_pred),color = 'blue')
plt.title('Epidemic curve vs Fit')
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Total Cases')
plt.legend(('fit (R2={:.3f})'.format(score), 'data'),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig('./FIT/fit_2.png', dpi=250)
plt.clf()
plt.close()
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
"Exponential $\chi^2 = {:.2E}$".format(result_exp.redchi),
"Logistic $\chi^2 = {:.2E}$".format(result_logistic.redchi),
'data'
),loc='upper right', bbox_to_anchor=(1.05, 1.17), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig('./FIT/fit_3.png', dpi=250)
plt.clf()
plt.close()

#predictions for future days
n_more_days = 10
more_days = [len(days)+i for i in range(1,n_more_days+1)]
prediction_days = np.concatenate((days, more_days), axis=None)

#evaluate params for new days fit
pred_params_exp = model_exp.make_params(decay = result_exp.params["decay"].value,
                                   amplitude = result_exp.params["amplitude"].value)

pred_params_logistic = model_logistic.make_params(sigma = result_logistic.params["sigma"].value,
                                   amplitude = result_logistic.params["amplitude"].value,
                                   center = result_logistic.params["center"].value)

# plot exponential fit vs logistic fit with predictions for new days
plt.scatter(days,y,color='red')
plt.plot(prediction_days, result_exp.eval(pred_params_exp, x=prediction_days),color='blue')
plt.plot(prediction_days, result_logistic.eval(pred_params_logistic, x=prediction_days),color='black')
#plt.title('Epidemic curve vs Fit')
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Total Cases')
plt.legend((
"Exponential $\chi^2 = {:.2E}$".format(result_exp.redchi),
"Logistic $\chi^2 = {:.2E}$".format(result_logistic.redchi),
'data'
),loc='upper right', bbox_to_anchor=(1.05, 1.17), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig('./FIT/fit_4.png', dpi=250)
plt.clf()
plt.close()

#logistic model 5 days ago
n_days = len(days)-5
days_less = days[:n_days]
y_less = y[:n_days]
params_logistic_5_days_ago = model_logistic.guess(y_less, x=days_less)
result_logistic_5_days_ago = model_logistic.fit(y_less, params_logistic_5_days_ago, x=days_less)

pred_params_logistic_5_days_ago = model_logistic.make_params(sigma = result_logistic_5_days_ago.params["sigma"].value,
                                   amplitude = result_logistic_5_days_ago.params["amplitude"].value,
                                   center = result_logistic_5_days_ago.params["center"].value)

# plot logistic fit vs logistic fit 5 days ago
plt.scatter(days,y,color='red')
plt.plot(prediction_days,result_logistic_5_days_ago.eval(pred_params_logistic_5_days_ago, x=prediction_days),color='brown')
plt.plot(prediction_days, result_logistic.eval(pred_params_logistic, x=prediction_days),color='black')
#plt.title('Epidemic curve vs Fit')
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Total Cases')
plt.legend((
"Logistic (5 days ago) $\chi^2 = {:.2E}$".format(result_logistic_5_days_ago.redchi),
"Logistic (now) $\chi^2 = {:.2E}$".format(result_logistic.redchi),
'data'
),loc='upper right', bbox_to_anchor=(1.05, 1.17), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig('./FIT/fit_4_bis.png', dpi=250)
plt.clf()
plt.close()
