# phonebook
 simple phonebook application using DynamoDB

##### add contact 
```
curl -X POST <your-function-url> \
-H "Content-Type: application/json" \                 
-d '{"operation": "add_contact", "name": "xyz", "phone_number": "1234567890"}'
{"message": "Contact added successfully", "id": "5da57224-be7b-46b1-a23f-aba710defc05"}%     
```

 ##### get contact 
 ```
 curl -X POST  <your-function-url>  \
-H "Content-Type: application/json" \
-d '{"operation": "get_contact", "id": "5da57224-be7b-46b1-a23f-aba710defc05" }' 
{"id": "5da57224-be7b-46b1-a23f-aba710defc05", "PhoneNumber": "1234567890", "Name": "xyz"}%      
```

 ##### delete contact 

```
 curl -X POST  <your-function-url>  \
-H "Content-Type: application/json" \
-d '{"operation": "delete_contact", "id": "5da57224-be7b-46b1-a23f-aba710defc05" }'
"Contact deleted successfully"%
```                     
