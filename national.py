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
#n_rows_head = 10
#print('\nLAST ' + str(n_rows_head) + ' ENTRIES')
#print(dataset.tail(n_rows_head).to_string(index=False))
#print('\nMINIMUM VALUES')
#print(dataset.min())
#print('\nMAXIMUM VALUES')
#print(dataset.max())
#print('\nMEAN VALUES')
#print(dataset.mean())

print('\n DATE, TOT CASES, CURRENTLY INFECTED, NEW INFECTED, VARIATION OF TOTAL INFECTED, HEALED, DECEASED')
print(dataset[
['data', 'totale_casi', 'totale_positivi', 'nuovi_positivi', 'variazione_totale_positivi', 'dimessi_guariti', 'deceduti']
].to_string(index=False))

# Write national report to file
report = open("./covid-19-national-report.txt", "w")
report.write("REPORT of DATE, TOT CASES, CURRENTLY INFECTED, NEW INFECTED, VARIATION OF TOTAL INFECTED, HEALED, DECEASED\n")
report.write(dataset[
['data', 'totale_casi', 'totale_positivi', 'nuovi_positivi', 'variazione_totale_positivi', 'dimessi_guariti', 'deceduti']
].to_string(index=False))
report.close()

################################################################################################################################
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
plt.scatter(days, dataset['nuovi_positivi'], c='orange')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curve-new-infected.png', dpi = 250)
plt.clf()

# total variations of infected
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Total variations of Infected')
plt.title('Total variations of infected curve')
plt.scatter(days, dataset['variazione_totale_positivi'], c='grey')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curve-variations-of-infected.png', dpi = 250)
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

new_healed = []
new_deceased = []

for i in range(len(dataset)):
    if(i < 1):
        new_healed.append(
        dataset['dimessi_guariti'].iloc[i]
        )
        new_deceased.append(
        dataset['deceduti'].iloc[i]
        )
    else:
        #otherwise calculate daily healed and deceased
        new_healed.append(
        dataset['dimessi_guariti'].iloc[i]-dataset['dimessi_guariti'].iloc[i-1]
        )
        new_deceased.append(
        dataset['deceduti'].iloc[i]-dataset['deceduti'].iloc[i-1]
        )


print('\nBILANCIO DI IERI')
print('NUOVI POSITIVI')
print(dataset['nuovi_positivi'].iloc[-2])
print('NUOVI GUARITI')
print(new_healed[-2])
print('NUOVI DECEDUTI')
print(new_deceased[-2])
print('VARIAZIONE TOTALE POSITIVI')
print(dataset['variazione_totale_positivi'].iloc[-2])

print('\nBILANCIO DI OGGI')
print('NUOVI POSITIVI')
print(dataset['nuovi_positivi'].iloc[-1])
print('NUOVI GUARITI')
print(new_healed[-1])
print('NUOVI DECEDUTI')
print(new_deceased[-1])
print('VARIAZIONE TOTALE POSITIVI')
print(dataset['variazione_totale_positivi'].iloc[-1])

# Write bilancio to file
report = open("./covid-19-bilancio-nazionale.txt", "w")
report.write('\nBILANCIO DI IERI')
report.write('\nNUOVI POSITIVI\n')
report.write(str(dataset['nuovi_positivi'].iloc[-2]))
report.write('\nNUOVI GUARITI\n')
report.write(str(new_healed[-2]))
report.write('\nNUOVI DECEDUTI\n')
report.write(str(new_deceased[-2]))
report.write('\nVARIAZIONE TOTALE POSITIVI\n')
report.write(str(dataset['variazione_totale_positivi'].iloc[-2]))
report.write('\n\nBILANCIO DI OGGI')
report.write('\nNUOVI POSITIVI\n')
report.write(str(dataset['nuovi_positivi'].iloc[-1]))
report.write('\nNUOVI GUARITI\n')
report.write(str(new_healed[-1]))
report.write('\nNUOVI DECEDUTI\n')
report.write(str(new_deceased[-1]))
report.write('\nVARIAZIONE TOTALE POSITIVI\n')
report.write(str(dataset['variazione_totale_positivi'].iloc[-1]))
report.close()

# new positives, healed, deceased
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Values')
plt.plot(days, dataset['nuovi_positivi'], c='orange', linestyle='-')
plt.plot(days, new_healed, c='limegreen', linestyle='-')
plt.plot(days, new_deceased, c='purple', linestyle='-')
plt.plot(days, dataset['variazione_totale_positivi'], c='grey',  linestyle='-')
plt.legend(('New Infected','New Healed','New Deceased', 'Total Variation of Infected'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curves-almost.png', dpi = 250)
plt.clf()

print('\ntotale_casi = totale_positivi + dimessi_guariti + deceduti\n')
print('\nvariazione_totale_positivi = nuovi_positivi - dimessi_guariti_oggi - deceduti_oggi\n')

#total cases and total currently positive
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Values')
plt.plot(days, dataset['totale_casi'], c='red', linestyle='-')
plt.plot(days, dataset['totale_positivi'], c='pink', linestyle='-')
plt.plot(days, dataset['dimessi_guariti'], c='green', linestyle='-')
plt.plot(days, dataset['deceduti'], c='blueviolet', linestyle='-')
plt.legend(('Total Cases','Currently Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curves-all.png', dpi = 250)
plt.clf()

#tamponi vs total cases and total currently positive
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Values')
plt.plot(days, dataset['tamponi'], c='darkgrey', linestyle='-')
plt.plot(days, dataset['totale_casi'], c='red', linestyle='-')
plt.plot(days, dataset['totale_positivi'], c='pink', linestyle='-')
plt.plot(days, dataset['dimessi_guariti'], c='green', linestyle='-')
plt.plot(days, dataset['deceduti'], c='blueviolet', linestyle='-')
plt.legend(('# Tests','Total Cases','Currently Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=3)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curves-with-tamponi.png', dpi = 250)
plt.clf()

################################################################################################################################

# stacked bar chart
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Values')
plt.xticks(rotation=90)
plt.xlabel('Time (days after 24/02)')
plt.title('Distribution of Ill People')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
plt.bar(days, dataset['isolamento_domiciliare'], color='yellow')
plt.bar(days, dataset['ricoverati_con_sintomi'], color='peru')
plt.bar(days, dataset['terapia_intensiva'], color='grey')
plt.legend(('at Home','at Hospital','Intensive Therapy'),loc='upper right', bbox_to_anchor=(1.05, 1.17), ncol=3)
plt.tight_layout()
plt.savefig('./curves/bar-chart-ill.png', dpi=250)
plt.clf()
plt.close()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Values')
plt.xticks(rotation=90)
plt.xlabel('Time (days after 24/02)')
plt.title('Distribution of Cases')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
plt.bar(days, dataset['totale_positivi'], color='pink')
plt.bar(days, dataset['dimessi_guariti'], color='green')
plt.bar(days, dataset['deceduti'], color='blueviolet')
plt.legend(('Currently Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.17), ncol=3)
plt.tight_layout()
plt.savefig('./curves/bar-chart-cases.png', dpi=250)
plt.clf()
plt.close()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Total Cases')
plt.xticks(rotation=90)
plt.xlabel('Time (days after 24/02)')
plt.title('Total Cases Every Day')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
plt.bar(days, dataset['totale_casi'], color='red')
plt.tight_layout()
plt.savefig('./curves/bar-chart-total-cases.png', dpi=250)
plt.clf()
plt.close()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Currently Infected')
plt.xticks(rotation=90)
plt.xlabel('Time (days after 24/02)')
plt.title('Currently Infected Every Day')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
plt.bar(days, dataset['totale_positivi'], color='pink')
plt.tight_layout()
plt.savefig('./curves/bar-chart-total-currently-infected.png', dpi=250)
plt.clf()
plt.close()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('New Infected')
plt.xticks(rotation=90)
plt.xlabel('Time (days after 24/02)')
plt.title('New Infected Every Day')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
plt.bar(days, dataset['nuovi_positivi'], color='orange')
plt.tight_layout()
plt.savefig('./curves/bar-chart-new-cases.png', dpi=250)
plt.clf()
plt.close()

# total variations of infected
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Total variations of Infected')
plt.xticks(rotation=90)
plt.xlabel('Time (days after 24/02)')
plt.title('Total Variations of Infected Every Day')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
plt.bar(days, dataset['variazione_totale_positivi'], color='grey')
plt.tight_layout()
plt.savefig('./curves/bar-chart-variations-of-cases.png', dpi=250)
plt.clf()
plt.close()

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
    if(i < 1):
        print('\nCalculating growth factors: skipping index',i)
    else:
        n1 = dataset['nuovi_positivi'].iloc[i]
        n0 = dataset['nuovi_positivi'].iloc[i-1]
        growth_factor.append(n1/n0)

print('\ngrowth factors day by day')
print(growth_factor)

# growth factor
plt.xlabel('Time (days after 24/02)')
plt.ylabel('Growth Factor')
plt.title('Growth Factor [dN(t+1)/dN(t)]')
plt.plot(days[1:], growth_factor, 'ko')
plt.plot(days[1:], growth_factor, color='grey', linestyle='--')
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
