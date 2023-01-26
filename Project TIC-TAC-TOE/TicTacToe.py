import random


class setup:
    '''
    This class is responsible for:
        1. Showing board each time when user as well as bot enters their turn
        2. Asking user if he / she wants to go first
    '''

    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]

    def display_board(self, board):
        '''
        Show board with human and bot enters their turn
        '''

        for i in range(3):
            display = ' | '.join(board[i * 3:i * 3 + 3])

            if i in range(2):
                sep = f"\n{'- ' * 5}\n"

            else:
                sep = '\n'

            print(display, end=sep)

    def get_turn(self):
        '''
        Asking user if he/she wants to go first.

           If user wants to go first then:
                Human: X
                Bot: O

            else:
                Human: O
                Bot: X
        '''

        option = True if input('Do you want to go first (y/n)? ').lower() == 'y' else False

        if option:
            return ('X', 'O')

        return ('O', 'X')


class playing(setup):
    '''
    This class is responsible for:
        1. Getting empty places
        2. Asking user where he/she want to place their turn
            > Checks if user inputs their turn in empty places. If not then shows warning.

        3. Placing bot turn as per the user's turn
            > Get empty places
            > Checks if bot itself can win. If yes bot places its turn to that place and wins the game.
            > If bot cannot win the game then it checks whether user can win the game. If yes, then bot blocks the user next move so user cannot win the game

        4. Check where user or bot won or the game became TIE
    '''

    def __init__(self):
        super().__init__()
        self.human, self.bot = setup().get_turn()
        self.winner_combo = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 4, 8), (2, 4, 6), (0, 3, 6), (1, 4, 7), (2, 5, 8)]

    def get_possible_moves(self):
        return [self.board.index(place) for place in self.board if place in [str(i) for i in range(1, 10)]]

    def human_move(self):
        try:
            place = int(input('\nWhere do you want to place?')) - 1

            if place in self.get_possible_moves() and place > -1:
                self.board[place] = self.human

            else:
                print('Invalid Move')
                print(self.display_board(self.board))
                self.human_move()

        except:
            print('Invalid Move')
            print(self.display_board(self.board))
            self.human_move()

    def is_winner(self, board):
        if not self.get_possible_moves():
            return 'Tie'

        for winner in self.winner_combo:
            if board[winner[0]] == board[winner[1]] == board[winner[2]] == board[winner[0]]:
                return board[winner[0]]

    def bot_move(self):
        possible_moves = self.get_possible_moves()

        if possible_moves:
            for move in possible_moves:  # Checking if bot can win
                self.board[move] = self.bot

                if self.is_winner(self.board):
                    self.board[move] = self.bot
                    return

                self.board[move] = str(move + 1)

            for move in possible_moves:  # Checking if player can win
                self.board[move] = self.human

                if self.is_winner(self.board):
                    self.board[move] = self.bot
                    return

                self.board[move] = str(move + 1)

            self.board[random.choice(possible_moves)] = self.bot

    def main(self):
        print(f'\nYou: {self.human}\nBot: {self.bot}\n')

        if self.bot == 'X':
            self.bot_move()

        self.display_board(self.board)

        while not self.is_winner(self.board):
            self.human_move()
            self.bot_move()
            self.display_board(self.board)

        if self.is_winner(self.board) == self.human:
            print('\nHuman Won')

        elif self.is_winner(self.board) == self.bot:
            print('\nBot Won')

        else:
            print('\nHuman and Bot got tied')


if __name__ == '__main__':
    playing().main()
