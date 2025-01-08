# Event API

## Description
Simple all in one REST-Api that manages events (like conferences, meetups, etc.).

---

## Table of Contents

1. [Features](#features)  
2. [Technologies Used](#technologies-used)  
3. [Installation](#installation) 
5. [API Documentation](#api-documentation) 
7. [License](#license)  

---

## Features

- List the primary features of your project:
  - Account managment (login/registration)
  - Event managment (create/update/delete)
  - Event registration (join/leave/partisipants list)

---

## Technologies Used

- **Backend**: Django  
- **Frontend**: None  
- **Database**: SQLite  
- **Other Tools**: Docker, Swagger

---

## Installation

### Prerequisites

- Install [Python](https://www.python.org/) (version X.X.X or later).  
- Install [Docker](https://www.docker.com/) (optional).  
- Clone this repository:  
  ```bash
  git clone https://github.com/warwar-official/event_api.git
  ```

### Steps

1. Navigate to the project directory:  
   ```bash
   cd event_api
   ```

2. Create and activate a virtual environment:  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:  
   ```bash
   python3 manage.py makemigrations EventAPI
   python3 manage.py migrate
   ```

5. Start the development server:  
   ```bash
   python3 manage.py runserver
   ```

### Using Docker (Optional)

1. Build the Docker image:  
   ```bash
   docker pull ghcr.io/warwar-official/event_api/event_api:latest .
   ```

2. Run the container:  
   ```bash
   docker run -d -p 8000:8000 --name event_api13 ghcr.io/warwar-official/event_api/event_api:latest
   ```

---

## API Documentation

- API documentation is available at [[Swagger UI URL]](http://localhost:8000/swagger/).  

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
