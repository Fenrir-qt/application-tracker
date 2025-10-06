# Application Tracker


## Overview
CareerQuest is a simple Django-based web app to track your job applications. Log each application with company, role, description, status, and date, then view your progress with a clean dashboard and quick search.

## Key Features
- **Authentication**: Sign up, log in (by username or email), and reset passwords.
- **Application management**: Add, edit, delete entries with statuses like Accepted, Offered, Pending, Rejected, or No Response.
- **Dashboard insights**: See totals by status and browse recent applications with pagination.
- **Search**: Find applications by company, role, description, or status.
- **Profile**: Update name, email, and password securely.

## Tech Stack
- **Backend**: Django
- **Database**: PostgreSQL (via `psycopg`)
- **Config**: `django-environ` for environment-based settings

