from azure.storage.blob import BlobServiceClient, BlobClient
import logging
import json
import botocore
import botocore.session
import helper as hp
import constants as const

import re

def getOktaUrl(filename):
    logging.info(f"Attempting to retrieve Okta URL from the blob storage for filename: {filename}")
    try:
#enter credentials
        accountName = hp.get_required_attr_from_env("AzureWebJobsStorage")
        container_name = const.CONTAINER
        logging.info(f"Using container: {container_name}")

        blob_service_client = BlobServiceClient.from_connection_string(accountName)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(filename)
        if blob_client.exists():
            logging.info(f"Found blob for filename: {filename}. Downloading...")
            streamdownloader = blob_client.download_blob()
            fileReader = json.loads(streamdownloader.readall())
            logging.info(f"Successfully retrieved and loaded JSON data for {filename}")
            return fileReader
        else:
            logging.warning(f"No blob found for filename: {filename}")
            return None
    except botocore.exceptions.ClientError as e:
        logging.error("Error while retrieving persisted url %s", str(e))
        logging.info("URL not found in storage_account bucket. Back-filling logs. ")
        return None
    except Exception as e:
        logging.error(f"Unexpected error occured: {e}")
        

def updateOktaUrl(filename,body):
    logging.info(f"Attempting to update Okta URL from the blob storage for filename: {filename}")

    try:
        accountName = hp.get_required_attr_from_env("AzureWebJobsStorage")
        container_name = const.CONTAINER
        logging.info(f"Using container: {container_name} for update operation")

        blob_service_client = BlobServiceClient.from_connection_string(accountName)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(filename)
        if blob_client.exists():
            logging.info(f"Blob exists for filename: {filename}. Uploading updates...")
            streamdownloader = blob_client.upload_blob(data=body, overwrite=True)
            logging.info(f"Successfully updated blob for filename: {filename}")
        else:
            logging.warning(f"No blob found for filename: {filename}. Creating a new blob...")
            blob_client.upload_blob(data=body)
            logging.info(f"Successfully created and uploaded data for new blob for filename: {filename}")
    except botocore.exceptions.ClientError as e:
        logging.error(f"Client error while uploading blob: {e}")
    except Exception as e:
        logging.error(f"Unexpected error occured during blob update: {e}")