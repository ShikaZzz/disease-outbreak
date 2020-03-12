#!/usr/bin/env python
# coding: utf-8

# In[32]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


# In[2]:


get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.auto_scroll_threshold = 9999;')


# In[3]:


## loading data
h1n1 = pd.read_csv('H1N12009.csv', encoding = "ISO-8859-1")
ebola= pd.read_csv('ebola_2014_2016_clean.csv')
sars= pd.read_csv('sars_2003_complete_dataset_clean.csv')


# In[4]:


#### prepare data for each disease
poilo = pd.read_csv('polio.csv',usecols=['Cname','2014'],encoding = "ISO-8859-1")
poilo.columns = ['Country','Cases']


# In[5]:


h1n1.columns = ['Country','Cases','Deaths','Date']


# In[6]:


ebola = ebola[['Date', 'Country', 'No. of confirmed, probable and suspected cases',
                     'No. of confirmed, probable and suspected deaths']]
ebola.columns = ['Date','Country','Cases','Deaths']


# In[7]:


ebola_bycountrydate = ebola.groupby(['Date', 'Country'])[['Cases', 'Deaths']]
ebola_bycountrydate = ebola_bycountrydate.sum().reset_index()


# In[8]:


sars = sars[['Date', 'Country', 'Cumulative number of case(s)', 
                   'Number of deaths', 'Number recovered']]
sars.columns = ['Date', 'Country', 'Cases', 'Deaths', 'Recovered']
sars_bycountryate = sars.groupby(['Date', 'Country'])[['Cases', 'Deaths', 'Recovered']]


# In[ ]:





# In[9]:


def groupby_cate(df):
    '''
    return dataframe based on group by Date and Country
    :param df: disease
    :type df: DataFrame
    :return: the number of cases and death by groups
    :rtype: DataFrame
    '''
    
    cases = df.groupby(['Date','Country'])[['Cases', 'Deaths']]
    cases = cases.sum().reset_index()
        
    return cases

def count_cases(df,total=True,countries=False):
    '''
    count the number of cases of disease group by a category. If total is True, count the total number;
    if total is False, count the cases of death
    :param df: disease
    :type disease: list 
    :param total: if count the total cases
    :type total: bool
    :return: the number of cases
    :rtype: int
    '''
    #assert isinstance(df, pd.DataFrame)
    assert isinstance(total, bool)
    
    for d in df: 
        disease = groupby_cate(d)
        total_cases = d[d['Date'] == max(d['Date'])].reset_index()
        disease_groupby = total_cases.groupby('Country')[['Cases','Deaths']].sum().reset_index()
        
        if countries == True:
            yield len(disease_groupby['Country'].value_counts())
        elif total==True:
            yield sum(disease_groupby['Cases'])
        else:
            yield sum(disease_groupby['Deaths'])
            
        
    
    


# In[10]:


## set no. of cases, no. of death, no of countries
s_cases,e_cases = count_cases([sars,ebola])
s_deaths, e_deaths = count_cases([sars,ebola],total=False)
s_countries, e_countries = count_cases([sars,ebola],countries=True)


# In[11]:


h_cases = 6724149
h_deaths = 19654
h_countries = 178

h1n1_fatality =  '0.01-0.08%'
ebola_fatality = '50%.'
sars_fatality ='11%'


# In[12]:


# p_cases = poilo['Cases'].sum()
# p_cases


# In[13]:


## no of cases
diseases = pd.DataFrame({
    'disease' : ['H1N1','SARS', 'EBOLA' ],
    'confirmed' : [h_cases, s_cases, e_cases],
    'deaths' : [h_deaths, s_deaths, e_deaths],
    'no_of_countries' : [h_countries, s_countries, e_countries],
    'fatality_rate':[h1n1_fatality,sars_fatality,ebola_fatality]
})


diseases.head()


# In[14]:


###visulization
#color scheme

h1n1_color = '#DC143C'
ebola_color = '#4169E1'
sars_color = '#FFD700'


# In[15]:


fig = px.bar(diseases.sort_values('confirmed',ascending=False), 
             x="confirmed", y="disease", color='disease', 
             text='confirmed', orientation='h', title='Total Cases of Each Disease Globally', 
             range_x=[0,7700000],
             color_discrete_sequence = [h1n1_color, ebola_color, sars_color])
fig.update_traces(texttemplate='%{text:.3s}',textposition='outside')
fig.update_layout(uniformtext_minsize=20, uniformtext_mode='hide',xaxis_title = 'No. of confirmed cases',font=dict(size=15))

fig.show()
fig.write_image("plot/total_case_by_disease.jpeg")


# In[16]:


fig = px.bar(diseases.sort_values('deaths',ascending=False), 
             x="deaths", y="disease", color='disease', 
             text='deaths', orientation='h', title='Disease Death Toll Globally',
             range_x=[0,21700],
             color_discrete_sequence = [h1n1_color, ebola_color, sars_color])
fig.update_traces(texttemplate='%{text:.3s}',textposition='outside')
fig.update_layout(uniformtext_minsize=20, uniformtext_mode='hide',font=dict(size=15))


fig.show()


# In[17]:


fig = px.bar(diseases.sort_values('no_of_countries', ascending=False),
             x="no_of_countries", y="disease", color='disease', 
             text='no_of_countries', orientation='h', title='No. of Infected Countries', 
             range_x=[0,190],
             color_discrete_sequence =  [h1n1_color, ebola_color, sars_color])
fig.update_traces(textposition='outside')
fig.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',xaxis_title='No. of countries',font=dict(size=15))
fig.show()


# In[18]:


import string
import re


# In[19]:


### h1n1

h1n1_datecountry = groupby_cate(h1n1)
h1n1_datecountry.index = pd.to_datetime(h1n1_datecountry['Date'])


# In[20]:


h1n1_com_cases = pd.read_csv('h1n1_cases.csv')
h1n1_com_death = pd.read_csv('h1n1_death.csv')
h1n1_world_final = pd.read_csv('h1n1_final_cases_world.csv')


# In[21]:


##clean data in the dataset of worldwide cases
RE_PUNCTUATION = '|'.join([re.escape(x) for x in string.punctuation])

h1n1_world_final['Cases']=h1n1_world_final['Cases'].str.replace(RE_PUNCTUATION, "")
h1n1_world_final['Deaths'] = h1n1_world_final['Deaths'].str.replace(RE_PUNCTUATION, "")


# In[22]:


h1n1_world_final['Cases'] = h1n1_world_final['Cases'].astype(int)
h1n1_top_cases = h1n1_world_final.sort_values('Cases',ascending=False)
h1n1_world_final['Deaths'] = h1n1_world_final['Deaths'].astype(int)
h1n1_top_deaths = h1n1_world_final.sort_values('Deaths',ascending=False)


# In[23]:


h1n1_top_cases_few = h1n1_top_cases.head(10)
h1n1_top_deaths_few = h1n1_top_deaths.head(10)


# In[24]:


fig = px.bar(h1n1_top_cases_few, 
             x='Cases',
             y='Country',
             color='Country', 
             text='Cases', orientation='h', title='H1N1: No. of Total Cases (Top 10 Countries)',
             range_x=[0,3.5e6])
fig.update_traces(texttemplate='%{text:.3s}',textposition='outside')
fig.update_layout(uniformtext_minsize=18, uniformtext_mode='hide',font=dict(size=15))


fig.show()


# In[25]:


fig = px.bar(h1n1_top_deaths_few, 
             x='Deaths',
             y='Country',
             color='Country', 
             text='Deaths', orientation='h', title='H1N1: No. of Deaths Cases (Top 10 Countries)',
             range_x=[0,4e3])
fig.update_traces(texttemplate='%{text:.3s}',textposition='outside')
fig.update_layout(uniformtext_minsize=18, uniformtext_mode='hide',font=dict(size=15))


fig.show()


# In[27]:


##### mexico vs US ######
## cases
mex_case = h1n1_com_cases[h1n1_com_cases.Country == 'Mexico']
us_case = h1n1_com_cases[h1n1_com_cases.Country == 'United States of America']
mex_death = h1n1_com_death[h1n1_com_cases.Country == 'Mexico']
us_death = h1n1_com_death[h1n1_com_cases.Country == 'United States of America']
# mex_case.columns[2:]


# In[30]:


get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.prototype._should_scroll = function(lines) {\n    return false;\n}')


# In[33]:





import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

fig = go.Figure()
fig.add_trace(go.Scatter(x=us_case.columns[2:], y=us_case.iloc[0,2:], name="US",
                    mode='lines+markers'))
fig.add_trace(go.Scatter(x=mex_case.columns[2:], y=mex_case.iloc[0,2:], name='Mexico',
                    mode='lines+markers'))
fig.update_layout(
    title_text="H1N1 Total Cases: US vs Mexico (First Wave)"
)
fig.show()


# In[34]:


fig = go.Figure()
fig.add_trace(go.Scatter(x=us_death.columns[2:], y=us_death.iloc[0,2:], name="US",
                    mode='lines+markers'))
fig.add_trace(go.Scatter(x=mex_death.columns[2:], y=mex_death.iloc[0,2:], name='Mexico',
                    mode='lines+markers'))
fig.update_layout(
    title_text="H1N1 Deaths: US vs Mexico (First Wave)"
)
fig.show()


# In[35]:


mex_total_case = h1n1_world_final[h1n1_world_final.Country=='Mexico']['Cases']
mex_total_deaths = h1n1_world_final[h1n1_world_final.Country=='Mexico']['Deaths']
us_total_case = h1n1_world_final[h1n1_world_final.Country=='United States']['Cases']
us_total_deaths = h1n1_world_final[h1n1_world_final.Country=='United States']['Deaths']


# In[36]:


h1n1_world_final.set_index('Country')


# In[37]:


## compare mexico vs us, H1N1
h1n1_world_final.set_index('Country')

h1n1_mex_us = h1n1_world_final.set_index('Country').loc[['Mexico', 'United States']]
h1n1_world_final.reset_index()

h1n1_us = h1n1_world_final[h1n1_world_final.Country=='United States']


# In[38]:


h1n1_world_final.sort_values(by=['Cases'], inplace=True,ascending=False)


# In[41]:




countries=['Mexico', 'US']
total_cases = [mex_total_case,us_total_case]
total_deaths = [mex_total_deaths,us_total_deaths]
fig = go.Figure(data=[
     go.Bar(name='Total Death', x=h1n1_mex_us.index, y=h1n1_mex_us['Deaths']),   
    go.Bar(name='Total Cases', x=h1n1_mex_us.index, y=h1n1_mex_us['Cases'])
    
])
# Change the bar mode
fig.update_layout(barmode='stack')
fig.show()


#x=mex_death.columns[2:], y=mex_death.iloc[0,2:], name='Mexico'


# In[43]:


Mexico = h1n1_datecountry[h1n1_datecountry.Country == 'Mexico']
US = h1n1_datecountry[h1n1_datecountry.Country == 'United States of America']
US


# In[44]:


##flight data
airport = pd.read_csv("airports-extended.csv")
flight_2009 = pd.read_csv("2009.csv", usecols=["FL_DATE","ORIGIN", "DEST", "CANCELLED", "CANCELLATION_CODE"])


# In[45]:


## process flight data for later analysis
flight_2009.index = pd.to_datetime(flight_2009['FL_DATE'])


# In[46]:


monthly_2009 = flight_2009.resample('M')['ORIGIN'].count()


# In[47]:



monthly_2009_df = monthly_2009.to_frame()


# In[48]:


monthly_2009


# In[49]:


month_name = monthly_2009.index.month_name()


# In[50]:


import plotly.graph_objects as go
fig = go.Figure(go.Scatter(
    x = month_name,
    y = monthly_2009_df['ORIGIN'],
))

fig.update_layout(
    title = 'No. of Flights in the U.S Monthly in 2009',
    xaxis_title = 'Month',
    yaxis_title = 'No. of Flights',
    xaxis_tickformat = '%d %B (%a)<br>%Y',
    uniformtext_minsize=20  
)

fig.show()

