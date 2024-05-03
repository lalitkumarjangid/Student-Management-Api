# fast-api
# Student Management API

This is a FastAPI application that provides a RESTful API for managing student data.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/lalitkumarjangid/fast-api.git
    
    ```

2. Install the required Python packages:
    ```bash
    pip install fastapi uvicorn pymongo python-dotenv
    ```

3. Set up your MongoDB URI in a `.env` file:
    ```bash
    echo "MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/" > .env
    ```
    Replace `<username>` and `<password>` with your MongoDB username and password.

## Running the Application

To start the application, run the following command:

```bash
uvicorn main:app --reload
```
### Live Link

```bash
https://fast-api-1-vhj6.onrender.com/api/students
```

### Follow me on Github
```bash
https://github.com/lalitkumarjangid
```
