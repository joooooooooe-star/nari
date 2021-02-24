"""The ACT version"""

from nari.types.event.base import Event
from nari.types.event import Type

class Version(Event):
    """Represents the act version"""
    __id__ = Type.version.value
    def __repr__(self):
        return f'<Version {self.params[0]}>'
