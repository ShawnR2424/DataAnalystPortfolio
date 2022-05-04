
# Load packages
import os
import pandas as pd

# Change Directory and import datasets

os.chdir('\\Users\Shanta\Desktop\Forage Accenture Project')

# Datasets needed to answer question - ReactionTypes has the metric of popularity
# Reaction has the main data with the type specified but missing a metric
# Content identifies all the categories of interest
# Need to merge to align categories with their scores
reaction = pd.read_csv('Reactions.csv')
content = pd.read_csv('Content.csv')
reactionTypes = pd.read_csv('ReactionTypes.csv')

# Remove rows that have NaN for reaction type
reactionClean = reaction.dropna(subset=['Type'])
#print((reactionClean['Type'].unique()))

# Merge reaction and content to identify the categories of the content, left join as the reactions is the main data
reactionContent = reactionClean.merge(content, left_on = 'Content ID', right_on='Content ID')

# Merge reactionTypes data to add scores and sentiment to merged content and reaction table
reactionContentScore = reactionContent.merge(reactionTypes, left_on = 'Type_x', right_on='Type')

# Remove some columns
rCS = reactionContentScore.drop(['Datetime','Unnamed: 0_y','URL', 'Unnamed: 0_x', 'Unnamed: 0', 'Type', 'User ID_x', 'User ID_y'], axis=1)
rCS_renamed = rCS.rename(columns={"Type_x":"Reaction Type", "Type_y":"Content Type"})

# Clean categories by removing quotes, lower casing all categories for consistency
rCS_renamed['Category'] = rCS_renamed['Category'].str.replace('"','')
rCS_renamed['Category'] = rCS_renamed['Category'].str.lower()

# Rank the Categories by sum of score descending
rCS_ranked = rCS_renamed.groupby('Category')['Score'].sum().sort_values(ascending=False)

rCS_renamed.to_csv (r'C:\Users\Shanta\Desktop\Forage Accenture Project\rcs_renamed.csv', index = True, header=True)
rCS_ranked.to_csv (r'C:\Users\Shanta\Desktop\Forage Accenture Project\rcs_ranked.csv', index = True, header=True)

