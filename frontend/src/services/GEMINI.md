# Services Module (Frontend)

This module centralizes all communication with the backend API. It abstracts the details of HTTP requests away from the Vue components, making the components cleaner and easier to manage.

## Responsibilities

-   Configure a base `axios` instance with the backend's base URL and default headers.
-   Export a clear, named function for each API endpoint required by the application.
-   Handle the specifics of `GET`, `POST`, etc., requests and their parameters.
-   Allow for easy modification and mocking of the API layer for testing or development.
