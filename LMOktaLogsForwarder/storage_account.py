from azure.storage.blob import BlobServiceClient, BlobClient
import logging
import json
import botocore
import botocore.session
from . import helper as hp
from . import constants as const

import re

def getOktaUrl(filename):
    try:
#enter credentials
        accountName = hp.get_required_attr_from_env("AzureWebJobsStorage")
        container_name = const.CONTAINER

        blob_service_client = BlobServiceClient.from_connection_string(accountName)
        container_client = blob_service_client.get_container_client(container_name)
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
        logging.info("URL not found in storage_account bucket. Back-filling logs. ")
        return None
        

def updateOktaUrl(filename,body):
    try:
        accountName = hp.get_required_attr_from_env("AzureWebJobsStorage")
        container_name = const.CONTAINER

        blob_service_client = BlobServiceClient.from_connection_string(accountName)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(filename)
        if blob_client.exists():
            streamdownloader = blob_client.upload_blob(data=body, overwrite=True)
        else:
            logging.error("Error while updating persisted url : container does not exist")
    except botocore.exceptions.ClientError as e:
        logging.error("Error while updating persisted url %s", str(e))