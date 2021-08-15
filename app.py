import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import preprocessor,helper
import plotly.figure_factory as ff
#df = pd.read_csv('Olympic_athlete_events.csv')
df_data1 = pd.read_csv('file1_olympic.csv')
df_data2 = pd.read_csv('file2_olympic.csv')
df=pd.concat([df_data1, df_data2], axis=0)
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)
st.sidebar.title('Summer Olympics Analysis')
#st.sidebar.image('https://globallymobilelocallygrounded.files.wordpress.com/2016/08/olympic-games.jpg')
st.sidebar.image('olympic_logo.png')


user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title('Overall Tally')
    elif selected_year!='Overall' and selected_country=='Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    elif selected_year=='Overall' and selected_country!='Overall':
        st.title(selected_country + ' Overall Performance')
    elif selected_year!='Overall' and selected_country!='Overall':
        st.title(selected_country + ' Performance in ' + str(selected_year) + ' Olympics')
    st.table(medal_tally)


    st.title('Total Medal for ' + selected_country + ' in ' + str(selected_year) + ' Olympics')
    final_df1 = helper.medal_tally_stackchart(df, selected_country)
    if selected_year=='Overall':
        filt = final_df1['Year'].isin(final_df1['Year'].unique())
    else:
        filt=(final_df1['Year']==selected_year)
    final_df2 = final_df1[filt]
    fig = px.bar(final_df2, x='Year', y='Medal_Count', color='Medal')
    st.plotly_chart(fig)

if user_menu=='Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    st.title('Top Statistics')
    col1,col2,col3 = st.beta_columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    fig.update_layout(
        # title="Athletes Over the Year",
        xaxis_title="Edition",
        yaxis_title="No. of Country",
        legend_title="Legend Title",
        font=dict(size=15, color="RebeccaPurple")
    )
    st.title('Participating Nations Over the Year')
    st.plotly_chart(fig)
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    fig.update_layout(
        # title="Athletes Over the Year",
        xaxis_title="Edition",
        yaxis_title="No. of Events",
        legend_title="Legend Title",
        font=dict(size=15, color="RebeccaPurple")
    )
    st.title('Events Over the Year')
    st.plotly_chart(fig)
    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x='Edition', y='Name')
    fig.update_layout(
        #title="Athletes Over the Year",
        xaxis_title="Edition",
        yaxis_title="No. of Athletes",
        legend_title="Legend Title",
        font=dict(size=15,color="RebeccaPurple")
    )
    st.title('Athletes Over the Year')
    st.plotly_chart(fig)

    st.title('No. of Events Over Time(Every Sport)')
    fig,ax = plt.subplots(figsize=(30,22))
    x = df.drop_duplicates(['Year', 'Event', 'Sport'])
    sns.set(font_scale=1.5)
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=='Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country',country_list)
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    fig.update_layout(
        # title="Athletes Over the Year",
        xaxis_title="Edition",
        yaxis_title="No. of Medals",
        legend_title="Legend Title",
        font=dict(size=15, color="RebeccaPurple")
    )
    st.title(selected_country + ' Medal Tally Over the Year')
    st.plotly_chart(fig)

    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(30,22))
    sns.set(font_scale=1.5)
    ax = sns.heatmap(pt,annot=True)
    st.title(selected_country + ' Excels In The Following Sport')
    st.pyplot(fig)

    st.title('Top 15 Athletes of ' + selected_country)
    top15_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top15_df)


if user_menu=='Athlete wise Analysis':
    st.sidebar.title('Athlete wise Analysis')
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600,
        xaxis_title="Athlete Age",
        yaxis_title="Probability",
        font=dict(size=13, color="RebeccaPurple")
    )
    st.title('Distribution of Athlete Age Based on Medal')
    st.plotly_chart(fig)
#--------------------------------------------------------------------
    x=[]
    name=[]
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
           'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
           'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
           'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Equestrianism',
           'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
           'Tennis', 'Modern Pentathlon', 'Golf', 'Softball', 'Archery',
           'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
           'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining',
           'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo',
           'Cricket', 'Ice Hockey', 'Motorboating','Figure Skating']
    for sport in famous_sports:
        temp_df=athlete_df[athlete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x,name,show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=900, height=500,
                      xaxis_title="Athlete Age",
                      yaxis_title="Probability",
                      legend_title="Olympics Sports",
                      font=dict(size=13, color="RebeccaPurple"))
    st.title('Distribution of Gold Medalist Athlete Age Based on Sport')
    st.plotly_chart(fig)
#----------------------------------------------------------------------------------
    st.title('Height vs Weight of Athlete')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig = px.scatter(temp_df, x="Weight", y="Height", color="Medal", hover_data=['region', 'Name'], symbol='Sex')
    fig.update_layout(autosize=False, width=900, height=650,
                      xaxis_title="Weight",
                      yaxis_title="Height",
                      legend_title="Medal, Sex",
                      font=dict(size=13, color="RebeccaPurple"))
    #plt.figure(figsize=(25,25))
    st.plotly_chart(fig)

    st.title('Men v/s Women Participation')
    final=helper.men_vs_women(df)
    fig = px.line(final,x='Year',y=['Male','Female'])
    fig.update_layout(autosize=False, width=800, height=500,
                      xaxis_title="Year of Olympics",
                      yaxis_title="Count of men and women",
                      legend_title="Gender",
                      font=dict(size=13, color="RebeccaPurple"))
    st.plotly_chart(fig)





















