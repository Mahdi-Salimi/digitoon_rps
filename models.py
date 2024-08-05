from orm.models import Model, StringField, IntegerField

class User(Model):
    username = StringField()
    score = IntegerField()
    games_played = IntegerField()

    def __init__(self, username: str, score: int = 0, games_played: int = 0, id: int = None):
        self.id = id
        self.username = username
        self.score = score
        self.games_played = games_played
        
    def __str__(self) -> str:
        return f"{self.username} - {self.score} points - {self.games_played} games played"


class Match(Model):
    player1_id = IntegerField()
    player2_id = IntegerField()
    player1_score = IntegerField()
    player2_score = IntegerField()
    result = StringField()

    def __init__(self, player1_id: int, player2_id: int, player1_score: int, player2_score: int, result: str, id: int = None):
        self.id = id
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.player1_score = player1_score
        self.player2_score = player2_score
        self.result = result
        
        
