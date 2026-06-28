# AI Hub

AI Hub is a Django-based business website and admin dashboard for an AI services company. It includes public pages for services, case studies, reviews, blogs, events, gallery images, contact inquiries, and an optional AI assistant powered by the OpenAI API.

This README is written for beginners who receive this project as a `.zip` file and want to run it on their own computer.

## Project Information

| Item | Details |
| --- | --- |
| Project name | AI Hub |
| Project type | Django web application |
| Current project version | 1.0.0 |
| Main framework | Django 5.2.1 |
| Programming language | Python |
| Tested Python version | Python 3.13.1 |
| Database used in settings | PostgreSQL |
| Optional AI feature | OpenAI assistant |
| Frontend | Django templates, HTML, CSS |
| Static files location | `home/static/` |
| Media upload location | `media/` |

## System Requirements

### Minimum Requirements

| Requirement | Minimum |
| --- | --- |
| Operating system | Windows 10, Windows 11, macOS, or Linux |
| RAM | 4 GB |
| Storage | 1 GB free space |
| Python | Python 3.11 or newer |
| Database | PostgreSQL 14 or newer |
| Browser | Chrome, Edge, Firefox, or Safari |
| Internet | Required only for installing packages and using the OpenAI assistant |

### Recommended Requirements

| Requirement | Recommended |
| --- | --- |
| Operating system | Windows 11 |
| RAM | 8 GB or more |
| Storage | 2 GB free space |
| Python | Python 3.13.1 |
| Database | PostgreSQL 16 or newer |
| Browser | Latest Chrome or Edge |

## Main Features

- Public home page for AI Hub.
- Services page with active services.
- Case studies page with image upload support.
- Customer review page and public review submission form.
- Blog/articles page.
- Events page with upcoming and past event status.
- Gallery page with uploaded images.
- Contact form with name, email, phone, company, country, job title, and job details.
- Secure custom admin dashboard.
- Admin inquiry management: view, search, mark responded, and delete.
- Admin content management for services, articles, case studies, events, gallery images, and reviews.
- Admin analytics dashboard.
- Admin user creation page.
- Optional AI assistant using OpenAI API.
- Admin inactivity timeout after 2 minutes.

## Project Folder Structure

```text
ai_hub/
├── ai_hub/                  # Main Django project settings and URLs
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── home/                    # Main website application
│   ├── migrations/
│   ├── static/home/css/
│   ├── templates/home/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── middleware.py
│   ├── models.py
│   └── views.py
├── media/                   # Uploaded images and media files
├── .env.example             # Example environment variables
├── db.sqlite3               # Existing SQLite file, not used by current settings
├── manage.py                # Django command file
├── requirements.txt         # Python packages
└── README.md
```

## Software You Need to Install

Before running the project, install these tools:

1. Python
   - Download from: https://www.python.org/downloads/
   - During installation on Windows, tick **Add Python to PATH**.

2. PostgreSQL
   - Download from: https://www.postgresql.org/download/
   - Remember the password you set for the `postgres` user.

3. Code editor
   - Recommended: Visual Studio Code.

4. Web browser
   - Recommended: Chrome or Microsoft Edge.

## How to Run the Project from a Zip File

### Step 1: Extract the Zip File

Right-click the zip file and extract it to a simple location, for example:

```text
D:\AI_Solutions\ai_hub
```

Avoid paths with special characters because they can sometimes create beginner setup issues.

### Step 2: Open the Project Folder

Open PowerShell or the VS Code terminal inside the project folder.

Example:

```powershell
cd D:\AI_Solutions\ai_hub
```

You should see `manage.py` in this folder.

### Step 3: Create a Virtual Environment

A virtual environment keeps this project's packages separate from other Python projects.

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

After activation, your terminal usually shows `(venv)` at the beginning of the line.

For macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Required Packages

```powershell
pip install -r requirements.txt
```

Installed main packages include:

```text
Django==5.2.1
openai>=1.99.0
Pillow>=10.0.0
psycopg2-binary==2.9.12
python-dotenv>=1.0.1
```

### Step 5: Create the Environment File

Copy `.env.example` and rename the copy to `.env`.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Then open `.env` and update it if needed.

Basic `.env` example:

```env
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4.1-mini
OPENAI_TIMEOUT=20
OPENAI_MAX_OUTPUT_TOKENS=220
ASSISTANT_CONTEXT_CACHE_SECONDS=300
```

The OpenAI key is optional. The website can still run without it, but the AI assistant will show an unavailable message for questions that are not answered by the built-in FAQ.

### Step 6: Create the PostgreSQL Database

The current project settings use PostgreSQL.

Default database values in `ai_hub/settings.py` are:

```text
Database name: ai_hub
Database user: your_user
Database password: your_password
Database host: localhost
Database port: 5432
```

Create a PostgreSQL database named:

```text
ai_hub
```

You can create it using pgAdmin or using the terminal.

Using PostgreSQL terminal:

```sql
CREATE DATABASE ai_hub;
```

If your PostgreSQL username, password, host, or port is different, add these values to your `.env` file:

```env
POSTGRES_DB=ai_hub
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-postgres-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Important: Set the  PostgreSQL passwor `POSTGRES_PASSWORD` in `.env`.

### Step 7: Run Database Migrations

Migrations create the required database tables.

```powershell
python manage.py migrate
```

### Step 8: Create an Admin User

Create your first admin account:

```powershell
python manage.py createsuperuser
```

Enter a username, email, and password when asked.

This account is used to log in to the custom admin dashboard.

### Step 9: Start the Development Server

```powershell
python manage.py runserver
```

If everything is working, the terminal will show a local URL like:

```text
http://127.0.0.1:8000/
```

Open that URL in your browser.

## Important Website URLs

| Page | URL |
| --- | --- |
| Home | `http://127.0.0.1:8000/` |
| Services | `http://127.0.0.1:8000/services/` |
| Case Studies | `http://127.0.0.1:8000/case-studies/` |
| Reviews | `http://127.0.0.1:8000/reviews/` |
| Submit Review | `http://127.0.0.1:8000/reviews/submit/` |
| Blog | `http://127.0.0.1:8000/blog/` |
| Gallery | `http://127.0.0.1:8000/gallery/` |
| Events | `http://127.0.0.1:8000/events/` |
| AI Assistant | `http://127.0.0.1:8000/assistant/` |
| Contact | `http://127.0.0.1:8000/contact/` |
| Admin Login | `http://127.0.0.1:8000/admin-panel/login/` |
| Admin Dashboard | `http://127.0.0.1:8000/admin-panel/` |
| Admin Analytics | `http://127.0.0.1:8000/admin-panel/analytics/` |
| Manage Inquiries | `http://127.0.0.1:8000/admin-panel/inquiries/` |
| Manage Content | `http://127.0.0.1:8000/admin-panel/content/` |
| Manage Admin Users | `http://127.0.0.1:8000/admin-panel/users/` |

## How to Use the Admin Dashboard

1. Go to:

```text
http://127.0.0.1:8000/admin-panel/login/
```

2. Log in using the superuser account you created.

3. From the dashboard, you can:
   - View total inquiries.
   - View new and responded inquiries.
   - See recent inquiries.
   - Manage services.
   - Manage articles/blogs.
   - Manage case studies.
   - Manage events.
   - Manage gallery images.
   - Approve or decline customer reviews.
   - Create admin users.

Admin users must have `is_staff=True`.

## Managing Website Content

Use the admin content panel:

```text
http://127.0.0.1:8000/admin-panel/content/
```

Available content sections:

- Services
- Articles
- Case Studies
- Events
- Gallery Images
- Customer Reviews

For image uploads, make sure the `media/` folder exists. Uploaded files are stored inside this folder.

## Contact Form Fields

The contact form collects:

- Name
- Email
- Phone
- Company name
- Country
- Job title
- Job details

Submitted contact requests appear in:

```text
http://127.0.0.1:8000/admin-panel/inquiries/
```

Admins can search inquiries, filter by status, mark an inquiry as responded, or delete it.

## Customer Review Flow

1. A visitor submits a review from:

```text
http://127.0.0.1:8000/reviews/submit/
```

2. The review is saved as pending and inactive.

3. Admin approves or declines the review.

4. Approved reviews become visible on the public reviews page.

## AI Assistant Setup

The AI assistant has two answer methods:

1. Built-in FAQ answers for common questions.
2. OpenAI API answers for other questions.

To enable OpenAI answers, add a valid key in `.env`:

```env
OPENAI_API_KEY=your-real-openai-api-key
```

Optional settings:

```env
OPENAI_MODEL=gpt-4.1-mini
OPENAI_TIMEOUT=20
OPENAI_MAX_OUTPUT_TOKENS=220
ASSISTANT_CONTEXT_CACHE_SECONDS=300
```

If no OpenAI key is provided, the project still runs normally, but the assistant may return:

```text
AI assistant is temporarily unavailable.
```

## Common Commands

Activate virtual environment:

```powershell
venv\Scripts\activate
```

Install packages:

```powershell
pip install -r requirements.txt
```

Run migrations:

```powershell
python manage.py migrate
```

Create admin user:

```powershell
python manage.py createsuperuser
```

Start server:

```powershell
python manage.py runserver
```

Stop server:

```text
Press CTRL + C in the terminal
```

## Troubleshooting

### Problem: `python` is not recognized

Python is not added to PATH.

Fix:

- Reinstall Python.
- Tick **Add Python to PATH** during installation.
- Close and reopen PowerShell.

### Problem: `pip install -r requirements.txt` fails

Try upgrading pip:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Problem: PostgreSQL connection error

Check these points:

- PostgreSQL is installed.
- PostgreSQL service is running.
- Database `ai_hub` exists.
- Username and password are correct.
- `.env` contains the correct `POSTGRES_PASSWORD`.
- Port is usually `5432`.

### Problem: password authentication failed for user `postgres`

Your PostgreSQL password is different from the default value in the project.

Add this to `.env`:

```env
POSTGRES_PASSWORD=your-postgres-password
```

### Problem: `no database named ai_hub`

Create the database first:

```sql
CREATE DATABASE ai_hub;
```

Then run:

```powershell
python manage.py migrate
```

### Problem: images are not showing

Check that:

- `DEBUG=True` in development.
- Uploaded images exist inside `media/`.
- The page is being opened through `python manage.py runserver`, not directly as an HTML file.

### Problem: cannot log in to admin dashboard

Check that:

- You created a superuser.
- The user has `is_staff=True`.
- You are using the custom login page:

```text
http://127.0.0.1:8000/admin-panel/login/
```

### Problem: admin logs out quickly

This project has an admin inactivity timeout of 2 minutes. If the admin does not interact with the dashboard for 2 minutes, the user is logged out automatically.

## Notes About SQLite

This project folder contains a `db.sqlite3` file, but the current `settings.py` uses PostgreSQL:

```python
'ENGINE': 'django.db.backends.postgresql'
```

For normal setup, use PostgreSQL. Only change to SQLite if you intentionally edit `ai_hub/settings.py`.

## Development Notes

- Main settings file: `ai_hub/settings.py`
- Main URL file: `ai_hub/urls.py`
- Main app: `home`
- Public views and admin dashboard logic: `home/views.py`
- Database models: `home/models.py`
- Forms: `home/forms.py`
- Admin timeout middleware: `home/middleware.py`
- Templates: `home/templates/home/`
- CSS: `home/static/home/css/site.css`

## Security Notes

Before deploying this project online:

- Set `DEBUG=False`.
- Use a strong secret key.
- Add your domain to `ALLOWED_HOSTS`.
- Store real passwords and API keys in environment variables.
- Do not share your `.env` file publicly.
- Use HTTPS on the live server.
- Use a production-ready web server such as Gunicorn or uWSGI behind Nginx or Apache.
- Configure static and media file serving correctly.
- Use a strong PostgreSQL password.

## Deployment Checklist

Before giving the website to real users:

- Confirm all pages open correctly.
- Confirm contact form saves inquiries.
- Confirm admin can log in.
- Confirm admin can manage content.
- Confirm image upload works.
- Confirm review approval works.
- Confirm OpenAI assistant works if enabled.
- Set production environment variables.
- Run migrations on the production database.
- Collect static files if your hosting platform requires it:

```powershell
python manage.py collectstatic
```

## Beginner Setup Summary

For a quick reminder, the full beginner flow is:

```powershell
cd D:\AI_Solutions\ai_hub
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

Admin login:

```text
http://127.0.0.1:8000/admin-panel/login/
```

## License

This project is prepared for educational, client demonstration, and business website development purposes. Add your final license here if you plan to publish it publicly on GitHub.
