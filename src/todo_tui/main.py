import sqlite3, winsound
from importlib.resources import files
from pathlib import Path
from typing import cast
from textual.app import App
from textual.binding import Binding
from textual.containers import Center, Horizontal, Vertical, VerticalScroll, Grid
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Footer, Header, Input, Label, Markdown, Static, Switch

PACKAGE = files("todo_tui")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if (PROJECT_ROOT / ".git").exists():
    DB_PATH = PROJECT_ROOT / "db" / "todo.db"
else:
    DB_PATH = Path.home() / ".todo-tui" / "todo.db"

#=======================================================Todo-App==============================================================#
class TodoApp(App):
    TITLE = "TODO-TUI"
    CSS_PATH = str(PACKAGE / "css" / "todo.tcss")
    BINDINGS = [
        Binding(key="h", action="home", description="Home"),
        Binding(key="s", action="settings", description="Settings"),
        Binding(key="question_mark", action="help", description="Show help screen", key_display="?"),
        Binding(key="q", action="quit", description="Quit the App"),
    ]

    sound_enabled = reactive(True)

    def check_action(self, action, parameters):
        if action == "app.pop_screen":
            if isinstance(self.screen, (HelpScreen, SettingsScreen)):
                return None
        return True

    def on_mount(self):
        DB_PATH.parent.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.bell_path = str(PACKAGE / "assets" / "bell.wav")
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS TASKS(
                ID INTEGER PRIMARY KEY,
                TASK TEXT NOT NULL,
                DONE INTEGER DEFAULT 0,
                CREATED_AT TEXT DEFAULT(datetime('now','localtime')),
                COMPLETED_AT TEXT
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS SETTINGS(
                KEY TEXT PRIMARY KEY,
                VALUE TEXT NOT NULL
            )
            """
        )
        self.conn.commit()
        self.load_settings()
        self.theme = "textual-dark"
        self.push_screen(WelcomeScreen())

    def load_settings(self):
        row = self.conn.execute("SELECT VALUE FROM SETTINGS WHERE KEY = ?", ("sound_enabled",)).fetchone()
        if row is not None:
            self.sound_enabled = row[0] == "1"
        else:
            self.sound_enabled = True

    def save_sound_setting(self, value: bool):
        self.conn.execute(
            "INSERT OR REPLACE INTO SETTINGS (KEY, VALUE) VALUES (?, ?)",
            ("sound_enabled", "1" if value else "0"),
        )
        self.conn.commit()

    def action_home(self):
        self.push_screen(WelcomeScreen())

    def action_help(self):
        self.push_screen(HelpScreen())

    def action_settings(self):
        self.push_screen(SettingsScreen())

    def action_quit(self):
        if not isinstance(self.screen, QuitScreen):
            self.push_screen(QuitScreen())

    def play_done_sound(self):
        if not self.sound_enabled:
            return
        winsound.PlaySound(
            self.bell_path,
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT,
        )

#=====================================================Welcome-Screen==========================================================#
class WelcomeScreen(Screen):
    def on_mount(self):
        self.theme = "textual-dark"
        self.query_one("#welcome_card").border_title = "Welcome"

    def compose(self):
        yield Header(show_clock=True)
        yield Center(
            Vertical(
                Label("TODO-TUI", id="welcome_title"),
                Label("Your simple Todo List", id="welcome_sub"),
                Button("Get Started", id="start_btn", variant="primary"),
                id="welcome_card"
            )
        )
        yield Footer()

    def on_button_pressed(self, event):
        if event.button.id == "start_btn":
            self.app.push_screen(TodoScreen())

#========================================================Todo-Screen==========================================================#
class TodoScreen(Screen):
    BINDINGS = [Binding(key="delete", action="delete_task", description="Delete Task")]

    @property
    def todo_app(self):
        return cast(TodoApp, self.app)

    @property
    def conn(self):
        return self.todo_app.conn

    def on_mount(self):
        self.theme = "textual-dark"
        available_list = self.query_one("#available_tasks_list")
        completed_list = self.query_one("#completed_tasks_list")
        for row in self.conn.execute("SELECT ID, TASK FROM TASKS WHERE DONE = 0 ORDER BY CREATED_AT"):
            available_list.mount(Checkbox(row[1], value=False, id=f"task_{row[0]}"))
        for row in self.conn.execute("SELECT ID, TASK FROM TASKS WHERE DONE = 1 ORDER BY COMPLETED_AT"):
            completed_list.mount(Checkbox(row[1], value=True, id=f"task_{row[0]}"))
        self.update_titles()
        self.query_one("#available_tasks_list").focus()

    def compose(self):
        yield Header(show_clock=True)
        yield Vertical(
            Horizontal(
                VerticalScroll(id="available_tasks_list", classes="tasks-list"),
                VerticalScroll(id="completed_tasks_list", classes="tasks-list"),
                id="lists_container"
            ),
            Input(placeholder="Add a task", type="text"),
        )
        yield Footer()

    def update_titles(self):
        available_list = self.query_one("#available_tasks_list")
        completed_list = self.query_one("#completed_tasks_list")
        todo_count = self.conn.execute("SELECT COUNT(*) FROM TASKS WHERE DONE = 0").fetchone()[0]
        completed_count = self.conn.execute("SELECT COUNT(*) FROM TASKS WHERE DONE = 1").fetchone()[0]
        available_list.border_title = f"Available ({todo_count})"
        completed_list.border_title = f"Completed ({completed_count})"

    def on_input_submitted(self, event):
        task = event.value.strip()
        if task:
            cursor = self.conn.execute("INSERT INTO TASKS (TASK) VALUES (?)", (task,))
            self.conn.commit()
            task_id = cursor.lastrowid
            self.query_one("#available_tasks_list").mount(Checkbox(task, value=False, id=f"task_{task_id}"))
            self.update_titles()
            event.input.clear()

    def on_checkbox_changed(self, event):
        checkbox = event.checkbox
        task_label = str(checkbox.label)
        done = int(event.value)
        checkbox_id = checkbox.id
        db_id = checkbox_id.replace("task_", "")

        db_done_row = self.conn.execute("SELECT DONE FROM TASKS WHERE ID = ?", (db_id,)).fetchone()
        if db_done_row is not None and db_done_row[0] == done:
            return
        if done:
            self.conn.execute("UPDATE TASKS SET DONE=1, COMPLETED_AT=datetime('now','localtime') WHERE ID=?", (db_id,))
            self.conn.commit()
            checkbox.remove()
            new_cb = Checkbox(task_label, value=True, id=checkbox_id)
            self.query_one("#completed_tasks_list").mount(new_cb)
            new_cb.focus()
            self.todo_app.play_done_sound()
        else:
            self.conn.execute("UPDATE TASKS SET DONE=0, COMPLETED_AT=NULL WHERE ID=?", (db_id,))
            self.conn.commit()
            checkbox.remove()
            new_cb = Checkbox(task_label, value=False, id=checkbox_id)
            self.query_one("#available_tasks_list").mount(new_cb)
            new_cb.focus()
        self.update_titles()

    def action_delete_task(self):
        checkbox = self.focused if isinstance(self.focused, Checkbox) else None
        if checkbox is None or not checkbox.id:
            checkbox = None
            for list_id in ("#available_tasks_list", "#completed_tasks_list"):
                for child in self.query_one(list_id).query(Checkbox):
                    if child.is_mouse_over:
                        checkbox = child
                        break
                if checkbox:
                    break

        if checkbox and checkbox.id:
            task_id = checkbox.id.replace("task_", "")
            is_completed = checkbox.value
            target_list_id = "#completed_tasks_list" if is_completed else "#available_tasks_list"
            def handle_result(confirmed):
                if confirmed:
                    self.conn.execute("DELETE FROM TASKS WHERE ID=?", (task_id,))
                    self.conn.commit()
                    try:
                        cb = self.query_one(f"#task_{task_id}")
                        cb.remove()
                    except Exception:
                        pass
                    target_list = self.query_one(target_list_id)
                    remaining = list(target_list.query(Checkbox))
                    if remaining:
                        remaining[0].focus()
                    else:
                        target_list.focus()
                    self.update_titles()
            self.app.push_screen(DeleteScreen(), handle_result)

#========================================================Help-Screen==========================================================#
class HelpScreen(Screen):
    BINDINGS = [Binding(key="escape", action="app.pop_screen", description="Back")]

    def compose(self):
        yield Header(show_clock=True)
        yield Markdown((PACKAGE / "docs" / "help.md").read_text(encoding="utf-8"))
        yield Footer()

#========================================================Quit-Screen==========================================================#
class QuitScreen(Screen):
    def on_mount(self):
        self.theme = "textual-dark"
        self.query_one("#dialog").border_title = "Quit"

    def compose(self):
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog"
        )

    def on_button_pressed(self, event):
        if event.button.id == "quit":
            self.app.exit()
        elif event.button.id == "cancel":
            self.app.pop_screen()

#========================================================Delete-Screen========================================================#
class DeleteScreen(Screen):
    def on_mount(self):
        self.theme = "textual-dark"
        self.query_one("#dialog").border_title = "Delete Task"

    def compose(self):
        yield Grid(
            Label("Are you sure you want to delete this task?", id="question"),
            Button("Delete", variant="error", id="delete_btn"),
            Button("Cancel", variant="primary", id="cancel_btn"),
            id="dialog"
        )

    def on_button_pressed(self, event):
        if event.button.id == "delete_btn":
            self.dismiss(True)
        elif event.button.id == "cancel_btn":
            self.dismiss(False)

#=======================================================Settings-Screen=======================================================#
class SettingsScreen(Screen):
    BINDINGS = [Binding(key="escape", action="app.pop_screen", description="Back")]

    def on_mount(self):
        self.theme = "textual-dark"
        self.query_one("#settings").border_title = "Settings"
        self.query_one("#custom-design", Switch).value = cast(TodoApp, self.app).sound_enabled

    def compose(self):
        yield Header(show_clock=True)
        yield Vertical(
            Label("Settings", id="settings_title"),
            Horizontal(
                Label("Play Completion Sound", classes="label"),
                Switch(value=True, animate=True, id="custom-design"),
                classes="container",
            ),
            id="settings"
        )
        yield Footer()

    def on_switch_changed(self, event: Switch.Changed):
        app = cast(TodoApp, self.app)
        app.sound_enabled = event.value
        app.save_sound_setting(event.value)

def main():
    app = TodoApp()
    app.run()

if __name__ == "__main__":
    main()