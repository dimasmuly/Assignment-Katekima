# Assignment-Katekima

## Description
This project is a warehouse management system built using Django. This system allows users to manage items, purchases, and sales.

## Prerequisites
Before you start, make sure you have the following:
- Python 3.x
- Django
- Django REST Framework

## Installation

1. **Clone Repository**
```bash
git clone <repository-url>
cd <repository-directory>
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate # For Linux/Mac
venv\Scripts\activate # For Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

## Project Configuration

1. **Database Settings**
Make sure you have configured the database in `settings.py`. By default, this project uses SQLite. You can change the database settings as needed.

2. **Database Migration**
Run the following commands to apply the migrations and create tables in the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Adding Initial Data (Optional)**
You can add initial data using the Django shell or through the provided API endpoints.

## Running the Project

1. **Run the Server**
Once all the configurations are complete, run the server with the following commands:
```bash
python manage.py runserver
```

2. **Application Access**
Open a browser and access the application at:
```
http://localhost:8000/
```

## Conclusion
This project is a simple example of a warehouse management system. 

If you have any questions or issues, please open an issue in this repository.