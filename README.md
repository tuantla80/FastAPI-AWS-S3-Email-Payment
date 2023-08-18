## 1. Overview  
### Managers:  
- To handle the business logic
- To communicate with DB
- To tranform data and add it to DB and pass the result
### Models  
- To structure tables in DB
- To define schema for the objects
### Resources (Routes)  
- To create endpoints of the app
- To define behavior on GET, POST, PUT, DELETE for different routes
- To communiocate with managers to achieve its purpose
### Schemas  
- To validate data and structures of request and response objects using pydantic
### Services  
- To communicate with third party apps.
- In this project: AWS S3, AWS SES (Simple Email Service) and Wise payment service.
### Utils  
- To include helper functions used in the app.
## 2. Authentication and Authorization  
### JWT (JSON Web Token)  
- Transmiting client <--> server in a stateless and secure way.
- 3 parts seperately by a dot (*******.********.*********)
  - Header: algo (eg. HS256) and type
  - Payload: data
  - Signature: encode content of header and payload to a secret string
### Custom HTTPBearer  
### Add role to user model  
## 3. AWS S3 Service  
### Create a bucket on S3  
### Connect with AWS service using boto3 library  
- Get credentials: Access key ID and Secret access key
### Upload user's images to S3
## 4. Database Migration Tool
### Alembic
