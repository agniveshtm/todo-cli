# TODO-CLI

A feature-rich, keyboard-driven **Terminal User Interface (TUI)** todo application built with [Textual](https://textual.textualize.io) and [Python](https://python.org). Manage your tasks right from the terminal with a clean, dark-themed interface and full keyboard navigation.

![Welcome Screen](assets/Welcome%20Screen%20(Screenshot).png)

## Features

- **Add Tasks** – Type a task in the input box and press `Enter` to add it instantly.
- **Complete / Un-complete Tasks** – Toggle checkboxes with `Space`. Completed tasks move to the **Completed** panel and play a success sound (Windows).
- **Delete Tasks** – Focus a task and press `Delete`. A confirmation dialog prevents accidental deletion.
- **Task Persistence** – All tasks are stored in a local **SQLite** database (`db/todo.db`) with creation and completion timestamps.
- **Quit Confirmation** – Press `q` to see a confirmation dialog before exiting.
- **Help Screen** – Press `?` to view all keybindings and usage instructions.
- **Home Navigation** – Press `h` from any screen to return to the Welcome screen.
- **Keyboard-Driven UI** – Full keyboard navigation with `Tab`, `Space`, `Delete`, `Esc`, and more.
- **Dark Theme** – A consistent `textual-dark` theme throughout the app.
- **Sound Feedback** – A bell sound plays when a task is marked complete (Windows only).

## Screenshots

### Welcome Screen

The landing page with the app title and a **Get Started** button to enter the main interface.

![Welcome Screen](assets/Welcome%20Screen%20(Screenshot).png)

### Task Area (Main Screen)

The core task management view with two panels: **Available** tasks on the left and **Completed** tasks on the right. An input bar at the bottom lets you add new tasks.

![Todo Task Area](assets/Todo-TaskArea%20(Screenshot).png)

## Architecture

```
todo_cli/
├── assets/                  # Static assets (images, sounds)
│   ├── bell.wav             # Success sound played on task completion
│   ├── Welcome Screen (Screenshot).png
│   └── Todo-TaskArea (Screenshot).png
├── css/
│   └── todo.tcss            # Textual CSS stylesheet for the TUI
├── db/
│   └── todo.db              # SQLite database (auto-generated on first run)
├── docs/
│   └── help.md              # Help content displayed on the Help screen
├── src/
│   └── todo_cli/
│       ├── __init__.py      # Package initializer
│       └── main.py          # Application entry point and all screen definitions
├── pyproject.toml           # Project metadata and build configuration (uv)
├── uv.lock                  # Lock file for uv package manager
├── .gitignore
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
      ├── Press "h"  → Welcome Screen
      └── Press "q"  → Quit Confirmation Dialog
```

### Screens Overview

| Screen           | Description |
|------------------|-------------|
| **Welcome**      | Landing page with the app title and **Get Started** button |
| **Todo**         | Main task management interface with Available / Completed panels and an input bar |
| **Help**         | Displays all keybindings and usage instructions (markdown) |
| **Quit**         | Modal dialog asking "Are you sure you want to quit?" |
| **Delete**       | Modal dialog asking "Are you sure you want to delete this task?" |

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
- [uv](https://docs.astral.sh/uv/) package manager (recommended) OR `pip`

### Install via Wheel (Recommended)

1. Download `todo_cli-0.1.0-py3-none-any.whl` from [Releases](https://github.com/agniveshtm/TODO/releases)

2. Install it using `pip`:

   ```bash
   pip install todo_cli-0.1.0-py3-none-any.whl
   ```

3. Run the application:

   ```bash
   todo-cli
   ```

### Install from Source (Development)

Clone the repository and install with `uv`:

```bash
git clone https://github.com/agniveshtm/TODO.git
cd TODO/todo_cli
uv sync
uv run todo-cli
```

Or with `pip`:

```bash
git clone https://github.com/agniveshtm/TODO.git
cd TODO/todo_cli
pip install -e .
todo-cli
```

## Usage

1. Launch the app with `todo-cli`
2. Click **Get Started** (or press `Enter`) on the Welcome screen
3. Type a task in the input box and press `Enter` to add it
4. Use `Tab` to navigate between checkboxes and `Space` to toggle task completion
5. Press `Delete` to remove a task (confirmation required)
6. Press `?` anytime to view the help screen
7. Press `q` and confirm to exit the application

## Project Links

- **GitHub Repository**: [github.com/agniveshtm/TODO](https://github.com/agniveshtm/TODO)
- **Releases**: [github.com/agniveshtm/TODO/releases](https://github.com/agniveshtm/TODO/releases)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
