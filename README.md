# Lab Results Extraction and Editing Web Application

## Overview

This project is a web application designed to extract, display, and allow editing of laboratory test results from uploaded reports (images). 
Users can view parsed lab data, edit details if needed, and save the corrected information to a PostgreSQL database.

---

## Features

- Upload lab reports and extract structured lab test data.
- Display patient info, clinic details, test dates, and individual test parameters.
- Editable form interface to correct or add missing data before saving.
- Save edited results securely in a PostgreSQL database.
- Responsive UI.
- Backend API built with FastAPI, using SQLAlchemy ORM for database operations.
- Support for various date formats when parsing test dates.

---

## Tech Stack

- **Frontend:** HTML, Bootstrap 5, Jinja2 templates (Flask / FastAPI templating)
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Python Packages:** `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2` (or `asyncpg`), `jinja2`

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Git

