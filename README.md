# Real-time Airport Dashboard

This Django application provides a real-time dashboard to visualize the status of planes, runways, gates, and hangars at an airport. It simulates airplane movement and updates the dashboard dynamically using WebSockets.

## Key Features

*   **Real-time Updates:**  Utilizes WebSockets to provide live updates on the status of airport entities.
*   **Simulated Airplane Movement:**  A background task simulates the movement of airplanes between different states (flying, landing, at gate, in hangar, preparing for takeoff).
*   **Status Tracking:**  Displays the current status and location of each plane.
*   **Resource Management:**  Shows the availability of runways, gates, and hangars, and which plane (if any) is currently using them.
*   **Web-based Interface:**  Accessible through a standard web browser.

## Tech Stack

*   **Python:**  The primary programming language.
*   **Django:**  A high-level Python web framework.
*   **Django Channels:**  Extends Django to handle WebSockets.
*   **django-background-tasks:**  For managing background tasks like the airplane movement simulation.
*   **Redis:**  Used as a channel layer for Django Channels.
*   **HTML, CSS, JavaScript:**  For the front-end dashboard interface.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python:** (version 3.7 or higher recommended)
*   **pip:**  Python package installer
*   **Redis:**  A fast, in-memory data store (required for Django Channels)

## Installation

1. **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd myproject
    ```

2. **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    *   **On Windows:**

        ```bash
        venv\Scripts\activate
        ```

    *   **On macOS and Linux:**

        ```bash
        source venv/bin/activate
        ```

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You might need to create a `requirements.txt` file. A basic one would include `Django`, `channels`, `channels-redis`, and `django-background-tasks`. You can generate it using `pip freeze > requirements.txt` after installing the dependencies)*

5. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

## Running the Application

1. **Start the Redis server:**

    Make sure your Redis server is running. If you installed it locally, you can usually start it with a command like `redis-server`.


2. **Run the channel layer worker:**

    Open a new terminal in the project directory and activate the virtual environment. Then, run the Daphne server (or your preferred ASGI server):

    ```bash
    daphne myproject.asgi:application
    ```

3. **Run the background tasks processor:**

    Open another new terminal, activate the virtual environment, and start the background task processor:

    ```bash
    python manage.py process_tasks
    ```

## Accessing the Dashboard

Once the servers are running, you can access the dashboard in your web browser at:
http://127.0.0.1:8000/


You should see a page displaying tables with real-time information about the planes, runways, gates, and hangars.

## Further Development

Here are some potential areas for further development:

*   **More Realistic Simulation:** Enhance the simulation logic to include factors like flight schedules, delays, and different types of aircraft.
*   **User Interface Improvements:**  Improve the visual presentation of the dashboard with better styling, charts, or maps.
*   **Administrative Interface:** Create an admin interface to manage and add new planes, runways, gates, and hangars.
*   **Error Handling and Logging:** Implement better error handling and logging for the background tasks and WebSocket connections.
*   **Testing:** Add unit and integration tests to ensure the reliability of the application.
*   **Authentication:** Implement user authentication and authorization for accessing the dashboard.