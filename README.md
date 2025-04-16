# HealthBot

A Django-based health management application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

## Running the Development Server

To start the development server, run:
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## Project Structure

- `healthbot/` - Main project directory
  - `manage.py` - Django's command-line utility for administrative tasks
  - `healthbot/` - Project configuration directory
    - `settings.py` - Project settings
    - `urls.py` - Project URL configuration
    - `wsgi.py` - WSGI configuration
    - `asgi.py` - ASGI configuration 