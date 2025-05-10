
---

# 🧪 Vialab – Blood Analysis Lab – Backend

This is the **backend** service for the **Vialab Blood Analysis Lab** system, built with **Django Rest Framework**. It provides API endpoints to support various lab functionalities such as managing exams, orders, feedback, authentication, and more.

---

## 🚀 Features

* 📊 Dashboard statistics and financial insights
* 📋 Exam listing and availability check
* 🧾 Order creation, status check, and notifications
* 📢 Announcements and ads
* 📬 Newsletter subscription
* ❓ FAQs management
* 💬 User feedback handling
* 🔐 Secure JWT authentication

---

## 📦 Tech Stack

* Python
* Django
* Django Rest Framework (DRF)
* Simple JWT for authentication

---

## 🔌 API Endpoints

### 📍 General

| Endpoint | Method | Description        |
| -------- | ------ | ------------------ |
| `/`      | GET    | General statistics |
| `/about` | GET    | About the lab      |

---

### ❓ FAQs

| Endpoint     | Method | Description        |
| ------------ | ------ | ------------------ |
| `/faqs`      | GET    | List all FAQs      |
| `/faqs/<id>` | GET    | Get a specific FAQ |

---

### 🧪 Exams

| Endpoint         | Method | Description                       |
| ---------------- | ------ | --------------------------------- |
| `/exams`         | GET    | List all exams                    |
| `/exams/<id>`    | GET    | Get details of a specific exam    |
| `/availablExams` | GET    | List available exams for patients |

---

### 🧾 Orders

| Endpoint       | Method           | Description                          |
| -------------- | ---------------- | ------------------------------------ |
| `/orders`      | GET, POST        | List all orders or create a new one  |
| `/orders/<id>` | GET, PUT, DELETE | Retrieve, update, or delete an order |
| `/orderCheck`  | POST             | Check order status                   |
| `/orderEmail`  | POST             | Send order confirmation via email    |

---

### 📢 Announcements

| Endpoint    | Method | Description                 |
| ----------- | ------ | --------------------------- |
| `/ads`      | GET    | List announcements          |
| `/ads/<id>` | GET    | Get a specific announcement |

---

### 💬 Feedback

| Endpoint          | Method    | Description             |
| ----------------- | --------- | ----------------------- |
| `/feedbacks`      | GET, POST | Submit or list feedback |
| `/feedbacks/<id>` | GET       | View specific feedback  |

---

### 📬 Newsletter

| Endpoint         | Method | Description             |
| ---------------- | ------ | ----------------------- |
| `/joiNewsletter` | POST   | Subscribe to newsletter |

---

### 📊 Financial Statistics

| Endpoint                            | Method | Description                      |
| ----------------------------------- | ------ | -------------------------------- |
| `/financials/<year>/<month>/<week>` | GET    | View weekly financial statistics |

---

### 🔐 Authentication

| Endpoint           | Method | Description                      |
| ------------------ | ------ | -------------------------------- |
| `/token`           | POST   | Obtain access and refresh tokens |
| `/token/refresh`   | POST   | Refresh JWT token                |
| `/password/change` | POST   | Change user password             |

---

## 🔧 Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/kimanxo/Vialab-Backend
   cd blood-analysis-backend
   ```

2. **Create a virtual environment and activate it**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**

   ```bash
   python manage.py migrate
   ```

5. **Start the development server**

   ```bash
   python manage.py runserver
   ```

---

## 📬 Contact

For questions or contributions, please open an issue or submit a pull request.

---

