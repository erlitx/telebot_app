## Telebot App

This app starts Telegram Bot which comminicate with users and have access to ODOO via RPC requests

## Install
1. Create .env file with following credentials
-----------------

    TOKEN=
    ODOO_HOST = 
    ODOO_PORT = 
    ODOO_DB = 
    ODOO_USERNAME = 
    ODOO_PWD = 


 TOKEN - is for a Telegram Bot token

2. Build Docker image:

    ```
    docker build -t telebot-app .
    ```

3. Run Docker container:

    ```
    docker run -d --name telebot-app-service telebot-app
    ``````






