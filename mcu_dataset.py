# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 22:02:42 2021

@author: Jean-Paul
"""


# %% Import module

import pandas as pd
#import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# %% Load dataset
#os.chdir("C:\\Users\Jean-Paul\SkyDrive\Data Science\Python\Kaggle\MCU_complete_dataset")
mcu_dataset=pd.read_csv("mcu dataset.csv", 
                        parse_dates = ["US release Date"])
#https://www.kaggle.com/datasets/rachit239/mcu-complete-dataset

# %% Explore the dataset
mcu_dataset.columns
mcu_dataset.info()
mcu_dataset.describe()



# %% Cleaning the dataset

# 1. Change the dollar columns to integer#

def convert_to_num(dollar_col):
    """
    Convert a dollar column from mcu_dataset to float by removing "$", "," and
    changing the type to float.

    Parameters
    ----------
    series : pandas.core.series.Series
        The Series object to be converted

    Returns
    -------
    
    pandas.core.series.Series
    The converted Series object

    """
    dollar_col=dollar_col.str.replace("$", "")
    dollar_col=dollar_col.str.replace(",", "")
    dollar_col=dollar_col.astype("float")
    return dollar_col

#Loop to convert all the dollar  column
# for col in ['Budget', 'Domestic Gross',
#        'Total Gross', 'Opening Gross']:
#     convert_to_num(col)
    
dollar_columns = ['Budget', 'Domestic Gross', 'Total Gross', 'Opening Gross']

mcu_dataset.loc[:, dollar_columns] = mcu_dataset.loc[:, dollar_columns].apply(convert_to_num)
    
#Rename the dollar columns
mcu_dataset.columns= ['Name', 'US release Date', 'Director', 'Producer', 'Duration', 'Genre',
       'IMDB rating', 'metascore', 'Cast', 'Budget($)', 'Domestic Gross($)',
       'Total Gross($)', 'Opening Gross($)', 'Oscar Nomination', 'Oscar won',
       'Phase']
    
# 2. Convert the "Phase" column to category #
mcu_dataset["Phase"]=mcu_dataset.Phase.astype("category")
mcu_dataset.Phase

# 3. Convert the "Duration" colum to timedelta
mcu_dataset["Duration"]=pd.to_timedelta(mcu_dataset.Duration)
mcu_dataset.Duration.mean()
mcu_dataset.Duration.max()
mcu_dataset.Duration.min()

# %% Chart analysis
sns.set_style("white")
f, axes= plt.subplots(1,1)
# Number movies/Phase
sns.countplot("Phase",data=mcu_dataset)
plt.show()
# Evolution budget accross time
g=sns.lineplot("US release Date", "Total Gross($)", data=mcu_dataset)
g.set_title("Budget evolution")
sns.despine()                           #remove borders

plt.show()

# Link between Budget and IMBD rating and score
f, axes= plt.subplots(2,2)
h1=sns.regplot("Budget($)", "IMDB rating", data=mcu_dataset, ci=None,
                   ax=axes[0,0])
h2=sns.regplot("Budget($)", "metascore", data=mcu_dataset, ci=None,
                   ax=axes[1,0])
h3=sns.regplot("Total Gross($)", "IMDB rating", data=mcu_dataset, ci=None,
                   ax=axes[0,1])
h4=sns.regplot("Total Gross($)", "metascore", data=mcu_dataset,ci=None, 
                   ax=axes[1,1])
plt.show()
# Return on Investment
mcu_dataset["Benefit($)"]=(mcu_dataset["Total Gross($)"]/mcu_dataset["Budget($)"])*100
sns.barplot('Name','Benefit($)', data=mcu_dataset.sort_values(by='Benefit($)', 
                                                              ascending=False)).\
    set_title("Return on Investment (ROI)")
plt.xticks(rotation=90)
plt.show()

# Relation between Budget and Benefit
sns.regplot("Budget($)", "Benefit($)", data=mcu_dataset, ci=None, 
            color="red", marker="H")\
    .set_title("Relation between Budget and ROI")
    
# %% Favorite actor
not_avengers_movies=['Iron Man', 'The incredible Hulk', 'Iron Man 2', 'Thor',
       'Captain America: The first Avenger',
       'Iron Man 3', 'Thor: The dark world',
       'Captain America : The Winter Soldier', 'Guardians Of the Galaxy',
        'Ant-Man',
       'Captain America: Civil War', 'Doctor Strange ',
       'Guardians of the Galaxy Vol. 2', 'Spider-Man:Homecoming',
       'Thor:Ragnarok', 'Black Panther', 
       'Ant-Man and the Wasp', 'Captain-Marvel', 
       'Spider-Man:Far From Home']
not_avengers_index = [list(mcu_dataset.Name.unique()).index(movies) \
                      for movies in not_avengers_movies]    #list comprehension to get index of not avengers movies

mcu_dataset_without_avengers=mcu_dataset.iloc[not_avengers_index, :] #creation of dataframe without the avengers movies

#isolate main actor
mcu_dataset_without_avengers["Main_actor"]=mcu_dataset_without_avengers.Cast.str.split(",", 1).str[0]

mcu_dataset_without_avengers.pivot_table(values=['IMDB rating','metascore'], 
                                         index='Main_actor', aggfunc=np.mean).\
    sort_values(by=['IMDB rating','metascore'], ascending=False)