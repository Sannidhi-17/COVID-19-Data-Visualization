#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#pip install dash==1.11.0


# In[ ]:


#pip install plotly==4.6.0


# In[1]:


import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table_experiments as dt
import dash.dependencies
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as py


# # Below Section Done By Nikita Kumari And Ajitesh Bhan

# In[2]:


covid19=pd.read_csv("covid_19.csv")
covid19.head()


# In[3]:


covid19=covid19.fillna('NoState')
# Change the data tye
num_cols=['Confirmed', 'Deaths', 'Recovered']
for col in num_cols:
    temp=[int(i) for i in covid19[col]]
    covid19[col]=temp
    
covid19.groupby(['Country/Region','Confirmed']).sum()
# Creating list of all regions of all counntries
test=covid19
uniq_reg=test['Country/Region'].unique()
states=[]
for reg in uniq_reg:
    states.append(test[test['Country/Region']==reg]['Province/State'].unique())  

# Total Confirmed cases per conutry

confirmcase=[]
for i in range(len(uniq_reg)):
    count=0
    covid_temp=covid19[covid19['Country/Region']==uniq_reg[i]]
    for state in states[i]:
        #print(state)
        count+=covid_temp[covid_temp['Province/State']==state].sort_values('ObservationDate').iloc[-1]['Confirmed']
    confirmcase.append(count)

    
## Total Deaths cases per conutry
total_deaths=[]
for i in range(len(uniq_reg)):
    count=0
    covid_temp=covid19[covid19['Country/Region']==uniq_reg[i]]
    for state in states[i]:
        #print(state)
        count+=covid_temp[covid_temp['Province/State']==state].sort_values('ObservationDate').iloc[-1]['Deaths']
    total_deaths.append(count)


# In[4]:


countrywise=pd.DataFrame(columns=['country','confirmed','deaths'],index=None)
countrywise.country=uniq_reg
countrywise.confirmed=confirmcase
countrywise.deaths=total_deaths
countrywise.to_csv('countrywise.csv')
countrywise.head()


# In[ ]:


data=countrywise.sort_values('confirmed',ascending=False)
#fig = px.treemap(data, path=['country'], values='confirmed',
   #               color='confirmed', hover_data=['country'],
    #              color_continuous_scale='Rainbow')
#fig.show()


# In[ ]:


#Distribution of confirmed and death cases around the globe 

from plotly.subplots import make_subplots
data=countrywise.sort_values('confirmed',ascending=False)
data.loc[data['confirmed'] < 20000, 'country'] = 'Other countries'
data.loc[data['deaths'] < 1000, 'country'] = 'Other countries'
labels=list(data['country'])

fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
fig.add_trace(go.Pie(labels=labels, values=list(data['confirmed']), name='country'),
              1, 1)
fig.add_trace(go.Pie(labels=labels, values=list(data['deaths']), name='country'),
              1, 2)
fig.update_traces(hole=.4, hoverinfo="label+percent+name",textposition='inside',textfont_size=12)

fig.update_layout(
    title_text="Distribution of confirmed and death cases around the globe.",
 
    annotations=[dict(text='Confirm', x=0.18, y=0.5, font_size=14, showarrow=False),
                 dict(text='Deaths', x=0.82, y=0.5, font_size=14, showarrow=False)])
fig.show()


# In[17]:


#Analysis of death and Infection around the globe.


dateandcountrywise = covid19.groupby(['ObservationDate', 'Country/Region'])['Confirmed', 'Deaths', 'Recovered'].max().reset_index()
x_date = covid19.groupby(['ObservationDate','Country/Region'])
x_date = (pd.DataFrame(x_date)).iloc[:,0].max()
cases_by_date = pd.DataFrame(dateandcountrywise)
figch = px.choropleth(cases_by_date, locations="Country/Region", locationmode='country names', 
                     color="Confirmed", hover_name="Country/Region",hover_data = [dateandcountrywise.Confirmed,dateandcountrywise.Deaths,dateandcountrywise.Recovered],projection="mercator",
                     animation_frame="ObservationDate",width=950, height=700,
                     color_continuous_scale='Reds',
                     range_color=[2000,6000],

                     title='Analysis of death and Infection around the globe.')

figch.update(layout_coloraxis_showscale=True)
figch.update_layout(
    autosize=False,
    width=1300,
    height=800)
#py.offline.iplot(figch)


# In[ ]:


# patient death ration according age group and gender
covid19age_sex=pd.read_csv("Covid19agegroup.csv")
covid19age_sex['birth_year'] = covid19age_sex['birth_year'] .fillna(0.0)
# getting age of patient
covid19age_sex['age'] = 2020 - covid19age_sex['birth_year'] 
bins = [18, 30, 40, 50, 60, 70, 120]
labels = ['18-29', '30-39', '40-49', '50-59', '60-69', '70+']
covid19age_sex['agerange'] = pd.cut(covid19age_sex.age, bins, labels = labels,include_lowest = True)
covid19age_sex.head()


# In[ ]:


# patient death ration according age group and gender
patient_dead = covid19age_sex[covid19age_sex.state == 'deceased']
male_death = patient_dead[patient_dead.sex=='male']
female_death = patient_dead[patient_dead.sex=='female']


# In[ ]:


sorted_pateient=patient_dead.sort_values("agerange", axis = 0, ascending = False,inplace=False, kind='quicksort', na_position='last')

figage_gender = px.histogram(sorted_pateient, x="agerange", color="sex",  title='Breakdown of the COVID 19 fatalities by age and gender wise. COVID 19 has had adverse effect on the elderly population.')
figage_gender.show()


# In[ ]:


# Hospital bed per 1000 people
beds=pd.read_csv("hospitalbeds.csv",engine='python')
data = beds.rename(
        columns = {'Country Name':'country'
                   ,'Country Code':'countrycode'
                   ,'Indicator Name':'Indname'
                   ,'Indicator Code':'Indcode'
                   }
        )

data = data.melt(id_vars = ['country','countrycode','Indname','Indcode']
                 ,var_name = 'year_RAW'
                 ,value_name = 'totalbed'
                 )


# In[ ]:


data['totalbed'] = data['totalbed'] .fillna(0)


# In[ ]:


beddata = data.groupby(['year_RAW', 'country'])['totalbed'].max().reset_index()
array = ['India', 'China','United States','Indonesia','Pakistan','Brazil','Nigeria','Bangladesh','Russia','Mexico','japan','Germany',
        'Russian Federation','France','United Kingdom','Turkey','Vietnam']
beddata = beddata[beddata.country.isin(array)]
beddata


# In[ ]:


beddata = beddata.groupby(['country'])['totalbed'].max().reset_index()
bedperth=beddata.sort_values("totalbed", axis = 0, ascending = False,inplace=False, kind='quicksort', na_position='last')
bedperth


# In[ ]:


figbed = go.Figure(go.Bar(
            x=bedperth.totalbed,
            y=bedperth.country,marker=dict(
          color='rgba(50, 171, 96, 0.6)'),
            orientation='h'))


figbed.update_layout(
    title="Hospital Beds per 1000 people (In Most populated country)",
    xaxis_title="Hospital Beds Per 1000 People",
    yaxis_title="Country",
    autosize=False,
    width=1200,
    height=700,
    font=dict(
        family='Courier New, monospace',
        size=18,
        color="#7f7f7f"
    )
)

figbed.add_annotation(
            x=5,
            y=0,
            text="<br> WHO <br>Recommended bed</b>")
figbed.update_annotations(dict(
            xref="x",
            yref="y",
            showarrow=True,
            font=dict(
            family="Courier New, monospace",
            size=16,
            color="#FF0000"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#000011",
        ax=0,
        ay=-400,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ffffff",
        opacity=0.8
))


figbed.show()


# In[ ]:


# Physician bed per 1000 people
physician=pd.read_csv("physician.csv",engine='python')


# In[ ]:


phdata = physician.rename(
        columns = {'Country Name':'country'
                   ,'Country Code':'countrycode'
                   ,'Indicator Name':'Indname'
                   ,'Indicator Code':'Indcode'
                   }
        )

phdata = phdata.melt(id_vars = ['country','countrycode','Indname','Indcode']
                 ,var_name = 'year_RAW'
                 ,value_name = 'totalph'
                 )
phdata.isnull().sum()


# In[ ]:


phdata['totalph'] = phdata['totalph'] .fillna(0)

array = ['China','United States','Italy','Spain','Germany',
        'Russian Federation','France','United Kingdom','Turkey','Brazil']
phdata = phdata[phdata.country.isin(array)]


# In[ ]:


physiciandata = phdata.groupby(['country'])['totalph'].max().reset_index()
physicianper1000=physiciandata.sort_values("totalph", axis = 0, ascending = True,inplace=False, kind='quicksort', na_position='last')
#physicianpersort=physicianper1000.nsmallest(5, 'totalph')
physicianper1000.head()


# In[ ]:




marker_offset = 0.04

def offset_signal(signal, marker_offset):
    if abs(signal) <= marker_offset:
        return 0
    return signal - marker_offset if signal > 0 else signal + marker_offset

data = [
    go.Scatter(
        x=physicianper1000.country,
        y=physicianper1000.totalph,
        mode='lines+markers',
        marker=dict(color='red')
    )
]

# Use the 'shapes' attribute from the layout to draw the vertical lines
layout = go.Layout(
    shapes=[dict(
        type='line',
        xref='x',
        yref='y',
        x0=i,
        y0=0,
        x1=i,
        y1=offset_signal(len(physicianper1000), marker_offset),
        line=dict(
            color='grey',
            width=1
        )
    ) for i in range(len(physicianper1000))],
    title='Physicians per 1000 people (In Worst Affected country)',
     xaxis_title ="Country",
     yaxis_title ="Physicians per 1000 people",
    autosize=False,
    width=1100,
    height=700,
    font=dict(
        family='Courier New, monospace',
        size=18,
        color="#7f7f7f"
    )

)


# Plot the chart
figphysician = go.Figure(data, layout)
figphysician.show()


# In[ ]:


# covid 19 comparision with different dieases

ebola = pd.read_csv("ebola.csv", parse_dates=['Date'])

# selecting important columns only
ebola = ebola[['Date', 'Country', 'No. of confirmed, probable and suspected cases',
                     'No. of confirmed, probable and suspected deaths']]
# renaming columns
ebola.columns = ['Date', 'Country', 'Cases', 'Deaths']
ebola.head()

ebola = ebola.groupby(['Date', 'Country'])['Cases', 'Deaths']
ebola = ebola.sum().reset_index()
ebola['Cases'] = ebola['Cases'].fillna(0)
ebola['Deaths'] = ebola['Deaths'].fillna(0)

# latest
ebolalatest = ebola[ebola['Date'] == max(ebola['Date'])].reset_index()
ebola_data = ebolalatest.groupby('Country')['Cases', 'Deaths'].sum().reset_index()
ebola_data.head()


# In[ ]:


# Sars Data

sars = pd.read_csv("sars.csv", parse_dates=['Date'])
# selecting important columns only
sars = sars[['Date', 'Country', 'Cumulative number of case(s)',  'Number of deaths', 'Number recovered']]
sars.columns = ['Date', 'Country', 'Cases', 'Deaths', 'Recovered']

sars = sars.groupby(['Date', 'Country'])['Cases', 'Deaths', 'Recovered']
sars = sars.sum().reset_index()

saralatest = sars[sars['Date'] == max(sars['Date'])].reset_index()
sars_data = saralatest.groupby('Country')['Cases', 'Deaths', 'Recovered'].sum().reset_index()
sars_data.head()


# In[ ]:


# comparision of above three

covid_cases = sum(countrywise['confirmed'])
covid_deaths = sum(countrywise['deaths'])
covid_country = len(countrywise['country'].value_counts())

ebola_cases = sum(ebola_data['Cases'])
ebola_deaths = sum(ebola_data['Deaths'])
ebola_country = len(ebola_data['Country'].value_counts())

sars_cases = sum(sars_data['Cases'])
sars_deaths = sum(sars_data['Deaths'])
sars_country = len(sars_data['Country'].value_counts())


# In[ ]:


total_comarision=pd.DataFrame(columns=['Pandemic','start_year','end_year','confirmed','death','no_country','Fertility'],index=None)

total_comarision.Pandemic=['COVID-19', 'SARS', 'EBOLA','MERS']
total_comarision.start_year=[2019, 2003, 2014, 2012]
total_comarision.end_year=[2020, 2004, 2016, 2017]
total_comarision.confirmed=[covid_cases, sars_cases, ebola_cases,2494]
total_comarision.death=[covid_deaths, sars_deaths, ebola_deaths,858]
total_comarision.no_country=[covid_country, ebola_country, sars_country,27]
total_comarision.Fertility = round((total_comarision['death']/total_comarision['confirmed'])*100, 2)
total_comarision.to_csv('comarision.csv')

total_comarision.head()


# In[ ]:


from plotly.subplots import make_subplots
import plotly.graph_objects as go


total_comarision=total_comarision.sort_values('confirmed',ascending=False)
total_comarision=total_comarision.sort_values('death',ascending=False)
stages = total_comarision.Pandemic
df_mtl = pd.DataFrame(dict(number=total_comarision.confirmed, stage=stages))
df_mtl['Category'] = 'Confirmed'
df_toronto = pd.DataFrame(dict(number=total_comarision.death, stage=stages))
df_toronto['Category'] = 'Death'

df = pd.concat([df_mtl, df_toronto], axis=0)
fig_confirm = px.funnel(df, x='number', y='stage', color='Category',title="COVID-19 with other known epedemics")
fig_confirm.show()


# In[ ]:


# Test performed by countryies per 1000 people

testing=pd.read_csv("test.csv")

testing = testing.rename(
        columns = {'Total tests per thousand':'TotalTest'
                   }
        )
testing['Date'] = pd.to_datetime(testing['Date'], errors='coerce')
testing.head()


# In[ ]:


array = ['United States','Italy','France','United Kingdom','South Korea','Germany']
testing = testing[testing.Entity.isin(array)]

figtesting = px.scatter(testing, x='Date', y='TotalTest', color='Entity',title='Test Performed per 1000 people')
figtesting.show()


# # Done By Sannidhi Bookseller

# In[ ]:


#read csv file
df = pd.read_csv('covid_19_data.csv')
df = df.rename(
        columns = {'Country/Region':'Country'
                   }
        )

df.head()


# In[ ]:


# find the active cases from the dataset and save in new column Active

df['Active'] = df['Confirmed'] - df['Deaths'] - df['Recovered']


# In[ ]:


# Select countries and apply in new dataframe

ar1 = ['Mainland China']
df1 = df[df.Country.isin(ar1)]
ar2 = ['South Korea']
df2 = df[df.Country.isin(ar2)]
ar3 = ['France']
df3 = df[df.Country.isin(ar3)]
ar4 = ['Italy']
df4 = df[df.Country.isin(ar4)]
ar5 = ['US']
df5 = df[df.Country.isin(ar5)]
ar6 = ['Spain']
df6 = df[df.Country.isin(ar6)]
ar7 = ['Germany']
df7 = df[df.Country.isin(ar7)]


# In[ ]:


#sum of the all active cases as per date
df1 = df1.groupby('ObservationDate')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
df2 = df2.groupby('ObservationDate')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
df3 = df3.groupby('ObservationDate')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
df4 = df4.groupby('ObservationDate')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
df5 = df5.groupby('ObservationDate')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
df6 = df6.groupby('ObservationDate')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
df7 = df7.groupby('ObservationDate')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()


# In[ ]:


#select specific dates for plotting 

array1 = ['22-01-2020', '30-01-2020', '10-02-2020', '20-02-2020', '29-02-2020', '10-03-2020',
         '20-03-2020', '30-03-2020','10-04-2020', '20-04-2020', '30-04-2020']
df1 = df1[df1.ObservationDate.isin(array1)]
df2 = df2[df2.ObservationDate.isin(array1)]
df3 = df3[df3.ObservationDate.isin(array1)]
df4 = df4[df4.ObservationDate.isin(array1)]
df5 = df5[df5.ObservationDate.isin(array1)]
df6 = df6[df6.ObservationDate.isin(array1)]
df7 = df7[df7.ObservationDate.isin(array1)]
df1


# In[ ]:


#sort the values as per confirmed

df1 = df1.sort_values(by='Confirmed')
df2 = df2.sort_values(by='Confirmed')
df3 = df3.sort_values(by='Confirmed')
df4 = df4.sort_values(by='Confirmed')
df5 = df5.sort_values(by='Confirmed')
df6 = df6.sort_values(by='Confirmed')
df7 = df7.sort_values(by='Confirmed')
df1


# In[ ]:


import plotly.graph_objs as go

figActive = go.Figure()

figActive.add_trace(go.Scatter(x=df1['ObservationDate'], y=df1['Active'], name = 'China',
                     line = {'width': 2, 'color': 'black'}))
figActive.add_trace(go.Scatter(x=df3['ObservationDate'], y=df3['Active'], name = 'France',
                    line = {'width': 2, 'color': 'Blue'}))
figActive.add_trace(go.Scatter(x=df4['ObservationDate'], y=df4['Active'], name = 'Italy',
                    line = {'width': 2, 'color': 'red'}))
figActive.add_trace(go.Scatter(x=df5['ObservationDate'], y=df5['Active'], name = 'USA',
                   line = {'width': 2, 'color': 'green'}))
figActive.add_trace(go.Scatter(x=df6['ObservationDate'], y=df6['Active'], name = 'Spain',
                    line = {'width': 2, 'color': 'orange'}))
figActive.add_trace(go.Scatter(x=df7['ObservationDate'], y=df7['Active'], name = 'Germany',
                    line = {'width': 2, 'color': 'yellow'}))



figActive.update_layout(
    #yaxis=dict(range=[0,12000]),
    xaxis = dict(
        tickmode = 'array',
        tickvals = ['22-01-2020', '30-01-2020', '10-02-2020', '20-02-2020', '29-02-2020', '10-03-2020',
         '20-03-2020', '30-03-2020','10-04-2020', '20-04-2020', '30-04-2020'],
        ticktext = ['22 Jan','30 Jan','10 Feb','20 Feb','29 Feb','10 Mar','20 Mar','30 Mar','30 Mar', '10 Apr','20 Apr','30 Apr'],
        tickangle=360
    ),
    autosize=False,
    width=1500,
    height=700,
    xaxis_title="<b> Dates </b> ",
    yaxis_title="<b> Number of active cases in thousand </b>",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#000000"
    )
)

figActive.add_annotation(
            x=6.05,
            y=1000,
            ax=0,
            ay=-360,
            text="<br> USA <br>on 20 March </b>")
figActive.add_annotation(
            x=5.60,
            y=5500,
            ax=0,
            ay=-200,
            text="<br> France <br>16th March </b>")
figActive.add_annotation(
            x=5.00,
            y=1000,
            ax=0,
            ay=-290,
            text="<br> Italy <br>10th March </b>")
figActive.add_annotation(
            x=7.15,
            y=70000,
            ax=0,
            ay=-250,
            text="<br> Germany <br>2nd April </b>")
figActive.add_annotation(
            x=0.10,
            y=1000,
            ax=0,
            ay=-250,
            text="<br> China <br>23rd January</b>")

figActive.add_annotation(
            x=5.40,
            y=5500,
            ax=0,
            ay=-450,
            text="<br> Spain <br>14th March</b>"),

figActive.update_annotations(dict(
            xref="x",
            yref="y",
            showarrow=True,
            font=dict(
            family="Courier New, monospace",
            size=16,
            color="#000000"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#000011",
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ffffff",
        opacity=0.8
))


# In[ ]:


# minus below row from above row for the date wise cases
df1['new'] = df1.Confirmed.diff()
df2['new'] = df2.Confirmed.diff()
df3['new'] = df3.Confirmed.diff()
df4['new'] = df4.Confirmed.diff()
df5['new'] = df5.Confirmed.diff()
df6['new'] = df6.Confirmed.diff()
df7['new'] = df7.Confirmed.diff()


# In[ ]:


# convert into positive number
df1['new'] = df1['new'].abs()
df2['new'] = df2['new'].abs()
df3['new'] = df3['new'].abs()
df4['new'] = df4['new'].abs()
df5['new'] = df5['new'].abs()
df6['new'] = df6['new'].abs()
df7['new'] = df7['new'].abs()


# In[ ]:


# now filling epmty space with cases
df1["new"].fillna("1")
df2["new"].fillna("1")
df3["new"].fillna("5")
df4["new"].fillna("3")
df5["new"].fillna("1")
df6["new"].fillna("2")
df7["new"].fillna("4")


# In[ ]:


import plotly.graph_objects as go # or plotly.express as px
figConfirmed = go.Figure()
figConfirmed.add_trace(go.Scatter(x=df1['ObservationDate'], y=df1['new'], name = 'China',
                     line = {'width': 2, 'color': 'black'}))
figConfirmed.add_trace(go.Scatter(x=df3['ObservationDate'], y=df3['new'], name = 'France',
                    line = {'width': 2, 'color': 'Blue'}))
figConfirmed.add_trace(go.Scatter(x=df4['ObservationDate'], y=df4['new'], name = 'Italy',
                    line = {'width': 2, 'color': 'red'}))
figConfirmed.add_trace(go.Scatter(x=df6['ObservationDate'], y=df6['new'], name = 'Spain',
                    line = {'width': 2, 'color': 'orange'}))
figConfirmed.add_trace(go.Scatter(x=df7['ObservationDate'], y=df7['new'], name = 'Germany',
                    line = {'width': 2, 'color': 'yellow'}))

figConfirmed.update_layout(
    #yaxis=dict(range=[0,12000
    xaxis = dict(
        tickmode = 'array',
        tickvals = ['22-01-2020', '30-01-2020', '10-02-2020', '20-02-2020', '29-02-2020', '10-03-2020',
         '20-03-2020', '30-03-2020','10-04-2020', '20-04-2020', '30-04-2020'],
        ticktext = ['22 Jan','30 Jan','10 Feb','20 Feb','29 Feb','10 Mar','20 Mar','30 Mar','30 Mar', '10 Apr','20 Apr','30 Apr'],
        tickangle=360
    ),
    autosize=False,
    width=1500,
    height=700,
    xaxis_title="<b> Dates </b> ",
    yaxis_title="<b> Number of Confirmed Cases in Thousand </b>",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#000000"
    )
)

figConfirmed.add_annotation(
            x=0.10,
            y=1000,
            ax=0,
            ay=-200,
            text="<br> China <br>23rd January")
figConfirmed.add_annotation(
            x=5.65,
            y=6500,
            ax=0,
            ay=-200,
            text="<br> France <br>16th March")
figConfirmed.add_annotation(
            x=7.25,
            y=49000,
            ax=0,
            ay=-200,
            text="<br> Germany <br>2nd April")
figConfirmed.add_annotation(
            x=5.00,
            y=7300,
            ax=0,
            ay=-290,
            text="<br> Italy <br>10th March")
figConfirmed.add_annotation(
            x=5.45,
            y=8200,
            ax=0,
            ay=-380,
            text="<br> Spain <br>14th March"),
figConfirmed.update_annotations(dict(
            xref="x",
            yref="y",
            arrowcolor = "#000011",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ffffff",
            opacity=0.8
))


# In[ ]:


#deaths pr day and storing in onther column
df1['new_deaths'] = df1.Deaths.diff()
df2['new_deaths'] = df2.Deaths.diff()
df3['new_deaths'] = df3.Deaths.diff()
df4['new_deaths'] = df4.Deaths.diff()
df5['new_deaths'] = df5.Deaths.diff()
df6['new_deaths'] = df6.Deaths.diff()
df7['new_deaths'] = df7.Deaths.diff()
df3


# In[ ]:


# filling empty values as per dataset
df1["new_deaths"].fillna("17")
df2["new_deaths"].fillna("0")
df3["new_deaths"].fillna("0")
df4["new_deaths"].fillna("0")
df5["new_deaths"].fillna("0")
df6["new_deaths"].fillna("0")
df7["new_deaths"].fillna("0")
df3


# In[ ]:


import plotly.graph_objects as go # or plotly.express as px
from plotly.subplots import make_subplots

figDeaths = go.Figure() # or any Plotly Express function e.g. px.bar(...)
figDeaths = make_subplots(rows=3, cols=2, shared_yaxes=False, x_title='Dates', 
                    y_title='Number of death in thousand ',
                    subplot_titles=("China Announced Lockdown On 23rd January ","USA Announced Lockdown On 20th March", "France 16th Announced Lockdown On March",
                                    "Italy Announced Lockdown On 10th March",
                                    "Spain Announced Lockdown On 14th March",
                                    "Germany Announced Lockdown On 2nd April"))
figDeaths.add_trace(go.Scatter(x=df1['ObservationDate'], y=df1['new_deaths'], name = 'China',
                     line = {'width': 2, 'color': 'black'}),row=1, col=1)
figDeaths.add_trace(go.Scatter(x=df5['ObservationDate'], y=df5['new_deaths'], name = 'USA',
                    line = {'width': 2, 'color': 'green'}),row=1, col=2)
figDeaths.add_trace(go.Scatter(x=df3['ObservationDate'], y=df3['new_deaths'], name = 'France',
                    line = {'width': 2, 'color': 'Blue'}),row=2, col=1)
figDeaths.add_trace(go.Scatter(x=df4['ObservationDate'], y=df4['new_deaths'], name = 'Italy',
                    line = {'width': 2, 'color': 'red'}),row=2, col=2)
figDeaths.add_trace(go.Scatter(x=df6['ObservationDate'], y=df6['new_deaths'], name = 'Spain',
                    line = {'width': 2, 'color': 'orange'}),row=3, col=1)
figDeaths.add_trace(go.Scatter(x=df7['ObservationDate'], y=df7['new_deaths'], name = 'Germany',
                    line = {'width': 2, 'color': 'green'}),row=3, col=2)

figDeaths.update_layout(height=1000, width=1500)
#fig.update_xaxes(tickangle=340)
figDeaths.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = ['22-01-2020', '30-01-2020', '10-02-2020', '20-02-2020', '29-02-2020', '10-03-2020',
         '20-03-2020', '30-03-2020','10-04-2020', '20-04-2020', '30-04-2020'],
        ticktext = ['22 Jan','30 Jan','10 Feb','20 Feb','29 Feb','10 Mar','20 Mar','30 Mar','30 Mar', '10 Apr','20 Apr','30 Apr'],
        tickangle=360
    ),
    xaxis2 = dict(
        tickmode = 'array',
        tickvals = ['22-01-2020', '30-01-2020', '10-02-2020', '20-02-2020', '29-02-2020', '10-03-2020',
         '20-03-2020', '30-03-2020','10-04-2020', '20-04-2020', '30-04-2020'],
        ticktext = ['22 Jan','30 Jan','10 Feb','20 Feb','29 Feb','10 Mar','20 Mar','30 Mar','30 Mar', '10 Apr','20 Apr','30 Apr'],
        tickangle=360
    ),
    xaxis3 = dict(
        tickmode = 'array',
        tickvals = ['22-01-2020', '30-01-2020', '10-02-2020', '20-02-2020', '29-02-2020', '10-03-2020',
         '20-03-2020', '30-03-2020','10-04-2020', '20-04-2020', '30-04-2020'],
        ticktext = ['22 Jan','30 Jan','10 Feb','20 Feb','29 Feb','10 Mar','20 Mar','30 Mar','30 Mar', '10 Apr','20 Apr','30 Apr'],
        tickangle=360
    ),
    xaxis4 = dict(
        tickmode = 'array',
        tickvals = ['22-01-2020', '30-01-2020', '10-02-2020', '20-02-2020', '29-02-2020', '10-03-2020',
         '20-03-2020', '30-03-2020','10-04-2020', '20-04-2020', '30-04-2020'],
        ticktext = ['22 Jan','30 Jan','10 Feb','20 Feb','29 Feb','10 Mar','20 Mar','30 Mar','30 Mar', '10 Apr','20 Apr','30 Apr'],
        tickangle=360
    ),
    xaxis5 = dict(
        tickmode = 'array',
        tickvals = ['22-01-2020', '30-01-2020', '10-02-2020', '20-02-2020', '29-02-2020', '10-03-2020',
         '20-03-2020', '30-03-2020','10-04-2020', '20-04-2020', '30-04-2020'],
        ticktext = ['22 Jan','30 Jan','10 Feb','20 Feb','29 Feb','10 Mar','20 Mar','30 Mar','30 Mar', '10 Apr','20 Apr','30 Apr'],
        tickangle=360
    ),
    xaxis6 = dict(
        tickmode = 'array',
        tickvals = ['22-01-2020', '30-01-2020', '10-02-2020', '20-02-2020', '29-02-2020', '10-03-2020',
         '20-03-2020', '30-03-2020','10-04-2020', '20-04-2020', '30-04-2020'],
        ticktext = ['22 Jan','30 Jan','10 Feb','20 Feb','29 Feb','10 Mar','20 Mar','30 Mar','30 Mar', '10 Apr','20 Apr','30 Apr'],
        tickangle=360
    )
)


# In[ ]:


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H1(children='Covid 19 Dataset Visualization'),

    html.Div(children=  html.H3(children='Section 1 (Analysis of Covid 19 Infection across the globe)')),
     dcc.Graph(
        id='worldgraph',
        figure=figch ),
      html.Div(children='Above graph provides the timeline of the COVID 19 Pandemic around the globe. The information displayed is the confirmed cases, recovered and deaths. Also the spread has been  mapped since start.',
              style={
        'color': '#0000A0'}),

     dcc.Graph(
        id='casepercountry',
        figure=fig ),
    
     html.Div(children=  html.H3(children='Section 2(Covid 19 states comparision )')),
    dcc.Graph(
        id='comparision_confirm',
        figure=fig_confirm),
     html.Div(children='Above graph compares COVID-19 with other known epedemics. The mortality rate for  COVID-19 is 7.03, SARS 9.64, EBOLA 39.52 and MERS 34.40. Although mortality rate of COVID-19 is low but what makes it dangerous is that it his highly communicable with R0 factor between 2 - 2.5, by comparison R0 for common cold is 1.5.',
              style={
        'color': '#0000A0'}),
    dcc.Graph(
        id='age_sexwise',
        figure=figage_gender),
    
   html.Div(children=  html.H3(children='Section 3(Hospital Bed And physician capacity across the globe )')),

    dcc.Graph(
        id='hospital_bed',
        figure=figbed),
    
      html.Div(children='Above graph displays the available hospital beds per 1000 popullation in 14 most populated countries in world. Note: WHO recommended ratio is 5 beds per 1000 population.',
              style={
        'color': '#0000A0'}),
    
    dcc.Graph(
        id='physician',
        figure=figphysician),
    html.Div(children='Above graph provides the analysis of the No. Of physicians per 1000 personnel in 10 countries that are severely affected by COVID-19',
              style={
        'color': '#0000A0'}),
    
    html.Div(children=  html.H3(children='Section 4(Covid 19 Testing)')),
    dcc.Graph(
        id='testing',
        figure=figtesting),
    html.Div(children='Above graph shows the COVID-19 testing per 1000 person in different countries.',
              style={
        'color': '#0000A0'}),
    
    html.Div(children=  html.H3(children='Section 5(Covid 19 Flattening Curve)')),
   
    html.H3(children='Active cases in worst hit countries '),
    html.Div(children='''Below graph displays the flattening of curve after social
    distancing measure are applied by different countries. The total no. Of active cases flatten and then decrease gradually.'''),
    
    dcc.Graph(id = 'Active Graph', figure=figActive),
    
    html.H3(children='Confirmed cases per country '),
    html.Div(children='''Below graph shows decrease in the new covid-19 cases after social distancing measures are inacted.'''),
    dcc.Graph(id = 'Confirmed Graph', figure=figConfirmed),
    
    html.H3(children='''Multiple Subplots with Shared Y-Axes'''),
    html.H3(children='''Below subplots shows the decline in death rate after lockdown was initiated in each country this was due to 
    the decrease in new cases which resulted in Medical Facilities not being overburdened.'''),
    
    dcc.Graph(id = 'Death Graph', figure=figDeaths),
    
               
])

if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:




