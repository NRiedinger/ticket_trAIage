# Smart Support Inbox
This project was created as part of a coding challenge. The goal was to build a small full-stack application that helps a customer support team triage inbound messages. 
The system stores support tickets, analyzes them, suggest replies and tracks wether those 
suggestions were useful.

For prioritizing, categorizing and suggesting replies, this system uses an OpenAI Agent
which analyzes every newly created ticket.

> **Note**: This application is just a proof-of-concept and not production ready. It dooes not contain authentication and ticket-creation and -handling is done in one place so it's not suitable for real-world-usage.



## Backend

### Requirements
> **Note**: The mentioned versions are the ones I used and not necessarily the minimum versions
- **Python** 3.12.1
- **PostgreSQL** 18.1

### Setup

1. Go to backend folder
    ```shell
    cd .\backend\
    ```

2. Create virtual environment
    ```shell
    python -m venv .env
    ```

3. Activate virtual environment
    ```shell
    .\.env\Scripts\activate
    ```

4. Install dependencies
    ```shell
    pip install django djangorestframework psycopg2 django-environ openai-agents
    ```
    
5. Make sure the environment variable `OPENAI_API_KEY` is set.

5. Run development server
    ```shell
    python manage.py runserver
    ```

### Testing

Run unit tests with
```shell
python manage.py test tickets
```

## Frontend

### Requirements
> **Note**: The mentioned versions are the ones I used and not necessarily the minimum versions
- **Node.js** 25.5.0

### Setup

1. Go to frontend folder
    ```shell
    cd .\frontend\
    ```

2. Install dependencies
    ```shell
    npm install
    ```

3. Run development server
    ```shell
    npm start
    ```
