import inspect
from enum import Enum    


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not(m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1]), p[0]) for p in props])
        return choices

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value
