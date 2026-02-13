# Specification: Dashboard and Visualization Enhancements

## 1. Requirement Overview
The user requested improved clarity for the data dashboard and a more informative 3D visualization scene for fracturing construction.

## 2. Dashboard Enhancements
- **Y-axis Units**: Every chart must display clear units (e.g., MPa, mm/d).
- **Threshold Visuals**: Horizontal lines representing "Warning" (Yellow) and "Critical" (Red) levels must be visible.
- **Dynamic Thresholds**: Values should be synced with the system alarm configuration.

## 3. 3D Visualization Upgrades
- **Geological Base Map**: Include 1:1 roadway mesh, coal seam volumes, and roof layer planes.
- **Borehole Representation**: Use 96mm diameter tube geometry for actual trajectories and dashed lines for designs.
- **Site Management**: Visual markers for drilling sites with parent-child relationship to boreholes.
- **Layer Control**: Ability to toggle visibility of different entities (Roadway, Coal, Design, Actual, etc.).
- **Interactive Inspection**: Detailed info panel on click showing borehole parameters.

## 4. Alarm System
- **Modal Popups**: Critical alarms must interrupt the UI with a modal and sound.
- **Simulated Data**: A background thread to generate periodic mock alarms for demonstration.
- **Connectivity**: Ensure CORS is enabled for smooth development.
