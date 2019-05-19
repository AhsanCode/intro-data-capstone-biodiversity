#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:02:31 2019

@author: Ahsan
"""
#“Are some species more likely to be endangered than others?”
import pandas as pd

species = pd.read_csv('species_info.csv')

#How many different species?
species_count = species.scientific_name.nunique()

#What are the different values of Category?
species_type = species.category.unique()
#print(species_type)
'''['Mammal' 'Bird' 'Reptile' 'Amphibian' 'Fish' 'Vascular Plant'
'Nonvascular Plant']'''

#What are the different values of conservation_status?
conservation_statuses = species.conservation_status.unique()
#print(conservation_statuses)
#[nan 'Species of Concern' 'Endangered' 'Threatened' 'In Recovery']

#How many unique species are there by conservation status?
conservation_counts = species.groupby('conservation_status').scientific_name.nunique().reset_index()

#Replace NaN in species dataframe with No Intervention
species.fillna('No Intervention', inplace = True)

#Now rerun how many unique species by conservation status
conservation_counts_fixed = species.groupby('conservation_status').scientific_name.nunique().reset_index()



from matplotlib import pyplot as plt
import numpy as np
#Order conservation counts fixed by smallest to largest
protection_counts = species.groupby('conservation_status')\
    .scientific_name.nunique().reset_index()\
    .sort_values(by='scientific_name')
    
log_lam = lambda col: np.log(col)
yaxis_values_pre = protection_counts.scientific_name.apply(log_lam)
yaxis_values_post = yaxis_values_pre.sort_values()

plt.figure(figsize=(15,4))
plt.bar(range(len(yaxis_values_post)), 
        yaxis_values_post,
        )
ax = plt.subplot()
ax.set_xticks(range(len(yaxis_values_post)))
xaxis_labels = protection_counts.conservation_status
ax.set_xticklabels(xaxis_labels)

#plt.title('Conservation Status by Species')
#plt.xlabel('conservation status')
plt.ylabel('Number of Species - LN(x) Format')

plt.savefig('Conservation Status by Species.png')
plt.show()









#Investigating Endangered Species

#add a column in species to show if it is protected or not
lam1 = lambda row: True if row.conservation_status != 'No Intervention' else False
species['is_protected'] = species.apply(lam1,axis=1)

# group by category and then is_protected
category_counts = species.groupby(['category','is_protected'])\
        .scientific_name\
        .nunique()\
        .reset_index()

#pivot this data for easier view
category_pivot = category_counts.pivot(
        columns='is_protected',
        index='category',
        values='scientific_name',
        ).reset_index()

#rename columns of pivot
category_pivot = \
category_pivot.rename(columns={\
                              False:'not_protected',\
                              True:'protected'\
                              })

#create columns percent protected
category_pivot['percent_protected'] = \
(category_pivot.protected/(category_pivot.protected+category_pivot.not_protected))*100
'''Protected implies that it is one of the 'Species of Concern' 'Endangered' 'Threatened' 'In Recovery'
categories. Highest percentage of protected species are mammals.'''









#Chi-Squared Test for Significance
#Create contingency table: y:mammal, bird; x: protected, not protected
from scipy.stats import chi2_contingency

contingency = [[30, 146],
              [75, 413]]

pval_bird_mammal = chi2_contingency(contingency)[1]
# No significant difference because pval > 0.05

contingency_reptile_mammal = [[30, 146],
                              [5, 73]]

pval_reptile_mammal = chi2_contingency(contingency_reptile_mammal)[1]
# Significant difference! pval_reptile_mammal < 0.05

contingency_all = [
        [7,72],
        [75,413],
        [11,115],
        [30,146],
        [5,328],
        [5,73],
        [46,4216],
        ]
pval_all = chi2_contingency(contingency_all)[1]
#print(pval_all)
#h0:No difference
#h1:significant difference
#Extreme difference! pval_all <0.05

#Final Thoughts on Protected Species
'''Now we can answer our initial question:

Are certain types of species more likely to be endangered?

We initially saw that there was a slight difference in the percentages of birds and mammals that fall into a protected category. Our null hypothesis here is that this difference was a result of chance.

When we ran our chi-squared test, we found a p-value of ~0.688, so we can conclude that the difference between the percentages of protected birds and mammals is not significant and is a result of chance.

But, when we compared the percentages of protected reptiles and mammals and ran the same chi-squared test, we calculated a p-value of ~0.038, which is significant.

Therefore, we can conclude that certain types of species are more likely to be endangered than others.'''

#---EXTRA DATA ANALYSIS ON species_info.csv
#A section describing the data in species_info.csv. 
#Be sure to include some (or all) of what you noticed while working through the notebook.


#create additional column with sum in category pivot: how many species per category?
#lam3 = lambda row: row.not_protected + row.protected
#category_pivot['sum'] = category_pivot.apply(lam3,axis=1)
#same sum with species per category: correct
category_pivot['Total'] = category_pivot.not_protected + category_pivot.protected
category_pivot.sort_values('percent_protected',inplace = True)

print(category_pivot.Total.sum())
print(conservation_counts_fixed.scientific_name.sum())
print(species_count)

#status = ['Endangered','In Recovery','No Intervention','Species of Concern','Threatened']
#cats = ['Mammal','Bird','Reptile','Amphibian','Fish','Vascular Plant','Nonvascular Plant']
    



#test to see if a species has different conservations status:

names = species.scientific_name
#species[names.isin(names[names.duplicated()])].sort_values("scientific_name")
  
#names.duplicated()
#returns a series with row false or true if duplicated

#names[names.duplicated()]
#returns all the names of duplicated rows (that were true)

#names.isin(names[names.duplicated()])
#in the original scientific names (5824), if the row is in the duplicated rows:true, false otherwise

duplicated_scientific_names = species[names.isin(names[names.duplicated()])].sort_values("scientific_name")
#a species can be duplicated because it has 1 or more common names per row,
#not all common names are in 1 row.   
'''
From duplicated_scientific_names: 
    1: Mammal, Canis lupus, Gray wolf is "Endangered" + "In recovery"
    2: Fish, Oncorhynchus mykiss, Rainbow trout is "threatened" + "no intervention"
'''





#How many different species per category are there?
num_species_per_cat = species.groupby('category')\
.scientific_name.nunique().reset_index()

Total_species_per_cat = num_species_per_cat.scientific_name.sum()

num_species_per_cat['% of Total'] = \
num_species_per_cat.scientific_name/Total_species_per_cat*100.0
'''
Confirmed: There are 5541 unique species.
'''


#formal test to arrive at 2 errors:

num_statuses_per_name = duplicated_scientific_names.groupby('scientific_name')\
.conservation_status.nunique().reset_index()



error_names = num_statuses_per_name[num_statuses_per_name.conservation_status > 1]
errors_all_info = pd.merge(species,
                           error_names,
                           left_on = 'scientific_name',
                           right_on = 'scientific_name',
                           how='inner')




#bar chart for number of species per category

#log_lam = lambda col: np.log(col)
y_pre = num_species_per_cat.scientific_name.apply(log_lam)
y_post = y_pre.sort_values()
plt.figure(figsize=(15,4))
plt.bar(range(len(y_post)),y_post)

ax = plt.subplot()
ax.set_xticks(range(len(y_post)))
xaxis_labels = num_species_per_cat.category
ax.set_xticklabels(xaxis_labels)

plt.title('Number of Species per Category')
plt.ylabel('Number of Species - LN(x) Format')

plt.savefig('Number of Species per Cat.png')
plt.show()


#How many species are protected bar chart:
plt.figure(figsize=(15,4))
plt.bar(range(len(category_pivot.percent_protected)),category_pivot.percent_protected.sort_values())

ax = plt.subplot()
ax.set_xticks(range(len(category_pivot.percent_protected)))
xaxis_labels = category_pivot.category
ax.set_xticklabels(xaxis_labels)

plt.title('Percentage of Protected Species Amongst each Category')
plt.ylabel('Percentage Protected (%)')

plt.savefig('protected species.png')
plt.show()








