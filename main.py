import json
import boto3
from boto3.dynamodb.conditions import Key
import uuid  

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Phonebook')

def lambda_handler(event, context):
    # Enable CORS for the Function URL
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Handle preflight requests (CORS)
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('CORS preflight successful')
        }
    
    print(event)
    body = json.loads(event['body'])
    operation = body['operation']
    
    if operation == 'add_contact':
        return add_contact(body, headers)
    elif operation == 'get_contact':
        return get_contact(body, headers)
    elif operation == 'delete_contact':
        return delete_contact(body, headers)
    else:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps('Invalid operation')
        }

def add_contact(event, headers):
    contact_id = str(uuid.uuid4())  # Generates a random unique ID
    name = event['name']
    phone_number = event['phone_number']
    
    # Add the contact to DynamoDB with the 'id' field
    table.put_item(
        Item={
            'id': contact_id,  # Primary key
            'Name': name,
            'PhoneNumber': phone_number
        }
    )
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps('Contact added successfully')
    }

def get_contact(event, headers):
    name = event['name']
    
    response = table.get_item(
        Key={
            'Name': name
        }
    )
    
    if 'Item' in response:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response['Item'])
        }
    else:
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps('Contact not found')
        }

def delete_contact(event, headers):
    name = event['name']
    
    response = table.delete_item(
        Key={
            'Name': name
        }
    )
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps('Contact deleted successfully')
    }
