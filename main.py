from posts import ig_posts_to_sql
from profiles import ig_profiles_to_sql

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MY_APIFY_TOKEN")
DATASET = os.getenv("APIFY_DATASET")
PROFILE_DATASET = os.getenv("APIFY_PROFILE_DATASET")

ig_posts_to_sql(DATASET, API_KEY)
ig_profiles_to_sql(PROFILE_DATASET, API_KEY)