class Sentinel:
    def __repr__(self):
        return '<{c} {name}>'.format(
                c=self.__class__.__name__, name=self._name)

    def __init__(self, name):
        self._name = name
