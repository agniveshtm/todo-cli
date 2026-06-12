# TODO-TUI

A feature-rich, keyboard-driven **Terminal User Interface (TUI)** todo application built with [Textual](https://textual.textualize.io) and [Python](https://python.org). Manage your tasks right from the terminal with a clean, dark-themed interface and full keyboard navigation.

![Welcome Screen](src/todo_tui/assets/Welcome%20Screen%20(Screenshot).png)

## Features

- **Add Tasks** – Type a task in the input box and press `Enter` to add it instantly.
- **Complete / Un-complete Tasks** – Toggle checkboxes with `Space`. Completed tasks move to the **Completed** panel and play a success sound (Windows).
- **Delete Tasks** – Focus a task and press `Delete`. A confirmation dialog prevents accidental deletion.
- **Task Persistence** – All tasks are stored in `~/.todo-tui/todo.db` with creation and completion timestamps.
- **Quit Confirmation** – Press `q` to see a confirmation dialog before exiting.
- **Help Screen** – Press `?` to view all keybindings and usage instructions.
- **Settings Screen** – Press `s` to open settings and toggle preferences (e.g. completion sound on/off). Settings persist across app restarts.
- **Home Navigation** – Press `h` from any screen to return to the Welcome screen.
- **Keyboard-Driven UI** – Full keyboard navigation with `Tab`, `Space`, `Delete`, `Esc`, and more.
- **Dark Theme** – A consistent `textual-dark` theme throughout the app.
- **Sound Feedback** – A bell sound plays when a task is marked complete (Windows only).

## Screenshots

### Welcome Screen

The landing page with the app title and a **Get Started** button to enter the main interface.

![Welcome Screen](src/todo_tui/assets/Welcome%20Screen%20(Screenshot).png)

### Task Area (Main Screen)

The core task management view with two panels: **Available** tasks on the left and **Completed** tasks on the right. An input bar at the bottom lets you add new tasks.

![Todo Task Area](src/todo_tui/assets/Todo-TaskArea%20(Screenshot).png)

### Settings Screen

Configure app preferences such as toggling the completion sound on/off. Settings persist across restarts.

![Settings Screen](src/todo_tui/assets/Settings%20Screen%20(Screenshot).png)

### Help Screen

Displays all keybindings and usage instructions for the app.

![Help Screen](src/todo_tui/assets/Help%20Screen%20(Screenshot).png)

## Architecture

```
todo-tui/
├── .github/
│   └── workflows/
│       └── release.yaml
├── src/
│   └── todo_tui/
│       ├── assets/                  # Static assets (images, sounds)
│       │   ├── bell.wav             # Success sound played on task completion
│       │   ├── Help Screen (Screenshot).png
│       │   ├── Settings Screen (Screenshot).png
│       │   ├── Todo-TaskArea (Screenshot).png
│       │   └── Welcome Screen (Screenshot).png
│       ├── css/
│       │   └── todo.tcss            # Textual CSS stylesheet for the TUI
│       ├── docs/
│       │   └── help.md              # Help content displayed on the Help screen
│       ├── __init__.py              # Package initializer
│       └── main.py                  # Application entry point and all screen definitions
├── tests/
│   └── test_benchmark.py
├── pyproject.toml                   # Project metadata and build configuration (uv)
├── uv.lock                          # Lock file for uv package manager
├── .gitignore
├── LICENSE
└── README.md
```

### Application Flow

```
Welcome Screen
      │
      ▼  (Click "Get Started" or press Enter)
  Todo Screen
      │
      ├── Add task (Input + Enter)
      ├── Toggle task (Checkbox + Space)
      ├── Delete task (Select + Delete key → confirmation dialog)
      │
      ├── Press "?" → Help Screen (Esc to go back)
      ├── Press "s" → Settings Screen (Esc to go back)
      ├── Press "h" → Welcome Screen
      └── Press "q" → Quit Confirmation Dialog
```

### Screens Overview

| Screen           | Description |
|------------------|-------------|
| **Welcome**      | Landing page with the app title and **Get Started** button |
| **Todo**         | Main task management interface with Available / Completed panels and an input bar |
| **Settings**     | Configure app preferences (e.g. toggle completion sound on/off) |
| **Help**         | Displays all keybindings and usage instructions (markdown) |
| **Quit**         | Modal dialog asking "Are you sure you want to quit?" |
| **Delete**       | Modal dialog asking "Are you sure you want to delete this task?" |

### Database Schema

The app uses SQLite with two tables:

**TASKS table** — stores all todo items:
```sql
CREATE TABLE TASKS(
    ID          INTEGER PRIMARY KEY,
    TASK        TEXT NOT NULL,
    DONE        INTEGER DEFAULT 0,
    CREATED_AT  TEXT DEFAULT(datetime('now','localtime')),
    COMPLETED_AT TEXT
);
```

**SETTINGS table** — stores user preferences (key-value pairs, e.g. `sound_enabled`):
```sql
CREATE TABLE SETTINGS(
    KEY   TEXT PRIMARY KEY,
    VALUE TEXT NOT NULL
);
```

### Tech Stack

- **[Python](https://python.org)** – Core programming language
- **[Textual](https://textual.textualize.io)** – Python framework for building Terminal User Interfaces
- **[SQLite](https://sqlite.org)** – Lightweight, embedded database for task persistence
- **[uv](https://github.com/astral-sh/uv)** – Fast Python package manager and project manager
- **[winsound](https://docs.python.org/3/library/winsound.html)** – Windows native sound API for task completion audio feedback

## Keybindings

| Key               | Action                                   |
|-------------------|------------------------------------------|
| `q`               | Quit the app (with confirmation)         |
| `h`               | Go to Welcome / Home screen              |
| `s`               | Open Settings screen                     |
| `?`               | Show help screen                         |
| `Esc`             | Go back / dismiss current screen         |
| `Delete`          | Delete the focused task (with confirmation) |
| `Tab` / `Shift+Tab` | Move focus between widgets            |
| `Enter`           | Add a task from the input box            |
| `Space`           | Check / Uncheck a task checkbox          |

## Benchmarks

Benchmarked using `pytest-benchmark` on Python 3.14.3 (Windows):

| Operation          | Mean       | OPS           |
|--------------------|------------|---------------|
| Update Task        | 1.32 μs    | 759,224 ops/s |
| Delete Task        | 1.51 μs    | 663,480 ops/s |
| Insert Task        | 1.78 μs    | 561,485 ops/s |
| Select All Tasks   | 17.56 μs   | 56,935 ops/s  |
| Select Available   | 21.20 μs   | 47,170 ops/s  |

> All database operations complete in **under 22 microseconds** on average.

## Installation

### Prerequisites

- Python 3.10 or higher

### Install via uv tool (Recommended)

The cleanest way — installs globally and registers the `todo-tui` command:

```bash
uv tool install git+https://github.com/agniveshtm/TODO-TUI.git
todo-tui
```

### Install via pipx

```bash
pipx install git+https://github.com/agniveshtm/TODO-TUI.git
todo-tui
```

### Install via pip

```bash
pip install git+https://github.com/agniveshtm/TODO-TUI.git
todo-tui
```

### Install via Wheel

1. Download `todo_tui-<version>-py3-none-any.whl` from [Releases](https://github.com/agniveshtm/TODO-TUI/releases)

2. Install it:

   ```bash
   cd Downloads
   uv tool install todo_tui-<version>-py3-none-any.whl
   ```

3. Run:

   ```bash
   todo-tui
   ```

### Install from Source (Development)

```bash
git clone https://github.com/agniveshtm/TODO-TUI.git
cd TODO-TUI
uv sync
uv run todo-tui
```

## Usage

1. Launch the app with `todo-tui`
2. Click **Get Started** (or press `Enter`) on the Welcome screen
3. Type a task in the input box and press `Enter` to add it
4. Use `Tab` to navigate between checkboxes and `Space` to toggle task completion
5. Press `Delete` to remove a task (confirmation required)
6. Press `s` to open Settings and toggle the completion sound on/off
7. Press `?` anytime to view the help screen
8. Press `q` and confirm to exit the application

## Project Links

- **GitHub Repository**: [github.com/agniveshtm/TODO-TUI](https://github.com/agniveshtm/TODO-TUI)
- **Releases**: [github.com/agniveshtm/TODO-TUI/releases](https://github.com/agniveshtm/TODO-TUI/releases)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.