# Cyber Security Base project 1

## Installation and startup instructions
1. Install poetry: https://python-poetry.org/docs/
2. Clone the repository and install dependencies

   ```bash
   poetry install
   ```
3. Create a .env file and set the variables SECRET_KEY and ADMIN_PASSWORD. For example,
   ```bash
   SECRET_KEY=123
   ADMIN_PASSWORD=password
   ```
4. Initialize the database

    ```bash
    poetry run python3 init_db.py
    ```
5. Start the app

     ```bash
     poetry run flask run
     ```
     You can login as an admin using the username "admin" and the password you set in step 3.
