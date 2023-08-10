## 1. Authentication and Authorization  
### JWT (JSON Web Token)  
- Transmiting client <--> server in a stateless and secure way.
- 3 parts seperately by a dot (hhhhhhhh.pppppppppppp.ssssssssss)
  - Header: algo and type
  - Payload: data
  - Signature: encode content of header and payload to a secret string  
