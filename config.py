from dotenv import load_dotenv
import os

load_dotenv()

# Конфигурация подключения к первой базе данных (образец)
first_db_config = {
    'user': os.getenv('USER_FIRST_DB'),
    'password': os.getenv('PASSWORD_FIRST_DB'),
    'database': os.getenv('DATABASE_FIRST_DB')
}

# Конфигурация подключения ко второй базе данных (боевой-проект)
second_db_config = {
    'user': os.getenv('USER_SECOND_DB'),
    'password': os.getenv('PASSWORD_SECOND_DB'),
    'database': os.getenv('DATABASE_SECOND_DB')
}
