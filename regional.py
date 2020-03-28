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
#print('\nFIRST ' + str(n_rows_head) + ' ENTRIES')
#print(dataset.head(n_rows_head))
#print('\nMINIMUM VALUES')
#print(dataset.min())
#print('\nMAXIMUM VALUES')
#print(dataset.max())
#print('\nMEAN VALUES')
#print(dataset.mean())

print('\n DATE, REGION, TOT CASES, CURRENTLY INFECTED, NEW INFECTED, HEALED, DECEASED')
print(dataset.iloc[lambda x: x.index > 629][
['data', 'denominazione_regione', 'totale_casi', 'totale_attualmente_positivi', 'nuovi_attualmente_positivi', 'dimessi_guariti', 'deceduti']
].to_string())

################################################################################################################################

################################################################################################################################
# features = [
# data,stato,codice_regione,denominazione_regione,lat,long,
# ricoverati_con_sintomi,terapia_intensiva,totale_ospedalizzati,isolamento_domiciliare,
# totale_attualmente_positivi,nuovi_attualmente_positivi,dimessi_guariti,deceduti,totale_casi,tamponi
# note_it, note_en
# ]
################################################################################################################################
# monitoring hospitals in fvg
print('\n MONITORING SITUATION IN FVG HOSPITALS')

last_date = '2020-03-28T17:00:00'
last_tot_cases = dataset.loc[dataset['data']==last_date][['denominazione_regione','totale_casi','totale_attualmente_positivi', 'totale_ospedalizzati', 'terapia_intensiva']]

print('\nTotale casi in fvg')
print(last_tot_cases.loc[last_tot_cases['denominazione_regione']=='Friuli Venezia Giulia']['totale_casi'].to_string(index=False))
print('Totale attualmente infetti in fvg')
print(last_tot_cases.loc[last_tot_cases['denominazione_regione']=='Friuli Venezia Giulia']['totale_attualmente_positivi'].to_string(index=False))
print('Totale ospedalizzati in fvg')
print(last_tot_cases.loc[last_tot_cases['denominazione_regione']=='Friuli Venezia Giulia']['totale_ospedalizzati'].to_string(index=False))
print('Ospedalizzati in terapia intensiva in fvg')
print(last_tot_cases.loc[last_tot_cases['denominazione_regione']=='Friuli Venezia Giulia']['terapia_intensiva'].to_string(index=False))
print('\n')

################################################################################################################################
# total cases by region
print('\n HOSPITALS\' SITUATION IN WHOLE ITALY')
print(last_tot_cases.to_string(index=False))
print('\n GENERAL SITUATION IN WHOLE ITALY')
last_tot_general = dataset.loc[dataset['data']==last_date][['denominazione_regione','nuovi_attualmente_positivi','dimessi_guariti', 'deceduti']]
print(last_tot_general.to_string(index=False))

# Write reports of hospital's situation to file
report_h = open("./covid-19-regional-hospital-report.txt", "w")
report_h.write("REPORT of REGIONAL HOSPITAL'S SITUATION\n")
report_h.write(last_tot_cases.to_string(index=False))
report_h.close()

# Write reports of general situation to file
report_g = open("./covid-19-regional-general-report.txt", "w")
report_g.write("REPORT of REGIONAL SITUATION\n")
report_g.write(last_tot_general.to_string(index=False))
report_g.close()

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
# FVG
days = [t[0] for t in enumerate(np.unique(dataset['data']))]
data_fvg = dataset.loc[dataset['denominazione_regione']=='Friuli Venezia Giulia']

plt.xlabel('Time (days after 24/02)')
plt.ylabel('Values for FVG')
plt.plot(days, data_fvg['totale_casi'], c='red', linestyle='-')
plt.plot(days, data_fvg['totale_attualmente_positivi'], c='pink', linestyle='-')
plt.plot(days, data_fvg['dimessi_guariti'], c='green', linestyle='-')
plt.plot(days, data_fvg['deceduti'], c='blueviolet', linestyle='-')
plt.legend(('Total Cases','Currently Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./region-fvg/fvg-curves-1.png', dpi = 250)
plt.clf()

plt.xlabel('Time (days after 24/02)')
plt.ylabel('Values for FVG')
plt.plot(days, data_fvg['nuovi_attualmente_positivi'], c='orange', linestyle='-')
plt.plot(days, data_fvg['dimessi_guariti'], c='green', linestyle='-')
plt.plot(days, data_fvg['deceduti'], c='blueviolet', linestyle='-')
plt.legend(('New Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=3)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./region-fvg/fvg-curves-2.png', dpi = 250)
plt.clf()

plt.xlabel('Time (days after 24/02)')
plt.ylabel('Values for FVG')
plt.plot(days, data_fvg['nuovi_attualmente_positivi'], c='orange', linestyle='-')
plt.plot(days, data_fvg['totale_ospedalizzati'], c='grey', linestyle='-')
plt.plot(days, data_fvg['terapia_intensiva'], c='black', linestyle='-')
plt.legend(('New Infected','In Hospital','Intensive Care'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=3)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./region-fvg/fvg-curves-3-hospital.png', dpi = 250)
plt.clf()

plt.xlabel('Time (days after 24/02)')
plt.ylabel('Values for FVG')
plt.plot(days, data_fvg['isolamento_domiciliare'], c='yellow', linestyle='-')
plt.plot(days, data_fvg['totale_ospedalizzati'], c='grey', linestyle='-')
plt.plot(days, data_fvg['terapia_intensiva'], c='black', linestyle='-')
plt.legend(('at Home','In Hospital','Intensive Care'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=3)
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.savefig('./region-fvg/fvg-curves-4-hospital.png', dpi = 250)
plt.clf()

tot_fvg = dataset.loc[dataset['denominazione_regione']=='Friuli Venezia Giulia']['totale_casi']
new_fvg = dataset.loc[dataset['denominazione_regione']=='Friuli Venezia Giulia']['nuovi_attualmente_positivi']

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

##############################################################################################################################

#curves for other regions
regions_data_list = [
dataset.loc[dataset['denominazione_regione']=='Abruzzo'],
dataset.loc[dataset['denominazione_regione']=='Basilicata'],
dataset.loc[dataset['denominazione_regione']=='P.A. Bolzano'],
dataset.loc[dataset['denominazione_regione']=='Calabria'],
dataset.loc[dataset['denominazione_regione']=='Campania'],
dataset.loc[dataset['denominazione_regione']=='Emilia Romagna'],
dataset.loc[dataset['denominazione_regione']=='Lazio'],
dataset.loc[dataset['denominazione_regione']=='Liguria'],
dataset.loc[dataset['denominazione_regione']=='Lombardia'],
dataset.loc[dataset['denominazione_regione']=='Marche'],
dataset.loc[dataset['denominazione_regione']=='Molise'],
dataset.loc[dataset['denominazione_regione']=='Piemonte'],
dataset.loc[dataset['denominazione_regione']=='Puglia'],
dataset.loc[dataset['denominazione_regione']=='Sardegna'],
dataset.loc[dataset['denominazione_regione']=='Sicilia'],
dataset.loc[dataset['denominazione_regione']=='Toscana'],
dataset.loc[dataset['denominazione_regione']=='P.A. Trento'],
dataset.loc[dataset['denominazione_regione']=='Umbria'],
dataset.loc[dataset['denominazione_regione']=='Valle d\'Aosta'],
dataset.loc[dataset['denominazione_regione']=='Veneto']
]

for region in regions_data_list:
    nome = np.unique(region['denominazione_regione'])[0]

    plt.xlabel('Time (days after 24/02)')
    plt.ylabel('Values for '+nome)
    plt.plot(days, region['totale_casi'], c='red', linestyle='-')
    plt.plot(days, region['totale_attualmente_positivi'], c='pink', linestyle='-')
    plt.plot(days, region['dimessi_guariti'], c='green', linestyle='-')
    plt.plot(days, region['deceduti'], c='blueviolet', linestyle='-')
    plt.legend(('Total Cases','Currently Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
    plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
    plt.savefig('./region-others/'+nome+'-curves-1.png', dpi = 250)
    plt.clf()

    plt.xlabel('Time (days after 24/02)')
    plt.ylabel('Values for '+nome)
    plt.plot(days, region['nuovi_attualmente_positivi'], c='orange', linestyle='-')
    plt.plot(days, region['dimessi_guariti'], c='green', linestyle='-')
    plt.plot(days, region['deceduti'], c='blueviolet', linestyle='-')
    plt.legend(('New Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=3)
    plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
    plt.savefig('./region-others/'+nome+'-curves-2.png', dpi = 250)
    plt.clf()
