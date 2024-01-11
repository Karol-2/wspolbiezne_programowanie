import uuid


class GameRoom:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.player1 = {}
        self.player2 = {}
        self.gameStarted = False

    def __str__(self):
        return f"Room ID: [ {self.id},\n Player 1: {self.player1},\n Player 2: {self.player2},\n Game Started: {self.gameStarted} \n ]"
