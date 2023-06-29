# Development Dockerfile for Django app

FROM python:3.8-slim

# Set the default directory where CMD will execute
WORKDIR gym_athletes

COPY . /gym_athletes
# Install dependencies
RUN apt-get update && apt-get install -y \
    && apt-get -y install libpq-dev gcc 
    
# upgrade pip
RUN pip install --upgrade pip
# Install dependencies from requirements file
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run Django's runserver by default

CMD ["python", "manage.py", "runserver"]