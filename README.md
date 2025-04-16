# library-app-afskd
# 📚 Library Management System

A simple RESTful API for managing books and borrowers, built with **FastAPI**, **SQLite**, and **OpenTelemetry**.

## Features

- List, add, and borrow books  
- Register and retrieve borrowers  
- View books borrowed by a specific borrower  
- Unit and integration tests with `pytest`  
- Basic observability using OpenTelemetry (1 span, 1 metric)

---

## 🚀 Local Setup

### 0. Prerequisites
    - python 3.11 or newer
    - pip 
    - pipenv

### 1. Clone the Repository

```bash
git clone https://github.com/pvarhegyi/library-app-afskd.git
cd library-app-afskd
```

### 2. Set up pipenv and install rependencies

```bash
    pipenv shell 
    pipenv install
```

### 3. Run the application 
```bash
uvicorn app.main:app --reload
```
Now the application is available at localhost:8080