from database import engine
import models

import requests
import json
import pandas as pd


def ig_profiles_to_sql(apify_profile_dataset, apify_key):
    oauth_url = f"https://api.apify.com/v2/datasets/{apify_profile_dataset}/items?token={apify_key}"

    models.Base.metadata.create_all(bind=engine)

    res = requests.get(url=oauth_url)

    with open("token.json", "w") as f:
        f.write(json.dumps(res.json(), indent=4))

    df = pd.DataFrame(res.json())

    # Function to safely serialize a column to JSON string
    def safe_json_serialize(s):
        try:
            return json.dumps(s) if not pd.isnull(s) else None
        except (TypeError, ValueError):
            return None
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
        'latestIgtvVideos': 'latest_igtv_videos'
    }, inplace=True)

    df = df.drop_duplicates(subset=['id'])
    df = df.drop(columns=['related_profiles', 'latest_posts', 'latest_igtv_videos'])

    try:
        df.to_sql('instagram_posts_profiles_test', engine, if_exists='append', index=False)
        print("Data loaded successfully: 200")
    except Exception as e:
        print(f"Something went wrong: {e}")