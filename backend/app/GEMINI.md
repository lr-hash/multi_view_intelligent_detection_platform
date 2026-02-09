# Core Application Module

This is the core module of the Flask backend application.

## Sub-modules

-   **`models.py`**: Defines the database schema using SQLAlchemy ORM models.
-   **`routes.py`**: Contains all the API endpoint definitions and request handling logic.
-   **`services.py`**: Holds the business logic, such as data processing algorithms and evaluation calculations, keeping the routes clean.
-   **`__init__.py`**: The application factory, responsible for creating and configuring the Flask app instance, including initializing extensions and registering blueprints.
