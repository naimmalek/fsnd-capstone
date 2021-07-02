# Casting Agency

## Udacity's FSND Capstone Project
Heroku : https://fsnd-udacity-nm.herokuapp.com/

Development url: http://localhost:5000

## Getting Started

### Installing Dependencies

#### Python 3.8.5

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Enviornment

Recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
```bash
python3 -m venv venv_capstone
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

## Running the server

To run the server, execute:

```bash
export DATABASE_URL=<database-connection-url>
export AUTH0_DOMAIN='udacity-naim.us.auth0.com'
export ALGORITHMS=['RS256']
export API_AUDIENCE='capstone'
export CLIENT_ID='hLskWh4qMzQdDm8rDNCv3wFlpfFdIP3N'
export FLASK_APP=app.py
export FLASK_DEBUG=true
flask run --reload
or
./run.sh
```

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application. 

Using the `--reload` flag will detect file changes and restart the server automatically.

## API Reference

## Getting Started
Live API URL `https://fsnd-udacity-nm.herokuapp.com/`.

Authentication: This application requires authentication to perform various actions. All the endpoints require various permissions.

The application has three different types of roles:
- Casting Assistant
  - can only view the list of artist and movies and can view complete information for any actor or movie
  - has `get:actors, get:actors-detail, get:movies, get:movies-detail` permissions
- Casting Director
  - can perform all the actions that `Casting Assistant` can
  - can also create an actor and movie and also update respective information
  - has `patch:actors, patch:movies, post:actors, post:movies` permissions in addition to all the permissions that `Casting Assistant` role has
- Executive Producer
  - can perform all the actions that `Executive Producer` can
  - can also delete an actor or a movie
  - has `delete:actors, delete:movies` permissions in addition to all the permissions that `Executive Producer` role has


## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "error": 404,
    "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
    "success": false
}
```

The API will return the following errors based on how the request fails:
 - 400: Bad Request
 - 401: Unauthorized
 - 403: Forbidden
 - 404: Not Found
 - 405: Method Not Allowed
 - 422: Unprocessable Entity
 - 500: Internal Server Error

## Endpoints

#### GET /health
 - Health
   - You can check api health, public endpoint, requires no authentication
 
 - Sample Request
   - `https://fsnd-udacity-nm.herokuapp.com/health`

<details>
<summary>Sample Response</summary>

```
{
    "health": "Running!!"
}
```

</details>

#### GET /actors
 - Usage
   - gets the list of all the actors
   - requires `get:actors` permission
 
 - Sample Request
   - `https://fsnd-udacity-nm.herokuapp.com/actors`

<details>
<summary>Sample Response</summary>

```
{
    "actors": [
        {
            "date_of_birth": "Thu, 25 Mar 1993 18:30:00 GMT",
            "full_name": "Jack",
            "id": 6
        },
        {
            "date_of_birth": "Thu, 25 Mar 1993 18:30:00 GMT",
            "full_name": "Jack",
            "id": 7
        }
    ],
    "success": true
}
```

</details>

#### GET /actors/{actor_id}
 - Usage
   - gets actor info by id
   - requires `get:actors-detail` permission
 
 - Sample Request
   - `https://fsnd-udacity-nm.herokuapp.com/actors/6`

<details>
<summary>Sample Response</summary>

```
{
    "actor": {
        "date_of_birth": "Thu, 25 Mar 1993 18:30:00 GMT",
        "full_name": "Jack",
        "id": 6
    },
    "success": true
}
```
  
</details>

#### POST /actors
 - Usage
   - creates a new actor
   - requires `post:actors` permission
 
 - Request Body
   - full_name: string, optional
   - date_of_birth: date, required
 
 - Sample Request
   - `https://fsnd-udacity-nm.herokuapp.com/actors`
   - Request Body
     ```
        {
            "full_name": "John well",
            "date_of_birth": "May 15, 1950"
        }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "actors": [
                {
                    "date_of_birth": "Thu, 15 May 1950 18:30:00 GMT",
                    "full_name": "John well",
                    "id": 8
                },
                ....
            ],
    "success": true
}
```
  
</details>

#### PATCH /actors/{actor_id}
 - Usage
   - updates the info for an actor
   - requires `patch:actors` permission
 
 - Request Body (at least one of the following fields required)
   - full_name: string, optional
   - date_of_birth: date, optional
 
 - Sample Request
   - `https://fsnd-udacity-nm.herokuapp.com/actors/6`
   - Request Body
     ```
       {
            "full_name": "Rose roler"
       }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "actor_info": {
        "date_of_birth": "April 30, 1988",
        "full_name": "Rose roler"
    },
    "success": true
}
```
  
</details>

#### DELETE /actors/{actor_id}
 - Usage
   - deletes the actor
   - requires `delete:actors` permission
   - will also delete the mapping to the movie but will not delete the movie from the database
 
 - Sample Request
   - `https://fsnd-udacity-nm.herokuapp.com/actors/5`

<details>
<summary>Sample Response</summary>

```
{
    "success": true
}
```
  
</details>

#### GET /movies
 - Usage
   - gets the list of all the movies
   - requires `get:movies` permission
 
 - Sample Request
   - `https://fsnd-udacity-nm.herokuapp.com/movies`

<details>
<summary>Sample Response</summary>

```
{
    "movies": [
        {
            "cast": [],
            "duration": 20,
            "id": 5,
            "imdb_rating": 9.9,
            "release_year": 2005,
            "title": "Harry potim"
        },
        {
            "cast": [],
            "duration": 20,
            "id": 6,
            "imdb_rating": 9.9,
            "release_year": 2005,
            "title": "Harry potim"
        }
    ],
    "success": true
}
```

</details>

#### GET /movies/{movie_id}
 - Usage
   - gets the complete info for a movie
   - requires `get:movies-detail` permission
 
 - Sample Request
   - `https://fsnd-udacity-nm.herokuapp.com/movies/1`

<details>
<summary>Sample Response</summary>

```
{
    "movie": {
        "cast": [],
        "duration": 20,
        "id": 6,
        "imdb_rating": 9.9,
        "release_year": 2005,
        "title": "Harry potim"
    },
    "success": true
}
```
  
</details>

#### POST /movies
 - Usage
   - creates a new movie
   - requires `post:movies` permission
 
 - Request Body
   - title: string, required
   - duration: integer, required
   - release_year: integer, required
   - imdb_rating: float, required
   - cast: array of string, non-empty, optional
 
 - NOTE
   - In the `cast` field pass actors's name which exist in the database prior to making this request.
 
 - Sample Request
   - `https://fsnd-udacity-nm.herokuapp.com/actors`
   - Request Body
     ```
        {
            "title": "Mr. robot",
            "duration": 150,
            "release_year": 2019,
            "imdb_rating": 9.9,
            "cast": ["Rami Malek"]
        }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "movies": [
       {
            "cast": ["Rami Malek"],
            "duration": 150,
            "id": 50,
            "imdb_rating": 9.9,
            "release_year": 2019,
            "title": "Mr. robot"
        },
        ...
    ]
    "success": true
}
```
  
</details>

#### PATCH /movie/{movie_id}
 - Usage
   - updates the info for a movie
   - requires `patch:movies` permission
 
 - Request Body (at least one of the following fields required)
   - title: string, optional
   - duration: integer, optional
   - release_year: integer, optional
   - imdb_rating: float, optional
   - cast: array of string, non-empty, optional
 
 - NOTE
   - In the `cast` field pass actors's name which exist in the database prior to making this request.
 
 - Sample Request
   - `https://fsnd-udacity-nm.herokuapp.com/movies/50`
   - Request Body
     ```
       {
            "imdb_rating": 8.1
       }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "movies": [
       {
            "cast": ["Rami Malek"],
            "duration": 150,
            "id": 50,
            "imdb_rating": 9.9,
            "release_year": 2019,
            "title": "Mr. robot"
        },
        ...
    ]
    "success": true
}
```
  
</details>

#### DELETE /movies/{movie_id}
 - Usage
   - deletes the movie
   - requires `delete:movies` permission
   - will not affect the actors present in the database
 
 - Sample Request
   - `https://fsnd-udacity-nm.herokuapp.com/movies/5`

<details>
<summary>Sample Response</summary>

```
{
    "success": true
}
```
  
</details>

## Testing.
For testing follow below commands.:
```
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting_agency.sql
python test.py
```