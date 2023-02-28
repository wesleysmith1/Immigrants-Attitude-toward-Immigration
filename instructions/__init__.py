from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    q1 = models.IntegerField(
        label="Suppose you are a Type 1 solver in Activity A, each question involves",
        choices=[
            [1, 'Finding the product of two randomly chosen single-digit numbers (e.g.: 9*7)'],
            [2, 'Finding the product of two randomly chosen double-digit numbers (e.g.: 27*49)'],
            [3, 'Finding the product of two randomly chosen single-digit numbers <b>three times</b> (e.g.: 9*7, 2*5, and 4 * 3)'],
        ]
    )
    q2 = models.IntegerField(
        label="Suppose you are a Type 2 solver in Activity A. In that case, each question involves",
        choices=[
            [1, 'Finding the product of two randomly chosen single-digit numbers (e.g.: 4*9)'],
            [2, 'Finding the product of two randomly chosen double-digit numbers (e.g.: 43*12)'],
            [3, 'Finding the product of two randomly chosen single-digit numbers <bthree times (e.g.: 8*5, 7*8, and 9 * 6)'],
        ]
    )
    q3 = models.IntegerField(
        label="Suppose you are a Type 1 solver in Activity B. In that case, each question involves",
        choices=[
            [1, 'Finding the product of two randomly chosen single-digit numbers (e.g.: 7*4)'],
            [2, 'Finding the product of two randomly chosen double-digit numbers (e.g.: 27*49)'],
            [3, 'Finding the product of two randomly chosen single-digit numbers three times (e.g.: 7*4, 5*7, and 8 * 6)'],
        ]
    )
    q4 = models.IntegerField(
        label="Suppose you are a Type 2 solver in Activity B. In that case, each question involves",
        choices=[
            [1, 'Finding the product of two randomly chosen single-digit numbers (e.g.: 6*7)'],
            [2, 'Finding the product of two randomly chosen double-digit numbers (e.g.: 34*25)'],
            [3, 'Finding the product of two randomly chosen single-digit numbers three times (e.g.: 9*7, 6*3 and 4 * 3)'],
        ]
    )
    q5 = models.IntegerField(
        label="If you answer 30 Type A in a round, you earn",
        choices=[
            [1, '$15'],
            [2, '$7.5'],
            [3, '$30'],
        ]
    )
    q6 = models.IntegerField(
        label="If you answer 30 Type B in a round, you earn",
        choices=[
            [1, '$15'],
            [2, '$7.5'],
            [3, '$30'],
        ]
    )
    q7 = models.IntegerField(
        label="If you are an employer which of the following can decrease your potential earnings",
        choices=[
            [1, 'Assigning Type 1 employees to Activity A'],
            [2, 'Assigning Type 2 employees to Activity A'],
            [3, 'Assigning Type 2 employees to Activity B'],
        ]
    )


# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
