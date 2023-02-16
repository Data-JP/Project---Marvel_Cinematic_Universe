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
import matplotlib.ticker as ticker
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

# 4. Use applymap and strip to remove leading and trailing spaces
mcu_dataset = mcu_dataset.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# %% Chart analysis
sns.set_style("white")
f, axes= plt.subplots(1,1)
# Number movies/Phase
sns.countplot("Phase",data=mcu_dataset)
plt.show()
# Evolution budget accross time
g=sns.lineplot("US release Date", "Budget($)", data=mcu_dataset, 
               color="cornflowerblue")
#♦g.set_title("Budget evolution")
g.set_ylabel("Budget($)", loc="top", rotation=360)
plt.annotate("Budget evolution", (mcu_dataset["US release Date"].iloc[-1], 
                                  mcu_dataset["Budget($)"].iloc[-1]), 
             textcoords="offset points", xytext=(40,-15), ha='center', 
             fontsize=12, color="cornflowerblue")

# Adding dollar sign
x=mcu_dataset["Budget($)"]            #variable to avoid 2 pairs of quotation marks
formatter = ticker.StrMethodFormatter('{x:,.0f} $')  # add dollar sign in the y label 
g.yaxis.set_major_formatter(formatter)

sns.despine()                           #remove borders
plt.show()

# Link between Budget, Total Gross($) and IMBD rating, score
f, axes= plt.subplots(2,2)

h1=sns.regplot(x="Budget($)", y="IMDB rating", data=mcu_dataset, ci=None, 
               color= "limegreen",
                   ax=axes[0,0])
h2=sns.regplot(x="Budget($)", y="metascore", data=mcu_dataset, ci=None,
               color= "limegreen", ax=axes[1,0])
h3=sns.regplot(x="Total Gross($)", y="IMDB rating", data=mcu_dataset, ci=None, color= "limegreen",
                   ax=axes[0,1])
h4=sns.regplot(x="Total Gross($)", y="metascore", data=mcu_dataset,ci=None, color= "limegreen",
                   ax=axes[1,1])
# Set titles
def set_titles(axes, titles):
    """
    Function to set the titles of the subplots in a grid.
    
    Parameters:
    axes (2D array of AxesSubplot objects): The subplots in the grid.
    titles (2D list of strings): The titles to set for each subplot.
    
    Returns:
    None
    """
    for i in range(axes.shape[0]):
        for j in range(axes.shape[1]):
            axes[i, j].set_title(titles[i][j])

# Define the titles for the subplots
titles = [["Correlation between Budget and IMBD rating", "Correlation between Total Gross and IMBD rating"], 
          ["Correlation between Budget and metascore", "Correlation between Total Gross and metascore"]]

# Call the set_titles function
set_titles(axes, titles)


# Share axes
axes[1,0].sharex(axes[0,0])
axes[0,0].sharey(axes[0,1])
axes[1,0].sharey(axes[1,1])
axes[0,1].sharex(axes[1,1])

# Remove x labels
for i in range(axes.shape[1]):
        axes[0, i].set_xlabel("")

# Remove labels
# h3.set_yticks([])
# h4.set_yticklabels(labels="")
# h3.set_xticklabels(labels="")
# h4.set_xticklabels(labels="")

# Adding dollar sign
#x=mcu_dataset["Budget($)"]            
# formatter = ticker.StrMethodFormatter('{x:,.0f} $')
# h1.xaxis.set_major_formatter(formatter)
# h2.xaxis.set_major_formatter(formatter)

sns.despine()   
plt.show()

# Return on Investment
mcu_dataset["ROI"]=np.divide(mcu_dataset["Total Gross($)"]-mcu_dataset["Budget($)"],
                              mcu_dataset["Budget($)"])
#(mcu_dataset["Total Gross($)"]/mcu_dataset["Budget($)"])*100
b=sns.barplot(y='Name',x='ROI', data=mcu_dataset.sort_values(by='ROI', 
                                                              ascending=False)).\
    set_title("Return on Investment of the various MCU films")

# Adding %-formatting to the x-axis
from matplotlib.ticker import PercentFormatter
b.axes.xaxis.set_major_formatter(PercentFormatter(1)) 

# Removing the x and y axis labels
b.axes.set_xlabel("")
b.axes.set_ylabel("")

sns.despine() 
plt.show()

# Ranking of reviews
mcu_dataset.loc[:,['Name','IMDB rating', 'metascore']].\
    sort_values(by='IMDB rating', ascending=False).reset_index(drop=True)

# Relation between Budget and ROI
r=sns.regplot(x="Budget($)", y="ROI", data=mcu_dataset, ci=None, 
            color="purple", marker="D")\
    .set_title("Relation between budget and ROI")

r.axes.set_ylabel("ROI", loc="top", rotation=360)

# Adding %-formatting to the y-axis
from matplotlib.ticker import PercentFormatter
r.axes.yaxis.set_major_formatter(PercentFormatter(1)) 

# Adding dollar sign
x=mcu_dataset["Budget($)"]            
formatter = ticker.StrMethodFormatter('{x:,.0f} $')   
r.axes.xaxis.set_major_formatter(formatter)

sns.despine() 
plt.show()
    
# %% Favorite actor

# List of MCU movies that are not part of the Avengers series
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

# Get index of not avengers movies
not_avengers_index = [list(mcu_dataset.Name.unique()).index(movies) \
                      for movies in not_avengers_movies]    #list comprehension to get index of not avengers movies

    
# Create dataframe without the avengers movies
mcu_dataset_without_avengers=mcu_dataset.iloc[not_avengers_index, :] #creation of dataframe without the avengers movies

# dictionary mapping each movie name to its corresponding superhero
movie_to_superhero = {'Iron Man': 'Iron Man', 
                      'The incredible Hulk': 'The Hulk',
                      'Iron Man 2': 'Iron Man', 
                      'Thor': 'Thor',
                      'Captain America: The first Avenger': 'Captain America', 
                      'Iron Man 3': 'Iron Man', 
                      'Thor: The dark world': 'Thor', 
                      'Captain America : The Winter Soldier': 'Captain America',
                      'Guardians Of the Galaxy': 'Guardians Of The Galaxy', 
                      'Ant-Man': 'Ant-Man', 'Captain America: Civil War': 'Captain America',
                      'Doctor Strange ': 'Doctor Strange', 
                      'Guardians of the Galaxy Vol. 2': 'Guardians Of The Galaxy', 
                      'Spider-Man:Homecoming': 'Spider-Man', 
                      'Thor:Ragnarok': 'Thor', 
                      'Black Panther': 'Black Panther',
                      'Ant-Man and the Wasp': 'Ant-Man', 
                      'Captain-Marvel': 'Captain Marvel',
                      'Spider-Man:Far From Home': 'Spider-Man'}

# Add new column with the name of the superhero for each movie
mcu_dataset_without_avengers['Superhero'] = mcu_dataset_without_avengers['Name'].\
    apply(lambda x: movie_to_superhero.get(x))
    #apply(lambda x: movie_to_superhero.get(x.split(':')[0], x.split(':')[0]))

# # Add new column with the name of the superhero for each movie
# mcu_dataset_without_avengers['Superhero'] = mcu_dataset_without_avengers['Name'].apply(lambda x: x.split(':')[0])

# #isolate main actor
# mcu_dataset_without_avengers["Main_actor"]=mcu_dataset_without_avengers.Cast.str.split(",", 1).str[0]

# Create pivot table with mean IMDB rating and metascore for each superhero
mcu_dataset_without_avengers.pivot_table(values=["IMDB rating",'metascore'],
                                          index='Superhero', aggfunc=np.mean).\
    sort_values(by=['IMDB rating','metascore'], ascending=False)