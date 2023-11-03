class Question():
    def __init__(self,title0,answer0):
        self._title = title0
        self._answer = answer0

    @property
    def title(self):
        return self._title

    @property
    def answer(self):
        return self._answer
