class DbManager:
    def __init__(self, db_path=''):
        try:
            self.conn = my_example_db.connect(db_path)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def execute(self, query: str, params: tuple = ()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            print('Executed query', query, params)
            return cursor
        except Exception as e:
            print(f"Error executing query: {e}")
            return None


class WorkingHourManager:
    def __init__(self, db_manager: DbManager):
        self.db_manager = db_manager

    def log(self, employee_id, time) -> None:
        query = 'INSERT INTO working_log (employee_id, time) VALUES (?, ?)'
        with self.db_manager as connection:
            connection.execute(query, (employee_id, time))
            print('Logged working hours', time)

    def total(self, employee_id, date_from=None, date_to=None):
        query = 'SELECT SUM(time) FROM working_log WHERE employee_id = ?'
        params = [employee_id]

        if date_from and date_to:
            query += ' AND date >= ? AND date <= ?'
            params.extend([date_from, date_to])

        with self.db_manager as connection:
            result = connection.execute(query, tuple(params)).fetchone()[0]
            return result * 60 * 60 if result else 0

    def salary(self, employee_id, date_from=None, date_to=None):
        query = 'SELECT hour_rate FROM employee_rates WHERE employee_id = ?'

        with self.db_manager as connection:
            hour_rate = connection.execute(query, (employee_id,)).fetchone()[0]
            hour_rate = hour_rate if hour_rate else 0

            if hour_rate != 0:
                total_time = self.total(employee_id, date_from, date_to)
                return total_time * hour_rate
            else:
                return 0
