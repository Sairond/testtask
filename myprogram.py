class Connection(typing.ContextManager):
    def execute(self, query: str, params: tuple):
        print('Executed query', query, params)


class DbManager:
    def open_connection(self) -> 'Connection':
        return Connection()


class WorkingHourManager:
    @staticmethod
    def log(employee_id, time) -> None:
        db_manager = DbManager()
        connection = db_manager.open_connection()
        print('Logged working hours', time)
        connection.execute(
        'INSERT INTO working_log (employee_id, time) VALUES (?, ?)',
        (employee_id, time,)
        )

    @staticmethod
    def total(employee_id):
        db_manager = DbManager()
        connection = db_manager.open_connection()
        return connection.execute(
        'SELECT SUM(time_in_seconds) FROM working_log WHERE employee_id = ?',
        (employee_id,)
        ).fetchone()[0] * 60 * 60

    @staticmethod
    def salary(employee_id, date_from, date_to):
        db_manager = DbManager()
        connection = db_manager.open_connection()

        hour_rate = connection.execute(
        'SELECT hour_rate FROM employee_rates WHERE employee_id = ?',(employee_id,)).fetchone()[0])

        total_time = connection.execute(
        ('SELECT sum(time_in_seconds) FROM working_log '
        'WHERE employee_id = ? and time_in_seconds >= ? and time_in_seconds <= ?'), (employee_id, date_from, date_to,)
        ).fetchone()[0])

        return total_time * hour_rate