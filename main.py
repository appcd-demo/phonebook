import json
import boto3
from boto3.dynamodb.conditions import Key
import uuid  

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Phonebook')

def lambda_handler(event, context):
    
    if 'body' in event: 
        body = json.loads(event['body'])
    else:  
        body = json.loads(event.get('body', '{}'))  

    operation = body.get('operation')
    
    if operation == 'add_contact':
        return add_contact(body)
    elif operation == 'get_contact':
        return get_contact(body)
    elif operation == 'delete_contact':
        return delete_contact(body)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid operation')
        }


def add_contact(event):
   
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
        'body': json.dumps('Contact added successfully')
    }


def get_contact(event):
    name = event['name']
    
    response = table.get_item(
        Key={
            'Name': name
        }
    )
    
    if 'Item' in response:
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Contact not found')
        }

def delete_contact(event):
    name = event['name']
    
    response = table.delete_item(
        Key={
            'Name': name
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Contact deleted successfully')
    }
