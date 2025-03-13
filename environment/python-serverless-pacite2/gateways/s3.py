import boto3
import urllib.parse
import csv
import codecs

class S3Gateway:
    
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3', region_name='us-east-2')
        self.s3_resource = boto3.resource('s3')
    
    def download_and_read_csv_from_event(self, event):
        try:
            # Extract file location from event
            bucket = event['Records'][0]['s3']['bucket']['name']
            key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
            local_filename = f'/tmp/{key}'
            
            # Download file
            self.s3_client.download_file(bucket, key, local_filename)
            
            # Read and parse CSV
            csv_data = []
            with open(local_filename, 'r') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    csv_data.append(row)
                    
            return csv_data
        except Exception as e:
            print(f"Error downloading/processing S3 file: {str(e)}")
            return []
    
    def create_and_upload_csv(self, filename, fieldnames, data):
        try:
            # Create local CSV file
            local_path = f'/tmp/{filename}'
            with open(local_path, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            
            # Upload to S3
            self.s3_client.upload_file(local_path, self.bucket_name, filename)
            return True
        except Exception as e:
            print(f"Error creating/uploading CSV: {str(e)}")
            return False