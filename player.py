class Player():
    def __init__(self,name0):
        self._name = name0
        self._is_playing = True
        self._points = 0
        self._is_blocked = False

    @property
    def name(self):
        return self._name

    @property
    def points(self):
        return self._points

    @property
    def is_blocked(self):
        return self._is_blocked

    def change_blocked(self):
        self._is_blocked = not self.is_blocked

class HumanPlayer(Player):
    def __init__(self,name0):
        super().__init__(name0)

class BotPlayer(Player):
    def __init__(self):
        super().__init__('Bot')
