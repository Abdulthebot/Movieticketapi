# Movie Ticket Booking API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.14+-red.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced, production-grade REST API for a movie ticket booking system. [cite_start]Built with Python, Django, and Django REST Framework, this project demonstrates a robust architecture focusing on security, scalability, and data integrity under concurrent load[cite: 3, 5].

## Key Features & Concepts Implemented

This implementation goes beyond basic CRUD operations to incorporate features essential for real-world, high-traffic applications.

-   [cite_start]**Modular Architecture**: The system is organized into distinct Django applications (`users`, `movies`, `bookings`, `core`) for a clean separation of concerns, enhancing maintainability and scalability[cite: 6, 7].
-   [cite_start]**JWT Authentication**: Secure, stateless user authentication using JSON Web Tokens (JWT) via the `djangorestframework-simplejwt` library[cite: 103].
-   [cite_start]**Concurrency-Safe Bookings**: Prevents race conditions (double-booking the same seat) by using atomic database transactions (`@transaction.atomic`) with pessimistic locking (`select_for_update`)[cite: 166, 170]. This guarantees data integrity.
-   [cite_start]**Object-Level Permissions**: A custom permission class (`IsBookingOwner`) ensures users can only view or cancel their own bookings, preventing unauthorized data access[cite: 201, 205].
-   [cite_start]**Advanced Server-Side Validation**: Multi-level validation in serializers prevents overbooking, double-booking, and invalid data submissions before hitting the database[cite: 220, 224].
-   [cite_start]**Interactive API Documentation**: Auto-generated, interactive API documentation with Swagger (OpenAPI) via `drf-yasg`, including full support for JWT authentication in the UI[cite: 262, 265].
-   [cite_start]**Comprehensive Unit Testing**: A full test suite using `APITestCase` verifies all critical business logic, including successful bookings, failure scenarios (e.g., booking a taken seat), and security permission checks[cite: 287, 293].
-   [cite_start]**Custom User Model**: Implemented from the start to allow for future flexibility and enhancements without complex migrations[cite: 36, 38].

## Tech Stack

-   [cite_start]**Backend**: Python, Django, Django REST Framework [cite: 433]
-   [cite_start]**Database**: SQLite (for development), PostgreSQL-ready [cite: 437]
-   [cite_start]**Authentication**: JSON Web Tokens (`djangorestframework-simplejwt`) [cite: 434]
-   [cite_start]**API Documentation**: Swagger/OpenAPI (`drf-yasg`) [cite: 435]
-   **Testing**: Django's built-in test framework (`APITestCase`)

## Setup and Installation

Follow these steps to get the project running locally.

**1. Clone the Repository**
```bash
git clone [https://github.com/your-username/movie-booking-api.git](https://github.com/your-username/movie-booking-api.git)
cd movie-booking-api
```

**2. Create and Activate a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Environment Variables**

Create a `.env` file in the project root by copying the example file:
```bash
cp .env.example .env
```
Now, open the `.env` file and set your `SECRET_KEY`.

**5. Run Database Migrations**
```bash
python manage.py migrate
```

**6. (Optional) Create a Superuser**
```bash
python manage.py createsuperuser
```

**7. Start the Development Server**
```bash
python manage.py runserver
```
The API will now be available at `http://127.0.0.1:8000/`.

## API Documentation & Usage

Interactive API documentation is available via Swagger UI. Once the server is running, navigate to:

-   [cite_start]**`http://127.0.0.1:8000/swagger/`** [cite: 504]

[cite_start]To test protected endpoints, click the **"Authorize"** button and enter your JWT in the format: `Bearer <your_jwt_token>`[cite: 505].

### API Workflow Example:

**1. Register a new user:**
```bash
curl -X POST [http://127.0.0.1:8000/api/users/signup/](http://127.0.0.1:8000/api/users/signup/) \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "email": "test@example.com", "password": "SecurePassword123", "password2": "SecurePassword123"}'
```

**2. Log in to get JWT tokens:**
```bash
curl -X POST [http://127.0.0.1:8000/api/users/login/](http://127.0.0.1:8000/api/users/login/) \
-H "Content-Type: application/json" \
-d '{"email": "test@example.com", "password": "SecurePassword123"}'
```
> **Response:**
> ```json
> {
>   "refresh": "...",
>   "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
> }
> ```

**3. Book a seat (requires authentication):**
> **Note:** Replace `<show_id>` and `<your_jwt_token>` accordingly.
```bash
curl -X POST [http://127.0.0.1:8000/api/shows/](http://127.0.0.1:8000/api/shows/)<show_id>/book/ \
-H "Authorization: Bearer <your_jwt_token>" \
-H "Content-Type: application/json" \
-d '{"seat_number": 5}'
```

## Running Tests

The test suite covers the core business logic. To run the tests:
```bash
python manage.py test apps.bookings
```

## Deployment Notes

For a production environment, ensure you:
-   Set `DEBUG = False` in `settings.py`.
-   Configure `ALLOWED_HOSTS` with your domain.
-   Use a production-grade database like PostgreSQL.
-   Serve the application using a WSGI server like Gunicorn or uWSGI.