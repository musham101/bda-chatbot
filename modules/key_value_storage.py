import boto3, os
from datetime import datetime
from boto3.dynamodb.conditions import Key

class KeyValueStorage:
    def create_conversation_logs_table(table_name='ConversationLogs', read_capacity=5, write_capacity=5):
        """
        Creates a DynamoDB table to store chatbot conversation logs.

        Parameters:
        - table_name (str): Name of the DynamoDB table to be created. Default is 'ConversationLogs'.
        - read_capacity (int): Read capacity units for the table. Default is 5.
        - write_capacity (int): Write capacity units for the table. Default is 5.

        The table uses:
        - 'UserID' as the partition key (HASH)
        - 'Timestamp' as the sort key (RANGE)

        This function uses environment variables for AWS credentials:
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_DEFAULT_REGION (defaults to 'us-east-1' if not set)

        If the table already exists, it will log a message and skip creation.
        """
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        
        try:
            table = dynamodb.create_table(
                TableName=table_name,
                AttributeDefinitions=[
                    {
                        'AttributeName': 'UserID',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'Timestamp',
                        'AttributeType': 'S'
                    }
                ],
                KeySchema=[
                    {
                        'AttributeName': 'UserID',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'Timestamp',
                        'KeyType': 'RANGE'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': read_capacity,
                    'WriteCapacityUnits': write_capacity
                }
            )
            print(f"Creating table '{table_name}'...")
            table.wait_until_exists()
            print(f"Table '{table_name}' created successfully!")
            return table

        except Exception as e:
            error_message = str(e)
            if 'ResourceInUseException' in error_message:
                print(f"Table '{table_name}' already exists.")
            else:
                print(f"Failed to create table '{table_name}': {error_message}")

    def insert_conversation_log(user_id, message, bot_response, table_name='ConversationLogs'):
        """
        Inserts a single conversation entry into the DynamoDB table.

        Parameters:
        - user_id (str): Unique identifier for the user.
        - message (str): The user's message to the chatbot.
        - bot_response (str): The chatbot's response.
        - table_name (str): Name of the DynamoDB table. Default is 'ConversationLogs'.

        The function uses environment variables for AWS credentials:
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_DEFAULT_REGION (defaults to 'us-east-1' if not set)
        """
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

        # Connect to DynamoDB
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

        table = dynamodb.Table(table_name)

        # Use current time as timestamp
        timestamp = datetime.utcnow().isoformat()

        try:
            table.put_item(
                Item={
                    'UserID': user_id,
                    'Timestamp': timestamp,
                    'Message': message,
                    'BotResponse': bot_response
                }
            )
            print(f"Inserted conversation log for user '{user_id}' at {timestamp}")
        except Exception as e:
            print(f"Failed to insert log for user '{user_id}': {str(e)}")

    def fetch_conversation_logs(user_id, limit=10, table_name='ConversationLogs', descending=True):
        """
        Fetches conversation logs for a given user from the DynamoDB table.

        Parameters:
        - user_id (str): The unique identifier for the user.
        - limit (int): Maximum number of log entries to retrieve. Default is 10.
        - table_name (str): Name of the DynamoDB table. Default is 'ConversationLogs'.
        - descending (bool): If True, returns messages in reverse chronological order.

        Returns:
        - List of conversation logs sorted by timestamp.
        """
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

        # Connect to DynamoDB
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

        table = dynamodb.Table(table_name)

        try:
            response = table.query(
                KeyConditionExpression=Key('UserID').eq(user_id),
                Limit=limit,
                ScanIndexForward=not descending  # False = newest first
            )

            logs = response.get('Items', [])
            print(f"Fetched {len(logs)} logs for user '{user_id}'.")
            return logs

        except Exception as e:
            print(f"Failed to fetch logs for user '{user_id}': {str(e)}")
            return []