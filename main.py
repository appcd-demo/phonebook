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

    # Return the contact ID in the response
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Contact added successfully', 'id': contact_id})
    }
def get_contact(event):
    try:
        contact_id = event.get('id')

        if not contact_id:
            return {
                'statusCode': 400,
                'body': json.dumps('Contact ID is required')
            }

        response = table.get_item(
            Key={
                'id': contact_id  # Querying using the 'id' as primary key
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
    except Exception as e:
        print(f"Error in get_contact: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }

def delete_contact(event):
    try:
        contact_id = event.get('id')

        if not contact_id:
            return {
                'statusCode': 400,
                'body': json.dumps('Contact ID is required')
            }

        table.delete_item(
            Key={
                'id': contact_id  # Deleting using the 'id' as primary key
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Contact deleted successfully')
        }
    except Exception as e:
        print(f"Error in delete_contact: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
