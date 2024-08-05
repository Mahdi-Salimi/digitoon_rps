# Rock Paper Scissors Game

This application allows users to play Rock Paper Scissors, register users, save game results to a database, and display a leaderboard.

## Getting Started

### Prerequisites

- Python 3.11.4
- SQLite3

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Mahdi-Salimi/digitoon_rps
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

### Database Setup

Before running the game, you need to set up the database and tables.

3. Run the migration script to create the database schema:

    ```bash
    python migrate.py
    ```

### Running the Game

After setting up the database, you can start the game:

```bash
python3 main.py
