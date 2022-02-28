import streamlit as st
import pandas as pd
import altair as alt

st.session_state.mask = 'Take me Home!'

current_chart = None


@st.cache
def load_vaccine_data():
    df_cc = pd.read_csv('data/covidcast-jhu-csse-confirmed_7dav_incidence_num-2020-03-01-to-2022-02-27.csv')
    df_a = pd.read_csv(
        'data/covidcast-fb-survey-smoothed_wcovid_vaccinated_appointment_or_accept-2020-03-01-to-2022-02-27.csv')
    df_v = pd.read_csv('data/covidcast-fb-survey-smoothed_wcovid_vaccinated-2020-03-01-to-2022-02-27.csv')

    df = df_v.merge(df_a,on='time_value', how='inner', sort=True)
    df = df[['time_value','value_x','stderr_x','sample_size_x','value_y','stderr_y','sample_size_y']]
    df.columns = ['time_value','Vaccinated','vaccinated_total_stderr','vaccinated_total_sample_size','Believe in Vaccine Effectiveness','vaccine_acceptance_stderr','vaccine_acceptance_sample_size']

    df_final =df.merge(df_cc, on='time_value', how='inner', sort=True)
    df_final = df_final[['time_value','Vaccinated','vaccinated_total_sample_size','Believe in Vaccine Effectiveness','vaccine_acceptance_sample_size','value']]
    df_final.columns = ['Time','Vaccinated','vaccinated_total_sample_size','Believe in Vaccine Effectiveness','vaccine_acceptance_sample_size','Daily New Covid Case Counts (7-day Moving Average)']

    df_final['Time'] = pd.to_datetime(df_final['Time'])
    
    return df_final


@st.cache
def load_masking_data():
    tested_positive = "data/covidcast-jhu-csse-confirmed_7dav_incidence_num-2021-01-01-to-2022-02-26.csv"
    df_tested_positive = pd.read_csv(tested_positive).rename(columns={"value": "positive"}).drop(
        ["geo_value", "signal", "issue", "lag", "stderr", "sample_size", "geo_type", "data_source", "Unnamed: 0"],
        axis=1)
    df_tested_positive['positive'] = df_tested_positive['positive'] / 10000

    wearing_mask = "data/covidcast-fb-survey-smoothed_wwearing_mask_7d-2021-02-09-to-2022-02-25.csv"
    df_wearing_mask = pd.read_csv(wearing_mask).rename(columns={"value": "wears_mask"}).drop(
        ["geo_value", "signal", "issue", "lag", "stderr", "sample_size", "geo_type", "data_source", "Unnamed: 0"],
        axis=1)
    belief_mask_effective = "data/covidcast-fb-survey-smoothed_wbelief_masking_effective-2021-06-04-to-2022-02-25.csv"
    df_belief_wearing_mask = pd.read_csv(belief_mask_effective).rename(columns={"value": "belief_mask"}).drop(
        ["geo_value", "signal", "issue", "lag", "stderr", "sample_size", "geo_type", "data_source", "Unnamed: 0"],
        axis=1)

    df_combined = df_tested_positive.merge(df_wearing_mask, 'inner', on='time_value').merge(df_belief_wearing_mask,
                                                                                            'inner', on='time_value')
    df = df_combined.melt('time_value').rename({"variable": "field_name"}, axis=1)

    return df


def get_masking_graph():
    df = load_masking_data()
    legend_selection = alt.selection_multi(fields=['field_name'], bind='legend')

    lines = alt.Chart(df).mark_line().encode(
        alt.X('time_value:T', axis=alt.Axis(title='Date')),
        alt.Y('value:Q'),
        alt.Color('field_name:N'),
        opacity=alt.condition(legend_selection, alt.value(1), alt.value(0.1)),
    ).properties(title="Comparing masking beliefs and behaviour to confirmed case count")

    nearest_selector = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['time_value'], empty='none')

    selectors = alt.Chart(df).mark_point().encode(
        x='time_value:T',
        opacity=alt.value(0),
    ).add_selection(nearest_selector)

    points = lines.mark_point().encode(
        opacity=alt.condition(nearest_selector, alt.value(1), alt.value(0))
    )

    text = lines.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest_selector, 'value:Q', alt.value(' '))
    )

    rules = alt.Chart(df).mark_rule(color='gray').encode(
        x='time_value:T',
    ).transform_filter(nearest_selector)

    layered_chart = alt.layer(
        lines, selectors, points, rules, text
    ).add_selection(
        legend_selection
    ).properties(
        width=800, height=400
    )

    return layered_chart


def get_vaccine_graph():
    df = load_vaccine_data()

    vacc_final = alt.Chart(df).mark_area(opacity=0.6).transform_fold(
    fold=['Vaccinated', 'Believe in Vaccine Effectiveness'], 
    as_=['Respondent Population', 'Respondent Population Percentage']
    ).encode(
        alt.X('Time:T'),
        alt.Y('Respondent Population Percentage:Q',scale=alt.Scale(zero=False, nice=False), stack=None),
        alt.Color('Respondent Population:N',scale=alt.Scale(domain=["Vaccinated", "Believe in Vaccine Effectiveness"], range=["gray", "lightblue"]))
    ).properties(width = 600)
    

    cli = alt.Chart(df).mark_line(tooltip=True, point=True).encode(
    x="Time",
    y="Daily New Covid Case Counts (7-day Moving Average)"
    ).properties(width = 600)

    selection = alt.selection_interval(encodings=['x'])
    final_chart = alt.vconcat(vacc_final.transform_filter(selection),cli.add_selection(selection))

    return final_chart


def display_graph(selection="Take me Home!"):
    if "menu" in st.session_state:
        selection = st.session_state.menu
    if selection == "Masking":
        current_chart = get_masking_graph()
        st.markdown("<h2 style='text-align: center; color: black;'>Masking and COVID-19</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #3a82a6'>What can I learn from this Plot?</h4>", unsafe_allow_html=True)
        st.markdown("<p>You can answer the following questions from this graph - <ul> <li>Are people more likely to "
                    "wear a mask when confirmed case count is higher or lower?</li> <li>Are people more likely to "
                    "believe that wearing a mask is effective in curbing the spread of COVID-19 when case count is "
                    "higher or lower? </li> <li>Do people’s beliefs about the effectiveness of masking agree with "
                    "their behavior of actually wearing a mask? </li></ul></p>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #3a82a6'>What data am I seeing?</h4>", unsafe_allow_html=True)
        st.markdown("<p> The data about masking comes from Facebook surveys where respondents answer questions about "
                    "whether they think masking is effective and whether they have worn a mask in public in the last "
                    "7 days. The blue line plots the proportion of respondents who believe masking is effective. The "
                    "red line plots the proportion of respondents who reported that they wore a mask in public in "
                    "the last 7 days. The data about confirmed case count comes from John’s Hopkins University’s "
                    "COVID-19 dataset. Case counts are scaled down by 10,000.</p>", unsafe_allow_html=True)

        st.markdown("<h4 style='color: #3a82a6'>How can I interact with this plot?</h4>", unsafe_allow_html=True)
        st.markdown("<p>Move your mouse across the plot to see a bar that indicates how the three peices of data "
                    "move together. You can also click on elements of the legend to see only the lines you're "
                    "interested in! Hold down shift while selecting to see more than one line simultaneously.</p>",
                    unsafe_allow_html=True)

        st.write(current_chart)
    elif selection == "Vaccination":
        current_chart = get_vaccine_graph()
        
        st.markdown("<h2 style='text-align: center; color: black;'>Vaccination and COVID-19</h2>",
                    unsafe_allow_html=True)
        
        st.markdown("<h4 style='color: #3a82a6'>What can I learn from this visualization?</h4>", unsafe_allow_html=True)
        st.markdown("<p>You can answer the following questions from these graphs - <ul> <li>Is people's perception about the effectiveness of vaccination more favorable when the case counts are high?</li> <li>Does the number of people getting vaccinated increase as the case counts rise?</li> <li>Do people's beliefs in the effectiveness of vaccination agree with their behavior of actually getting vaccinated?</li></ul></p>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #3a82a6'>What data am I seeing?</h4>", unsafe_allow_html=True)
        st.markdown("<p> The data about vaccination comes from Facebook surveys where respondents answer questions about "
        "whether they think vaccination is effective and whether they have actually been vaccinated."
        "The first graph below depicts a comparison of the percentage of survery respondents that believe that vaccines are effective against Covid-19 (light blue region) against the percentage that have been vaccinated (dark blue region) as the pandemic progresses from June 2021 to February 2022. The second graph below shows a plotting of the 7-day moving average of the daily new covid case counts from June 2021 to February 2022.</p>", unsafe_allow_html=True)

        st.markdown("<h4 style='color: #3a82a6'>How can I interact with these plots?</h4>", unsafe_allow_html=True)
        st.markdown("<p>The second chart depicting the covid case counts allows you to select a range of time for which you can see the panned version of the vaccination graph. Feel free to explore how the vaccination beliefs and behaviors correlate during different phases of the pandemic.</p>",
                    unsafe_allow_html=True)
        st.write(current_chart)

    elif selection == "Take me Home!" or selection == "Select One" :
        st.markdown("<h2 style='text-align: center; color: #1b1b1c;'> <span style='color: #3a82a6'> Unmasking </span> "
                    "the Relationship between Perception and Behaviour</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #3a82a6;'> The COVID-19 Edition</h3>",
                    unsafe_allow_html=True)

        st.markdown("<p style='font-family:Helvetica'><span style='color: #3a82a6'> Do you ever wonder if people "
                    "change they way they think about the COVID-19 pandemic as the severity of the pandemic changes? "
                    "</span> Do more people think masking is effective as the case counts increase? Do more people perceive the importance of vaccination as the case counts rise?</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-family:Helvetica'><span style='color: #3a82a6'> What about whether we change our "
                    "behavior as the pandemic evolves? </span> Do more people actually wear masks when case "
                    "counts are high?</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-family:Helvetica'> <span style='color: #3a82a6'> Do people's behaviors move "
                    "hand-in-hand with their perceptions? </span> If more people believe vaccination is "
                    "effective, do we actually see more people getting vaccinated? </p>",
                    unsafe_allow_html=True)
        st.markdown("<p style='font-family:Helvetica'> Use the options on the sidebar to pick out what COVID-19 "
                    "related perception/behavior you want to study and get answers to these questions! </p>",
                    unsafe_allow_html=True)


st.sidebar.image("img/proto.png", use_column_width=True, output_format="PNG")

selector = st.sidebar.selectbox(
    "What COVID-19 Behavior Would You Like to Study?",
    ("Select One", "Vaccination", "Masking", "Take me Home!"),
    on_change=display_graph(),
    key="menu",
)
