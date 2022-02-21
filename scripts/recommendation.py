# functions for making recommendations

import pandas as pd

def make_recs(sim, df, i, n):
    '''
    returns a dataframe of top n recommendations, based on the similarity matrix provided and dataframe 
    provided, for a user who viewed the internship with the ith ID.
    
    INPUT:
    sim - similarity matrix(dataframe)
    df - original dataframe with all the data
    i - id of the internship that was viewed by the user
    n - top n recommendations to be made to the user 
    
    OUTPUT:
    recs_df - dataframe consisting of the recommended internships
    
    '''
    ith_series = sim[i]
    ith_series = ith_series.sort_values(ascending = False)
    recs = ith_series.head(int(n)+1).index.tolist()
    
    # what might happen is that multiple elements attain maximum similarity value. Then it is possible that 
    # we don't get i in our recs. so for that the below is done. 
    if i in recs: 
        recs.remove(i)
    else:
        recs = recs[:-1]
        
    # below ensures that the order of the recommendations is as in recs cause otherwise the use of .isin
    # reorders recs in the way they appear in df, i.e, in ascending order
    recs_df = df[df.id.isin(recs)].set_index('id').T[recs].T.reset_index()
    
    return recs_df
