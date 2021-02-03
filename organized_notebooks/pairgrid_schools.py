# Load packages
import os
import pandas as pd
import numpy as np

# This line is needed to display plots inline in Jupyter Notebook
#matplotlib inline

# Required for basic python plotting functionality
import matplotlib.pyplot as plt

# Required for formatting dates later in the case
import datetime
import matplotlib.dates as mdates

# Required to display image inline
#from IPython.display import Image

# Advanced plotting functionality with seaborn
import seaborn as sns

sns.set(style="whitegrid")  # can set style depending on how you'd like it to look

#import statsmodels.api as sm
#from statsmodels.formula.api import ols
#import statsmodels
#from scipy import stats
#from pingouin import pairwise_ttests #this is for performing the pairwise tests
#import warnings
#warnings.filterwarnings("ignore")  # Suppress all warnings

school_df=pd.read_csv('dashboard_school_df.csv', index_col=0)
g = sns.PairGrid(school_df)
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
g.map_diag(sns.kdeplot, lw=3, legend=False)
plt.savefig('pairgrid.png')
