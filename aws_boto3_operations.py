import boto3
from botocore.exceptions import ClientError

# ----------- S3: List files in a specified bucket -----------
def list_s3_objects(bucket_name):
    s3 = boto3.client('s3')
    print(f"Listing objects in bucket: {bucket_name}")
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f" - {obj['Key']}")
        else:
            print("Bucket is empty.")
    except ClientError as e:
        print(f"Error: {e}")

# ----------- DynamoDB: Create table -----------
def create_dynamodb_table(table_name):
    dynamodb = boto3.client('dynamodb')

    try:
        response = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Creating DynamoDB table: {table_name}")
        waiter = boto3.client('dynamodb').get_waiter('table_exists')
        waiter.wait(TableName=table_name)
        print("Table created successfully.")
    except ClientError as e:
        print(f"Error: {e}")

# ----------- DynamoDB: Insert item -----------
def insert_item_dynamodb(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    try:
        response = table.put_item(
            Item={
                'id': '001',
                'name': 'Test Item',
                'description': 'This is a sample item'
            }
        )
        print("Item inserted successfully.")
    except ClientError as e:
        print(f"Error: {e}")

# ----------- Main Execution -----------
if __name__ == "__main__":
    bucket_name = "my-cli-demo-bucket-tartela-bucket"
    table_name = "MyTestTable"

    list_s3_objects(bucket_name)
    create_dynamodb_table(table_name)
    insert_item_dynamodb(table_name)
