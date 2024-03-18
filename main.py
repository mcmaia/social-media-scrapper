from posts import ig_posts_to_sql, post_to_bq
from profiles import ig_profiles_to_sql
import pandas as pd
from database import Base, SessionLocal, engine
from models import InstagramPost

import os
from dotenv import load_dotenv

load_dotenv()


# Your environment variables
MY_APIFY_TOKEN = os.getenv("MY_APIFY_TOKEN")
APIFY_DATASET = os.getenv("APIFY_DATASET")
BQ_DATA_SET = os.getenv("BQ_DATA_SET")
BQ_DATA_SET_LOCATION = os.getenv("BQ_DATA_SET_LOCATION")
BQ_TABLE_ID = os.getenv("BQ_TABLE_ID")
PROFILE_DATASET = os.getenv("APIFY_PROFILE_DATASET")

# Set up the session
Base.metadata.create_all(bind=engine)
session = SessionLocal()

# Querying InstagramPost
query_result = session.query(InstagramPost).all()

# Convert query results to a list of dictionaries
data = [{key: getattr(post, key) for key in post.__dict__.keys() if not key.startswith('_')} for post in query_result]

# Convert the list of dictionaries to a DataFrame
psql_table_df = pd.DataFrame(data)
psql_table_df = psql_table_df.astype(str)

# Call functions
# ig_posts_to_sql(APIFY_DATASET, MY_APIFY_TOKEN)
post_to_bq(psql_table_df, BQ_DATA_SET, BQ_TABLE_ID, BQ_DATA_SET_LOCATION)

# ig_profiles_to_sql(PROFILE_DATASET, MY_APIFY_TOKEN)
