import mysql.connector


class DatabaseCorrection:
    """
    Класс для корректировки базы данных

    Args:
        first_db_config (dict): Конфигурация первой базы данных
        second_db_config (dict): Конфигурация второй базы данных
    """

    def __init__(self, first_db_config, second_db_config):
        self.first_db_config = first_db_config
        self.second_db_config = second_db_config

    def create_connection(self, db_config):
        """
        Создает подключение к базе данных MySQL

        Args:
            db_config (dict): Конфигурация базы данных

        Returns:
            mysql.connector.connection.MySQLConnection or None: Объект соединения или None в случае ошибки
        """
        connection = None
        try:
            connection = mysql.connector.connect(**db_config)
            print("Подключение к базе данных MySQL прошло успешно")
        except mysql.connector.Error as e:
            print(f"Произошла ошибка при подключении к базе данных: {e}")

        return connection

    def correct_second_db(self):
        """
        Корректирует вторую базу данных
        """
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

        # Получение данных из таблиц второй базы данных перед коррекцией
        before_data = {}
        for table in second_tables:
            second_db_cursor.execute(f"SELECT * FROM {table}")
            rows = second_db_cursor.fetchall()
            before_data[table] = rows

        # Коррекция базы данных
        # Добавление новых таблиц
        new_tables = list(set(first_tables) - set(second_tables))
        for table in new_tables:
            # Получение структуры таблицы из первой базы данных
            first_db_cursor.execute(f"SHOW CREATE TABLE {table}")
            create_table_query = first_db_cursor.fetchone()[1]

            # Создание новой таблицы во второй базе данных по образцу из первой базы данных
            second_db_cursor.execute(create_table_query)

        # Коррекция полей существующих таблиц
        for table in first_tables:
            # Получение списка полей таблицы из первой базы данных
            first_db_cursor.execute(f"SHOW COLUMNS FROM {table}")
            first_columns = [row[0] for row in first_db_cursor.fetchall()]

            # Получение списка полей таблицы из второй базы данных
            second_db_cursor.execute(f"SHOW COLUMNS FROM {table}")
            second_columns = [row[0] for row in second_db_cursor.fetchall()]

            # Добавление новых полей в существующую таблицу во второй базе данных
            new_columns = list(set(first_columns) - set(second_columns))
            for column in new_columns:
                # Получение типа данных поля из первой базы данных
                first_db_cursor.execute(f"SHOW COLUMNS FROM {table} WHERE Field = '{column}'")
                column_info = first_db_cursor.fetchone()[1]

                # Добавление нового поля в существующую таблицу во второй базе данных
                alter_table_query = f"ALTER TABLE {table} ADD COLUMN {column} {column_info}"
                second_db_cursor.execute(alter_table_query)

        # Получение данных из таблиц базы данных test1 после коррекции
        after_data = {}
        for table in second_tables:
            second_db_cursor.execute(f"SELECT * FROM {table}")
            rows = second_db_cursor.fetchall()
            after_data[table] = rows

        # Проверка изменений в данных
        success = True
        for table in second_tables:
            if before_data[table] != after_data[table]:
                print(f"В таблице {table} данные были потеряны после корректировки")
                success = False

        # Сохранение изменений во второй базе данных или откат
        if success:
            second_db_connection.commit()  # Сохранение изменений
            print("Операция завершена успешно")
        else:
            second_db_connection.rollback()  # Окат транзакции
            print("Операция была отменена")

        # Закрытие соединений
        first_db_connection.close()
        second_db_connection.close()
