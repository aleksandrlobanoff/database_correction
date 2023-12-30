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

        # Создание курсоров для работы с базами данных
        first_db_cursor = first_db_connection.cursor()
        second_db_cursor = second_db_connection.cursor()

        # Получение списка таблиц из первой базы данных
        first_db_cursor.execute("SHOW TABLES")
        first_tables = [row[0] for row in first_db_cursor.fetchall()]

        # Получение списка таблиц из второй базы данных
        second_db_cursor.execute("SHOW TABLES")
        second_tables = [row[0] for row in second_db_cursor.fetchall()]

        # Коррекция базы данных
        # Добавление новых таблиц
        new_tables = list(set(first_tables) - set(second_tables))
        for table in new_tables:
            # Получение структуры таблицы из первой базы данных
            first_db_cursor.execute(f"SHOW CREATE TABLE {table}")
            create_table_query = first_db_cursor.fetchone()[1]

            # Создание новой таблицы во второй базе данных по образцу из первой базы данных
            second_db_cursor.execute(create_table_query)

            second_db_connection.commit()

        # Закрытие соединений
        first_db_connection.close()
        second_db_connection.close()

