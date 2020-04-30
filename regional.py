import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

matplotlib.rc('xtick', labelsize=5)
matplotlib.rc('ytick', labelsize=5)

# Importing the dataset
dataset = pd.read_csv('./dati/dpc-covid19-ita-regioni.csv')

################################################################################################################################

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

################################################################################################################################
################################################################################################################################

# yesterday
yesterday='2020-04-29T17:00:00'
yesterday_tot_cases = dataset.loc[dataset['data']==yesterday][
['denominazione_regione','totale_casi', 'totale_positivi', 'nuovi_positivi', 'dimessi_guariti', 'deceduti', 'variazione_totale_positivi',
'isolamento_domiciliare', 'totale_ospedalizzati', 'terapia_intensiva']
]

# today
last_date = '2020-04-30T17:00:00'
last_tot_cases = dataset.loc[dataset['data']==last_date][
['denominazione_regione','totale_casi', 'totale_positivi', 'nuovi_positivi', 'dimessi_guariti', 'deceduti', 'variazione_totale_positivi',
'isolamento_domiciliare', 'totale_ospedalizzati', 'terapia_intensiva']
]

print('\nTotale casi in fvg')
print(last_tot_cases.loc[last_tot_cases['denominazione_regione']=='Friuli Venezia Giulia']['totale_casi'].to_string(index=False))
print('+',last_tot_cases.loc[last_tot_cases['denominazione_regione']=='Friuli Venezia Giulia']['nuovi_positivi'].to_string(index=False))
print('Totale attualmente infetti in fvg')
print(last_tot_cases.loc[last_tot_cases['denominazione_regione']=='Friuli Venezia Giulia']['totale_positivi'].to_string(index=False))
print('+',last_tot_cases.loc[last_tot_cases['denominazione_regione']=='Friuli Venezia Giulia']['variazione_totale_positivi'].to_string(index=False))
print('Totale in isolamento domiciliare in fvg')
print(last_tot_cases.loc[last_tot_cases['denominazione_regione']=='Friuli Venezia Giulia']['isolamento_domiciliare'].to_string(index=False))
print('Totale ospedalizzati in fvg')
print(last_tot_cases.loc[last_tot_cases['denominazione_regione']=='Friuli Venezia Giulia']['totale_ospedalizzati'].to_string(index=False))
print('Ospedalizzati in terapia intensiva in fvg')
print(last_tot_cases.loc[last_tot_cases['denominazione_regione']=='Friuli Venezia Giulia']['terapia_intensiva'].to_string(index=False))
print('\n')

# Write reports of hospital's situation to file
report_h = open("./covid-19-regional-report.txt", "w")
report_h.write("REPORT of REGIONAL SITUATION\n")
report_h.write(last_tot_cases.to_string(index=False))
report_h.close()

################################################################################################################################
################################################################################################################################

counts_tot_cases_by_region = [
(region, last_tot_cases.loc[last_tot_cases['denominazione_regione']==region]['totale_casi']) for region in np.unique(dataset['denominazione_regione'])
]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Total Cases')
#plt.ylim(0,10)
plt.xticks(rotation=90)
plt.xlabel('Region')
plt.title('Total Cases by region')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
for j,f in counts_tot_cases_by_region:
    plt.bar(j, f)
plt.tight_layout()
plt.savefig('total_cases_by_region.png', dpi=250)
plt.clf()
plt.close()

##############################################################################################################################
##############################################################################################################################

# time axis
days = [t[0] for t in enumerate(np.unique(dataset['data']))]

##############################################################################################################################
##############################################################################################################################

# bar charts for fvg
tot_fvg = dataset.loc[dataset['denominazione_regione']=='Friuli Venezia Giulia']['totale_casi']
new_fvg = dataset.loc[dataset['denominazione_regione']=='Friuli Venezia Giulia']['nuovi_positivi']
var_fvg = dataset.loc[dataset['denominazione_regione']=='Friuli Venezia Giulia']['variazione_totale_positivi']

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Total Cases')
#plt.ylim(0,10)
plt.xticks(rotation=90)
plt.xlabel('Time (days after 24/02)')
plt.title('Total Cases in FVG')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
for j,f in zip(days, tot_fvg):
    plt.bar(j, f, color='red')
plt.tight_layout()
plt.savefig('./region-fvg/fvg-total-cases.png', dpi=250)
plt.clf()
plt.close()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('New Cases')
#plt.ylim(0,10)
plt.xticks(rotation=90)
plt.xlabel('Time (days after 24/02)')
plt.title('New Daily Cases in FVG')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
for j,f in zip(days, new_fvg):
    plt.bar(j, f, color='orange')
plt.tight_layout()
plt.savefig('./region-fvg/fvg-new-cases.png', dpi=250)
plt.clf()
plt.close()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ylabel('Total Variations of Infected People')
#plt.ylim(0,10)
plt.xticks(rotation=90)
plt.xlabel('Time (days after 24/02)')
plt.title('Total Variations of Cases in FVG Every Day')
plt.grid(linestyle='--', linewidth=0.2, color='lightgrey')
for j,f in zip(days, var_fvg):
    plt.bar(j, f, color='grey')
plt.tight_layout()
plt.savefig('./region-fvg/fvg-total-variation-cases.png', dpi=250)
plt.clf()
plt.close()

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

# curves for all regions
regions_data_list = [dataset.loc[dataset['denominazione_regione']==region] for region in np.unique(dataset['denominazione_regione'])]

for region in regions_data_list:
    nome = np.unique(region['denominazione_regione'])[0]

    plt.xlabel('Time (days after 24/02)')
    plt.ylabel('Values for '+nome)
    plt.plot(days, region['totale_casi'], c='red', linestyle='-')
    plt.plot(days, region['totale_positivi'], c='pink', linestyle='-')
    plt.plot(days, region['dimessi_guariti'], c='green', linestyle='-')
    plt.plot(days, region['deceduti'], c='blueviolet', linestyle='-')
    plt.legend(('Total Cases','Currently Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
    plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
    plt.savefig('./region-others/'+nome+'-curves-1.png', dpi = 250)
    plt.clf()

    new_healed = []
    new_deceased = []

    for i in range(len(region['dimessi_guariti'])):
        if(i < 1):
            new_healed.append(
            region['dimessi_guariti'].iloc[i]
            )
            new_deceased.append(
            region['deceduti'].iloc[i]
            )
        else:
            #otherwise calculate daily healed and deceased
            new_healed.append(
            region['dimessi_guariti'].iloc[i]-region['dimessi_guariti'].iloc[i-1]
            )
            new_deceased.append(
            region['deceduti'].iloc[i]-region['deceduti'].iloc[i-1]
            )

    plt.xlabel('Time (days after 24/02)')
    plt.ylabel('Values for '+nome)
    plt.plot(days, region['nuovi_positivi'], c='orange', linestyle='-')
    plt.plot(days, new_healed, c='limegreen', linestyle='-')
    plt.plot(days, new_deceased, c='purple', linestyle='-')
    plt.plot(days, region['variazione_totale_positivi'], c='grey',  linestyle='-')
    plt.legend(('New Infected','New Healed','New Deceased', 'Total Variation of Infected'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
    plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
    plt.savefig('./region-others/'+nome+'-curves-2.png', dpi = 250)
    plt.clf()

    plt.xlabel('Time (days after 24/02)')
    plt.ylabel('Values for '+nome)
    plt.plot(days, region['isolamento_domiciliare'], c='goldenrod', linestyle='-')
    plt.plot(days, region['totale_ospedalizzati'], c='darkred', linestyle='-')
    plt.plot(days, region['ricoverati_con_sintomi'], c='purple', linestyle='-')
    plt.plot(days, region['terapia_intensiva'], c='black', linestyle='-')
    plt.legend(('at Home','Total in Hospital','Hospitalized with Symptoms','Intensive Care'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
    plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
    plt.savefig('./region-others/'+nome+'-curves-3.png', dpi = 250)
    plt.clf()

    # calculate growth factor
    growth_factor = []

    for i, _ in enumerate(region['totale_casi']):
        if(i < 1):
            print('\nCalculating growth factors: skipping index',i)
        else:
            n1 = region['totale_casi'].iloc[i]
            n0 = region['totale_casi'].iloc[i-1]
            growth_factor.append(n1/n0)

    # growth factor
    plt.xlabel('Time (days after 24/02)')
    plt.ylabel('Growth Factor in '+nome)
    plt.title('Growth Factor [N(t+1)/N(t)] in '+nome)
    plt.plot(days[1:], growth_factor, 'ko')
    plt.plot(days[1:], growth_factor, color='grey', linestyle='--')
    plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
    plt.savefig('./region-others/'+nome+'-growth-factor.png', dpi = 250)
    plt.clf()

    # trajectory of cases
    plt.xlabel('Total Cases in '+nome)
    plt.ylabel('New Cases in '+nome)
    plt.title('Trajectory of Cases for '+nome)
    plt.plot(region['totale_casi'],region['nuovi_positivi'] , 'ko')
    plt.plot(region['totale_casi'],region['nuovi_positivi'], color='red', linestyle='--')
    plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
    plt.savefig('./region-others/'+nome+'-trajectory.png', dpi = 250)
    plt.clf()
