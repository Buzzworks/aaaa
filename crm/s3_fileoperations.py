import os,boto3
from django.conf import settings
from google.cloud import storage
from google.oauth2 import service_account
import time


def fileTransferToCloudStorage(self,file_name,s3_location_file_name,src_path=settings.MEDIA_ROOT,remove_orignal=True):
    try:
        if settings.S3_PHONEBOOK_BUCKET_NAME != "":
            upload_to_s3(file_name,s3_location_file_name,src_path)
        elif settings.S3_GCLOUD_BUCKET_NAME != "":
            upload_to_gcp(file_name, s3_location_file_name,src_path)        
        if remove_orignal:
            os.remove(src_path+"/"+file_name)
        return True
    except Exception as e:
        print("Error :: Transfering file to S3", e)

def cloudStoragefileDownloadToServer(self,file_name,s3_location_file_name,dest_path=settings.MEDIA_ROOT):
    try:
        if settings.S3_PHONEBOOK_BUCKET_NAME != "":
            s3_download_server(file_name,s3_location_file_name,dest_path)
            return True
        elif settings.S3_GCLOUD_BUCKET_NAME != "":
            gcp_download_server(s3_location_file_name,dest_path)
    except Exception as e:
        print("Error :: File Download from S3 to Server", e)

def get_generate_signed_url(file_name,dest_path=settings.MEDIA_ROOT):
    try:
        if settings.GS_BUCKET_NAME!="":
            blob = getGCloudBucket(file_name)
            expiration_time = int(time.time() + 3600)
            return blob.generate_signed_url(expiration_time)
    except Exception as e:
        print("Error :: File Download from S3 to Server", e)

def upload_to_s3(file_name,s3_location_file_name,src_path):
    try:
        s3_resource_bucket = boto3.resource('s3',aws_access_key_id=settings.S3_ACCESS_KEY,
                            aws_secret_access_key= settings.S3_SECRET_KEY) if settings.S3_ACCESS_KEY and settings.S3_SECRET_KEY else boto3.resource('s3')
        s3_bucket_name = s3_resource_bucket.Bucket(settings.S3_PHONEBOOK_BUCKET_NAME)				
        s3_bucket_name.put_object(Key=s3_location_file_name,Body=open(src_path+"/"+file_name,'rb'))
    except Exception as e:
        print("Error at upload_to_s3",e)
def upload_to_gcp(source_file_name, destination_blob_name,src_path):
    """Uploads a file to the bucket."""
    try:
        blob = getGCloudBucket(src_path+'/'+destination_blob_name)
        
        blob.upload_from_filename(src_path+'/'+source_file_name)
        print(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )
        return True
    except Exception as e:
        print("Error :: File Upload to GCP error ",e)

def gcp_download_server(s3_location_file_name,dest_path):
    try:
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        blob = getGCloudBucket(dest_path+"/"+s3_location_file_name)
        blob.download_to_filename(dest_path+"/"+s3_location_file_name)
    except Exception as e:
        print("Errro at download GCP", e)
        
def s3_download_server(file_name,s3_location_file_name,dest_path):
    try:
        s3_resource_bucket = boto3.client('s3',aws_access_key_id=settings.S3_ACCESS_KEY,
                    aws_secret_access_key= settings.S3_SECRET_KEY) if settings.S3_ACCESS_KEY and settings.S3_SECRET_KEY else boto3.client('s3')
        with open(dest_path+"/"+file_name, 'wb') as f:
            s3_resource_bucket.download_fileobj(settings.S3_PHONEBOOK_BUCKET_NAME, s3_location_file_name, f)
    except Exception as e:
        print("s3_download_server error ",e)

def getGCloudBucket(file_name):
    try:
        if settings.JSON_KEY:
            storage_credentials = service_account.Credentials.from_service_account_info(settings.JSON_KEY)
            storage_client = storage.Client(project=settings.JSON_KEY['project_id'], credentials=storage_credentials)
        else:
            storage_client = storage.Client()
        bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
        blob = bucket.blob(file_name)
        return blob
    except Exception as e:
        print("Error at Get GLoudData",e)
