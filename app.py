class App:
    def __init__(self):
        self._state = None
        self._authorization = False

    def get_state(self):
        return self._state

    def set_state(self, new_state):
        self._state = new_state

    def set_authorization(self, value):
        self._authorization = value
