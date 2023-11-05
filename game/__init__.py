from otree.api import *
from otree.api import models, BasePlayer, BaseGroup, BaseSubsession, Currency

doc = """
This is a  game(mini ultimatum) with 3 players. 
...
Player 1 endows Ksh 200, sends an amount to Player 2. 
..
Player 3(the punisher), will decide to punish or not. 
.....
Payouts depend on Player 3's choice.
...
Followed by an exit survey.
"""



class Constants(BaseConstants):
    name_in_url = 'game'
    players_per_group = 3
    num_rounds = 1
    endowment = Currency(200)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    amount_sent = models.CurrencyField(
        initial=None,
        doc="Amount sent to Player 2."
    )
    punish_decision = models.BooleanField(
        initial=False,
        doc="Whether the group decides to punish Player 1 or not."
    )

    @staticmethod
    def payoff(group):
        players = group.get_players()
        amount_sent = group.amount_sent

        for player in players:
            if group.punish_decision:
                # Player 3 chose to punish
                player.payout_player1 = 0
                player.payout_player2 = 0
            else:
                # Player 3 chose not punish
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

#The intro page is displayed only on the first round
class Intro(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
#The Player1 page allows the player to enter the amount they 
# want to send to Player 2. 
# The entered amount is stored in the amount_sent field of the group.



class Player1(Page):
    form_model = 'player'
    form_fields = ['amount_to_send']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.group.amount_sent = player.amount_to_send
#The Player3 page allows Player 3 to decide whether to punish Player 1 or not. 
# The decision is stored in the punish_decision field of the group.
# The page also calculates the payouts for Player 1 and Player 2 based on the group's decision.



class Player3(Page):
    form_model = 'player'
    form_fields = ['punish_decision']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.group.punish_decision = player.punish_decision

    @staticmethod
    def vars_for_template(player: Player):
        amount_sent = player.group.amount_sent
        player.group.payoff(player.group)

        return {
            'punish_decision': player.group.punish_decision,
            'player1_payout': player.payout_player1,
            'player2_payout': player.payout_player2,
            'amount_sent': amount_sent,
              }

#The Calculation page displays the amount sent, 
# the punish decision, and the payouts for Player 1 and Player 2.


class Calculation(Page):
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
        
        
        
#The Questions page asks the player to select the capital city of Kenya from the given options.

  
        
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

    def before_next_page(self,timeout_happened):
        if self.round_number == 1:
            self.player.correct_math_answer = self.vars_for_template(self.player)['correct_math_answer']
        self.before_next_page()

#The Finish page signifies the end of the game.
# The page_sequence variable defines the order in which the pages will be displayed to the players.
 #I tried linking the next button but I got some errors

class Finish(Page):
    pass


page_sequence = [Intro, Player1, Player3, Calculation, Questions,Finish]


        





