# making a function to create filters to view relevant ids

import pandas as pd

def knowledge_based_filters(clean_df, paid = 'all', location = 'all', skill_cat = 'all'):
    '''
    subsets dataset according to filters specified.

    INPUT:
    clean_df - dataframe obtained from clean.clean_prep_data
    paid - 'all', 'paid' or 'unpaid' according to compensation needs
    location - any location in India where you want to look for internships
    skill_cat - skills or categories for which you want to find internships

    OUTPUT:
    clean-df - subset of the original dataframe according to filters inputted

    '''
    if paid == 'paid':
        clean_df = clean_df[clean_df.compensation == 'paid']
    elif paid == 'unpaid':
        clean_df = clean_df[clean_df.compensation == 'unpaid']
    if location != 'all':
        clean_df = clean_df[(clean_df.job_loc.str.contains(location[:5])) | (clean_df.job_loc.str.contains('anywhere'))]
    if skill_cat != 'all':
        clean_df = clean_df[(clean_df.skills.str.contains(skill_cat[:3])) | (clean_df.category.str.contains(skill_cat[:3]) | clean_df.details.str.contains(skill_cat[:3]))]
    try:
        clean_df.iloc[0,:]
    except:
        print('No internships found for your filters')
        quit()

    return clean_df
