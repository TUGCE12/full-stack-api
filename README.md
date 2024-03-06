# GLOV-API README

## Overview

Welcome to the GLOV-API project! This project provides an API for accessing the GLOV endpoint. This README guide will help you set up and test the API locally using Docker and provide instructions for testing the public API.

## Local Test

### Prerequisites

Make sure you have Docker installed on your machine. You can find instructions for installing Docker [here](https://docs.docker.com/get-docker/).

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/TUGCE12/glov-api.git
   ```

2. Navigate to the project directory:

   ```bash
   cd glov-api
   ```

3. Run the following command to start the API using Docker:

   ```bash
   docker-compose up
   ```

### Test Locally

Open a new terminal and use the following curl commands to test the local API:

```bash
# Test without streaming
curl -X GET http://127.0.0.1:5000/glov_endpoint?stream=false -H "Authorization: USER123"

# Test with streaming
curl -X GET http://127.0.0.1:5000/glov_endpoint?stream=true -H "Authorization: USER123"

# Test with a different user
curl -X GET http://127.0.0.1:5000/glov_endpoint?stream=false -H "Authorization: USER1234"
```

### Docker Check

Check Docker to ensure that two containers are running. You can use the following command:

```bash
docker ps
```

You should see two containers related to the GLOV-API project.
![docker images and containers](image.png)

## Public API Test

The API is also available publicly. You can test it using the following curl command:

```bash
# Replace XXX with a 3-digit numeric ID
curl -X GET https://gaw-xfmleg7qtq-uc.a.run.app/glov_endpoint?stream=false -H "Authorization: USERXXX"
```

## Important Notes

- **Authorization:** Ensure you replace USERXXX with a valid 3-digit numeric ID when testing the public API.

Thank you!