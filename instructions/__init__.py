from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    SOLUTIONS = dict(
        q1=1,
        q2=3,
        q3=1,
        q4=1,
        q5=1,
        q6=1,
        q7=2,
    )

    INSTRUCTIONS_TEMPLATE = 'instructions/InstructionsSummary.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    q1 = models.IntegerField(
        label="Suppose you are a Type 1 Solver in Activity A. In that case, each Activity involves",
        choices=[
            [1, "Finding the product of two randomly chosen single-digit numbers (e.g.: 9*7)"],
            [2, "Finding the product of two randomly chosen double-digit numbers (e.g.: 27*49)"],
            [3, "Finding the product of two randomly chosen single-digit numbers three times (e.g.: 9*7, 2*5, and 4 * 3)"],
        ],
        widget=widgets.RadioSelect,
    )
    q2 = models.IntegerField(
        label="Suppose you are a Type 2 Solver in Activity A. In that case, each question involves",
        choices=[
            [1, 'Finding the product of two randomly chosen single-digit numbers (e.g.: 4*9)'],
            [2, 'Finding the product of two randomly chosen double-digit numbers (e.g.: 43*12)'],
            [3, 'Finding the product of two randomly chosen single-digit numbers three times (e.g.: 8*5, 7*8, and 9 * 6)'],
        ],
        widget=widgets.RadioSelect,

    )
    q3 = models.IntegerField(
        label="Suppose you are a Type 1 Solver in Activity B. In that case, each Activity involves",
        choices=[
            [1, 'Finding the product of two randomly chosen single-digit numbers (e.g.: 7*4)'],
            [2, 'Finding the product of two randomly chosen double-digit numbers (e.g.: 27*49)'],
            [3, 'Finding the product of two randomly chosen single-digit numbers three times (e.g.: 7*4, 5*7, and 8 * 6)'],
        ],
        widget=widgets.RadioSelect,
    )
    q4 = models.IntegerField(
        label="Suppose you are a Type 2 Solver in Activity B. In that case, each Activity involves",
        choices=[
            [1, 'Finding the product of two randomly chosen single-digit numbers (e.g.: 6*7)'],
            [2, 'Finding the product of two randomly chosen double-digit numbers (e.g.: 34*25)'],
            [3, 'Finding the product of two randomly chosen single-digit numbers three times (e.g.: 9*7, 6*3 and 4 * 3)'],
        ],
        widget=widgets.RadioSelect,
    )
    q5 = models.IntegerField(
        label="If you complete 10 Activity A correctly in a round, you earn",
        choices=[
            [1, '$15'],
            [2, '$7.5'],
            [3, '$30'],
        ],
        widget=widgets.RadioSelect,
    )
    q6 = models.IntegerField(
        label="If you complete 16 Activity B correctly in a round, you earn",
        choices=[
            [1, '$12'],
            [2, '$7.5'],
            [3, '$24'],
        ],
        widget=widgets.RadioSelect,
    )
    q7 = models.IntegerField(
        label="If you are an employer which of the following can decrease your potential earnings",
        choices=[
            [1, 'Assigning Type 1 employees to Activity A'],
            [2, 'Assigning Type 2 employees to Activity A'],
            [3, 'Assigning Type 2 employees to Activity B'],
        ],
        widget=widgets.RadioSelect,
    )


# PAGES
class Instructions(Page):
    pass


class Question1(Page):
    form_model = 'player'
    form_fields = ['q1']
    @staticmethod
    def error_message(player, values):
        if values['q1'] != C.SOLUTIONS['q1']:
            return "You answered incorrectly. Try again."


class Question2(Page):
    form_model = 'player'
    form_fields = ['q2']
    @staticmethod
    def error_message(player, values):
        if values['q2'] != C.SOLUTIONS['q2']:
            return "You answered incorrectly. Try again."


class Question3(Page):
    form_model = 'player'
    form_fields = ['q3']
    @staticmethod
    def error_message(player, values):
        if values['q3'] != C.SOLUTIONS['q3']:
            return "You answered incorrectly. Try again."

class Question4(Page):
    form_model = 'player'
    form_fields = ['q4']
    @staticmethod
    def error_message(player, values):
        if values['q4'] != C.SOLUTIONS['q4']:
            return "You answered incorrectly. Try again."

class Question5(Page):
    form_model = 'player'
    form_fields = ['q5']
    @staticmethod
    def error_message(player, values):
        if values['q5'] != C.SOLUTIONS['q5']:
            return "You answered incorrectly. Try again."
        

class Question6(Page):
    form_model = 'player'
    form_fields = ['q6']
    @staticmethod
    def error_message(player, values):
        if values['q6'] != C.SOLUTIONS['q6']:
            return "You answered incorrectly. Try again."


class Question7(Page):
    form_model = 'player'
    form_fields = ['q7']
    @staticmethod
    def error_message(player, values):
        if values['q7'] != C.SOLUTIONS['q7']:
            return "You answered incorrectly. Try again."


page_sequence = [Instructions, Question1, Question2, Question3, Question4, Question5, Question6, Question7,]
