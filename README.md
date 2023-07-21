# open-knesset-backend

## Local Development

### Prerequisites

* Python 3.10+

### install:

python -m venv venv

### windows:

venv\Scripts\activate

### macos:

. venv/bin/activate

### install all requirements:

pip install -r requirements.txt

### create file .env:

OKNESSET_DB_USER="USER NAME"
OKNESSET_DB_PASSWORD="PASSWORD"
OKNESSET_DB_HOST="HOST"
OKNESSET_DB_PORT="PORT"
OKNESSET_DB_NAME="postgres"

### execute:

uvicorn main:app --reload

## Running using Docker

This is the same way the app is run in production.

Create the `.env` file as described above.

Build:

```
docker build -t open-knesset-backend .
```

Run:

```
docker run --env-file .env -p 8000:8000 open-knesset-backend
```
