# README.md
## Backend Technical Test
Welcome to the Backend Technical Test! This system is designed to manage products in a catalog with capabilities for user management, product querying, and notifications for administrative changes.

It implements a REST API using:
* FastAPI
* Sqlalchemy
* Postgres
* Alembic
* Celery
* Redis

## Features
1. User Management:
    * Admin users can create, update, and delete products.
    * Admin users can also manage other admin users.
    * Anonymous users can only query product information.

2. Product Management:
    * Products have attributes like SKU, name, price, and brand.
    * All changes made by admins to products trigger notifications to all other admins by email.

3. Query Tracking:
    * The system tracks how many times each product is queried by the users.

4. Notification System:
    * Whenever a product is modified, created or deleted by an admin, all the admins are notified.
    * This is implemented using a task queue (Redis) and email notifications (AWS SES).

5. API Documentation:
    * The system uses FastAPI, which provides automatically generated interactive API documentation.

## CI
Github Actions was used to control the CI, for this 2 tasks were created:
* To be able to maintain the quality of the code using Linter (Black).
* An action was created to run the unit tests and verify the functionality of the code.

# Setup and Installation
## Requirements
    * Docker and Docker Compose
    * Make (Optional)

## Installation
1. Clone the Repository:
```console
git clone <repository-url>
cd basic-catalog-system
```

2. Environment Configuration
The application can be configured using environment variables.
```console
make setup
```
This will generate the .env file where you need to configure the keys for AWS SES

3. Build and Start Services:
You can use Docker Compose to build and start the application:
```console
docker compose up --build
```

Alternatively, you can use the Makefile for common setup tasks:
```console
make build     # Build Docker images
make up        # Start services
make down      # Stop services
```

## Accessing the API

Once the application is running, you can access the API documentation at:

* Swagger UI: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

## User

By default, when the service starts, it creates a user with the keys:
* username: root
* password: root

The main idea for this user is to create a user for the administrator and be deleted.
