import sqlite3
import pytest

@pytest.fixture
def conn():
    conn = sqlite3.connect("db/todo.db")
    yield conn
    conn.close()

def test_insert_task(benchmark, conn):
    benchmark(conn.execute, "INSERT INTO TASKS (TASK) VALUES (?)", ("test task",))

def test_select_all(benchmark, conn):
    benchmark(conn.execute, "SELECT * FROM TASKS")

def test_select_available(benchmark, conn):
    benchmark(conn.execute, "SELECT ID, TASK FROM TASKS WHERE DONE = 0")

def test_update_done(benchmark, conn):
    benchmark(conn.execute, "UPDATE TASKS SET DONE=1 WHERE ID=1")

def test_delete_task(benchmark, conn):
    benchmark(conn.execute, "DELETE FROM TASKS WHERE ID=1")