from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, BlobClient
import logging
import json
import botocore
import botocore.session
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from . import helper as hp
import re
# def retrieveSecret():
#     # keyVaultName = "OktaSecretPooja"
#     # KVUri = f"https://{keyVaultName}.vault.azure.net"

#     # credential = DefaultAzureCredential()
#     # client = SecretClient(vault_url=KVUri, credential=credential)
#     # retrieved_secret = client.get_secret("testPooja1")
#     #print(type(retrieved_secret.value))
#     #print(retrieved_secret.value)
#     #secret1 = json.loads(retrieved_secret.value)
#     #secret2 = json.loads(secret1)
#     #print(secret2['LM_ACCESS_ID'])
#     lm_key = "\""+os.environ['LM_KEY']+"\""
#     print(os.environ['LM_KEY'])
#     secret123 = json.loads(lm_key)
#     secret1234 = json.loads(secret123)
#     print(secret1234['LM_ACCESS_ID'])



def getOktaUrl(filename):
    try:
#enter credentials
        accountName = hp.get_required_attr_from_env("AzureWebJobsStorage")#"DefaultEndpointsProtocol=https;AccountName=poojaoktatestbe30;AccountKey=IDJEhdsLHcDRAJLTN5YeHtW+PEULRBIOWo9EHo2dRj4r3cE4RnGw+gVGqU/r68tOqPyhSRfz7iwj+AStK2WGsg==;EndpointSuffix=core.windows.net"#hp.get_required_attr_from_env("AzureWebJobsStorage")
        #account_name = re.search("AccountName=(.*?);", accountName).group(1)#'oktaurlstorepooja'
        #account_key = re.search("AccountKey=(.*?);", accountName).group(1)#'WdOazonRM+creM1aMvIKFkx8BIx4OA0TcXO+x2oVKRMkLxqey8lkNxRMli0JqBWWaTNawy/55W9Z+AStePOFyg=='
        container_name1 = 'oktalinkcontainer'

        #create a client to interact with blob storage
        #connect_str = hp.get_required_attr_from_env("AzureWebJobsStorage")#'DefaultEndpointsProtocol=https;AccountName=' + account_name + ';AccountKey=' + account_key + ';EndpointSuffix=core.windows.net'
        
       
        blob_service_client = BlobServiceClient.from_connection_string(accountName)
        container_client = blob_service_client.get_container_client(container_name1)
        blob_client = container_client.get_blob_client(filename)
        if blob_client.exists():
            streamdownloader = blob_client.download_blob()
            fileReader = json.loads(streamdownloader.readall())
            logging.info(fileReader)
            return fileReader
        else:
            return None
    except botocore.exceptions.ClientError as e:
        logging.error("Error while retrieving persisted url %s", str(e))
        #if bucket_exists(BUCKET):
        logging.info("URL not found in s3 bucket. Back-filling logs. ")
        return None
        # else:
        #     raise Exception("Unable to connect to S3 bucket %s. It does not exist. S3 bucket is required to persist "
        #                     "the last reported "
        #                     "timestamp. Exception=%s", BUCKET, e)


def updateOktaUrl(filename,body):
    accountName = hp.get_required_attr_from_env("AzureWebJobsStorage")#"DefaultEndpointsProtocol=https;AccountName=poojaoktatestbe30;AccountKey=IDJEhdsLHcDRAJLTN5YeHtW+PEULRBIOWo9EHo2dRj4r3cE4RnGw+gVGqU/r68tOqPyhSRfz7iwj+AStK2WGsg==;EndpointSuffix=core.windows.net"#hp.get_required_attr_from_env("AzureWebJobsStorage")
    #account_name = re.search("AccountName=(.*?);", accountName).group(1)#'oktaurlstorepooja'
    #account_key = re.search("AccountKey=(.*?);", accountName).group(1)#'WdOazonRM+creM1aMvIKFkx8BIx4OA0TcXO+x2oVKRMkLxqey8lkNxRMli0JqBWWaTNawy/55W9Z+AStePOFyg=='
    container_name1 = 'oktalinkcontainer'

    #create a client to interact with blob storage
    #connect_str = 'DefaultEndpointsProtocol=https;AccountName=' + account_name + ';AccountKey=' + account_key + ';EndpointSuffix=core.windows.net'
    
    blob_service_client = BlobServiceClient.from_connection_string(accountName)
    container_client = blob_service_client.get_container_client(container_name1)
    blob_client = container_client.get_blob_client(filename)
    streamdownloader = blob_client.upload_blob(data=body, overwrite=True)