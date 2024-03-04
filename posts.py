import json
import pandas as pd
from models import Base #, InstagramPost, Comment  
from database import engine, SessionLocal
from sqlalchemy.orm import Session



# Definir uma função auxiliar para verificar se um objeto é iterável
def is_iterable(obj):
    try:
        iter(obj)
        return not isinstance(obj, str)  # Excluir strings, que são iteráveis
    except TypeError:
        return False

# Set up the session
Base.metadata.create_all(bind=engine)

# Load JSON data
with open('source/novo.json', 'r', encoding='utf-8') as f: 
    data = json.load(f)

#Create data frame
df = pd.DataFrame(data)

df.rename(columns={
    'id': 'id',
    'inputUrl': 'inputurl',
    'type': 'type',
    'shortCode': 'shortcode',
    'caption': 'caption',
    'url': 'url',
    'commentsCount': 'commentscount',
    'dimensionsHeight': 'dimensionsheight',
    'dimensionsWidth': 'dimensionswidth',
    'displayUrl': 'displayurl',
    'videoUrl': 'videourl',
    'alt': 'alt',
    'likesCount': 'likescount',
    'videoViewCount': 'videoviewcount',
    'videoPlayCount': 'videoplaycount',
    'timestamp': 'timestamp',
    'locationName': 'locationname',
    'locationId': 'locationid',
    'ownerFullName': 'ownerfullname',
    'ownerUsername': 'ownerusername',
    'ownerId': 'ownerid',
    'productType': 'producttype',
    'videoDuration': 'videoduration',
    'isSponsored': 'issponsored',
    'hashtags': 'hashtags',
    'mentions': 'mentions',
    'images': 'images',
    'childPosts': 'childposts',
    'taggedUsers': 'taggedusers',
    'musicInfo': 'musicinfo',
    'coauthorProducers': 'coauthorproducers',
    'latestComments': 'latestcomments',
    'firstComment': 'firstcomment',
    'isPinned': 'ispinned'
}, 
inplace=True)

df = df.drop(columns=['musicinfo', 'hashtags', 'mentions', 'images', 'childposts', 'taggedusers', 'coauthorproducers', 'latestcomments', 'firstcomment', 'ispinned'])

# def insert_dataframe_to_db(df, engine):
#     # Serialize columns that need to be in JSON format
#     json_columns = ['musicinfo', 'hashtags', 'mentions', 'images', 'childposts', 'taggedusers', 'coauthorproducers']
#     for col in json_columns:
#         if col in df.columns:
#             # Update the lambda function to handle iterables and None values properly
#             df[col] = df[col].apply(lambda x: json.dumps(x) if not pd.isnull(x) and not isinstance(x, (list, dict)) else None)

#     # Convert dataframe to list of dictionaries for insertion
#     data_to_insert = df.to_dict(orient='records')

#     # Insert data into the database
#     with engine.connect() as connection:
#         for record in data_to_insert:
#             insert_statement = f"""
#                 INSERT INTO public.instagram_posts_test ({', '.join(record.keys())})
#                 VALUES ({', '.join(['%s']*len(record))})
#                 ON CONFLICT (id) DO NOTHING;
#             """
#             connection.execute(insert_statement, list(record.values()))



# Salvar para CSV (opcional)
df.to_csv('teste.csv', index=False)
# Inserir no banco de dados
df.to_sql('instagram_posts_test', engine, if_exists='append', index=False)
# insert_dataframe_to_db(df, engine)
