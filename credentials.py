from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
from dotenv import load_dotenv 
import json
import base64

def sql_engine_string_generator(datahub_host, datahub_db, datahub_user, datahub_pwd): 

    # set a try except clause to grab the online credentials keys and if not, grab them locally as environment variables
    try:
        # set the key vault path
        KEY_VAULT_URL = "https://fsdh-swapit-dw1-poc-kv.vault.azure.net/"
        error_occur = False

        # Retrieve the secrets containing DB connection details
        credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

        # Retrieve the secrets containing DB connection details
        DB_HOST = secret_client.get_secret(datahub_host).value
        DB_NAME = secret_client.get_secret(datahub_db).value
        DB_USER = secret_client.get_secret(datahub_user).value
        DB_PASS = secret_client.get_secret(datahub_pwd).value
        print ('Credentials loaded from FSDH')
        
        # Try to get user
        token = credential.get_token("https://management.azure.com/", scopes=["user.read"])

        base64_meta_data = token.token.split(".")[1].encode("utf-8") + b'=='
        json_bytes = base64.decodebytes(base64_meta_data)
        json_string = json_bytes.decode("utf-8")
        json_dict = json.loads(json_string)
        current_user_id = json_dict["upn"]
        print(f"{current_user_id=}")
        

    except Exception as e:
        # declare FSDH keys exception
        error_occur = True
        # print(f"An error occurred: {e}")

        # load the .env file using the dotenv module remove this when running a powershell script to confirue system environment vars
        load_dotenv() # default is relative local directory 
        env_path='.env'
        DB_HOST = os.getenv(datahub_host)
        DB_NAME = os.getenv(datahub_db)
        DB_USER = os.getenv(datahub_user)
        DB_PASS = os.getenv(datahub_pwd)
        print ('Credentials loaded locally')

    # set the sql engine string
    sql_engine_string=('postgresql://{}:{}@{}/{}?sslmode=require').format(DB_USER,DB_PASS,DB_HOST,DB_NAME)
    print ('sql engine string: ',sql_engine_string)
    return sql_engine_string,current_user_id





if __name__=='__main__':
    app.run(debug=True)
