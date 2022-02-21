# importing argparse
import argparse

# defining arguments for command line interface
parser = argparse.ArgumentParser(description='Scrape, clean and make recommendations on internship data')
parser.add_argument('--scrape',help = 'scrape data from the web', action = 'store_true')
parser.add_argument('--recs',help = 'clean and prepare data and make recommendations',action = 'store_true')
parser.add_argument('--load_loc',help= 'enter path to load data to be used from')
parser.add_argument('--store_loc',help='enter path to store output')

args = parser.parse_args()

# import libs
import pandas as pd
import clean, recommendation, scrape, knowledge
import sys

# making everything work

# 1st case: If only scraping has to be done, i.e, --scrape is there but --recs isn't
if args.scrape:
    if not args.recs:
        print('\n')
        print('Ignoring --load_loc if specified as new data has to be scraped')
        print('\n')
        df = scrape.scrape()
        if args.store_loc:
            df.to_csv(args.store_loc)
        else:
            print('saving your scraped data as scraped_df.csv in the current directory')
            df.to_csv('scraped_df.csv')

# 2nd case where both --scrape and --recs have been specified
    else:
        print('Ignoring --load_loc if specified as new data has to be scraped')
        df = scrape.scrape()
        clean_df = clean.clean_prep_data(df)

        print('Please enter yes if you want to set any filters. Otherwise enter no: ')
        knowledge_text = input()
        if knowledge_text == 'yes':
            print('Enter a specific location you want to search for. If you want no filters on location, type all: ')
            loc = input()
            print('Enter whether you want paid or unpaid internships. If you want no filters on compensation, type all: ')
            paid = input()
            print('Enter a specific skill/category you want to search for. If you want no filters on this, type all: ')
            skill_cat = input()
            clean_df_1 = knowledge.knowledge_based_filters(clean_df, paid.lower().strip(), loc.lower().strip(), skill_cat.lower().strip())
        else:
            clean_df_1 = clean_df     

        print('These ids represent the most relevant profiles:', clean_df_1['id'].values.tolist())
        print('Please enter one of these ids to save the profile related to this id in your current directory: ')
        id_int = int(input())
        df_id = clean_df[clean_df['id'] == id_int]
        df_id.to_csv('id_profile_' + str(id_int)+'.csv')
        len_clean_df = clean_df.shape[0]
        print('Please enter the no. of recommended internships you want to make between 1-{}: '.format(len_clean_df))
        n_int = int(input())
        sim = clean.return_sim(clean_df)
        df_recs = recommendation.make_recs(sim, clean_df, id_int, n_int)
        if args.store_loc:
            df_recs.to_csv(args.store_loc)
        else:
            df_recs.to_csv('df_recommendations.csv')
            print('Saved your recommendations in your current directory')

# 3rd case: If only recommendations to be made, i.e., --recs has been specified but --scrape hasn't been
## Note that this is almost the same as the above case. So any changes there will have to be most likely made here too and vice-versa
if args.recs:
    if not args.scrape:
        try:
            df = pd.read_csv(args.load_loc)
        except:
            print('Please enter correct loaction to load data from')
            quit()
        clean_df = clean.clean_prep_data(df)

        print('Please enter yes if you want to set any filters. Otherwise enter no: ')
        knowledge_text = input()
        if knowledge_text == 'yes':
            print('Enter a specific location you want to search for. If you want no filters on location, type all: ')
            loc = input()
            print('Enter whether you want paid or unpaid internships. If you want no filters on compensation, type all: ')
            paid = input()
            print('Enter a specific skill/category you want to search for. If you want no filters on this, type all: ')
            skill_cat = input()
            clean_df= knowledge.knowledge_based_filters(clean_df, paid.lower().strip(), loc.lower().strip(), skill_cat.lower().strip())     

        print('These ids represent the most relevant profiles:', clean_df['id'].values.tolist())
        print('Please enter one of these ids to save the profile related to this id in your current directory: ')
        id_int = int(input())
        df_id = clean_df[clean_df['id'] == id_int]
        df_id.to_csv('id_profile_' + str(id_int)+'.csv')
        len_clean_df = clean_df.shape[0]
        print('Please enter the no. of recommended internships you want to make between 1-{}: '.format(len_clean_df))
        n_int = int(input())
        sim = clean.return_sim(clean_df)
        df_recs = recommendation.make_recs(sim, clean_df, id_int, n_int)
        if args.store_loc:
            df_recs.to_csv(args.store_loc)
        else:
            df_recs.to_csv('df_recommendations.csv')
            print('Saved your recommendations in your current directory')














