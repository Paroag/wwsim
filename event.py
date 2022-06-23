class Event:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Event):
            return self.name == other.name
        return False

    def forward_time(self, delta_t):
        pass
