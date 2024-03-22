from posts import ig_posts_to_sql, post_to_bq
from profiles import ig_profiles_to_sql, profile_to_bq
import pandas as pd
from database import Base, SessionLocal, engine
from models import InstagramPost, InstagramProfile

import os
from dotenv import load_dotenv

load_dotenv()


# Your environment variables
MY_APIFY_TOKEN = os.getenv("MY_APIFY_TOKEN")
APIFY_POSTS_DATASET = os.getenv("APIFY_POSTS_DATASET")
BQ_POSTS_TABLE_ID = os.getenv("BQ_POSTS_TABLE_ID")
BQ_DATA_SET_LOCATION = os.getenv("BQ_DATA_SET_LOCATION")
BQ_DATASET_ID = os.getenv("BQ_DATASET_ID")
APIFY_PROFILE_DATASET = os.getenv("APIFY_PROFILE_DATASET")
BQ_PROFILES_TABLE_ID = os.getenv("BQ_PROFILES_TABLE_ID")

# Set up the session
Base.metadata.create_all(bind=engine)
session = SessionLocal()

# Querying InstagramPost
posts_query_result = session.query(InstagramPost).all()
profile_query_result = session.query(InstagramProfile).all()

# Convert query results to a list of dictionaries
data = [{key: getattr(post, key) for key in post.__dict__.keys() if not key.startswith('_')} for post in posts_query_result]

# Convert the list of dictionaries to a DataFrame
psql_table_df = pd.DataFrame(data)
psql_table_df = psql_table_df.astype(str)

# Posts
ig_posts_to_sql(APIFY_POSTS_DATASET, MY_APIFY_TOKEN)
# def post_to_bq(psql_table, bq_dataset_id, bq_table_id, bq_dataset_location):
post_to_bq(psql_table_df, BQ_DATASET_ID, BQ_POSTS_TABLE_ID, BQ_DATA_SET_LOCATION)

# Profiles 
ig_profiles_to_sql(APIFY_PROFILE_DATASET, MY_APIFY_TOKEN)
#def profile_to_bq(psql_profile_table, bq_dataset_id, bq_profile_table_id, bq_dataset_location):
profile_to_bq(psql_table_df, BQ_DATASET_ID, BQ_PROFILES_TABLE_ID, BQ_DATA_SET_LOCATION)