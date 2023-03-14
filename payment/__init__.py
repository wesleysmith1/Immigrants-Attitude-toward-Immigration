from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'payment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # point to dollar conversion
    POINT_CONVERSION = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    full_name = models.StringField(label="Full name:")
    selected_payoff = models.FloatField(initial=0)
    participation = models.CurrencyField(initial=0)
    total_payoff = models.CurrencyField(initial=0)


# PAGES
class Payment(Page):
    @staticmethod
    def vars_for_template(player: Player):
        
        payment_round = player.session.vars['payment_round']
        round_results = player.participant.vars['round_results']

        for info in round_results:
            if info['round'] == payment_round:
                player.selected_payoff = info['payoff']
                break

        player.participation = player.session.config['participation_fee']

        player.total_payoff = player.participation + player.selected_payoff * C.POINT_CONVERSION

        return dict(
            payment_round = payment_round,
            round_results = round_results,
        )
    

class Thanks(Page):
    form_fields = ['full_name']
    form_model = 'player'


class Final(Page):
    pass


page_sequence = [Payment, Thanks, Final]
