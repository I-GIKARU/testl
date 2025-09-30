# 🔐 Authentication

This supports multiple user types (`Student`, `Client`, `Admin`), email confirmation, password reset, and protected dashboards.

---

## 🚀 Features

- ✅ JWT-based authentication using **cookies**
- ✅ User registration with role support (`student`, `client`, `admin`)
- ✅ Login/logout using `flask-jwt-extended`
- ✅ Email confirmation with token
- ✅ Password reset via email token
- ✅ Role-based access control decorators
- ✅ Secure password hashing using `bcrypt`
- ✅ RESTful API with `Flask-RESTful`

---

## 🧩 Tech Stack

- **Flask**
- **Flask-JWT-Extended**
- **Flask-SQLAlchemy**
- **Flask-Bcrypt**
- **Flask-Mail**
- **SQLite** (default, can be swapped with PostgreSQL/MySQL)

---

## ⚙️ Environment Configuration (`.env`)

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///app.db

# Email settings (for Gmail SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-email-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Frontend (used in links)
FRONTEND_URL=http://localhost:3000

# Cookie settings
JWT_COOKIE_SECURE=false
JWT_ACCESS_TOKEN_EXPIRES=3600

.
├── app/
│   ├── models.py         # User models and helper functions
│   ├── resources.py      # API endpoints (login, register, etc.)
│   ├── utils.py          # Utility functions (email, decorators)
│   ├── extensions.py     # Flask extensions setup
├── config.py             # App configuration
