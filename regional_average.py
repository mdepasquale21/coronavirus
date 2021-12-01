import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

matplotlib.rc('xtick', labelsize=5)
matplotlib.rc('ytick', labelsize=5)

# Importing the dataset
dataset = pd.read_csv('./dati/dpc-covid19-ita-regioni.csv')

# time axis
days = [t[0] for t in enumerate(np.unique(dataset['data']))]

################################################################################################################################
# average some quantities weekly to smooth out the curves and remove noise

time = 7

# average time to calculate weeks and not days
dd = days[::time]
weeks = [i for i in range(len(dd))]

# data,stato,codice_regione,denominazione_regione,lat,long,
# ricoverati_con_sintomi,terapia_intensiva,totale_ospedalizzati,
# isolamento_domiciliare,totale_positivi,variazione_totale_positivi,
# nuovi_positivi,dimessi_guariti,deceduti,totale_casi,tamponi,casi_testati,note_it,note_en
# drop string columns
dataset = dataset.drop(columns=['data','stato','codice_regione','lat','long','note'])

# only
# denominazione_regione,
# ricoverati_con_sintomi,terapia_intensiva,totale_ospedalizzati,
# isolamento_domiciliare,totale_positivi,variazione_totale_positivi,
# nuovi_positivi,dimessi_guariti,deceduti,totale_casi,tamponi,casi_testati

# regions data
regions_data_list = [dataset.loc[dataset['denominazione_regione']==region] for region in np.unique(dataset['denominazione_regione'])]

################################################################################################################################

# average curves for all regions

for df in regions_data_list:
    nome = np.unique(df['denominazione_regione'])[0]
    print('Calculating average every',time,'days')
    ave_df = df.drop('denominazione_regione',axis=1).groupby(np.arange(len(df))//time, axis=0).mean()

    plt.xlabel('Time (weeks after 24/02/2020)')
    plt.ylabel('Values for '+nome)
    plt.plot(weeks, ave_df['totale_casi'], c='red', linestyle='-')
    plt.plot(weeks, ave_df['totale_positivi'], c='pink', linestyle='-')
    plt.plot(weeks, ave_df['dimessi_guariti'], c='green', linestyle='-')
    plt.plot(weeks, ave_df['deceduti'], c='blueviolet', linestyle='-')
    plt.legend(('Total Cases','Currently Infected','Healed','Deceased'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
    plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
    plt.savefig('./regions-average/'+nome+'-curves-1.png', dpi = 250)
    plt.clf()

    new_healed = []
    new_deceased = []

    for i in range(len(ave_df['dimessi_guariti'])):
        if(i < 1):
            new_healed.append(
            ave_df['dimessi_guariti'].iloc[i]
            )
            new_deceased.append(
            ave_df['deceduti'].iloc[i]
            )
        else:
            #otherwise calculate daily healed and deceased
            new_healed.append(
            ave_df['dimessi_guariti'].iloc[i]-ave_df['dimessi_guariti'].iloc[i-1]
            )
            new_deceased.append(
            ave_df['deceduti'].iloc[i]-ave_df['deceduti'].iloc[i-1]
            )

    plt.xlabel('Time (weeks after 24/02/2020)')
    plt.ylabel('Values for '+nome)
    plt.plot(weeks, ave_df['nuovi_positivi'], c='orange', linestyle='-')
    plt.plot(weeks, new_healed, c='limegreen', linestyle='-')
    plt.plot(weeks, new_deceased, c='purple', linestyle='-')
    plt.plot(weeks, ave_df['variazione_totale_positivi'], c='grey',  linestyle='-')
    plt.legend(('New Infected','New Healed','New Deceased', 'Total Variation of Infected'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
    plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
    plt.savefig('./regions-average/'+nome+'-curves-2.png', dpi = 250)
    plt.clf()

    plt.xlabel('Time (weeks after 24/02/2020)')
    plt.ylabel('Values for '+nome)
    plt.plot(weeks, ave_df['isolamento_domiciliare'], c='goldenrod', linestyle='-')
    plt.plot(weeks, ave_df['totale_ospedalizzati'], c='darkred', linestyle='-')
    plt.plot(weeks, ave_df['ricoverati_con_sintomi'], c='purple', linestyle='-')
    plt.plot(weeks, ave_df['terapia_intensiva'], c='black', linestyle='-')
    plt.legend(('at Home','Total in Hospital','Hospitalized with Symptoms','Intensive Care'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
    plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
    plt.savefig('./regions-average/'+nome+'-curves-3.png', dpi = 250)
    plt.clf()

    plt.xlabel('Time (weeks after 24/02/2020)')
    plt.ylabel('Values for '+nome)
    plt.plot(weeks, ave_df['totale_ospedalizzati'], c='darkred', linestyle='-')
    plt.plot(weeks, ave_df['ricoverati_con_sintomi'], c='purple', linestyle='-')
    plt.plot(weeks, ave_df['terapia_intensiva'], c='black', linestyle='-')
    plt.legend(('Total in Hospital','Hospitalized with Symptoms','Intensive Care'),loc='upper right', bbox_to_anchor=(1.05, 1.15), ncol=2)
    plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
    plt.savefig('./regions-average/'+nome+'-curves-4.png', dpi = 250)
    plt.clf()

    # calculate growth factor
    growth_factor = []

    for i, _ in enumerate(ave_df['totale_casi']):
        if(i < 1):
            print('\nCalculating growth factors: skipping index',i)
        else:
            n1 = ave_df['totale_casi'].iloc[i]
            n0 = ave_df['totale_casi'].iloc[i-1]
            growth_factor.append(n1/n0)

    # growth factor
    plt.xlabel('Time (weeks after 24/02/2020)')
    plt.ylabel('Growth Factor in '+nome)
    plt.title('Growth Factor [N(t+1)/N(t)] in '+nome)
    plt.plot(weeks[1:], growth_factor, 'ko')
    plt.plot(weeks[1:], growth_factor, color='grey', linestyle='--')
    plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
    plt.savefig('./regions-average/'+nome+'-growth-factor.png', dpi = 250)
    plt.clf()

    # trajectory of cases
    plt.xlabel('Total Cases in '+nome)
    plt.ylabel('New Cases in '+nome)
    plt.title('Trajectory of Cases for '+nome)
    plt.plot(ave_df['totale_casi'],ave_df['nuovi_positivi'] , 'ko')
    plt.plot(ave_df['totale_casi'],ave_df['nuovi_positivi'], color='red', linestyle='--')
    plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
    plt.savefig('./regions-average/'+nome+'-trajectory.png', dpi = 250)
    plt.clf()
