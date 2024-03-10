import json
import pandas as pd
from database import engine
from models import Base
from competitors_mapping import client_1, client_2, client_3, client_4, client_qui, client_tai, client_tar, client_ypy

import requests

def ig_posts_to_sql(apify_dataset, apify_key):

    oauth_url = f"https://api.apify.com/v2/datasets/{apify_dataset}/items?token={apify_key}"

    # Set up the session
    Base.metadata.create_all(bind=engine)
    
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

    # Drop complex xolumns
    df = df.drop(columns=['music_info', 'hashtags', 'mentions', 'images', 'child_posts', 'tagged_users', 'coauthor_producers', 'latest_comments', 'first_comment', 'is_pinned'])


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
        print("Data loaded successfully: 200")
    except Exception as e:
        print(f"Something went wrong: {e}")