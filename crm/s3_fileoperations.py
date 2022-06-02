import os,boto3
from django.conf import settings

def fileTransferToS3(self,file_name,s3_location_file_name,src_path=settings.MEDIA_ROOT,remove_orignal=True):
    try:
        s3_resource_bucket = boto3.resource('s3',aws_access_key_id=settings.S3_ACCESS_KEY,
                            aws_secret_access_key= settings.S3_SECRET_KEY) if settings.S3_ACCESS_KEY and settings.S3_SECRET_KEY else boto3.resource('s3')
        s3_bucket_name = s3_resource_bucket.Bucket(settings.S3_PHONEBOOK_BUCKET_NAME)				
        s3_bucket_name.put_object(Key=s3_location_file_name,Body=open(src_path+"/"+file_name,'rb'))
        if remove_orignal:
            os.remove(src_path+"/"+file_name)
        return True
    except Exception as e:
        print("Error :: Transfering file to S3", e)

def s3fileDownloadToServer(self,file_name,s3_location_file_name,dest_path=settings.MEDIA_ROOT):
    try:
        s3_resource_bucket = boto3.client('s3',aws_access_key_id=settings.S3_ACCESS_KEY,
							aws_secret_access_key= settings.S3_SECRET_KEY) if settings.S3_ACCESS_KEY and settings.S3_SECRET_KEY else boto3.client('s3')
        with open(dest_path+"/"+file_name, 'wb') as f:
            s3_resource_bucket.download_fileobj(settings.S3_PHONEBOOK_BUCKET_NAME, s3_location_file_name, f)
        return True
    except Exception as e:
        print("Error :: File Download from S3 to Server", e)

def s3singedUrl(S3_location):
    try:
        s3_resource_bucket = boto3.client('s3',aws_access_key_id=settings.S3_ACCESS_KEY,
							aws_secret_access_key= settings.S3_SECRET_KEY) if settings.S3_ACCESS_KEY and settings.S3_SECRET_KEY else boto3.client('s3')
        url = s3_resource_bucket.generate_presigned_url(
        ClientMethod='get_object', 
        Params={'Bucket': settings.S3_PHONEBOOK_BUCKET_NAME, 'Key': S3_location},
        ExpiresIn=300)
        return url
    except Exception as e:
        print('s3 signed Url ',e)