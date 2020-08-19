"""Stuff for preparecast"""
from datetime import datetime

from nari.types.event import Event
from nari.types.actor import Actor
from nari.types.ability import Ability


class PrepareCast(Event): # pylint: disable=too-few-public-methods
    """Event represents the preparation towards a cast"""
    def __init__(self, *,
                 timestamp: datetime,
                 source_actor: Actor,
                 ability: Ability,
                 target_actor: Actor):
        super().__init__(timestamp)
        self.source_actor = source_actor
        self.ability = ability
        self.target_actor = target_actor

    def __repr__(self):
        return '<PrepareCast>'
