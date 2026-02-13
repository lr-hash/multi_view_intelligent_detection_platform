# Implementation Plan: Dashboard and Visualization Enhancements

## Phase 1: Dashboard Clarity [DONE]
- [x] Install `chartjs-plugin-annotation`.
- [x] Update `DashboardView.vue` chart options.
- [x] Add Y-axis titles and threshold line configurations.

## Phase 2: System Connectivity & Alarm Simulation [DONE]
- [x] Install and configure `flask-cors`.
- [x] Implement `simulate_periodic_alarms` thread in `socket_events.py`.
- [x] Upgrade `AlarmNotification.vue` to support high-priority modal alerts and sound.

## Phase 3: High-Fidelity 3D Scene [DONE]
- [x] Create `backend/seed_visual_data.py` for rich demo data.
- [x] Extend `three-utils.js` with roadway, site marker, and coal seam functions.
- [x] Refactor `VisualizeView.vue` with layer management and enhanced rendering.
- [x] Implement click-to-inspect logic for borehole details.
