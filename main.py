from posts import ig_posts_to_sql

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MY_APIFY_TOKEN")
DATASET = os.getenv("APIFY_DATASET")

ig_posts_to_sql(DATASET, API_KEY)