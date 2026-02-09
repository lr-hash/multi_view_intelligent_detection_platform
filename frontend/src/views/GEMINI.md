# Views Module

This directory contains the main page-level components for the application. Each view typically corresponds to a specific route defined in the `router`.

## Responsibilities

-   Represent a full page or a major section of the user interface.
-   Fetch and manage the primary data required for that page by calling functions from the `services` module.
-   Compose and arrange smaller, reusable components from the `components` directory to build the page's layout.
-   Handle the overall state and logic for a specific user-facing feature.

## Current Views

-   **`HomeView.vue`**: The landing page of the application.
-   **`DashboardView.vue`**: Displays the real-time data dashboard with core metrics.
-   **`VisualizeView.vue`**: Hosts the 3D visualization scene for drilling design and trajectories.
