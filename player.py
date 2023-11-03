class Player():
    def __init__(self,name0):
        self._name = name0
        self._is_playing = True
        self._points = 0

    @property
    def name(self):
        return self._name

class HumanPlayer(Player):
    def __init__(self,name0):
        super().__init__(name0)

class BotPlayer(Player):
    def __init__(self):
        super().__init__('Bot')
