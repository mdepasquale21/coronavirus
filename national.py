import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import seaborn as sns

#import data
dataset = pd.read_csv('./dati/dpc-covid19-ita-andamento-nazionale.csv')

print('\nDATA EXPLORATION')
print('\nSHAPE')
print(dataset.shape)
print('\nINFO')
dataset.info()
print('\nDESCRIPTION')
print(dataset.describe())
#n_rows_head = 18
#print('\nFIRST ' + str(n_rows_head) + ' ENTRIES')
#print(dataset.head(n_rows_head))
#print('\nMINIMUM VALUES')
#print(dataset.min())
#print('\nMAXIMUM VALUES')
#print(dataset.max())
#print('\nMEAN VALUES')
#print(dataset.mean())

print('\n DATE, TOT CASES, CURRENTLY INFECTED, NEW INFECTED, HEALED, DECEASED')
print(dataset[
['data', 'totale_casi', 'totale_attualmente_positivi', 'nuovi_attualmente_positivi', 'dimessi_guariti', 'deceduti']
].to_string())

################################################################################################################################
# features = [
# data, stato, ricoverati_con_sintomi, terapia_intensiva, totale_ospedalizzati, isolamento_domiciliare,
# totale_attualmente_positivi, nuovi_attualmente_positivi,
# dimessi_guariti, deceduti, totale_casi, tamponi
# ]
################################################################################################################################

days = [t[0] for t in enumerate(dataset['data'])]

# create scatter plot
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Total Cases')
plt.title('Epidemic curve')
plt.scatter(days, dataset['totale_casi'], c='red')
#plt.scatter(days, dataset['totale_casi'], c='black')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/epidemic-curve.png', dpi = 250)
plt.clf()

plt.xlabel('Time (days after 24/02)')
plt.ylabel('Log of Total Cases')
plt.title('Epidemic curve')
plt.scatter(days, np.log(dataset['totale_casi']), c='red')
plt.legend(('log data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/epidemic-curve-log.png', dpi = 250)
plt.clf()

from sklearn.linear_model import LinearRegression, Ridge, Lasso

x = [[days[i]] for i in range(len(days))] #make a 2-D array
#print(x)
y= np.log(dataset['totale_casi'])

#Building the model
regressor = LinearRegression()
#regressor = Ridge()
#regressor = Lasso()

# train on data without last few days
minus_last_days_to_skip = -1
x_train = x[:minus_last_days_to_skip]
x_test = x[minus_last_days_to_skip:]
y_train = y[:minus_last_days_to_skip]
y_test = y[minus_last_days_to_skip:]

regressor.fit(x_train,y_train)
Y_pred_train = regressor.predict(x_train) # useful for plot
Y_pred_test = regressor.predict(x_test)

join_x = np.concatenate((x_train, x_test), axis=None)
join_y = np.concatenate((y_train, y_test), axis=None)
join_pred = np.concatenate((Y_pred_train, Y_pred_test), axis=None)

score = regressor.score(join_x[:, np.newaxis], join_y) # R2 score
growth = regressor.coef_[0] # coefficients reg.coef_ is an array in general, when fitting multidimensional X values
n0 = regressor.intercept_ # intercepts

print('\nSCORE:\n', score)
#print('Y TRUE - Y PREDICTED DIFFERENCES:\n', y - Y_pred_train) # difference between true and predicted values
print('COEFFICIENT:\n', growth)
print('INTERCEPT:\n', n0)

#plot of fit vs data
plt.scatter(join_x,join_y,color = 'red')
plt.plot(join_x,join_pred,color = 'blue')
plt.title('Epidemic curve vs Fit')
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Log of Total Cases')
plt.legend(('fit (R2={:.3f})'.format(score), 'log data'),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/epidemic-curve-fit-TRAIN.png', dpi=250)
plt.clf()

plt.scatter(join_x,np.exp(join_y),color = 'red')
plt.plot(join_x,np.exp(join_pred),color = 'blue')
plt.title('Epidemic curve vs Fit')
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Total Cases')
plt.legend(('fit (R2={:.3f})'.format(score), 'data'),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/epidemic-curve-fit-TRAIN-2.png', dpi=250)
plt.clf()

last = len(dataset['totale_casi'])
print('\nEXPONENTIAL PREDICTION FOR DAY',last)
pred = regressor.predict([[last]])
print(pred)
print('number of predicted cases', np.exp(pred))

################################################################################################################################

# new infected
plt.xlabel('Time (days after 24/02)')
plt.ylabel('New Infected')
plt.title('New infected curve')
plt.scatter(days, dataset['nuovi_attualmente_positivi'], c='orange')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/new-infected-curve.png', dpi = 250)
plt.clf()

# healed people
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Healed')
plt.title('Healed curve')
plt.scatter(days, dataset['dimessi_guariti'], c='green')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/healed-curve.png', dpi = 250)
plt.clf()

# deceased people
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Deceased')
plt.title('Deceased curve')
plt.scatter(days, dataset['deceduti'], c='blueviolet')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/deceased-curve.png', dpi = 250)
plt.clf()

################################################################################################################################

#everything
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Values')
#plt.title('All curves')
plt.plot(days, dataset['totale_casi'], c='red', linestyle='-')
plt.plot(days, dataset['nuovi_attualmente_positivi'], c='orange', linestyle='-')
plt.plot(days, dataset['dimessi_guariti'], c='green', linestyle='-')
plt.plot(days, dataset['deceduti'], c='blueviolet', linestyle='-')
plt.legend(('Total Cases','New Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/all-curves.png', dpi = 250)
plt.clf()

# new positives, healed, deceased
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Values')
plt.plot(days, dataset['nuovi_attualmente_positivi'], c='orange', linestyle='-')
plt.plot(days, dataset['dimessi_guariti'], c='green', linestyle='-')
plt.plot(days, dataset['deceduti'], c='blueviolet', linestyle='-')
plt.legend(('New Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=3)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/almost-all-curves.png', dpi = 250)
plt.clf()

print('\ntotale_casi = totale_attualmente_positivi + dimessi_guariti + deceduti\n')

#total cases and total currently positive
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Values')
plt.plot(days, dataset['totale_casi'], c='red', linestyle='-')
plt.plot(days, dataset['totale_attualmente_positivi'], c='pink', linestyle='-')
plt.plot(days, dataset['nuovi_attualmente_positivi'], c='orange', linestyle='-')
plt.plot(days, dataset['dimessi_guariti'], c='green', linestyle='-')
plt.plot(days, dataset['deceduti'], c='blueviolet', linestyle='-')
plt.legend(('Total Cases','Currently Infected','New Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=3)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/all-case-all-current-curves.png', dpi = 250)
plt.clf()

################################################################################################################################

# fatality rate
fatality_rate_1 = dataset['deceduti']/dataset['totale_casi']
fatality_rate_2 = dataset['deceduti']/(dataset['deceduti'] + dataset['dimessi_guariti'])
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Fatality Rate')
plt.plot(days, fatality_rate_1, c='darkslateblue', linestyle='-')
plt.plot(days, fatality_rate_2, c='saddlebrown', linestyle='-')
plt.legend(('dec/tot.cases','dec/(dec+heal)'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/fatality-rate.png', dpi = 250)
plt.clf()

# outcome of closed cases (%)
recovery_rate = dataset['dimessi_guariti']/(dataset['deceduti'] + dataset['dimessi_guariti'])
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Recovery vs Fatality Rate (%)')
plt.plot(days, recovery_rate, c='limegreen', linestyle='-')
plt.plot(days, fatality_rate_2, c='saddlebrown', linestyle='-')
plt.legend(('heal/(dec+heal)','dec/(dec+heal)'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/outcome-closed-cases.png', dpi = 250)
plt.clf()

# calculate growth factor
growth_factor = []

for i, _ in enumerate(dataset['totale_casi']):
    if(i < 2):
        print('\nCalculating growth factors: skipping index',i)
    else:
        n2 = dataset['totale_casi'].iloc[i]
        n1 = dataset['totale_casi'].iloc[i-1]
        n0 = dataset['totale_casi'].iloc[i-2]
        growth_factor.append((n2-n1)/(n1-n0))

print('\ngrowth factors day by day')
print(growth_factor)

# growth factor
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Growth Factor')
plt.title('Growth Factor [dN(t+1)/dN(t)]')
plt.plot(days[2:], growth_factor, 'ko')
plt.plot(days[2:], growth_factor, color='grey', linestyle='--')
#plt.legend(('data','linked'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/growth-factor.png', dpi = 250)
plt.clf()

# calculate growth rate
growth_rate = []

for i, _ in enumerate(dataset['totale_casi']):
    if(i < 1):
        print('\nCalculating growth rates: skipping index',i)
    else:
        n2 = dataset['totale_casi'].iloc[i]
        n1 = dataset['totale_casi'].iloc[i-1]
        growth_rate.append(((n2-n1)/n1)*100.0)

print('\ngrowth rates % day by day')
print(growth_rate)

# growth rate
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Growth Rate %')
plt.title('Growth Rate [(N(t+1)-N(t))/N(t)]x100')
plt.plot(days[1:], growth_rate, 'bo')
plt.plot(days[1:], growth_rate, color='cyan', linestyle='--')
#plt.legend(('data','linked'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/growth-rate.png', dpi = 250)
plt.clf()
