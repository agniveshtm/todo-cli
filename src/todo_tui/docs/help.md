# TODO-TUI Help

## Keybindings

| Key | Action |
|-----|--------|
| `^p` | Open the command palette |
| `q` | Quit the app (with confirmation) |
| `h` | Go to Welcome / Home screen |
| `?` | Show this help screen |
| `esc` | Go back / dismiss the current screen (e.g. help, dialogs) |
| `Delete` | Delete the focused task (with confirmation) |
| `Tab` / `Shift+Tab` | Move focus between widgets |
| `Enter` | Add a task from the input box |
| `Space` | Check / Uncheck a task |

## How to Use

### Getting Started
- Launch the app and click **Get Started** on the Welcome screen (or press `h` from any screen)
- You'll see two panels: **Available** tasks on the left and **Completed** tasks on the right

### Adding Tasks
- Type a task description in the input box at the bottom
- Press **Enter** to add it
- The task appears in the **Available** list on the left

### Completing / Un-completing Tasks
- Navigate to a task checkbox using `Tab` or click on it
- Press **Space** to toggle its state
- Completed tasks move to the **Completed** panel on the right
- A success sound plays when marking a task as done
- Un-completing a task moves it back to the **Available** panel

### Deleting Tasks
- Focus a task checkbox and press **Delete**
- A confirmation dialog appears : click **Delete** or press `Tab` then **Enter** to confirm
- The task is permanently removed from the database

### Navigation
- Press `h` from any screen to return to the Welcome screen
- Press `q` to quit : a confirmation dialog ensures you don't exit accidentally

### Quit Confirmation
- Pressing `q` opens a dialog asking **"Are you sure you want to quit?"**
- click **Quit** to exit, or **Cancel** to return

## Screens Overview

| Screen | Description |
|--------|-------------|
| **Welcome** | Landing page with title and **Get Started** button |
| **Todo** | Main task management interface with two lists and an input box |
| **Quit** | Modal dialog confirming intent to exit the application |
| **Delete** | Modal dialog confirming intent to delete a task |

## Technical Details

- Built with [Textual](https://textual.textualize.io) : a Python TUI framework
- Data is persisted in a local **todo.db** database (`.todo-tui/todo.db`)
- Tasks are stored with creation and completion timestamps
- A success sound (`bell.wav`) plays when a task is marked complete (Windows only)