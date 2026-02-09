# API Module

This module contains all the RESTful API endpoint definitions for the backend, organized by feature. It acts as the primary interface between the frontend application and the backend logic.

## Sub-modules (by feature)

-   **`integration.py`**: Endpoints for ingesting data from external systems (KJ653, SOS) and managing integration interfaces.
-   **`processing.py`**: Endpoints related to the status and control of backend data processing tasks.
-   **`visualization.py`**: Endpoints that provide structured data specifically for frontend visualizations (dashboards, 3D models, etc.).
-   **`evaluation.py`**: Endpoints for generating and retrieving fracturing effect evaluation reports.
-   **`auxiliary.py`**: Endpoints for auxiliary functions like querying alarm history and system logs.
