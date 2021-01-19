
import base64
import datetime
import json
import os
import pandas as pd

# Read the data file and take a look at the data

df = pd.read_csv('schoolsdata.txt', sep=",") 
df.drop([0], axis=0, inplace=True) 
df.drop(['Filler'], axis=1 , inplace = True) #it is all blank information
df.drop(['Test Year','Test Type'], axis=1, inplace=True) #drop because we know is only 2017, test type is B for all 
df=df.reset_index() 
df.drop(['index'], axis = 1, inplace=True) 
df=df.apply(pd.to_numeric, errors='coerce')
#Will drop Grade 13 to see if our numbers align properly
rg =[6,7,8,11,4,5,3]
df=df.loc[df['Grade'].apply(lambda x: x in rg)]
#Converting all the assessment columns from percentage columns to absolute numbers for exceeded, nearly met, not met 
df['Total Standard Exceeded'] =(df['Students Tested']*df['Percentage Standard Exceeded']/100).round(decimals=0) 
df['Total Standard Met'] =(df['Students Tested']*df['Percentage Standard Met']/100).round(decimals=0) 
df['Total Standard Nearly Met'] =(df['Students Tested']*df['Percentage Standard Nearly Met']/100).round(decimals=0)
df['Total Standard Not Met'] =(df['Students Tested']*df['Percentage Standard Not Met']/100).round(decimals=0)
df['Total Standard Met and Above'] =(df['Students Tested']*df['Percentage Standard Met and Above']/100).round(decimals=0)
#Percentage was multiplied by the students tested information and not the total enrollment information.

eco_subgroups_sg= [200,201,202,203,204,205,206,207,220,221,222,223,224,225,226,227]
eco_subgroups_selected = df.loc[df['Subgroup ID'].apply(lambda x: x in eco_subgroups_sg)]

df_eco_mean=eco_subgroups_selected.groupby(['County Code','District Code','School Code','Subgroup ID','Test Id']).agg({'Mean Scale Score':'mean'}).reset_index() 
df_eco_ethnicity_new=eco_subgroups_selected.groupby(['County Code','District Code','School Code','Subgroup ID','Test Id'])['Total Tested At Entity Level', 'Total Tested with Scores', 'CAASPP Reported Enrollment', 'Students Tested' ,'Students with Scores','Total Standard Exceeded', 'Total Standard Met','Total Standard Met and Above', 'Total Standard Nearly Met','Total Standard Not Met'].sum()
df_eco_ethnicity_new=df_eco_ethnicity_new.reset_index() 
new_eco_df=pd.merge(df_eco_mean, df_eco_ethnicity_new, how='outer', on=['County Code','District Code','School Code','Subgroup ID','Test Id']) 
new_eco_df= new_eco_df.sort_values(by=['District Code']) 
new_eco_df=new_eco_df.dropna() 
new_eco_df.to_csv(r'schools_ass_eco.csv',index=False, header=True)
