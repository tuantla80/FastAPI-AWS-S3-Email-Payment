## 1. Overview  
### Managers:  
- To handle the business logic
- To communicate with DB
- To tranform data and add it to DB and pass the result
### Models  
- To structure tables in DB
- To define schema for the objects
### Resources (Router)  
- To create endpoints of the app
- To define behavior on GET, POST, PUT, DELETE for different routes
### Schemas  
- To validate data and structures of request and response objects  

## 2. Authentication and Authorization  
### JWT (JSON Web Token)  
- Transmiting client <--> server in a stateless and secure way.
- 3 parts seperately by a dot (*******.********.*********)
  - Header: algo (eg. HS256) and type
  - Payload: data
  - Signature: encode content of header and payload to a secret string
## 3. Database Migration Tool
### Alembic
