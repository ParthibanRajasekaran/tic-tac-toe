# Christmas Tic-Tac-Toe 🎄

A festive-themed Tic-Tac-Toe game built with Flask and styled for Christmas! 🎅🤶 The game includes an AI opponent (Grinch) with a robust Minimax algorithm to make competitive moves.

## Features

- Play as Santa against the Grinch (AI).
- Displays win, lose, or draw messages with Christmas-themed visuals.
- Fully responsive design with festive styles and animations.
- Reset functionality to restart the game.
- Automated testing to validate backend logic.

---

## 🛠️ Setup Instructions

Follow these steps to set up and run the project locally:

### 1. Clone the Repository
```bash
git clone <repository_url>
cd tic-tac-toe
```
### 2. Set Up a Virtual Environment
Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### 3. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

🚀 Running the Application
To start the Flask application, run:
```bash
python app.py
```
- The game will be hosted at http://127.0.0.1:5000.
- Open this URL in your browser to play the game.

🧪 Running the Tests
To validate the functionality of the backend, run the tests:
```bash
pytest test/test_app.py
```

### Testing Details:
- Tests include logic for valid/invalid moves, win/draw conditions, and board reset functionality.
- Each test is defined in test/test_app.py.

🎅 Credits
Developed with ❤️ for the holiday season. Enjoy!