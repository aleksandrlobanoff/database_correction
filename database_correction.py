import mysql.connector


class DatabaseCorrection:
    def __init__(self, first_db_config, second_db_config):
        self.first_db_config = first_db_config
        self.second_db_config = second_db_config

    def create_connection(self, db_config):
        connection = None
        try:
            connection = mysql.connector.connect(**db_config)
            print("Подключение к базе данных MySQL прошло успешно")
        except mysql.connector.Error as e:
            print(f"Произошла ошибка при подключении к базе данных: {e}")

        return connection

    def correct_second_db(self):
        # Подключение к первой и второй базам данных
        first_db_connection = self.create_connection(self.first_db_config)
        second_db_connection = self.create_connection(self.second_db_config)

