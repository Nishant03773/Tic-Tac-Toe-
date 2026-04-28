<![CDATA[<div align="center">

# 🎮 Tic-Tac-Toe

### A modern, ML-powered Tic-Tac-Toe desktop app built with Python & CustomTkinter

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-latest-purple?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML%20Powered-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [How the AI Works](#-how-the-ai-works)
- [ML Model & Training](#-ml-model--training)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
  - [Retraining the Model](#retraining-the-model-optional)
- [Game Modes](#-game-modes)
- [Game Rules](#-game-rules)
- [Configuration & Theming](#-configuration--theming)
- [Dataset](#-dataset)
- [Contributing](#-contributing)

---

## 🌟 Overview

This is a **feature-rich, desktop Tic-Tac-Toe application** that goes beyond the classic game. It combines a polished, modern UI with a **Machine Learning AI opponent** trained on thousands of real game states — giving players a genuinely challenging experience.

The app supports two modes:
- **Solo (vs AI)** — Challenge an ML-powered opponent that reasons strategically.
- **1v1 (Player vs Player)** — Play locally against a friend on the same machine.

Both modes feature live scoreboards, a turn-status bar, light/dark theme toggling, and a smooth, responsive interface.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **ML-Powered AI** | AI opponent uses a trained Decision Tree model to predict the best move |
| 🛡️ **AI Defense Logic** | AI checks for immediate wins first, then blocks player threats before using ML |
| 👥 **Two Game Modes** | Solo (vs AI) and Player vs Player (local 2-player) |
| 📊 **Live Scoreboard** | Real-time win, loss, and draw counters for each session |
| 🌗 **Dark / Light Theme** | Toggle between dark and light modes — syncs across all screens |
| 🎨 **Modern UI** | Glassmorphic card-style design with rounded corners and smooth layouts |
| 📜 **About Screen** | In-app rules reference, AI explanation, and win-pattern guide |
| ♻️ **New Game Button** | Reset the board without losing the session score |
| 📱 **Fixed Window** | Clean 420×740 non-resizable window for a consistent experience |

---

## 📸 Screenshots

> The app includes three main screens:

| Home Screen | Solo (vs AI) | Player vs Player |
|---|---|---|
| Choose mode & enter player names | Play against the ML AI | Challenge a friend locally |

> The About screen provides in-app rules, AI logic explanation, and win-pattern reference.

---

## 📁 Project Structure

```
Tic-Tac-Toe/
│
├── main.py                  # App entry point — builds the home screen & routes to game modes
├── ai_game.py               # Solo mode: Player vs AI game logic and UI
├── pvp_game.py              # 1v1 mode: Player vs Player game logic and UI
├── about_screen.py          # About / rules screen with scrollable content
├── components.py            # Shared UI components (TopBar, ButtonManager)
├── config.py                # Centralised colour tokens and button themes
├── assest.py                # Icon/image path constants
├── game.py                  # Legacy standalone AI game (prototype/reference)
│
├── training.py              # ML model training script (run once to regenerate model)
├── model.pkl                # Pre-trained Decision Tree model (serialised with pickle)
├── tic_tac_toe.csv          # Dataset of board states used for training
│
├── logos/                   # PNG icon assets used throughout the UI
│   ├── tic-tac-toe.png      # App logo
│   ├── cross.png            # X symbol icon
│   ├── circle.png           # O symbol icon
│   ├── reset.png            # New Game / Reset icon
│   ├── left_arrow.png       # Back navigation icon
│   ├── power_button.png     # Close/quit icon
│   ├── dark_mode.png        # Theme toggle icon (dark)
│   └── light_mode.png       # Theme toggle icon (light)
│
├── tic_tac_toe_graphs/      # EDA visualisation outputs from training
│   ├── Class Distribution.png
│   ├── Board feature distribution.png
│   └── Feature Correlation Heatmap.png
│
└── requirements.txt         # Python package dependencies
```

---

## 🤖 How the AI Works

The AI opponent in **Solo mode** uses a **three-tier decision strategy**:

```
Step 1 — Win Check
  ↓  Can the AI win on this move?  →  YES → Play that cell
  ↓  NO

Step 2 — Block Check
  ↓  Is the player about to win?   →  YES → Block that cell
  ↓  NO

Step 3 — ML Model
     Evaluate all remaining empty cells using the trained Decision Tree.
     For each candidate cell, simulate placing "O" there, then ask the
     model: "What is the probability that this board state leads to an AI win?"
     → Pick the cell with the highest win probability.
```

This layered approach means the AI **never misses a direct win or an obvious block** while still falling back to learned strategy for all other moves.

---

## 🧠 ML Model & Training

### Dataset

- **File:** `tic_tac_toe.csv`
- **Source:** UCI Machine Learning Repository — Tic-Tac-Toe Endgame Dataset
- **Size:** 958 game-end board configurations
- **Features:** 9 columns (one per cell) — values are `x`, `o`, or `b` (blank)
- **Label (`Class`):** `positive` (X wins) or `negative` (X does not win)

### Preprocessing

| Step | Detail |
|---|---|
| Strip byte-string formatting | Raw values are byte strings (e.g. `b'x'`) — stripped to plain strings |
| Encode symbols to integers | `x → 1`, `o → -1`, `b → 0` |
| Encode class label | `positive → 1`, `negative → 0` |

### Model

| Property | Value |
|---|---|
| Algorithm | `DecisionTreeClassifier` (scikit-learn) |
| Train / Test Split | 80% / 20% (random_state=42) |
| Serialisation | `pickle` — saved as `model.pkl` along with feature names to avoid warnings |

> **Note:** Feature names are saved alongside the model (`pickle.dump((model, x.columns), ...)`) so that prediction DataFrames are correctly structured and scikit-learn doesn't raise `UserWarning` about missing feature names.

### EDA Graphs

Three exploratory visualisations are pre-generated in `tic_tac_toe_graphs/`:

- **Class Distribution** — counts of positive vs negative outcomes
- **Board Feature Distribution** — histograms of cell-value frequencies
- **Feature Correlation Heatmap** — Pearson correlation between all 9 cell positions and the target label

---

## 🛠 Tech Stack

| Library | Purpose |
|---|---|
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Modern themed Tkinter widgets (dark/light mode, rounded corners) |
| [Pillow (PIL)](https://pillow.readthedocs.io/) | Loading and resizing PNG icon assets |
| [scikit-learn](https://scikit-learn.org/) | Decision Tree classifier for AI move prediction |
| [pandas](https://pandas.pydata.org/) | CSV loading, preprocessing, and feature DataFrame construction |
| [numpy](https://numpy.org/) | Numerical operations (indirect dependency) |
| [matplotlib](https://matplotlib.org/) | EDA graph generation during training |
| [seaborn](https://seaborn.pydata.org/) | Styled statistical plots (heatmap, countplot) |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8 or higher** — [Download](https://www.python.org/downloads/)
- **pip** (comes bundled with Python)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Nishant03773/Tic-Tac-Toe-.git
   cd Tic-Tac-Toe-
   ```

2. **Create a virtual environment** *(recommended)*

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
python main.py
```

The application window (420×740) will launch immediately.

### Retraining the Model *(optional)*

If you want to retrain the ML model from scratch (e.g. after modifying the dataset or switching algorithms):

```bash
python training.py
```

This will:
1. Load and preprocess `tic_tac_toe.csv`
2. Train a new `DecisionTreeClassifier`
3. Print the model accuracy to the console
4. Overwrite `model.pkl` with the new model + feature names

---

## 🎮 Game Modes

### Solo Mode — You vs AI

- Enter your name on the home screen (optional; defaults to `"You"`)
- Click **Play vs AI** to start
- You play as **X**, the AI plays as **O**
- You always move first
- The AI responds after a 300 ms delay (simulates "thinking")
- The scoreboard tracks your wins, AI wins, and draws for the session

### Player vs Player Mode — 1v1

- Enter both player names on the home screen (optional; defaults to `Player 1` / `Player 2`)
- Click **Play 1v1** to start
- **Player 1 → X**, **Player 2 → O**
- Players alternate turns; the status bar always shows whose turn it is
- Scores are tracked across rounds until the app is closed

---

## 📜 Game Rules

1. **3×3 Grid** — The game is played on a 3×3 board with 9 cells.
2. **Two Symbols** — Player 1 is X · Player 2 (or AI) is O.
3. **Alternate Turns** — Players take turns placing their symbol in any empty cell.
4. **Win Condition** — Get 3 of your symbols in a row — horizontally, vertically, or diagonally.
5. **Draw** — If all 9 cells are filled with no winner, the game is a draw.
6. **No Takebacks** — A placed symbol cannot be moved or removed.
7. **New Game** — Use the **New Game** button to reset the board while keeping the session score.

### Win Patterns

| Type | Pattern |
|---|---|
| Rows | Top, middle, or bottom row |
| Columns | Left, centre, or right column |
| Diagonals | Top-left → Bottom-right **or** Top-right → Bottom-left |

---

## 🎨 Configuration & Theming

All colour tokens and button styles are defined centrally in **`config.py`**, making it easy to customise the entire app's palette in one place.

### Colour Tokens

| Token | Dark Mode | Light Mode | Purpose |
|---|---|---|---|
| `DARK_BG` / `LIGHT_BG` | `#0f172a` | `#f8fafc` | Main background |
| `DARK_SURFACE` / `LIGHT_SURFACE` | `#1e293b` | `#ffffff` | Card surfaces |
| `DARK_SURFACE2` / `LIGHT_SURFACE2` | `#273348` | `#f1f5f9` | Secondary surfaces / cell backgrounds |
| `DARK_BORDER` / `LIGHT_BORDER` | `#334155` | `#e2e8f0` | Card and input borders |
| `DARK_TEXT` / `LIGHT_TEXT` | `#f1f5f9` | `#0f172a` | Primary text |
| `DARK_SUBTEXT` / `LIGHT_SUBTEXT` | `#94a3b8` | `#64748b` | Secondary / muted text |
| `ACCENT` | `#6366f1` | `#6366f1` | Primary accent (indigo) |
| `ACCENT_HOVER` | `#4f46e5` | `#4f46e5` | Accent hover state |
| `WIN_COLOR` | `#22c55e` | `#22c55e` | Win result highlight (green) |
| `LOSE_COLOR` | `#ef4444` | `#ef4444` | Loss result highlight (red) |
| `DRAW_COLOR` | `#f59e0b` | `#f59e0b` | Draw result highlight (amber) |

### Theme Toggling

The **TopBar** component (top-left button on every screen) toggles between **Dark** and **Light** mode using `customtkinter.set_appearance_mode()`. The theme change propagates instantly across all active screens via the `ButtonManager` which also updates button border widths (borders are shown only in light mode for visual contrast).

---

## 📊 Dataset

| Property | Detail |
|---|---|
| Name | Tic-Tac-Toe Endgame Dataset |
| Source | [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/Tic-Tac-Toe+Endgame) |
| Records | 958 |
| Features | 9 (one per board cell: `top-left`, `top-middle`, ..., `bottom-right`) |
| Target | `Class` — `positive` (X wins) or `negative` (X does not win) |
| Format | CSV |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. **Fork** the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a **Pull Request**

### Ideas for Contribution

- [ ] Add difficulty levels for the AI (Easy / Medium / Hard)
- [ ] Persist scores across sessions using a local database or JSON file
- [ ] Add sound effects for moves, wins, and draws
- [ ] Implement an Undo last move feature
- [ ] Add animated winning-line highlight on the board
- [ ] Package the app as a standalone `.exe` using PyInstaller

---

<div align="center">

Made with ❤️ using Python & CustomTkinter

</div>
]]>
