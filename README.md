# library-app-afskd
# Library Management System

A simple RESTful API for managing books and borrowers, built with **FastAPI**, **SQLite**, and **OpenTelemetry**.

## Features

- List, add, and borrow books  
- Register and retrieve borrowers  
- View books borrowed by a specific borrower  
- Unit and integration tests with `pytest`  
- Basic observability using OpenTelemetry (1 span, 2 metrics)

---

## Local Setup

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
Now the application is available at http://localhost:8000.
Interactive docs (Swagger UI): http://localhost:8000/docs

## Running the tests
The unit tests and integration tests can be run with the following command:

```bash
pytest
```

There are a few integration tests added that use a test DB and describe more complex scenarios. A few unit tests have also been added for the `book_service` module. 

## Observability

- Span Tracing: A custom span is added around the borrow_book service function to trace the performance of this operation.

- Metrics: 
    - Two counter metrics have been added: 
        - The time it takes to complete a "borrow book" operation. This allows us to detect if it's getting slower for some reason.
        - The number of failed borrow attempts. This could be important because if this number increases, it's possible that borrowers are trying to borrow nonexistent books or books that are not available. If this happens often, that could mean that somehting is wrong on our side (e.g. we're wrongly indicating that a book is available but it's not). It could also be interesting to track these failed attempts by error type. 


## Notes, possible improvements
Since this project is a PoC, many things could be improved / added

- Extending test cases to all modules.
- The task description didn't specify but it would be useful to have an endpoint that ends the loan. 
- The project could be Dockerized.
- It would also be beneficial to use an external database. Now we're using SQLite which is fine for a PoC but it would be more better to set up an external database. 
- More spans and metrics could be added, to more functions to improve observability. 
