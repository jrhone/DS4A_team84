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
    st.title('The impact of financial investment on student’s academic outcome for the state of California​ for diff ethnicities')

    st.markdown('''
    The analysis was performed on Data from 2016-2017 school year.
    Data Analysis has been performed at the District level, were Mean scale scores are the mean of all schools in the district for all the grades.

    * Test id 1 are the results for Literature and Arts.
    * Test id 2 are the results for Mathematics 

    Data Sources:
            - Enrollment and Revenue data gathered from the Nacional Center for Education Statistics - table generator. https://nces.ed.gov/ccd/elsi/tableGenerator.aspx

           - Assessment data gathered from California assessment student performance and progress. 
    https://caaspp-elpac.cde.ca.gov/caaspp/ResearchFileList?ps=true&lstTestYear=2019&lstTestType=B&lstCounty=00&lstDistrict=00000&lstSchool=0000000


    Districts with higher than 20K revenue per student were outliers in our data and were filtered, a total of 9 districts.
    ''')

    df = pd.read_csv('~/team_84/organized notebooks/total_enrollment_per_race_with_districtcode.csv', index_col = 0)
    # filtering based on total enrollment

    _ = plt.hist(df['Revenue per student'], density=False, bins=30)
    _ = plt.ylabel('Number of ocurrences')
    _ = plt.xlabel('Revenue')
    _ = plt.title("Revenue per Student")

    st.pyplot(plt)
