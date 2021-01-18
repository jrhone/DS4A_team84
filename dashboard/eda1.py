import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as sm
#import warnings
import altair as alt
# pip uninstall protobuf python3-protobuf
# pip install --upgrade pip
# pip install --upgrade protobuf 

# app1.py
import streamlit as st
def app():
    st.title('Does school funding impact students academic performance?')
    # https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4
    # http://awesome-streamlit.org/https://news.ycombinator.com/item?id=21158487https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace
    # https://docs.streamlit.io/en/stable/caching.html
    ## Initial EDA

    df = pd.read_csv('~/team_84/notebooks/20210111/final_merged.csv', index_col = 0)
    # filtering based on total enrollment
    df = df[df['Total Enrollment'] != 0]
    df = df[df['Total Enrollment'] > 250]

    # filtering office of education out of the main dataset for analysis
    # dataset containing only districts called office of education:
    OFFICE_OF_EDUCATION = df[df['Agency Name'].str.contains('COUNTY OFFICE OF EDUCATION')]

    # filter office of education out of the main dataset
    df = df[~df['Agency Name'].str.contains('COUNTY OFFICE OF EDUCATION')]

    # filter Charters out of the main dataset
    df = df[~df['Agency Name'].str.contains('SBE - AUDEO CHARTER')]

    # sort by alphabetical oder on Agency Name
    df = df.sort_values(['Agency Name'])

    # dataset containing school districts with over $20,000 revenue per student
    df_high_funding = df[(df['Revenue per student'] > 20_000)]

    # update the main dataset to not include schools with over 20k revenue per student nor zero revenue per student
    df = df[~(df['Revenue per student'] > 20_000)]
    df = df[~(df['Revenue per student'] == 0)]

    '''
    ## DATASET TEST ID 1
    '''

    list = ['1.0']
    test_Id1 = df[df['Test Id'].isin(list)]
    test_ID1 = test_Id1.drop(['Test Id', 'County Code', 'Total Tested At Entity Level', 
                   'Total Standard Met and Above', 'Total Revenue',
                  'Total Tested with Scores', 'Students with Scores', 'District Code'], axis=1)

    _ = plt.hist(test_ID1['Revenue per student'], density=False, bins=30)
    _ = plt.ylabel('Number of ocurrences')
    _ = plt.xlabel('Revenue')
    _ = plt.title("Revenue per Student")

    st.pyplot(plt)

    # https://github.com/streamlit/streamlit/issues/638
    plt.figure() 

    st.markdown('## PASS/FAIL Dataset - Test ID 1')

    # adding pass and fail columns 
    test_ID1['Pass'] = test_ID1['Total Standard Exceeded'] + test_ID1['Total Standard Met']
    test_ID1['Fail'] = test_ID1['Total Standard Nearly Met'] + test_ID1['Total Standard Not Met']

    # creating a new dataframe by copying
    pass_fail_df = test_ID1.copy()

    # dropping columns
    pass_fail_df = pass_fail_df.drop(['Total Standard Exceeded', 'Total Standard Met', 'Total Standard Nearly Met', 
                   'Total Standard Not Met', 'CAASPP Reported Enrollment', 'Count Enrollment per ethnicity'], axis=1)

    #rearranging columns
    pass_fail_df = pass_fail_df.reindex(columns=['Agency Name', 'Subgroup ID','Revenue per student', 
                                                 'Mean Scale Score', 'Students Tested',
                                                 'Pass', 'Fail'])

    #corr.style.background_gradient(cmap='coolwarm')
    # https://github.com/altair-viz/altair/pull/1945
    corrMatrix = pass_fail_df.corr().reset_index().melt('index')
    corrMatrix.columns = ['var1', 'var2', 'correlation']
    chart = alt.Chart(corrMatrix).mark_rect().encode(
        x=alt.X('var1', title=None),
        y=alt.Y('var2', title=None),
        color=alt.Color('correlation', legend=None),
    ).properties(
        width=alt.Step(80),
        height=alt.Step(80)
    )

    chart += chart.mark_text(size=25).encode(
        text=alt.Text('correlation', format=".2f"),
        color=alt.condition(
            "datum.correlation > 0.1",
            alt.value('white'),
            alt.value('black')
        )
    )
    chart.height=800
    st.altair_chart(chart)


    #hour_to_filter = st.sidebar.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
    #st.sidebar.checkbox('Show raw data')
    school_district_size = st.sidebar.selectbox(
        "Filter by school distric size",
        ("Large", "Medium", "Small")
    )

    school_district_size_options = {"Large": 60000, "Medium": 30000, "Small": 10}
    # large title: ## Large districts: above 60,000 total enrollment
    st.markdown('# TEST ID 1 dataset broken down by district size')



    list1 = ['White', 'Black', 'Hispanic']

    # Step 2: filter based on the list above
    test_ID1 = test_ID1[test_ID1['Subgroup ID'].isin(list1)]

    # filtering based on total enrollment
    large_districts_ID1 = test_ID1[test_ID1['Total Enrollment'] < school_district_size_options[school_district_size]]

    # there are 2 school dsitricts with enrollment larger or equal to 100,000
    #large_districts_ID1['Agency Name'].unique()

    _ = plt.hist(large_districts_ID1['Mean Scale Score'], density=False, bins=200)
    st.pyplot(plt)

