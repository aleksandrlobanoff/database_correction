from config import first_db_config, second_db_config
from database_correction import DatabaseCorrection

if __name__ == "__main__":
    # Создание экземпляра класса DatabaseCorrection
    db_correction = DatabaseCorrection(first_db_config, second_db_config)
    db_correction.correct_second_db()
