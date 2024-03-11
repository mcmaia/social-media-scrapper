from competitors_mapping import client_1,client_2,client_3,client_4,client_qui,client_tai,client_tar,client_ypy

import json
import pandas as pd
import requests
from google.cloud import bigquery
from google.oauth2.service_account import Credentials
import pandas_gbq

from database import engine


def ig_posts_to_sql(apify_dataset, apify_key):

    oauth_url = f"https://api.apify.com/v2/datasets/{apify_dataset}/items?token={apify_key}"

    # # Set up the session
    # Base.metadata.create_all(bind=engine)
    
    res = requests.get(url=oauth_url)

    # Write JSON data
    with open("token.json", "w") as f:
        f.write(json.dumps(res.json(), indent=4))

    #Create data frame
    df = pd.DataFrame(res.json())

    # Renaming columns to ajst to standard
    df.rename(columns={
        'id': 'id_post',
        'username': 'username',
        'inputUrl': 'input_url',
        'type': 'type',
        'shortCode': 'short_code',
        'caption': 'caption',
        'url': 'url',
        'commentsCount': 'comments_count',
        'dimensionsHeight': 'dimensions_height',
        'dimensionsWidth': 'dimensions_width',
        'displayUrl': 'display_url',
        'videoUrl': 'video_url',
        'alt': 'alt',
        'likesCount': 'likes_count',
        'videoViewCount': 'video_view_count',
        'videoPlayCount': 'video_play_count',
        'timestamp': 'timestamp',
        'locationName': 'location_name',
        'locationId': 'location_id',
        'ownerFullName': 'owner_full_name',
        'ownerUsername': 'owner_username',
        'ownerId': 'owner_id',
        'productType': 'product_type',
        'videoDuration': 'video_duration',
        'isSponsored': 'is_sponsored',
        'hashtags': 'hashtags',
        'mentions': 'mentions',
        'images': 'images',
        'childPosts': 'child_posts',
        'taggedUsers': 'tagged_users',
        'musicInfo': 'music_info',
        'coauthorProducers': 'coauthor_producers',
        'latestComments': 'latest_comments',
        'firstComment': 'first_comment',
        'isPinned': 'is_pinned',
        'error' : 'error'
    }, 
    inplace=True)

    try:
        # Columns to drop if they exist
        columns_to_drop = ['music_info', 'hashtags', 'mentions', 'images', 'child_posts', 'tagged_users', 'coauthor_producers', 'latest_comments', 'first_comment', 'is_pinned']
        
        # Drop columns if they exist
        for col in columns_to_drop:
            if col in df.columns:
                df = df.drop(columns=col)
    except Exception:
        pass

    # Each competitor of our clients
    def determine_client(username):
        username = str(username)
        if username in client_ypy:
            return client_1
        elif username in client_tar:
            return client_2
        elif username in client_qui:
            return client_3   
        elif username in client_tai:
            return client_4   
        else:
            return 'Other'  

        # Apply the function to the 'username' column to create a new 'client' column
    df['client'] = df['owner_username'].apply(determine_client)

    # Save ro CSV - For testing
    df.to_csv('teste.csv', index=False)

    try:
        df.to_sql('instagram_posts_test', engine, if_exists='append', index=False)
        print("Data loaded successfully to psql: 200")
    except Exception as e:
        print(f"Something went wrong sending data to psql: {e}")


def post_to_bq(psql_table, bq_dataset_id, bq_table_id, bq_dataset_location):
    
    credentials = Credentials.from_service_account_file('config/gcp_credentials.json')
    client = bigquery.Client.from_service_account_json('config/gcp_credentials.json')
    

    # Create a new dataset
    dataset_id = bq_dataset_id
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = bq_dataset_location
    try:
        dataset = client.create_dataset(dataset)
    except Exception:
        pass

    table_id = bq_table_id
    schema = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("username", "STRING"),
        bigquery.SchemaField("id_post", "STRING"),
        bigquery.SchemaField("input_url", "STRING"),
        bigquery.SchemaField("type", "STRING"),
        bigquery.SchemaField("short_code", "STRING"),
        bigquery.SchemaField("caption", "STRING"),
        bigquery.SchemaField("url", "STRING"),
        bigquery.SchemaField("comments_count", "INTEGER"),
        bigquery.SchemaField("dimensions_height", "INTEGER"),
        bigquery.SchemaField("dimensions_width", "INTEGER"),
        bigquery.SchemaField("display_url", "STRING"),
        bigquery.SchemaField("video_url", "STRING"),
        bigquery.SchemaField("alt", "STRING"),
        bigquery.SchemaField("likes_count", "INTEGER"),
        bigquery.SchemaField("video_view_count", "INTEGER"),
        bigquery.SchemaField("video_play_count", "INTEGER"),
        bigquery.SchemaField("timestamp", "TIMESTAMP"),
        bigquery.SchemaField("location_name", "STRING"),
        bigquery.SchemaField("location_id", "STRING"),
        bigquery.SchemaField("owner_full_name", "STRING"),
        bigquery.SchemaField("owner_username", "STRING"),
        bigquery.SchemaField("owner_id", "STRING"),
        bigquery.SchemaField("product_type", "STRING"),
        bigquery.SchemaField("video_duration", "FLOAT"),
        bigquery.SchemaField("is_sponsored", "STRING"),
        bigquery.SchemaField("error", "STRING"),
        bigquery.SchemaField("client", "STRING"),
        # For JSON fields, BigQuery supports the STRING type, but you could also use STRUCT or RECORD for more complex structures
        # bigquery.SchemaField("musicInfo", "STRING"),
        # bigquery.SchemaField("hashtags", "STRING"),
        # bigquery.SchemaField("mentions", "STRING"),
        # bigquery.SchemaField("images", "STRING"),
        # bigquery.SchemaField("childPosts", "STRING"),
        # bigquery.SchemaField("taggedUsers", "STRING"),
        # bigquery.SchemaField("coauthorProducers", "STRING"),
    ]
    
    table_ref = dataset_ref.table(table_id)
    table = bigquery.Table(table_ref, schema=schema)

    try:
        pandas_gbq.to_gbq(psql_table,
                        destination_table=f"{dataset_id}.{table_id}",
                        project_id='staging-voxis',
                        if_exists='replace',
                        credentials=credentials)
        print("Data loaded successfully to BQ: 200")
    except Exception as e:
        print(f"Something went wrong sending data to BQ: {e}")
    
       

