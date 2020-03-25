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
].to_string(index=False))

# Write national report to file
report = open("./covid-19-national-report.txt", "w")
report.write("REPORT of DATE, TOT CASES, CURRENTLY INFECTED, NEW INFECTED, HEALED, DECEASED\n")
report.write(dataset[
['data', 'totale_casi', 'totale_attualmente_positivi', 'nuovi_attualmente_positivi', 'dimessi_guariti', 'deceduti']
].to_string(index=False))
report.close()

################################################################################################################################
# features = [
# data, stato, ricoverati_con_sintomi, terapia_intensiva, totale_ospedalizzati, isolamento_domiciliare,
# totale_attualmente_positivi, nuovi_attualmente_positivi,
# dimessi_guariti, deceduti, totale_casi, tamponi
# ]
################################################################################################################################

days = [t[0] for t in enumerate(dataset['data'])]

# total cases
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Total Cases')
plt.title('Epidemic curve')
plt.scatter(days, dataset['totale_casi'], c='red')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curve-total-cases.png', dpi = 250)
plt.clf()

# new infected
plt.xlabel('Time (days after 24/02)')
plt.ylabel('New Infected')
plt.title('New infected curve')
plt.scatter(days, dataset['nuovi_attualmente_positivi'], c='orange')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curve-new-infected.png', dpi = 250)
plt.clf()

# healed people
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Healed')
plt.title('Healed curve')
plt.scatter(days, dataset['dimessi_guariti'], c='green')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curve-healed.png', dpi = 250)
plt.clf()

# deceased people
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Deceased')
plt.title('Deceased curve')
plt.scatter(days, dataset['deceduti'], c='blueviolet')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curve-deceased.png', dpi = 250)
plt.clf()

################################################################################################################################

# new positives, healed, deceased
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Values')
plt.plot(days, dataset['nuovi_attualmente_positivi'], c='orange', linestyle='-')
plt.plot(days, dataset['dimessi_guariti'], c='green', linestyle='-')
plt.plot(days, dataset['deceduti'], c='blueviolet', linestyle='-')
plt.legend(('New Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=3)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curves-almost.png', dpi = 250)
plt.clf()

print('\ntotale_casi = totale_attualmente_positivi + dimessi_guariti + deceduti\n')

#total cases and total currently positive
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Values')
plt.plot(days, dataset['totale_casi'], c='red', linestyle='-')
plt.plot(days, dataset['totale_attualmente_positivi'], c='pink', linestyle='-')
plt.plot(days, dataset['dimessi_guariti'], c='green', linestyle='-')
plt.plot(days, dataset['deceduti'], c='blueviolet', linestyle='-')
plt.legend(('Total Cases','Currently Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curves-all.png', dpi = 250)
plt.clf()

################################################################################################################################

# fatality rate
fatality_rate_1 = dataset['deceduti']/dataset['totale_casi']
fatality_rate_2 = dataset['deceduti']/(dataset['deceduti'] + dataset['dimessi_guariti'])
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Fatality Rate (%)')
plt.plot(days, fatality_rate_1*100, c='darkslateblue', linestyle='-')
plt.plot(days, fatality_rate_2*100, c='saddlebrown', linestyle='-')
plt.legend(('% dec/tot.cases','% dec/(dec+heal)'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/fatality-rate.png', dpi = 250)
plt.clf()

# outcome of closed cases (%)
recovery_rate = dataset['dimessi_guariti']/(dataset['deceduti'] + dataset['dimessi_guariti'])
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Recovery vs Fatality Rate (%)')
plt.plot(days, recovery_rate*100, c='limegreen', linestyle='-')
plt.plot(days, fatality_rate_2*100, c='saddlebrown', linestyle='-')
plt.legend(('% heal/(dec+heal)','% dec/(dec+heal)'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
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
plt.ylabel('Growth Rate (%)')
plt.title('Growth Rate [(N(t+1)-N(t))/N(t)]x100')
plt.plot(days[1:], growth_rate, 'bo')
plt.plot(days[1:], growth_rate, color='cyan', linestyle='--')
#plt.legend(('data','linked'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/growth-rate.png', dpi = 250)
plt.clf()
