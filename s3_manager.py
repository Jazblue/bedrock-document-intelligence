import boto3
import os

BUCKET_NAME = "bedrock-document-agent-storage"

s3 = boto3.client("s3")


def upload_document(file_path):

    filename = os.path.basename(file_path)

    s3.upload_file(
        file_path,
        BUCKET_NAME,
        filename
    )

    print(f"Uploaded {filename} to S3")

    return filename


def download_document(filename):

    os.makedirs("downloads", exist_ok=True)

    local_path = f"downloads/{filename}"

    s3.download_file(
        BUCKET_NAME,
        filename,
        local_path
    )

    print(f"Downloaded {filename} from S3")

    return local_path