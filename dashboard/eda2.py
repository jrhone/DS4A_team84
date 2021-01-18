# app2.py
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
def app():
    df = pd.read_csv('~/team_84/notebooks/20210111/final_merged_latest.csv', index_col = 0)
    '''
    # TEST ID 1  braken down by district size
    '''
    #Converting all the assessment columns back to  percentage columns for exceeded, nearly met, not met to show completion results as percentage of test taken
    df['Percentate Std Exceed'] =(df['Total Standard Exceeded']/df['Students Tested']*100).round(decimals=0)
    df['Percentage Std Met'] =(100*df['Total Standard Met']/df['Students Tested']).round(decimals=0)
    df['Percentage Std Nearly Met'] =(100*df['Total Standard Nearly Met']/df['Students Tested']).round(decimals=0)
    df['Percentage Std Not Met'] =(100*df['Total Standard Not Met']/df['Students Tested']).round(decimals=0)
    df['Percentage Std Met and Above'] =(100*df['Total Standard Met and Above']/df['Students Tested']).round(decimals=0)
    #Percentage was multiplied by the students tested information and not the total enrollment information.
    #Students tested in Math and Literacy can be the same students or different students, we don't have that information.
    #we are adding the results of both exams, this can cause a duplicate in value of students tested, I will separate both datasets

    df['Pass'] = df['Percentate Std Exceed'] + df['Percentage Std Met']
    df['Fail'] = df['Percentage Std Nearly Met'] + df['Percentage Std Not Met']
    # filtering based on total enrollment
    df = df[df['Total Enrollment'] != 0]
    df = df[df['Total Enrollment'] > 250]

    # need to filter out the 6 schools that have more students tested than enrolled

    # dataset containing school districts with over $20,000 revenue per student
    df_high_funding = df[(df['Revenue per student'] > 20_000)]

    # update the main dataset to not include schools with over 20k revenue per student nor zero revenue per student
    df = df[(df['Revenue per student'] < 20_000)]
    df = df[(df['Revenue per student'] != 0)]
    
    st.markdown('## Ethnicity breakdown in districts w/high funding')

    #plt.figure(figsize=(6, 4))
    sns.barplot(x='Count Enrollment per ethnicity',y='Agency Name',hue='Subgroup ID',data=df_high_funding)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

    # https://github.com/streamlit/streamlit/issues/638
    plt.figure() 

    st.markdown('## We are looking at the schools and were are they in the revenue/score comparison')

    plt.figure(figsize=(10, 4))
    sns.scatterplot(x='Revenue per student', y='Mean Scale Score', hue='Agency Name',data=df_high_funding)
    st.pyplot(plt)

    # https://github.com/streamlit/streamlit/issues/638
    plt.figure() 

    def best_fit(X, Y):

        xbar = sum(X)/len(X)
        ybar = sum(Y)/len(Y)
        n = len(X) # or len(Y)

        numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
        denum = sum([xi**2 for xi in X]) - n * xbar**2

        b = numer / denum
        a = ybar - b * xbar

        #print('best fit line:\ny = {:.2f} + {:.2f}x'.format(a, b))

        return a, b
    a, b = best_fit(df_high_funding['Revenue per student'],df_high_funding['Mean Scale Score'])
    plt.scatter(df_high_funding['Revenue per student'],df_high_funding['Mean Scale Score'])
    yfit = [a + b * xi for xi in df_high_funding['Revenue per student']]
    plt.plot(df_high_funding['Revenue per student'], yfit)
    plt.title('Mean Scale Score relationship to Revenue for Highly funded districts')
    plt.xlabel('Revenue per Student')
    _=plt.ylabel('Mean Scale Score')
    st.pyplot(plt)