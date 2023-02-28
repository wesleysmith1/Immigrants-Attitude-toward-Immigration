from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'workpilot'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    problems_solved = models.IntegerField(initial=0)


# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


class Work(Page):
    timeout_seconds = 30

    @staticmethod
    def live_method(player, data):
        if player.field_maybe_none('problems_solved') == None:
            player.problems_solved = 1
        else:
            player.problems_solved = player.problems_solved + 1


page_sequence = [Work, Results]
