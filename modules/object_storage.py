from dotenv import load_dotenv
import boto3
import os

load_dotenv()

class ObjectStorage:
    def create_s3_folder(bucket_name, folder_name):
        """
        Creates a folder (zero-byte object with a trailing slash) in an Amazon S3 bucket.

        Parameters:
        - bucket_name (str): Name of the S3 bucket where the folder will be created.
        - folder_name (str): Name of the folder to be created. A trailing slash is added if not present.

        This function uses environment variables for AWS credentials:
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_DEFAULT_REGION (defaults to 'us-east-1' if not set)
        """
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

        if not folder_name.endswith('/'):
            folder_name += '/'

        try:
            s3.put_object(Bucket=bucket_name, Key=folder_name)
            print(f"Folder '{folder_name}' created in bucket '{bucket_name}'")
        except Exception as e:
            print(f"Error creating folder: {e}")

    def upload_file_to_s3(bucket_name, folder_name, local_file_path):
        """
        Uploads a local file to a specified folder within an Amazon S3 bucket.

        Parameters:
        - bucket_name (str): Name of the S3 bucket.
        - folder_name (str): Target folder inside the S3 bucket. A trailing slash is added if missing.
        - local_file_path (str): Full path to the local file to be uploaded.

        The function uses environment variables for AWS credentials:
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_DEFAULT_REGION (defaults to 'us-east-1' if not set)

        The file will be uploaded as 's3://bucket_name/folder_name/file_name'.
        """
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

        file_name = os.path.basename(local_file_path)

        if not folder_name.endswith('/'):
            folder_name += '/'
        s3_key = folder_name + file_name

        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

        try:
            s3.upload_file(local_file_path, bucket_name, s3_key)
            print(f"✅ File '{file_name}' uploaded to 's3://{bucket_name}/{s3_key}'")
            return f"s3://{bucket_name}/{s3_key}"
        except Exception as e:
            print(f"❌ Upload failed: {e}")
    
    def download_file_from_s3(bucket_name, s3_file_path, local_destination):
        """
        Downloads a file from a specified path in an Amazon S3 bucket to a local destination.

        Parameters:
        - bucket_name (str): Name of the S3 bucket.
        - s3_file_path (str): Full key (path) of the file in the S3 bucket (e.g., 'folder/subfolder/filename.ext').
        - local_destination (str): Local file path where the downloaded file will be saved.

        The function uses environment variables for AWS credentials:
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_DEFAULT_REGION (defaults to 'us-east-1' if not set)
        """
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

        try:
            s3.download_file(bucket_name, s3_file_path, local_destination)
            print(f"✅ File downloaded from 's3://{bucket_name}/{s3_file_path}' to '{local_destination}'")
        except Exception as e:
            print(f"❌ Download failed: {e}")

    def delete_file_from_s3(bucket_name, s3_file_path):
        """
        Deletes a specific file from an Amazon S3 bucket.

        Parameters:
            bucket_name (str): The name of the S3 bucket.
            s3_file_path (str): The full path (key) to the file in the bucket.
        """
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

        try:
            s3.delete_object(Bucket=bucket_name, Key=s3_file_path)
            print(f"🗑️ File 's3://{bucket_name}/{s3_file_path}' has been deleted.")
        except Exception as e:
            print(f"❌ Error deleting file: {e}")