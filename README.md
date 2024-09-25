# Cropio-geo-tapi

## Project Description

This project uses Django, Django REST Framework, and PostGIS to manage and provide geometric data (fields) through a RESTful API. The API supports querying fields based on geographical parameters, enabling users to analyze agricultural land efficiently.

## Project Setup

### Requirements

- Python 3.9+
- Docker and Docker Compose
- PostgreSQL with PostGIS support

### Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/vadym-lev/Cropio-geo-tapi.git
   cd ...Cropio-geo-tapi/geoapi
   ```

2. **Add data file**: we can upload a data file `.geojsons` to `geoapi/data` to further upload this 
    data to the database using a script

3. **Docker Setup:**
   Ensure that Docker and Docker Compose are installed on your machine.

4. **Run Docker Compose:**
   ```bash
   docker-compose up --build
   ```

5. **Run Database Migrations:**
   After the services are up, run the following command to apply migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

6. **Create a Superuser:**
   To access the Django admin panel, create a superuser account:
   ```bash
   docker-compose exec web python manage.py load_geojson data/fr-subset.geojsons
   ```


## Model Description

### Field Model

The `Field` model represents an agricultural field with the following attributes:

- `id`: Auto-generated unique identifier for the field (Primary Key).
- `crop`: The type of crop grown in the field (CharField, max length 100).
- `productivity`: A float representing the productivity of the field.
- `area_ha`: A float representing the area of the field in hectares.
- `region`: The ISO code of the region where the field is located (CharField, max length 10).
- `history`: A JSON field to store historical data about the field (optional).
- `score`: A float representing the score or quality of the field (optional).
- `geometry`: A MultiPolygonField that stores the geometric shape of the field, allowing for complex geometric representations.

To improve query performance, an index for the `geometric` and `crop` field is added

## API Endpoints

### 1. Get Fields Nearby
**URL**: `/api/fields/nearby/`  
**Method**: `GET`  
**Description**: Retrieves fields within a specified radius of a geographic point.  
**Query Parameters**:
- `latitude` (float, required): Latitude of the point.
- `longitude` (float, required): Longitude of the point.
- `radius` (float, optional, default=1000): Search radius in meters.
- `crop` (string, optional): Filter by specific crop type.

**Example Request**:
```bash
curl -X GET 'http://localhost:8000/api/fields/nearby/?latitude=48.8566&longitude=2.3522&radius=5000&crop=wheat'
```

### 2. Get Fields Inside a Polygon
**URL**: `/api/fields/inside/`  
**Method**: `POST`  
**Description**: Retrieves fields that are located within a specified polygon.  
**Request Payload**:
```json
{
  "coordinates": [[[0.0, 48.8], [0.5, 48.8], [0.5, 48.9], [0.0, 48.9], [0.0, 48.8]]]
}
```

**Example Request**:
```bash
curl -X POST 'http://localhost:8000/api/fields/inside/' -H 'Content-Type: application/json' -d '{"coordinates": [[[2.0, 48.8], [2.5, 48.8], [2.5, 48.9], [2.0, 48.9], [2.0, 48.8]]]}'
```

### 3. Get Fields Intersecting with Geometry
**URL**: `/api/fields/intersect/`  
**Method**: `POST`  
**Description**: Retrieves fields that intersect with a specified geometric shape.  
**Request Payload**:
```json
{
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[0.0, 48.8], [0.5, 48.8], [0.5, 48.9], [0.0, 48.9], [0.0, 48.8]]]
  }
}
```

**Example Request**:
```bash
curl -X POST 'http://localhost:8000/api/fields/intersect/' -H 'Content-Type: application/json' -d '{"geometry": {"type": "Polygon", "coordinates": [[[2.0, 48.8], [2.5, 48.8], [2.5, 48.9], [2.0, 48.9], [2.0, 48.8]]]}}'
```

### 4. Get Statistics for a Region
**URL**: `/api/fields/region_stats/`  
**Method**: `GET`  
**Description**: Retrieves statistics about fields in a specified region.  
**Query Parameters**:
- `region` (string, required): The ISO code of the region to filter by.

**Example Request**:
```bash
curl -X GET 'http://localhost:8000/api/fields/region_stats/?region=FR'
```

