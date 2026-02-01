# fs_coding_challenge
Full-Stack Coding Challenge: Smart Support Inbox (Python Backend)

## Installation

### Backend

1. Go to backend
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
