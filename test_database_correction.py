import unittest
import mysql.connector

from database_correction import DatabaseCorrection


class DatabaseCorrectionTest(unittest.TestCase):

    def setUp(self):
        self.first_db_config = {
            'user': 'your_username',
            'password': 'your_password',
            'database': 'first_test_db_name'
        }
        self.second_db_config = {
            'user': 'your_username',
            'password': 'your_password',
            'database': 'first_test_db_name'
        }

        self.db_correction = DatabaseCorrection(self.first_db_config, self.second_db_config)

    @staticmethod
    def create_test_database(db_config, tables):
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Удаление таблиц, если они уже существуют
        for table_name, _ in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        # Создание таблиц
        for table_name, columns in tables:
            create_table_query = f"CREATE TABLE {table_name} ("
            for column_name, column_type in columns.items():
                create_table_query += f"{column_name} {column_type}, "

            create_table_query = create_table_query[:-2] + ");"
            cursor.execute(create_table_query)

        connection.commit()
        return connection

    def populate_test_table(self, connection, table_name, data):
        cursor = connection.cursor()
        insert_query = f"INSERT INTO {table_name} VALUES (%s, %s)"

        for row in data:
            cursor.execute(insert_query, row)

        connection.commit()

    def test_correct_second_db_add_new_tables(self):
        # Создаем тестовые базы данных с таблицами
        first_db_connection = self.create_test_database(self.first_db_config, [
            ("table1", {"id": "INT", "name": "VARCHAR(255)"}),
            ("table3", {"id": "INT", "age": "INT"})
        ])
        second_db_connection = self.create_test_database(self.second_db_config, [
            ("table1", {"id": "INT", "name": "VARCHAR(255)"})
        ])

        # Вызываем метод correct_second_db
        self.db_correction.correct_second_db()

        # Проверяем, что новая таблица была добавлена во вторую базу данных
        second_db_cursor = second_db_connection.cursor()
        second_db_cursor.execute("SHOW TABLES")
        second_tables = [row[0] for row in second_db_cursor.fetchall()]
        self.assertIn("table3", second_tables)

    def test_correct_second_db_correct_existing_tables(self):
        # Создаем тестовые базы данных с таблицами
        first_db_connection = self.create_test_database(self.first_db_config, [
            ("table1", {"id": "INT", "name": "VARCHAR(255)", "email": "VARCHAR(255)"})
        ])
        second_db_connection = self.create_test_database(self.second_db_config, [

            ("table1", {"id": "INT", "name": "VARCHAR(255)"})
        ])

        # Вызываем метод correct_second_db
        self.db_correction.correct_second_db()

        # Получаем структуру таблицы из второй базы данных
        second_db_cursor = second_db_connection.cursor()
        second_db_cursor.execute("DESCRIBE table1")
        second_columns = [row[0] for row in second_db_cursor.fetchall()]

        # Проверяем, что новое поле было добавлено во вторую базу данных
        self.assertIn("email", second_columns)


if __name__ == "__main__":
    unittest.main()
