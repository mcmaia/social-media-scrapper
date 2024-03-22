from database import engine
import models

import logging
import requests
import json
import pandas as pd

from google.cloud.exceptions import NotFound
from google.cloud import bigquery
from google.oauth2.service_account import Credentials
import pandas_gbq

logger = logging.getLogger(__name__)

def ig_profiles_to_sql(apify_profile_dataset, apify_key):
    oauth_url = f"https://api.apify.com/v2/datasets/{apify_profile_dataset}/items?token={apify_key}"

    res = requests.get(url=oauth_url)

    with open("token.json", "w") as f:
        f.write(json.dumps(res.json(), indent=4))

    df = pd.DataFrame(res.json())

    # Function to safely serialize a column to JSON string
    # def safe_json_serialize(s):
    #     try:
    #         return json.dumps(s) if not pd.isnull(s) else None
    #     except (TypeError, ValueError):
    #         return None
    # Replace 'NaN' with None to ensure compatibility with database
    df = df.where(pd.notnull(df), None)

    # Display changes and data types to verify adjustments
    print(df.head())
    print(df.dtypes)

    df.rename(columns={
        'inputUrl': 'input_url',
        'id': 'id',
        'username': 'username',
        'url': 'url',
        'fullName': 'full_name',
        'biography': 'biography',
        'externalUrl': 'external_url',
        'externalUrlShimmed': 'external_url_shimmed',
        'followersCount': 'followers_count',
        'followsCount': 'follows_count',
        'hasChannel': 'has_channel',
        'highlightReelCount': 'highlight_reel_count',
        'isBusinessAccount': 'is_business_account',
        'joinedRecently': 'joined_recently',
        'businessCategoryName': 'business_category_name',
        'private': 'private',
        'verified': 'verified',
        'profilePicUrl': 'profile_pic_url',
        'profilePicUrlHD': 'profile_pic_url_hd',
        'igtvVideoCount': 'igtv_video_count',
        'relatedProfiles': 'related_profiles',
        'latestPosts': 'latest_posts',
        'latestIgtvVideos': 'latest_igtv_videos',
        'postsCount': 'posts_count'

    }, inplace=True)

    df = df.drop_duplicates(subset=['id'])
    df = df.drop(columns=['related_profiles', 'latest_posts', 'latest_igtv_videos'])

    try:
        df.to_sql('instagram_profiles_test', engine, if_exists='append', index=False)
        print("Data PROFILES loaded successfully: 200")
    except Exception as e:
        print(f"Something went wrong: {e}")


def profile_to_bq(psql_profile_table, bq_dataset_id, bq_profile_table_id, bq_dataset_location):
    logger.info('Dumpping profile data do BQ')
    
    credentials = Credentials.from_service_account_file('config/gcp_credentials.json')
    client = bigquery.Client.from_service_account_json('config/gcp_credentials.json')
    logger.info('credentials and Client')
    
    # Create or get dataset
    dataset_id = bq_dataset_id
    dataset_ref = client.dataset(dataset_id)
    try:
        # Try to get the dataset, if it exists, this will succeed
        dataset = client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_id} already exists, proceeding with existing dataset.")
        logger.info('trying to create dataset')
    except NotFound:
        # If the dataset does not exist, create it
        print(f"Dataset {dataset_id} does not exist, creating new dataset.")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = bq_dataset_location
        dataset = client.create_dataset(dataset)
        print(f"Dataset {dataset_id} created.")
        logger.info('Dataset exists')

    table_id = bq_profile_table_id
    logger.info('Declair table')
    try:
        pandas_gbq.to_gbq(psql_profile_table,
                        destination_table=f"{dataset_id}.{table_id}",
                        project_id='staging-voxis',
                        if_exists='replace',
                        credentials=credentials)
        print("Data PROFILES loaded successfully to BQ: 200")
        logger.info('Data POSTS loaded successfully to BQ')
    except Exception as e:
        print(f"Something went wrong sending data POSTS to BQ: {e}")
        logger.info('f"Something went wrong sending data PROFILES to BQ: {e}')