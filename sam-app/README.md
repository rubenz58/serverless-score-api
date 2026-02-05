# Serverless Risk API

A serverless REST API built on AWS to demonstrate cloud-native backend development using **AWS Lambda**, **API Gateway**, **DynamoDB**, and **AWS SAM**.

This project focuses on:
- Infrastructure as Code (IaC)
- Event-driven serverless architecture
- AWS-managed scalability and observability
- Clean, minimal Python Lambda functions

---

## Architecture Overview

The application follows a fully serverless design:
Client → API Gateway → Lambda → DynamoDB

**AWS Services used**
- **API Gateway** – HTTP interface and routing
- **AWS Lambda (Python 3.11)** – business logic
- **Amazon DynamoDB** – persistent storage
- **AWS SAM** – deployment and infrastructure definition
- **Amazon CloudWatch** – logging and monitoring

---

## API Endpoints

### Create a score
**POST `/score`**

Request body:
```json
{
  "value": 42
}
```

Response:
```json
{
  "id": "uuid-generated-id"
}
```

### Get a score
**GET `/score/{id}`**
Response:
```json
{
  "id": "uuid-generated-id",
  "value": 42,
  "created_at": "2026-02-05T16:14:25.123Z"
}
```

---

## Data Model (DynamoDB)

| Attribute    | Type | Description |
|--------------|------|-------------|
| `id`         | S    | Primary key (UUID) |
| `value`      | N    | Score value |
| `created_at` | S    | ISO-8601 timestamp |

- Billing mode: **PAY_PER_REQUEST**
- No capacity planning required

---

## Deployment

### Prerequisites
- AWS CLI configured
- AWS SAM CLI installed
- Python 3.11

### Deploy to AWS
``bash
sam build
sam deploy --guided

### Local Development
Run the API locally using SAM:
``bash
sam local start-api

Example request:
``bash
curl -X POST http://127.0.0.1:3000/score \
  -H "Content-Type: application/json" \
  -d '{"value": 10}'

---

## Observability

``markdown
## Observability & Logging

The application is observable at both the API and compute layers:

- **API Gateway access logs** capture incoming request metadata
  (HTTP method, resource path, request ID).
- Logs are streamed to **Amazon CloudWatch Logs**.
- Each API request can be correlated with the corresponding Lambda execution.

Example access log entry:
c536c1bf-a119-4859-90f1-1991df6ae9d1) HTTP Method: POST, Resource Path: /score

---

## Security Considerations

- API endpoints are intentionally **unauthenticated** for demo purposes.
- Lambda functions use **IAM roles with scoped permissions**.
- In a production environment, authentication could be added via:
  - Amazon Cognito
  - IAM authorizers
  - Custom JWT authorizers

---

## Cleanup

All resources can be removed cleanly with:

``bash
sam delete

---

## Author
Ruben Zaccaroni
Software Engineer
Python • AWS • Serverless • REST APIs