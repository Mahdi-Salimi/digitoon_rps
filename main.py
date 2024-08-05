from models import User, Match
from orm.cnt import Connections

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
        player1.score += 1
        player1.games_played += 1
        player2.games_played += 1
        player1.save()
        player2.save()
        Match(player1_id=player1.id, player2_id=player2.id, player1_score=player1_wins, player2_score=player2_wins, result=result).save()
        return player1.username
    else:
        print(f"{player2.username} wins the game!")
        result = f"Win against {player1.username}: {player2_wins} rounds to {player1_wins}."
        player2.score += 1
        player2.games_played += 1
        player1.games_played += 1
        player1.save()
        player2.save()
        Match(player1_id=player1.id, player2_id=player2.id, player1_score=player1_wins, player2_score=player2_wins, result=result).save()
        return player2.username


def main() -> None:
    User.create_table()
    User.migrate()
    Match.create_table()
    Match.migrate()

    while True:
        action = input("Choose an action: register, play, leaderboard, history, quit: ").lower()

        if action == 'register':
            username = input("Enter a username: ")
            if User.get(username=username) is None:
                User(username=username).save()
                print(f"User {username} registered successfully.")
            else:
                print("Username already taken.")

        elif action == 'play':
            user1 = input("Enter the username of player 1: ")
            user2 = input("Enter the username of player 2: ")
            player1 = User.get(username=user1)
            player2 = User.get(username=user2)
            if player1 and player2:
                while True:
                    winner = play_game(player1, player2)
                    play_again = input("Do you want to play again? (yes/no): ").lower()
                    if play_again != 'yes':
                        break
            else:
                print("Both users must be registered to play.")

        elif action == 'leaderboard':
            users = User.all()
            if users:
                print("\nLeaderboard:")
                sorted_users = sorted(users, key=lambda x: x.score, reverse=True)
                for user in sorted_users:
                    print(user)
            else:
                print("No users registered yet.")

        elif action == 'history':
            username = input("Enter the username to view history: ")
            player = User.get(username=username)
            if player:
                matches = Match.findall()
                user_matches = [match for match in matches if match.player1_id == player.id or match.player2_id == player.id]
                print(f"\n{username}'s last 5 matches:")
                for match in user_matches[-5:]:
                    print(match)
            else:
                print("User not found or not registered.")

        elif action == 'quit':
            break

        else:
            print("Invalid action. Please try again.")


if __name__ == "__main__":
    main()

