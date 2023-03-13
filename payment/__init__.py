from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'payment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    full_name = models.StringField(label="Full name:")


# PAGES
class Payment(Page):
    @staticmethod
    def vars_for_template(player: Player):
        
        payment_round = player.session.vars['payment_round']
        round_results = player.participant.vars['round_results']

        for info in round_results:
            if info['round'] == payment_round:
                player.payoff = info['payoff']
                break

        return dict(
            payment_round = payment_round,
            round_results = round_results,
        )
    

class Thanks(Page):
    pass


class Final(Page):
    pass


page_sequence = [Payment, Thanks, Final]
