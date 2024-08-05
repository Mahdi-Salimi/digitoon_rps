from typing import List


class User:
    def __init__(self, username: str):
        self.username = username
        self.score = 0
        self.history = []
        self.games_played = 0

    def add_result(self, result: str) -> None:
        self.history.append(result)
        self.games_played += 1
        if len(self.history) > 5:
            self.history.pop(0)

    def get_history(self) -> List[str]:
        return self.history

    def __str__(self) -> str:
        return f"{self.username} - {self.score} points - {self.games_played} games played"


class Leaderboard:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Leaderboard, cls).__new__(cls)
            cls._instance.users = {}
        return cls._instance

    def add_user(self, username: str) -> None:
        if username not in self.users:
            self.users[username] = User(username)

    def record_win(self, winner: str) -> None:
        if winner in self.users:
            self.users[winner].score += 1

    def get_leaderboard(self) -> List[str]:
        sorted_users = sorted(self.users.values(),
                              key=lambda x: x.score, reverse=True)
        return [str(user) for user in sorted_users]


def get_winner(move1: str, move2: str) -> str:
    '''
    returns winner of each round
    '''
    outcomes = {
        'rock': 'scissors',
        'scissors': 'paper',
        'paper': 'rock'
    }
    if move1 == move2:
        return 'draw'
    elif outcomes[move1] == move2:
        return 'player1'
    else:
        return 'player2'


def get_valid_move(player: User) -> str:
    valid_moves = ['rock', 'paper', 'scissors']
    while True:
        move = input(
            f"{player.username}, enter your move (rock/paper/scissors): ").lower()
        if move in valid_moves:
            return move
        else:
            print("Invalid move. Please enter 'rock', 'paper', or 'scissors'.")


def play_round(player1: User, player2: User) -> tuple[str, str, str]:
    move1 = get_valid_move(player1)
    move2 = get_valid_move(player2)
    return move1, move2, get_winner(move1, move2)


def play_game(player1: User, player2: User):
    print(f"{player1.username} vs {player2.username} - Play until one player wins by 3 rounds difference")
    player1_wins = 0
    player2_wins = 0

    while abs(player1_wins - player2_wins) < 3:
        move1, move2, winner = play_round(player1, player2)
        if winner == 'player1':
            player1_wins += 1
            print(f"{player1.username} wins this round!")
        elif winner == 'player2':
            player2_wins += 1
            print(f"{player2.username} wins this round!")
        else:
            print("This round is a draw!")

    if player1_wins > player2_wins:
        print(f"{player1.username} wins the game!")
        result = f"Win against {player2.username}: {player1_wins} rounds to {player2_wins}."
        player1.add_result(result)
        player2.add_result(
            f"Loss against {player1.username}: {player2_wins} rounds to {player1_wins}.")
        return player1.username
    else:
        print(f"{player2.username} wins the game!")
        result = f"Win against {player1.username}: {player2_wins} rounds to {player1_wins}."
        player2.add_result(result)
        player1.add_result(
            f"Loss against {player2.username}: {player1_wins} rounds to {player2_wins}.")
        return player2.username


def main() -> None:
    leaderboard = Leaderboard()

    while True:
        # print(leaderboard.users)
        action = input(
            "Choose an action: register, play, leaderboard, history, quit: ").lower()

        if action == 'register':
            username = input("Enter a username: ")
            leaderboard.add_user(username)
            print(f"User {username} registered successfully.")

        elif action == 'play':
            user1 = input("Enter the username of player 1: ")
            user2 = input("Enter the username of player 2: ")
            if user1 in leaderboard.users and user2 in leaderboard.users:
                while True:
                    winner = play_game(
                        leaderboard.users[user1], leaderboard.users[user2])
                    if winner:
                        leaderboard.record_win(winner)
                    play_again = input(
                        "Do you want to play again? (yes/no): ").lower()
                    if play_again != 'yes':
                        break
            else:
                print("Both users must be registered to play.")

        elif action == 'leaderboard':
            if leaderboard.users:
                print("\nLeaderboard:")
                for entry in leaderboard.get_leaderboard():
                    print(entry)
            else:
                print("No users registered yet.")

        elif action == 'history':
            username = input("Enter the username to view history: ")
            if username in leaderboard.users:
                print(f"\n{username}'s last 5 matches:")
                for result in leaderboard.users[username].get_history():
                    print(result)
            else:
                print("User not found or not registered.")

        elif action == 'quit':
            break

        else:
            print("Invalid action. Please try again.")


if __name__ == "__main__":
    main()

