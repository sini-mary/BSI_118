from otree.api import *
from otree.api import models, BasePlayer, BaseGroup, BaseSubsession, Currency

doc = """
A Mini Ultimatum Game with 3 players. 
Player 1 endows Ksh 200, sends an amount to Player 2. 
Player 3, the Punisher, observes and decides to punish or not. 
Payouts depend on Player 3's choice. An exit survey follows.
"""



class Constants(BaseConstants):
    name_in_url = 'ultimatum_game'
    players_per_group = 3
    num_rounds = 1
    endowment = Currency(200)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    amount_sent = models.CurrencyField(
        initial=None,
        doc="Amount sent by Player 1 to Player 2."
    )
    punish_decision = models.BooleanField(
        initial=False,
        doc="Whether the group decides to punish Player 1 or not."
    )

    @staticmethod
    def calculate_payoffs(group):
        players = group.get_players()
        amount_sent = group.amount_sent

        for player in players:
            if group.punish_decision:
                # Player 3 chose to "Punish"
                player.payout_player1 = 0
                player.payout_player2 = 0
            else:
                # Player 3 chose to "Not Punish"
                player.payout_player1 = Constants.endowment - amount_sent
                player.payout_player2 = amount_sent
class Player(BasePlayer):
    amount_to_send = models.CurrencyField(
        min=0, max=Constants.endowment,
        label="Please choose the amount to send to Player 2:"
    )
    punish_decision = models.BooleanField(
        choices=[[True, 'Punish'], [False, 'Not Punish']],
        label="Do you want to punish Player 1?"
    )

    # Player 1's payout
    payout_player1 = models.CurrencyField()

    # Player 2's payout
    payout_player2 = models.CurrencyField()
    
    capital_city = models.StringField(
        choices=[
            ('nairobi', 'Nairobi'),
            ('mombasa', 'Mombasa'),
            ('kisumu', 'Kisumu')
        ],
        label="What is the capital city of Kenya?"
    )


class Intro(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Player1(Page):
    form_model = 'player'
    form_fields = ['amount_to_send']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.group.amount_sent = player.amount_to_send


class Player3(Page):
    form_model = 'player'
    form_fields = ['punish_decision']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.group.punish_decision = player.punish_decision

    @staticmethod
    def vars_for_template(player: Player):
        amount_sent = player.group.amount_sent
        player.group.calculate_payoffs(player.group)

        return {
            'amount_sent': amount_sent,
            'punish_decision': player.group.punish_decision,
            'player1_payout': player.payout_player1,
            'player2_payout': player.payout_player2,
        }


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        amount_sent = player.group.amount_sent
        punish_decision = player.group.punish_decision
        payout_player1 = player.payout_player1
        payout_player2 = player.payout_player2

        return {
            'amount_sent': amount_sent,
            'punish_decision': punish_decision,
            'player1_payout': payout_player1,
            'player2_payout': payout_player2,
        }
        
        
        
        
        
class Questions(Page):
    form_model = 'player'
    form_fields = ['capital_city']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'correct_math_answer': 29,
        }

    @staticmethod
    def error_message(player: Player, values):
        errors = {}

        # Validate the answer for the math_question
        if values['math_question'] != Questions.vars_for_template(player)['correct_math_answer']:
            errors['math_question'] = 'Incorrect answer. Please enter the correct sum of 14 and 15.'

        return errors

    def before_next_page(self):
        if self.round_number == 1:
            # Store the correct math answer for future reference
            self.player.correct_math_answer = self.vars_for_template(self.player)['correct_math_answer']


   

class Finish(Page):
    pass


page_sequence = [Intro, Player1, Player3, Results, Questions,Finish]


        





