#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 19:20:09 2019

@author: Ahsan
"""

#Part 2 - Observations DataFrame

import pandas as pd
from matplotlib import pyplot as plt

species = pd.read_csv('species_info.csv')
species.fillna('No Intervention', inplace = True)
species['is_protected'] = species.conservation_status != 'No Intervention'

observations = pd.read_csv('observations.csv')

#create new column in species to see if 'Sheep' is in common names
lam1 = lambda row: True if 'Sheep' in row.common_names else False
species['is_sheep'] = species.apply(lam1,axis=1)

#select all rows where there is the word sheep 
species_is_sheep = species[species.is_sheep == True]

#select all rows now that are actually mammals and not plants
sheep_species = species[
        (species.is_sheep == True) & 
        (species.category == 'Mammal')] 

#Merge sheep_species and observations
sheep_observations = pd.merge(sheep_species,observations,how='inner')

#For each national park, how many observations?
obs_by_park = sheep_observations.groupby(\
'park_name')\
.observations.sum()\
.reset_index()
'''This is the total number of sheep observed in each park over the past 7 days'''

#Plotting a bar chart to show number of sheeps in each park

plt.figure(figsize=(16,4))
plt.bar(range(len(obs_by_park.observations)), obs_by_park.observations)

ax = plt.subplot()
ax.set_xticks(range(len(obs_by_park.observations)))
xaxis_labels = obs_by_park.park_name
ax.set_xticklabels(xaxis_labels)

plt.title('Observations of Sheep per Week')
plt.ylabel('Number of Observations')

plt.savefig('Obs of Sheep per week.png')
plt.show()

#How many parks?
parks_num = observations.park_name.nunique()

