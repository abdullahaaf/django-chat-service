
# Example Chatting Service API using Django, implement with Rest API and PostgreSQL

This API assume that all users already registered and already have token attached to them



## API Documentation
For API Documentation, kindly refer to link below:
https://documenter.getpostman.com/view/2479819/2s935uFLPY
## Installation
### I gonna recommend to install it using Docker instead you will configure some stuff on your laptop
1. Clone this repository
2. Enter to project folder
3. Create .env file from .env.example with configuration:
```bash
DB_NAME=<your_db_name>
DB_HOST=<use db container name that defined in docker-compose.yml>
DB_PASS=<your_db_password>
DB_USER=<your_db_username> 
```
#### this for login to django admin site
```bash
SUUSERNAME=<your_superuser_username>
SUPASSWORD=<your_superuser_password>
SUEMAIL=<your_superuser_email>
FIRST_NAME=<your_superuser_first_name>
LAST_NAME=<your_superuser_last_name>
```
4. Run
```bash
  docker compose up -d 
```
5. Once container is up, open browser and go to ```yourip:8000```, eg: ```localhost:8000```
6. Login to Django admin site with configured credential on .env
7. Add user, and attach token to those user
    