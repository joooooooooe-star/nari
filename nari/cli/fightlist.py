"""Helper classes for parsing out fights from event data"""

from typing import List

from nari.parser.analyser import Analyser, AnalyserTopic
# from nari.types.event.act import Type as EventType
from nari.types.event import Event
from nari.types.event.instance import InstanceInit, InstanceFade
# from nari.types.event.act.directorupdate import DirectorUpdate, DirectorUpdateCommand


class FightList(Analyser):
    """Takes a stream of (filtered) DirectorUpdate events and parses them into an array of fights"""
    # pylint: disable=attribute-defined-outside-init
    def init(self):
        column_headers: List[str] = ['date', 'instance id', 'encounters']
        self.matrix = [column_headers]
        self.fight_log: List[dict] = []
        self.current_fight: dict = {}
        self.add_event_hook(predicate=lambda e: isinstance(e, (InstanceInit, InstanceFade)), callback=self.fight_event)
        self.add_topic_hook(AnalyserTopic.stream_end, callback=self.complete)

    def fight_event(self, event: Event):
        """For each fight event, figure out stuff"""
        # safety check
        if not isinstance(event, (InstanceInit, InstanceFade)):
            return
        # command = event.director_command
        # if command == DirectorUpdateCommand.init:
        if isinstance(event, InstanceInit):
            if self.current_fight:
                self.fight_log.append(self.current_fight)
            self.current_fight = {
                'date': event.timestamp,
                'name': str(event.instance_id),
            }
        # elif command in (DirectorUpdateCommand.fadeout, DirectorUpdateCommand.clear): # naive, but functional?
            # self.current_fight['fights'] = self.current_fight.get('fights', 0) + 1

    def complete(self):
        """Wrap up any lingering issues"""
        if self.current_fight:
            self.fight_log.append(self.current_fight)

    def results(self):
        for fight in self.fight_log:
            num_fights = fight.get('fights', 0)
            amtstr = 'fight' if num_fights == 1 else 'fights'
            self.matrix.append([
                f'[{fight["date"]}',
                fight['name'],
                f'{num_fights} {amtstr}'
            ])
        return self.matrix
