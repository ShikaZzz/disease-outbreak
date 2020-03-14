import sys
import os
# filedir = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(os.path.join(filedir,"./../"))
from src.get_datatype import GetDatatype
import pandas as pd
import numpy as np
from datetime import datetime
from src.convert2type3 import Convert2Type3
from src.spread_animator import OutbreakSpreadAnimator
import matplotlib.pyplot as plt
from matplotlib.pylab import gca

# df = pd.read_excel('./../Project/NewData/Polio_complete.xls')
# df = df.rename(columns={'on a country name for its incidence time series ':'Country'})
# df.fillna(0)

# for year in df.keys().values[1:]:
#     df[year] = df[year].apply(lambda x: str(x).replace("'",""))
#     df[year] = pd.to_numeric(df[year], errors='coerce').fillna(0).astype(int)   





# df = pd.read_csv('./../Project/influenza-laboratory-confirmed-cases-by-county-beginning-2009-10-season-1.csv')
# df['month_yr'] = df['Week Ending Date'].apply(lambda x: np.datetime64(datetime.strptime(x,'%m/%d/%Y').date(),"D"))
# df = df.sort_values('month_yr')
# df.rename(columns={'Count':'Value','month_yr':'Date','County':'Country'},inplace=True)

# df['Value'] = pd.to_numeric(df["Value"], errors='coerce').fillna(0).astype(int)   
# print(df.dtypes)



# df = pd.read_excel('./../Project/data/ebola/ebola_data_db_format.xlsx')

# df.rename(columns={'value':'Value'},inplace=True)
# df['Date'] = df['Date'].apply(lambda x: np.datetime64(datetime.strptime(x,'%Y-%m-%d').date(),"D"))

fname = 'sars_2003_complete_dataset_clean.csv'

# df = pd.read_csv('./../Project/sars_2003_complete_dataset_clean.csv')
# df.rename(columns={'Cumulative number of case(s)':'Value'},inplace=True)
# df['Date'] = df['Date'].apply(lambda x: np.datetime64(datetime.strptime(x,'%Y-%m-%d').date(),"D"))

Indicator = None;countries=None
# df = 'sars.csv';Indicator='Number of deaths'
# df = 'polio.xls'
df = 'ebola.xlsx';
# Indicator="Cumulative number of confirmed, probable and suspected Ebola cases"
Indicator1 = "Cumulative number of confirmed Ebola deaths"
Indicator2 = "Cumulative number of confirmed Ebola cases"

# 'Cumulative number of confirmed, probable and suspected Ebola cases',
# 'Cumulative number of confirmed Ebola cases',
# 'Cumulative number of probable Ebola cases',
# 'Cumulative number of suspected Ebola cases',
# 'Cumulative number of confirmed, probable and suspected Ebola deaths',
# 'Cumulative number of confirmed Ebola deaths',
# 'Cumulative number of probable Ebola deaths',
# 'Cumulative number of suspected Ebola deaths',
# id_name = Indicator.replace("Cumulative number of ","").replace(" Ebola ","").replace(",","").replace(" ","_")

countries = ['Guinea','Liberia','Sierra Leone']
# df = df.infer_dtypes()#.astype(int)
ebola,Type = GetDatatype().check_type(df,is_fname=True,Indicator=Indicator)
ebola_confirmed_cases = Convert2Type3().convert2_type3(ebola,Indicator=Indicator2)
ebola_confirmed_deaths = Convert2Type3().convert2_type3(ebola,Indicator=Indicator1)

fig = plt.figure(figsize=(7,7))
ax = gca()
plt.plot(ebola_confirmed_cases.sum(numeric_only=True),label='confirmed cases')
plt.plot(ebola_confirmed_deaths.sum(numeric_only=True),label='confirmed deaths')
plt.legend()
fig.autofmt_xdate()
plt.title("Ebola Outbreak")
plt.ylabel("Cumulative number")
plt.savefig(os.path.join(filedir,"./../plots/ebola_outbreak.png"))
plt.show()





# print("TYPE....:",Type)
# _,Type = GetDatatype().check_type(DATA_conv,is_fname=False)
# print("TYPE-----:",Type)
# temp = pd.to_datetime(DATA_conv.keys()[1]).year#.astype("datetime64[M]")
# print(temp)
# OutbreakSpreadAnimator().animate(DATA_conv,countries=countries,fname=df.split(".")[0]+"{}.mp4".format(id_name))