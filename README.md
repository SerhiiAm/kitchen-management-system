# Kitchen Management System 🍳

A web application built with Django for managing kitchen operations, tracking dishes, types of cuisine, and chefs (
cooks) assignments.

## 🚀 Features

* **Authentication & Authorization:** Secure access with separate permissions for regular cooks and supervisors/admins (
  using custom `UserPassesTestMixin`).
* **Session Tracking:** Built-in visit counter utilizing Django sessions.
* **Advanced Search:** Interactive searching and filtering for Dishes, Dish Types, and Cooks.
* **Modern UI:** Fully customized responsive interface based on a premium Bootstrap dashboard layout.
* **Robust Testing:** Covered with unit tests for views, forms, and models ensuring stability and security.

## 🛠️ Tech Stack

* **Backend:** Python 3.x, Django 4.x / 5.x
* **Database:** SQLite (Development)
* **Frontend:** HTML5, CSS3, Bootstrap 5, Crispy Forms

## 📊 Database Structure

*(The database schema includes custom Cook model extending AbstractUser)*

## 🔧 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SerhiiAm/kitchen-management-system.git
   cd kitchen-management-system
   ```
