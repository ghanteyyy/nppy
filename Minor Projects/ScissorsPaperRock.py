import random


class ScissorsPaperRock:
    '''
    Game Rules:
        If a rock and scissors are formed, the rock wins, because a rock can smash scissors.
        If scissors and paper are formed, the scissors win, because scissors can cut paper.
        If paper and a rock are formed, the paper wins, because a sheet of paper can cover a rock.
    '''

    def __init__(self):
        self.choices = ['s', 'p', 'r']
        self.user_winning = [('r', 's'), ('s', 'p'), ('p', 'r')]   # Combination for user to win

    def get_user_input(self):
        '''
        Ask user to input their choice
        '''

        user_input = input('\nscissors (s) or paper (p) or rock (r): ').lower()

        if user_input in self.choices:
            return user_input

        else:
            print('Invalid input')

    def get_bot_input(self):
        '''
        Bot Input: Random choice between "s p r"
        '''

        return random.choice(self.choices)

    def check_winner(self, user, bot):
        '''
        Check if user won or bot or the game is draw
        '''

        if user == bot:
            return 'Draw'

        for winner in self.user_winning:
            if winner == (user, bot):
                return 'You Won'

        return 'You Lost'

    def play(self):
        '''
        Playing the game
        '''

        print('\nQuit Command: Ctrl + C')

        try:
            while True:
                user_input = self.get_user_input()

                while not user_input:   # If user_input is none
                    user_input = self.get_user_input()

                bot_input = self.get_bot_input()

                print(f'You: {user_input}\nBot: {bot_input}')

                winner = self.check_winner(user_input, bot_input)
                print(winner)

        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    srp = ScissorsPaperRock()
    srp.play()
