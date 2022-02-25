import streamlit as st
import pandas as pd
import altair as alt
import os


st.header("Assignment 2 app")

# wget --content-disposition "https://api.covidcast.cmu.edu/epidata/covidcast/csv?signal=jhu-csse:confirmed_incidence_num&start_day=2021-01-01&end_day=2021-12-31&geo_type=nation"

# wget --content-disposition "https://api.covidcast.cmu.edu/epidata/covidcast/csv?signal=fb-survey:smoothed_wcovid_vaccinated&start_day=2021-01-01&end_day=2021-12-31&geo_type=nation"

# wget --content-disposition "https://api.covidcast.cmu.edu/epidata/covidcast/csv?signal=fb-survey:smoothed_wcovid_vaccinated_appointment_or_accept&start_day=2021-01-01&end_day=2021-12-31&geo_type=nation"


@st.cache
def load(file):
    return pd.read_csv(file)

df_cc = load('covidcast-jhu-csse-confirmed_incidence_num-2021-01-01-to-2021-12-31.csv')
df_a = load('covidcast-fb-survey-smoothed_wcovid_vaccinated_appointment_or_accept-2021-01-01-to-2021-12-31.csv')
df_v = load('covidcast-fb-survey-smoothed_wcovid_vaccinated-2021-01-01-to-2021-12-31.csv')


df = df_v.merge(df_a,on='time_value', how='inner', sort=True)
df = df[['time_value','value_x','stderr_x','sample_size_x','value_y','stderr_y','sample_size_y']]
df.columns = ['time_value','vaccinated_total_percent','vaccinated_total_stderr','vaccinated_total_sample_size','vaccine_acceptance_percent','vaccine_acceptance_stderr','vaccine_acceptance_sample_size']

df_final =df.merge(df_cc, on='time_value', how='inner', sort=True)
df_final = df_final[['time_value','vaccinated_total_percent','vaccinated_total_sample_size','vaccine_acceptance_percent','vaccine_acceptance_sample_size','value']]
df_final.columns = ['time_value','vaccinated_total_percent','vaccinated_total_sample_size','vaccine_acceptance_percent','vaccine_acceptance_sample_size','Daily New Covid Case Counts']

df_final['time_value'] = pd.to_datetime(df_final['time_value'])
ind = df_final.groupby(pd.Grouper(freq='W', key='time_value', label='left')).mean().index
df2 = df_final.groupby(pd.Grouper(freq='W', key='time_value', label='right')).mean().reset_index()
df2['start_date'] = ind
df2['time_value'] = df2['start_date'].dt.strftime('%Y/%m/%d') + ' - ' + df2['time_value'].dt.strftime('%Y/%m/%d')


input_dropdown = alt.binding_select(options = ["Adelie", "Chinstrap", "Gentoo"], name="Species")
picked = alt.selection_single(encodings=["color"], bind=input_dropdown)

vacc_final = alt.Chart(df2).mark_area(opacity=0.6).transform_fold(
    fold=['vaccinated_total_percent', 'vaccine_acceptance_percent'], 
    as_=['variable', 'value']
).encode(
    alt.X('time_value:N'),
    alt.Y('value:Q',scale=alt.Scale(zero=False, nice=False), stack=None),
    alt.Color('variable:N',scale=alt.Scale(domain=["vaccinated_total_percent", "vaccine_acceptance_percent"], range=["gray", "lightblue"]))
).properties(width = 600)

cli = alt.Chart(df2).mark_line(tooltip=True, point=True).encode(
   x="time_value",
   y="Daily New Covid Case Counts"
).properties(width = 600)

selection = alt.selection_interval(encodings=['x'])
final_chart = cli.add_selection(selection) | vacc_final.transform_filter(selection)

st.write(final_chart)