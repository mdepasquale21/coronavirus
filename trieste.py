import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

matplotlib.rc('xtick', labelsize=5)
matplotlib.rc('ytick', labelsize=5)

# Importing the dataset
dataset = pd.read_csv('./dati/dpc-covid19-ita-province.csv')

################################################################################################################################

print('\nDATA EXPLORATION')
print('\nSHAPE')
print(dataset.shape)
print('\nINFO')
dataset.info()
#print('\nDESCRIPTION')
#print(dataset.describe())
#n_rows_head = 10
#print('\nFIRST ' + str(n_rows_head) + ' ENTRIES')
#print(dataset.head(n_rows_head))
#print('\nMINIMUM VALUES')
#print(dataset.min())
#print('\nMAXIMUM VALUES')
#print(dataset.max())
#print('\nMEAN VALUES')
#print(dataset.mean())

################################################################################################################################

################################################################################################################################
# features = [
#data,stato,codice_regione,denominazione_regione,
#codice_provincia,denominazione_provincia,sigla_provincia,
#lat,long,totale_casi
# ]
################################################################################################################################
# monitoring Trieste
print('\n MONITORING SITUATION IN TRIESTE')

last_date = '2020-03-21 17:00:00'
last_tot_cases = dataset.loc[dataset['data']==last_date][['denominazione_provincia','totale_casi']]

print('\nTotale casi a Trieste')
print(last_tot_cases.loc[last_tot_cases['denominazione_provincia']=='Trieste']['totale_casi'].to_string(index=False))
print('\n')

################################################################################################################################

##############################################################################################################################
# TRIESTE
days = [t[0] for t in enumerate(np.unique(dataset['data']))]
tot_ts = dataset.loc[dataset['denominazione_provincia']=='Trieste']['totale_casi']

plt.xlabel('Time (days after 24/02)')
plt.ylabel('Total Cases')
plt.title('Total Cases in Trieste')
plt.plot(days, tot_ts, c='red', linestyle='-')
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./fvg/ts-total-cases-curve.png', dpi = 250)
plt.clf()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Total Cases')
plt.xticks(rotation=90)
plt.xlabel('Time (days after 24/02)')
plt.title('Total Cases in Trieste')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
for j,f in zip(days, tot_ts):
    plt.bar(j, f, color='red')
plt.tight_layout()
plt.savefig('./fvg/ts-total-cases-barplot.png', dpi=250)
plt.clf()
plt.close()
