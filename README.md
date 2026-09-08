# Corporate Asset Tracking

A multi-tenant web platform for tracking corporate device/asset logs, with strict company-scoped access control — each company's admins can only view and manage their own organization's data.

## Overview

Companies frequently need a simple way to track assets (devices, equipment, etc.) issued to or used by their organization, without exposing that data to other companies on a shared platform. This project implements that as a multi-tenant Django application: any company can register, and once registered, their admins are scoped strictly to their own company's records — with no visibility into any other company's assets or logs.

## Key Features

- **User Authentication** — Company admins sign up and register under their company name; standard login/session-based auth.
- **Company-Scoped Access Control** — Each admin can only view and manage device logs belonging to their own company. Cross-company data access is not possible through the application.
- **Device Log Management** — Admins can create new asset/device logs and view their company's existing log history after login.
- **Login Redirect Flow** — Successful signup or login redirects directly to the company's Device Log List, keeping the workflow simple.

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite
- **Frontend:** Django templates (HTML)

## Why Multi-Tenant Access Control

The core design problem this project solves isn't just storing asset data — it's making sure Company A can never see Company B's data, even though both are using the same application and the same underlying database. This is enforced at the application layer: every query for device logs is scoped to the requesting admin's company, not just filtered in the UI. This is the same least-privilege principle behind role-based access control (RBAC) in production systems — restricting access to only what a given identity is authorized to see, rather than relying on the interface alone to hide unauthorized data.

## Getting Started

```bash
# Clone the repository
git clone https://github.com/sami1310/Corporate-Asset-Tracking.git
cd Corporate-Asset-Tracking/corporate_asset_tracking

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Django
pip install django

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/` and register a new company account to get started.

## Project Structure

```
Corporate-Asset-Tracking/
│   .gitignore
│   README.md
│
└───corporate_asset_tracking/
    │   manage.py
    │
    ├───accounts/              # User authentication & company registration
    │       models.py
    │       views.py
    │       urls.py
    │       admin.py
    │
    ├───asset_logs/            # Device/asset log tracking (core feature)
    │       models.py
    │       views.py
    │       forms.py
    │       urls.py
    │       admin.py
    │
    ├───corporate_asset_tracking/  # Project settings
    │       settings.py
    │       urls.py
    │       wsgi.py / asgi.py
    │
    └───templates/
            signup.html
            login.html
            device_log_list.html
            create_device_log.html
```

Two Django apps drive the project: `accounts` handles company registration and authentication, while `asset_logs` implements the core device-log tracking and the company-scoped access control described above.

## Key Takeaways

- Designing for multi-tenancy from the start — rather than bolting on access restrictions later — meant every data access path had to be scoped by company at the query level, not just hidden in the UI.
- This project's access-control model mirrors the RBAC/least-privilege patterns used in production security contexts: an identity should only ever be able to reach the data it's explicitly authorized for.
