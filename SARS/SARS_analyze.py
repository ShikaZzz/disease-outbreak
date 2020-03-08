'''
Read 'sars_2003_complete_dataset_clean.csv', 
find out the 5 countries with the most cases of SARS, 
draw 2 line chart on the trend of increase of total cases and deaths,
draw a bar chart on the number of total cases and deaths.
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# DataFrame (read CSV)
df = pd.DataFrame(pd.read_csv('sars_2003_complete_dataset_clean.csv',header=0))
#print(df.dtypes)

grouped_country = df.groupby('Country')
#print(grouped_country.size())
#print(grouped_country.max())


# find out the countries with the most cases
df_max = grouped_country.max()
#df_max.to_csv('sars_max.csv')
# We just find that in China, Hong Kong, Taiwan, Canada, Singapore, there are largest number of cases.
print('Total number of cases is ' + str(df_max['Cumulative number of case(s)'].sum()))
print('Total number of deaths is ' + str(df_max['Number of deaths'].sum()))
print('Total number of recovered is ' + str(df_max['Number recovered'].sum()))
print('Death rate: ' + str(df_max['Number of deaths'].sum()/df_max['Cumulative number of case(s)'].sum()))


# DataFrame of countries with most cases
# China-CN, Hong Kong-HK, Taiwan-TW, Canada-CAN, Singapore-SGP
df_CN = grouped_country.get_group('China')
df_HK = grouped_country.get_group('Hong Kong SAR, China')
df_TW = grouped_country.get_group('Taiwan, China')
df_CAN = grouped_country.get_group('Canada')
df_SGP = grouped_country.get_group('Singapore')


# trend of cumulative number of cases
ax1 = df_CN.plot(x='Date',y='Cumulative number of case(s)',label='China',figsize=(8,4))
df_HK.plot(ax=ax1,x='Date',y='Cumulative number of case(s)',label='Hong Kong SAR, China')
df_TW.plot(ax=ax1,x='Date',y='Cumulative number of case(s)',label='Taiwan, China')
df_CAN.plot(ax=ax1,x='Date',y='Cumulative number of case(s)',label='Canada')
df_SGP.plot(ax=ax1,x='Date',y='Cumulative number of case(s)',label='Singapore')
plt.xlabel('Time')
plt.ylabel('Total cases')
plt.xticks(rotation=0)
plt.title('Cumulative number of SARS cases')
plt.grid(True)
#plt.legend(bbox_to_anchor=(1.05,0),loc=3,borderaxespad=0)
plt.show()


# Trend of cumulative number of deaths
ax2 = df_CN.plot(x='Date',y='Number of deaths',label='China',figsize=(8,4))
df_HK.plot(ax=ax2,x='Date',y='Number of deaths',label='Hong Kong SAR, China')
df_TW.plot(ax=ax2,x='Date',y='Number of deaths',label='Taiwan, China')
df_CAN.plot(ax=ax2,x='Date',y='Number of deaths',label='Canada')
df_SGP.plot(ax=ax2,x='Date',y='Number of deaths',label='Singapore')
plt.xlabel('Time')
plt.ylabel('Total deaths')
plt.xticks(rotation=0)
plt.title('Cumulative number of SARS deaths')
plt.grid(True)
#plt.legend(bbox_to_anchor=(1.05,0),loc=3,borderaxespad=0)
plt.show()


# Bar chart
df_max_max = df_max.loc[['Canada','China','Hong Kong SAR, China','Taiwan, China','Singapore'],\
    ['Number of deaths','Cumulative number of case(s)']]
df_max_max = df_max_max.rename(columns={'Cumulative number of case(s)':'Number of cases'})
#print(df_max_max)
df_max_max.plot.bar(stacked=True)
plt.xlabel('Country/Region')
plt.ylabel('Total cases')
plt.xticks(rotation=45)
plt.title('Total cases of SARS')
plt.show()
