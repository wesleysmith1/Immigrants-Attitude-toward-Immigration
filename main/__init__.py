from otree.api import *
import random


doc = """
Your app description
"""



class C(BaseConstants):
    NAME_IN_URL = 'main'
    PLAYERS_PER_GROUP = 9
    NUM_ROUNDS = 2 #13

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
    allow_type_two = models.BooleanField(initial=None, label="Would you like to admit Type 2 Solvers to the Activity?")
    selected = models.BooleanField(initial=True)
    # payment per math problem(s) completed
    marginal_pay = models.FloatField(initial=None)
    # total math plrobelms solved (1 or 2 depending on type and color)
    problems_solved = models.IntegerField(initial=0)
    # using custom points field because otree points round
    payoff_points = models.FloatField(initial=0)

    def set_color(self):
        if self.id_in_group == 1:
            self.color = None

        if self.id_in_group in C.GREEN_GROUP:
            self.color = C.GREEN
        elif self.id_in_group in C.BLUE_GROUP:
            self.color = C.BLUE

    def number_problems(self):
        if self.field_maybe_none('type') == 1 and self.job == C.JOB_A:
            return 3
        else:
            return 1

# FUNCTIONS
def creating_session(subsession: Subsession):

    import random
    subsession.session.vars['payment_round'] = random.randint(1, C.NUM_ROUNDS-1)

    if subsession.round_number == 1:
        subsession.session.vars['blue_type_2'] = random.sample(C.BLUE_GROUP, 2)

    for player in subsession.get_players():
        player.participant.vars['round_results'] = []
        player.set_color()

        if player.field_maybe_none('color') == C.GREEN:
            player.type = 1
        elif player.field_maybe_none('color') == C.BLUE:

            if player.id_in_group in subsession.session.vars['blue_type_2']:
                player.type = 2
            else:
                player.type = 1

        # employer is never selected
        if player.id_in_group == C.EMPLOYER:
            player.selected = False
            

def adjusted_round(round_num):
    """adjust round number to not include tutorial. """
    return round_num-1


# PAGES
class Vote(Page):
    form_model = 'player'
    form_fields = ['allow_type_two']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group in C.GREEN_GROUP
    
    @staticmethod
    def vars_for_template(player: Player):

        return dict(
            round=adjusted_round(player.round_number),
        )
    
class MyWaitPage(WaitPage):
    template_name = 'main/MyWaitPage.html'

    @staticmethod
    def after_all_players_arrive(group: Group):
        # select player
        group.green_decision_maker = random.choice(C.GREEN_GROUP)
        group.allow_type_two = [p.allow_type_two for p in group.get_players() if p.id_in_group == group.green_decision_maker][0]

        if not group.allow_type_two:
            players = [ p for p in group.get_players() if p.field_maybe_none('type') == 2 ]
            for player in players:
                player.selected=False


class Wait(WaitPage):
    pass

class MyWaitPage3(WaitPage):
    template_name = 'main/MyWaitPage3.html'


class SelectWorkers(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        # list of selected ids
        selected_ids = [p.id_in_group for p in player.get_others_in_group() if p.selected]
        random.shuffle(selected_ids)
        return dict(
                selected_ids=selected_ids,
                round=adjusted_round(player.round_number),
            )
    
    @staticmethod
    def live_method(player, data):
        for player in player.get_others_in_group():
            if player.id_in_group in data['job_a']:
                player.job = C.JOB_A
                player.marginal_pay = C.JOB_A_PAY
            elif player.id_in_group in data['job_b']:
                player.job = C.JOB_B 
                player.marginal_pay = C.JOB_B_PAY


class Work(Page):
    timeout_seconds = 30

    @staticmethod
    def live_method(player, data):
        if player.field_maybe_none('problems_solved') == None:
            player.problems_solved = 1
        else:
            player.problems_solved = player.problems_solved + 1

        return {player.id_in_group: player.problems_solved}

    @staticmethod
    def is_displayed(player: Player):
        return player.selected

    @staticmethod
    def vars_for_template(player: Player):
        number_problems = player.number_problems()
        return dict(
                number_problems=number_problems,
                round=adjusted_round(player.round_number),
            )
    
class MyWaitPage2(WaitPage):
    template_name = 'main/MyWaitPage2.html'
    
    @staticmethod
    def after_all_players_arrive(group: Group):
        # calculate payoffs
        for player in group.get_players():
            if player.id_in_group == 1:

                total_a_problems = sum([p.problems_solved if p.field_maybe_none('job') == C.JOB_A else 0 for p in player.group.get_players()])
                total_b_problems = sum([p.problems_solved if p.field_maybe_none('job') == C.JOB_B else 0 for p in player.group.get_players()])

                player.payoff_points = (.8*total_a_problems + .5*total_b_problems) - .5*total_a_problems - .25*total_b_problems

            elif player.field_maybe_none('job') != None:
                player.payoff_points = player.problems_solved * player.marginal_pay


class AssignerResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

    @staticmethod
    def vars_for_template(player: Player):

        return dict(
            total_problems_solved = sum([p.problems_solved for p in player.group.get_players()]),
            total_a_problems = sum([p.problems_solved if p.field_maybe_none('job') == C.JOB_A else 0 for p in player.group.get_players()]),
            total_b_problems = sum([p.problems_solved if p.field_maybe_none('job') == C.JOB_B else 0 for p in player.group.get_players()]),
            total_a_solvers = sum([1 if p.field_maybe_none('job') == C.JOB_A else 0 for p in player.group.get_players()]),
            total_b_solvers = sum([1 if p.field_maybe_none('job') == C.JOB_B else 0 for p in player.group.get_players()]),
            round=adjusted_round(player.round_number),
        )

class SolverResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group != 1
    
    @staticmethod
    def vars_for_template(player: Player):

        return dict(
            total_problems_solved = sum([p.problems_solved for p in player.group.get_players()]),
            assigner_payoff = player.group.get_player_by_id(1).payoff_points,
            round=adjusted_round(player.round_number),
        )
    
class PayoffWait(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        # no payoffs for tutorial
        if group.round_number == 1:
            return
        # calculate payoffs
        for player in group.get_players():
            results = dict(
                round=player.round_number-1, # exclude the tutorial! 
                role='Assigner' if player.id_in_group == 1 else 'Solver',
                payoff=player.payoff_points,
                )
            player.participant.vars['round_results'].append(results)


page_sequence = [Vote, MyWaitPage, SelectWorkers, MyWaitPage3, Work, MyWaitPage2, AssignerResults, SolverResults, PayoffWait]
