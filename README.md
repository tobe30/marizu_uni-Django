# Marizu Uni - Student Management System 🎓

A Django-based web application for managing student admissions, profiles, and academic results.
  ADMIN USERNAME ->to signin
  tobemarizu@gmail.com
  12345

STUDENT USERNAME -> TO sign in
cindy@gmail.com
password: k1Iw0k4alm

divine@gmail.com
password:ghby9MDkav

camsy@gmail.com
password:1QIgGLgIxG

TEACHER USERNAME->to signin
maduemeemeka08@gmail.com
password:maRizut1#

---

## 🚀 Features

- Student application portal with document upload
- Teacher and student dashboards
- Admission approval by teachers
- Automated student account creation upon admission
- Result management (teachers upload, students check results)
- User profile management

---

## 🛠 Tech Stack

- Django (Python)
- HTML5 & CSS3
- Bootstrap 5
- SQLite (default, can be switched to PostgreSQL)
- Git & GitHub

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/tobe30/marizu_uni-Django.git
cd marizu_uni-Django

python -m venv venv
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On Mac/Linux

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver


