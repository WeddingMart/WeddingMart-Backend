# FastAPI Backend

This repository contains a FastAPI backend for WeddingMart. Follow the instructions below to set up and run the project.

## Quick Start
```sh
python3 -m venv env
source env/bin/activate
pip install fastapi uvicorn sqlalchemy asyncpg python-dotenv pyjwt bcrypt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.6 or later.
- You have installed `pip` (Python package installer).

## Installation

1. **Clone the repository**:

   ```sh
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Create a virtual environment**:

   ```sh
   python3 -m venv env
   ```

3. **Activate the virtual environment**:

   On macOS and Linux:
   ```sh
   source env/bin/activate
   ```
   On Windows:
   ```sh
   .\env\Scripts\activate
   ```

4. **Install the required packages**:

   ```sh
   pip3 install -r requirements.txt
   ```

## Running the Application

To run the FastAPI application, execute the following command (from the top level directory; not in /app):

```sh
python3 main.py
```

To run in production
```sh
uvicorn app.main:app --reload
```

The application will start and be accessible at `http://127.0.0.1:8000`.

## API Documentation

FastAPI automatically generates interactive API documentation at the following endpoints once the server is running:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## Project Structure

The project structure is as follows:

```
.
│
├── app/             
│   ├── __init__.py 
│   ├── main.py     
│   ├── database.py 
│   └── routers/    
│       ├── __init__.py
│       └── item_router.py
│
├── README.md       
└── requirements.txt

```

## Contributing

To contribute to this project, follow these steps:

1. Fork this repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Submit a pull request.

## License



## Contact

If you have any questions or feedback, feel free to contact the project maintainers.
