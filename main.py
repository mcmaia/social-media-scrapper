from posts import ig_posts_to_sql, post_to_bq
from profiles import ig_profiles_to_sql, profile_to_bq
import pandas as pd
from database import Base, SessionLocal, engine
from models import InstagramPost
import logging

import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

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
logger.info('DB instance')

# Querying InstagramPost
query_result = session.query(InstagramPost).all()
logger.info('Getting local database')

# Convert query results to a list of dictionaries
data = [{key: getattr(post, key) for key in post.__dict__.keys() if not key.startswith('_')} for post in query_result]
logger.info('Convert query results to a list of dictionaries')

# Convert the list of dictionaries to a DataFrame
psql_table_df = pd.DataFrame(data)
psql_table_df = psql_table_df.astype(str)
logger.info(f'{psql_table_df} created')

# Call functions
#POSTS
ig_posts_to_sql(APIFY_POSTS_DATASET, MY_APIFY_TOKEN)
post_to_bq(psql_table_df, BQ_DATASET_ID, BQ_POSTS_TABLE_ID, BQ_DATA_SET_LOCATION)
#PROFILES
ig_profiles_to_sql(APIFY_PROFILE_DATASET, MY_APIFY_TOKEN)
profile_to_bq(psql_table_df, BQ_DATASET_ID, BQ_PROFILES_TABLE_ID, BQ_DATA_SET_LOCATION>>>>>>> main
