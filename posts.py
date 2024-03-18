from google.cloud.exceptions import NotFound
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
        if username in [
            "institutoupdate", "movimentosemterra", "apiboficial", "estamosprontas", "vamosjuntasorg", "redeaponte", "institutoperegum", "juventudenegrapolitica", "girlupbrasil", "climadeeleicao", "instadatenda", "seja.democracia", "elasnopoderbr", "votenelas", "novasnarrativasevangelicas", "advocacy_hub", "institutoalziras", "todaznapolitica", "raps_brasil", "_nossas", "somos_quid", "laboraoficinaeleitoral", "fogocruzadobr", "votelgbt", "movimentoacredito", "euvotoemnegra", "mulheres_nas_urnas", "mevotoserafeminista", "casafluminense", "anacarolinalouren", "ariovaldo", "biancasantanadelua", "caetanoscannavino", "clementeganz", "professorheliosantos", "marcio.black", "institutomariellefranco", "isernarede", "perifaconnection", "perifa_lab", "coalizaonegrapordireitos", "conectas", "instituto.soudapaz", "fundacaotide", "aguaesaneamento_", "institutoalziras", "iepsoficial", "procomum", "institutotalanoa", "institutounibanco", "pactopelademocracia", "transparenciainternacionalbr"
        ]:
            return 'ypykuera'
        elif username in [
            "lucasmiglio", "tarcirleidebrito", "comandante_marinho", "bruno.balarini", "delegadojefersonbotelho"
        ]:
            return 'tarcirlei'
        elif username in [
            "quilomboperiferico", "keit.lima", "jussarabassosp", "luanapsol", "toninhovespoli", "celsogiannazi", "lunazarattini", "deboralimamtst", "ivonesilvasp", "quilomboperiferico"
        ]:
            return 'quilombo_periferico'   
        elif username in [
            "carlosbolsonaro", "tainadepaularj", "luciananovaesoficial", "edsonsantosrio", "cesarmaia", "sou_thaisferreira"
        ]:
            return 'taina_de_paula'         
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
    
    # Create or get dataset
    dataset_id = bq_dataset_id
    dataset_ref = client.dataset(dataset_id)
    try:
        # Try to get the dataset, if it exists, this will succeed
        dataset = client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_id} already exists, proceeding with existing dataset.")
    except NotFound:
        # If the dataset does not exist, create it
        print(f"Dataset {dataset_id} does not exist, creating new dataset.")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = bq_dataset_location
        dataset = client.create_dataset(dataset)
        print(f"Dataset {dataset_id} created.")

    table_id = bq_table_id
    try:
        pandas_gbq.to_gbq(psql_table,
                        destination_table=f"{dataset_id}.{table_id}",
                        project_id='staging-voxis',
                        if_exists='replace',
                        credentials=credentials)
        print("Data loaded successfully to BQ: 200")
    except Exception as e:
        print(f"Something went wrong sending data to BQ: {e}")
    
       

