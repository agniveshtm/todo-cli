# TODO-TUI Help

## Keybindings

| Key | Action |
|-----|--------|
| `^p` | Open the command palette |
| `q` | Quit the app (with confirmation) |
| `h` | Go to Welcome / Home screen |
| `s` | Open Settings screen |
| `?` | Show this help screen |
| `esc` | Go back / dismiss the current screen (e.g. help, settings, dialogs) |
| `Delete` | Delete the focused task (with confirmation) |
| `Ctrl+d` | Delete All — open multi-select modal for the focused task list (Available / Completed) |
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

### Deleting Tasks (Individual)
- Focus a task checkbox and press **Delete**
- A confirmation dialog appears : click **Delete** or press `Tab` then **Enter** to confirm
- The task is permanently removed from the database

### Deleting Tasks (Delete All)
- Focus the **Available** or **Completed** task list container (via `Tab` or click on the border) and press **Ctrl+d**
- A Delete All modal opens showing all tasks in that list with checkboxes
- Use the **Select All** checkbox to toggle all tasks, or check individual tasks
- Click **Delete All** to remove all selected tasks, or **Cancel** to abort

### Navigation
- Press `h` from any screen to return to the Welcome screen
- Press `s` to open the Settings screen
- Press `?` to open this help screen from any screen
- Press `q` to quit : a confirmation dialog ensures you don't exit accidentally

### Quit Confirmation
- Pressing `q` opens a dialog asking **"Are you sure you want to quit?"**
- click **Quit** to exit, or **Cancel** to return

## Settings

- Press `s` from any screen to open the Settings screen
- Toggle **Play Completion Sound** to enable/disable the sound effect when marking a task as done
- Press `esc` to return to the previous screen

## Screens Overview

| Screen | Description |
|--------|-------------|
| **Welcome** | Landing page with title and **Get Started** button |
| **Todo** | Main task management interface with two lists and an input box |
| **Settings** | Configure app preferences (e.g. toggle completion sound on/off) |
| **Help** | This screen — keybindings and usage instructions |
| **Quit** | Modal dialog confirming intent to exit the application |
| **Delete** | Modal dialog confirming intent to delete a task |
| **Delete All** | Modal dialog with task checkboxes, Select All, and Delete/Cancel buttons |

## Technical Details

- Built with [Textual](https://textual.textualize.io) : a Python TUI framework
- Data is persisted in a local **todo.db** database (`.todo-tui/todo.db`)
- Tasks are stored with creation and completion timestamps
- A success sound (`bell.wav`) plays when a task is marked complete (Windows only)
- Settings (such as the completion sound toggle) are persisted in a **SETTINGS** table inside `todo.db` and survive app restarts
