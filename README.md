
# Drama Box Api

This project is a Theatre Management API built with Django, Docker, and PostgreSQL.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Clone the Repository](#clone-the-repository)
4. [Setting Up Environment Variables](#setting-up-environment-variables)
5. [Starting the Application with Docker](#starting-the-application-with-docker)
6. [Database Initialization](#database-initialization)
7. [Accessing the API](#accessing-the-api)
8. [API Endpoints](#api-endpoints)
9. [Stopping the Application](#stopping-the-application)
10. [Contributing](#contributing)
11. [License](#license)

## Features

- User authentication with JWT
- CRUD operations for plays, actors, genres, performances, and reservations
- Filtering and pagination for API responses
- Email notifications for reservations

## Technologies

- Django
- Django REST Framework
- PostgreSQL
- Docker
- Redis (for task queue)
- Celery (for background tasks)


## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Docker
- Docker Compose

### Clone the Repository

```bash
git clone https://github.com/Narberal90/drama-box-api.git
cd drama-box-api
```

## Setting Up Environment Variables

A `.env.sample` file is included in the project. It shows the necessary environment variables. You should create a `.env` file based on this sample:

```plaintext
SECRET_KEY=your_secret_key
DJANGO_DEBUG=False
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_password_here
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
...
```

Make sure to update these values according to your environment. For example:

- `SECRET_KEY`: A secret key for your Django app.
- `DJANGO_DEBUG`: Set this to `False` for production.
- `EMAIL_HOST_USER`: Your Gmail address for sending emails.
- `EMAIL_HOST_PASSWORD`: Your Gmail app password.
- `POSTGRES_DB`: The name of the PostgreSQL database.
- `POSTGRES_USER`: Your PostgreSQL username.
- `POSTGRES_PASSWORD`: Your PostgreSQL password.
- `POSTGRES_HOST`: The hostname for the PostgreSQL service (`db` is used when running inside Docker).

### Starting the Application with Docker

To build and run the project using Docker, use the following command:

```bash
docker-compose up --build
```

This will:

- Build the Docker containers for the Django app and PostgreSQL.
- Start the containers.

### Database Initialization

The project includes a sample data file, `initial_data.json`, which can be loaded into the database after starting the application:

```bash
docker-compose exec web python manage.py loaddata initial_data.json
```

The initial superuser credentials are:

- Email: `admin@admin.com`
- Password: `1111`

If you need to create a new superuser, you can do so by running:

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to set up the new superuser.

### Accessing the API

The API will be accessible at `http://localhost:8000/api/`.

### API Endpoints

- `/api/theatre/actors/` - Manage actors
- `/api/theatre/genres/` - Manage genres
- `/api/theatre/plays/` - Manage plays
- `/api/theatre/theatrehalls/` - Manage theatre halls
- `/api/theatre/performances/` - Manage performances
- `/api/theatre/reservations/` - Manage reservations
- 
- `/api/user/register/` - Register a new user
- `/api/user/token/` - Obtain a token for authentication
- `/api/user/token/refresh/` - Refresh your authentication token
- `/api/user/token/verify/` - Verify your authentication token
- `/api/user/me/` - Manage your user profile

### Stopping the Application

To stop the application, press `Ctrl+C` in your terminal or run:

```bash
docker-compose down
```

## Contributing

Contributions are welcome! Please create an issue or submit a pull request for any improvements.

## License

This project is licensed under the MIT License.
