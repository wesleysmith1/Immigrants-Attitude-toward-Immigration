from otree.api import *
import random


doc = """
Your app description
"""



class C(BaseConstants):
    NAME_IN_URL = 'main'
    PLAYERS_PER_GROUP = 9
    NUM_ROUNDS = 13

    GREEN = 'Green'
    BLUE = 'Blue'

    EMPLOYER = 1
    GREEN_GROUP = [2,3,4,5]
    BLUE_GROUP = [6,7,8,9]

    JOB_A = 'A'
    JOB_B = 'B'

    JOB_A_PAY = .5
    JOB_B_PAY = .25

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    green_decision_maker = models.IntegerField()
    allow_type_two = models.BooleanField()


class Player(BasePlayer):
    # Type of player. Fixed for whole session
    type = models.IntegerField(choices=[1,2], initial=None)
    # Color of player. Fixed for whole session
    color = models.StringField(initial=None)
    # job assigned by employer
    job = models.StringField(choices=['A', 'B'], initial=None)
    # type 1 players vote whether to allow type 2 to compete
    allow_type_two = models.BooleanField(initial=None, label="Would you like Type 2 to participate?")
    selected = models.BooleanField(initial=True)
    # payment per math problem(s) completed
    marginal_pay = models.FloatField(initial=None)
    # total math plrobelms solved (1 or 2 depending on type and color)
    problems_solved = models.IntegerField(Initial=None)

    def set_color(self):
        if self.id_in_group == 1:
            self.color = None

        if self.id_in_group in C.GREEN_GROUP:
            self.color = C.GREEN
        elif self.id_in_group in C.BLUE_GROUP:
            self.color = C.BLUE

    def number_problems(self):
        if self.field_maybe_none('type') == 1 and self.job == C.JOB_A:
            return 2
        else:
            return 1

# FUNCTIONS
def creating_session(subsession: Subsession):

    if subsession.round_number == 1:
        subsession.session.vars['blue_type_2'] = random.choices(C.BLUE_GROUP, k=2)

    for player in subsession.get_players():
        player.set_color()

        if player.color == C.GREEN:
            player.type = 1
        elif player.color == C.BLUE:
            # = 2 if player.id_in_group in blue_type_1 else 1
            if player.id_in_group in subsession.session.vars['blue_type_2']:
                player.type = 2
            else:
                player.type = 1

        # employer is never selected
        if player.id_in_group == C.EMPLOYER:
            player.selected = False
            

# PAGES
class Vote(Page):
    form_model = 'player'
    form_fields = ['allow_type_two']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group in C.GREEN_GROUP

class Wait(WaitPage):
    
    @staticmethod
    def after_all_players_arrive(group: Group):
        # select player
        group.green_decision_maker = random.choice(C.GREEN_GROUP)
        group.allow_type_two = [p.allow_type_two for p in group.get_players() if p.id_in_group == group.green_decision_maker][0]

        if not group.allow_type_two:
            players = [ p for p in group.get_players() if p. field_maybe_none('type') == 2 ]
            for player in players:
                player.selected=False


class SelectWorkers(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        # list of selected ids
        selected_ids = [p.id_in_group for p in player.get_others_in_group() if p.selected]
        random.shuffle(selected_ids)
        return dict(selected_ids=selected_ids)
    
    @staticmethod
    def live_method(player, data):
        print('received a bid from', data)
        for player in player.get_others_in_group():
            if player.id_in_group in data['job_a']:
                player.job = C.JOB_A
                player.marginal_pay = C.JOB_A_PAY
            elif player.id_in_group in data['job_b']:
                player.job = C.JOB_B 
                player.marginal_pay = C.JOB_B_PAY


class Work(Page):
    timeout_seconds = 600 #30

    @staticmethod
    def live_method(player, data):
        if player.field_maybe_none('problems_solved') == None:
            player.problems_solved = 1
        else:
            player.problems_solved = player.problems_solved + 1

    @staticmethod
    def is_displayed(player: Player):
        return player.selected

    @staticmethod
    def vars_for_template(player: Player):
        number_problems = player.number_problems()
        return dict(number_problems=number_problems)
    

class ResultsWait(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        # calculate payoffs
        pass


class Results(Page):
    pass


# page_sequence = [SelectWorkers]
# page_sequence = [Work, Wait, SelectWorkers]
page_sequence = [Vote, Wait, SelectWorkers, Wait, Work, ResultsWait, Results]
