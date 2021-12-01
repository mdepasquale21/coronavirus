import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import seaborn as sns

#import data
dataset = pd.read_csv('./dati/dpc-covid19-ita-andamento-nazionale.csv')

#print('\nDATA EXPLORATION')
#print('\nSHAPE')
#print(dataset.shape)
#print('\nINFO')
#dataset.info()
#print('\nDESCRIPTION')
#print(dataset.describe())
#n_rows_head = 10
#print('\nLAST ' + str(n_rows_head) + ' ENTRIES')
#print(dataset.tail(n_rows_head).to_string(index=False))
#print('\nMINIMUM VALUES')
#print(dataset.min())
#print('\nMAXIMUM VALUES')
#print(dataset.max())
#print('\nMEAN VALUES')
#print(dataset.mean())

################################################################################################################################
################################################################################################################################

# curves

days = [t[0] for t in enumerate(dataset['data'])]

# total cases
plt.xlabel('Time (days after 24/02/2020)')
plt.ylabel('Total Cases')
plt.title('Epidemic curve')
plt.scatter(days, dataset['totale_casi'], c='red')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curve-total-cases.png', dpi = 250)
plt.clf()

# new infected
plt.xlabel('Time (days after 24/02/2020)')
plt.ylabel('New Infected')
plt.title('New infected curve')
plt.scatter(days, dataset['nuovi_positivi'], c='orange')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curve-new-infected.png', dpi = 250)
plt.clf()

# total variations of infected
plt.xlabel('Time (days after 24/02/2020)')
plt.ylabel('Total variations of Infected')
plt.title('Total variations of infected curve')
plt.scatter(days, dataset['variazione_totale_positivi'], c='grey')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curve-variations-of-infected.png', dpi = 250)
plt.clf()

# healed people
plt.xlabel('Time (days after 24/02/2020)')
plt.ylabel('Healed')
plt.title('Healed curve')
plt.scatter(days, dataset['dimessi_guariti'], c='green')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curve-healed.png', dpi = 250)
plt.clf()

# deceased people
plt.xlabel('Time (days after 24/02/2020)')
plt.ylabel('Deceased')
plt.title('Deceased curve')
plt.scatter(days, dataset['deceduti'], c='blueviolet')
plt.legend(('data',),loc='upper right', bbox_to_anchor=(1.05, 1.15))
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curve-deceased.png', dpi = 250)
plt.clf()

################################################################################################################################
################################################################################################################################
################################################################################################################################

# calculate new healed and new deceased every day, not present in df

new_healed = []
new_deceased = []
new_tamponi=[]

for i in range(len(dataset)):
    if(i < 1):
        new_healed.append(
        dataset['dimessi_guariti'].iloc[i]
        )
        new_deceased.append(
        dataset['deceduti'].iloc[i]
        )
        new_tamponi.append(
        dataset['tamponi'].iloc[i]
        )
    else:
        #otherwise calculate daily healed and deceased
        new_healed.append(
        dataset['dimessi_guariti'].iloc[i]-dataset['dimessi_guariti'].iloc[i-1]
        )
        new_deceased.append(
        dataset['deceduti'].iloc[i]-dataset['deceduti'].iloc[i-1]
        )
        new_tamponi.append(
        dataset['tamponi'].iloc[i]-dataset['tamponi'].iloc[i-1]
        )

# insert new quantities in dataframe
dataset.insert(loc=9,column='nuovi_guariti', value=new_healed)
dataset.insert(loc=10,column='nuovi_deceduti', value=new_deceased)
dataset.insert(loc=11,column='nuovi_tamponi', value=new_tamponi)

# print national report
print('\n DATE, TOT CASES, CURRENTLY INFECTED, NEW INFECTED, NEW HEALED, NEW DECEASED, VARIATION OF TOTAL INFECTED')
print(dataset[
['data', 'totale_casi', 'totale_positivi', 'nuovi_positivi', 'nuovi_guariti', 'nuovi_deceduti', 'variazione_totale_positivi']
].to_string(index=False))

# Write national report to file
report = open("./covid-19-national-report.txt", "w")
report.write("REPORT of DATE, TOT CASES, CURRENTLY INFECTED, NEW INFECTED, NEW HEALED, NEW DECEASED, VARIATION OF TOTAL INFECTED\n")
report.write(dataset[
['data', 'totale_casi', 'totale_positivi', 'nuovi_positivi', 'nuovi_guariti', 'nuovi_deceduti', 'variazione_totale_positivi']
].to_string(index=False))
report.close()

# Write total national report to file
total_report = open("./covid-19-national-report-total.txt", "w")
total_report.write("REPORT of DATE, TOT CASES, CURRENTLY INFECTED, HEALED, DECEASED\n")
total_report.write(dataset[
['data', 'totale_casi', 'totale_positivi', 'dimessi_guariti', 'deceduti']
].to_string(index=False))
total_report.close()

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

# new positives, new healed, new deceased and total variations
plt.xlabel('Time (days after 24/02/2020)')
plt.ylabel('Values')
plt.plot(days, dataset['nuovi_positivi'], c='orange', linestyle='-')
plt.plot(days, dataset['nuovi_guariti'], c='limegreen', linestyle='-')
plt.plot(days, dataset['nuovi_deceduti'], c='purple', linestyle='-')
plt.plot(days, dataset['variazione_totale_positivi'], c='grey',  linestyle='-')
plt.legend(('New Infected','New Healed','New Deceased', 'Total Variation of Infected'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curves-almost.png', dpi = 250)
plt.clf()

################################################################################################################################
################################################################################################################################
################################################################################################################################

print('\ntotale_casi = totale_positivi + dimessi_guariti + deceduti\n')
print('\nvariazione_totale_positivi = nuovi_positivi - nuovi_guariti - nuovi_deceduti\n')

# comparison of more curves

#total cases and total currently positive
plt.xlabel('Time (days after 24/02/2020)')
plt.ylabel('Values')
plt.plot(days, dataset['totale_casi'], c='red', linestyle='-')
plt.plot(days, dataset['totale_positivi'], c='pink', linestyle='-')
plt.plot(days, dataset['dimessi_guariti'], c='green', linestyle='-')
plt.plot(days, dataset['deceduti'], c='blueviolet', linestyle='-')
plt.legend(('Total Cases','Currently Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curves-all.png', dpi = 250)
plt.clf()

#curves for people at home, in hospital and in intensive care
plt.xlabel('Time (days after 24/02/2020)')
plt.ylabel('Values')
plt.plot(days, dataset['isolamento_domiciliare'], c='goldenrod', linestyle='-')
plt.plot(days, dataset['totale_ospedalizzati'], c='darkred', linestyle='-')
plt.plot(days, dataset['ricoverati_con_sintomi'], c='purple', linestyle='-')
plt.plot(days, dataset['terapia_intensiva'], c='black', linestyle='-')
plt.legend(('at Home','Total in Hospital','Hospitalized with Symptoms','Intensive Care'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curves-hospital-home.png', dpi = 250)
plt.clf()

#curves for people in hospital and in intensive care
plt.xlabel('Time (days after 24/02/2020)')
plt.ylabel('Values')
plt.plot(days, dataset['totale_ospedalizzati'], c='darkred', linestyle='-')
plt.plot(days, dataset['ricoverati_con_sintomi'], c='purple', linestyle='-')
plt.plot(days, dataset['terapia_intensiva'], c='black', linestyle='-')
plt.legend(('Total in Hospital','Hospitalized with Symptoms','Intensive Care'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curves-hospital.png', dpi = 250)
plt.clf()

#tamponi vs total cases and total currently positive
plt.xlabel('Time (days after 24/02/2020)')
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

dataset.insert(loc=12, column='rapporto_nuovi_positivi_tamponi', value=(dataset['nuovi_positivi']/dataset['nuovi_tamponi']))

#new infected/new tests ratio daily
plt.xlabel('Time (days after 24/02/2020)')
plt.ylabel('New Infected/New Tests')
plt.title('New Infected/New Tests Ratio')
plt.plot(days, dataset['rapporto_nuovi_positivi_tamponi'], c='darkslateblue', linestyle='-')
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/curves-with-tamponi-over-new.png', dpi = 250)
plt.clf()

################################################################################################################################

# stacked bar charts

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Values')
plt.xticks(rotation=90)
plt.xlabel('Time (days after 24/02/2020)')
plt.title('Distribution of Ill People')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
plt.bar(days, dataset['isolamento_domiciliare'], color='yellow')
plt.bar(days, dataset['ricoverati_con_sintomi'], color='peru')
plt.bar(days, dataset['terapia_intensiva'], color='grey')
plt.legend(('at Home','at Hospital','Intensive Care'),loc='upper right', bbox_to_anchor=(1.05, 1.17), ncol=3)
plt.tight_layout()
plt.savefig('./curves/bar-chart-ill.png', dpi=250)
plt.clf()
plt.close()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Values')
plt.xticks(rotation=90)
plt.xlabel('Time (days after 24/02/2020)')
plt.title('Distribution of Hospitalized People')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
plt.bar(days, dataset['ricoverati_con_sintomi'], color='peru')
plt.bar(days, dataset['terapia_intensiva'], color='grey')
plt.legend(('at Hospital','Intensive Care'),loc='upper right', bbox_to_anchor=(1.05, 1.17), ncol=3)
plt.tight_layout()
plt.savefig('./curves/bar-chart-hospital.png', dpi=250)
plt.clf()
plt.close()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Values')
plt.xticks(rotation=90)
plt.xlabel('Time (days after 24/02/2020)')
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

# bar charts

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Total Cases')
plt.xticks(rotation=90)
plt.xlabel('Time (days after 24/02/2020)')
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
plt.xlabel('Time (days after 24/02/2020)')
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
plt.xlabel('Time (days after 24/02/2020)')
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
plt.xlabel('Time (days after 24/02/2020)')
plt.title('Total Variations of Infected Every Day')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
plt.bar(days, dataset['variazione_totale_positivi'], color='grey')
plt.tight_layout()
plt.savefig('./curves/bar-chart-variations-of-cases.png', dpi=250)
plt.clf()
plt.close()

################################################################################################################################
################################################################################################################################

# fatality rate
fatality_rate_1 = dataset['deceduti']/dataset['totale_casi']
fatality_rate_2 = dataset['deceduti']/(dataset['deceduti'] + dataset['dimessi_guariti'])
plt.xlabel('Time (days after 24/02/2020)')
plt.ylabel('Fatality Rate (%)')
plt.plot(days, fatality_rate_1*100, c='darkslateblue', linestyle='-')
plt.plot(days, fatality_rate_2*100, c='saddlebrown', linestyle='-')
plt.legend(('% dec/tot.cases','% dec/(dec+heal)'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/fatality-rate.png', dpi = 250)
plt.clf()

# outcome of closed cases (%)
recovery_rate = dataset['dimessi_guariti']/(dataset['deceduti'] + dataset['dimessi_guariti'])
plt.xlabel('Time (days after 24/02/2020)')
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
        n1 = dataset['totale_casi'].iloc[i]
        n0 = dataset['totale_casi'].iloc[i-1]
        growth_factor.append(n1/n0)

print('\ngrowth factors yesterday and today')
print(growth_factor[-2], growth_factor[-1])

# growth factor
plt.xlabel('Time (days after 24/02/2020)')
plt.ylabel('Growth Factor')
plt.title('Growth Factor [N(t+1)/N(t)]')
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

print('\ngrowth rates % yesterday and today')
print(growth_rate[-2], growth_rate[-1])

# growth rate
plt.xlabel('Time (days after 24/02/2020)')
plt.ylabel('Growth Rate (%)')
plt.title('Growth Rate [(N(t+1)-N(t))/N(t)]x100')
plt.plot(days[1:], growth_rate, 'bo')
plt.plot(days[1:], growth_rate, color='cyan', linestyle='--')
#plt.legend(('data','linked'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/growth-rate.png', dpi = 250)
plt.clf()

# trajectory of cases
plt.xlabel('Total Cases')
plt.ylabel('New Cases')
plt.title('Trajectory of Cases')
plt.plot(dataset['totale_casi'],dataset['nuovi_positivi'] , 'ko')
plt.plot(dataset['totale_casi'],dataset['nuovi_positivi'], color='red', linestyle='--')
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/trajectory.png', dpi = 250)
plt.clf()

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
# average some quantities weekly to smooth out the curves and remove noise

time = 7

# average time to calculate weeks and not days
dd = days[::time]
weeks = [i for i in range(len(dd))]

# drop string columns
dataset.drop(columns=['data', 'stato', 'note'])

# average weekly dataset
ave_dataset = dataset.groupby(np.arange(len(dataset))//time, axis=0).mean()

# weekly average new positives, new healed, new deceased and total variations
plt.xlabel('Time (weeks after 24/02/2020)')
plt.ylabel('Weekly Average Values')
plt.plot(weeks, ave_dataset['nuovi_positivi'], c='orange', linestyle='-')
plt.plot(weeks, ave_dataset['nuovi_guariti'], c='limegreen', linestyle='-')
plt.plot(weeks, ave_dataset['nuovi_deceduti'], c='purple', linestyle='-')
plt.plot(weeks, ave_dataset['variazione_totale_positivi'], c='grey',  linestyle='-')
plt.legend(('New Infected','New Healed','New Deceased', 'Total Variation of Infected'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/average-curves-almost.png', dpi = 250)
plt.clf()

# weekly average new infected/new tests ratio
plt.xlabel('Time (weeks after 24/02/2020)')
plt.ylabel('Average New Infected/New Tests')
plt.title('New Infected/New Tests Ratio (Weekly Average)')
plt.plot(weeks, ave_dataset['rapporto_nuovi_positivi_tamponi'], c='darkslateblue', linestyle='-')
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/average-curves-with-tamponi-over-new.png', dpi = 250)
plt.clf()

# weekly average trajectory of cases
plt.xlabel('Total Cases')
plt.ylabel('New Cases')
plt.title('Trajectory of Cases (Weekly Average)')
plt.plot(ave_dataset['totale_casi'],ave_dataset['nuovi_positivi'] , 'ko')
plt.plot(ave_dataset['totale_casi'],ave_dataset['nuovi_positivi'], color='red', linestyle='--')
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/average-trajectory.png', dpi = 250)
plt.clf()

# weekly average only new infected
plt.xlabel('Time (weeks after 24/02/2020)')
plt.ylabel('Average New Infected')
plt.title('New infected curve (Weekly Average)')
plt.plot(weeks, ave_dataset['nuovi_positivi'], c='orange')
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/average-curve-new-infected.png', dpi = 250)
plt.clf()
plt.close()

# weekly average barchart new infected
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Average New Infected')
plt.xticks(rotation=90)
plt.xlabel('Time (weeks after 24/02/2020)')
plt.title('Average New Infected Every Week')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
plt.bar(weeks, ave_dataset['nuovi_positivi'], color='orange')
plt.tight_layout()
plt.savefig('./curves/average-bar-chart-new-cases.png', dpi=250)
plt.clf()
plt.close()

# weekly average only infected
plt.xlabel('Time (weeks after 24/02/2020)')
plt.ylabel('Average Infected')
plt.title('Infected curve (Weekly Average)')
plt.plot(weeks, ave_dataset['totale_positivi'], c='pink')
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./curves/average-curve-infected.png', dpi = 250)
plt.clf()
plt.close()

# weekly average barchart infected
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Average Infected')
plt.xticks(rotation=90)
plt.xlabel('Time (weeks after 24/02/2020)')
plt.title('Average Infected Every Week')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
plt.bar(weeks, ave_dataset['totale_positivi'], color='pink')
plt.tight_layout()
plt.savefig('./curves/average-bar-chart-infected.png', dpi=250)
plt.clf()
plt.close()
