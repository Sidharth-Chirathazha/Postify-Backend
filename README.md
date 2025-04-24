# Postify Backend API

![Postify Logo](https://res.cloudinary.com/dz9kgofdy/image/upload/v1/postify/logo)

## 📝 Overview

Postify is a modern blog-sharing platform where users can create, share, and interact with content through comments and likes. This repository contains the backend API built with Django and Django REST Framework.

## 🚀 Technologies

- **Django & Django REST Framework** - Robust Python web framework
- **PostgreSQL** - Powerful, open-source relational database
- **Cloudinary** - Cloud storage for media files
- **JWT Authentication** - Secure user authentication
- **CORS Support** - Cross-Origin Resource Sharing

## ⚙️ Prerequisites

Before setting up the project, make sure you have the following installed:

- Python 3.8+
- PostgreSQL
- Git

## 🛠️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sidharth-Chirathazha/Postify-Backend.git
```

### 2. Create and activate virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
cd postify-backend/postify_backend
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the `postify_backend` directory with the following variables:

```
SECRET_KEY=YOUR_DJANGO_SECRET_KEY
DEBUG=FALSE(PRODUCTION)/TRUE(DEVELOPMENT)
DATABASE_URL=YOUR_DATABASE_URL
CLOUDINARY_CLOUD_NAME=YOUR_CLOUDINARY_CLOUDNAME
CLOUDINARY_API_KEY=YOUR_CLOUDINARY_API_KEY
CLOUDINARY_API_SECRET=YOUR_CLOUDINARY_API_SECRET
CORS_ALLOWED_ORIGINS=FRONTEND_BASE_URL
```

### 5. Set up PostgreSQL database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database and user (in PostgreSQL prompt)
CREATE DATABASE YOUR_DBNAME;
CREATE USER YOUR_USERNAME WITH PASSWORD 'YOUR_PASSWORD';
ALTER ROLE YOUR_USERNAME SET client_encoding TO 'utf8';
ALTER ROLE YOUR_USERNAME SET default_transaction_isolation TO 'read committed';
ALTER ROLE YOUR_USERNAME SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE YOUR_DBNAME TO YOUR_USERNAME;
\q
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 8. Run development server

```bash
python manage.py runserver
```

The API should now be accessible at `FRONTEND_BASE_URL/api/`



The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-access-token>
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
