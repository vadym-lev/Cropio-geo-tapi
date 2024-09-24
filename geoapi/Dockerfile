FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin

# Set up work directory
WORKDIR /app

# Install Python packages
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Run the Django app
CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8000", "geoapi.wsgi:application"]