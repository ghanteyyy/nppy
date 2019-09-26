class TIC_TAC_TOE:
    def __init__(self):
        self.__BOARD = [str(i + 1) for i in range(9)]
        self.__WINNER = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

    def get_first_move(self):
        '''Check if user wants to make their turn first'''

        go_first = True if input('\nDo you want to make your move first (y / N)?: ').lower() == 'y' else False

        if go_first:
            player_move, bot_move = 'X', 'O'

        else:
            player_move, bot_move = 'O', 'X'

        return go_first, player_move, bot_move

    def display_board(self):
        '''Display board after each time player and computer enter their respective turns'''

        print(f'\n{" " * 10} {self.__BOARD[0]} | {self.__BOARD[1]} | {self.__BOARD[2]}')
        print(f'{" " * 11}- - - - -')
        print(f'{" " * 10} {self.__BOARD[3]} | {self.__BOARD[4]} | {self.__BOARD[5]}')
        print(f'{" " * 11}- - - - -')
        print(f'{" " * 10} {self.__BOARD[6]} | {self.__BOARD[7]} | {self.__BOARD[8]}\n')

    def players_turn(self):
        '''Get player's move'''

        try:
            move = int(input(f'Your Turn [{human_turn}]: '))

            if self.__BOARD[move - 1] in [human_turn, bot_turn]:
                print('\nMove already Placed !\n')
                self.players_turn()

            else:
                self.__BOARD[move - 1] = human_turn

        except ValueError:
            print('Invalid Input ...\n')
            self.players_turn()

    def computers_turn(self):
        '''Get computer moves'''

        test_board = self.__BOARD[:]   # Making a copy of original board for getting best possible moves to be make by bot:
        get_possible_moves = [int(self.__BOARD.index(value)) for value in self.__BOARD if value.isdigit()]  # Getting all possible turns that are left.

        for move in get_possible_moves:  # Checking if computer can win
            test_board[move] = bot_turn

            if self.is_winner(test_board) == bot_turn:    # If computer can win then getting the same move
                return move

            test_board[move] = str(move)   # Undoing the move if computer cannot win

        for move in get_possible_moves:  # Checking if human can win in next move
            test_board[move] = human_turn

            if self.is_winner(test_board) == human_turn:   # Getting the move that can block next human's move and not letting them to win
                return move

            test_board[move] = str(move)

        return get_possible_moves[0]

    def is_winner(self, BOARD):
        '''Determining the winner of the game'''

        for winner in self.__WINNER:
            if BOARD[winner[0]] == BOARD[winner[1]] == BOARD[winner[2]]:
                return BOARD[winner[0]]

        if len([int(self.__BOARD.index(value)) for value in self.__BOARD if value.isdigit()]) == 0:
            return 'TIE'

        return None

    def play_again(self):
        '''Replaying the game'''

        choice = input('\nDo you want to play again (y / N)? :').lower()

        if choice == 'y':
            TIC_TAC_TOE().main()

    def main(self):
        global human_turn, bot_turn

        go_first, human_turn, bot_turn = self.get_first_move()

        if go_first is False:   # If player does not want to go first then compyter is going first
            self.__BOARD[self.computers_turn()] = bot_turn

        self.display_board()

        while not self.is_winner(self.__BOARD):  # Playing game till nobody wins or becomes TIE
            self.players_turn()

            if not self.is_winner(self.__BOARD):
                if len([value for value in self.__BOARD if value.isdigit()]) != 0:
                    self.__BOARD[self.computers_turn()] = bot_turn
                    self.display_board()

        if self.is_winner(self.__BOARD) == human_turn:  # Player won the game
            print('\nYou Won')

        elif self.is_winner(self.__BOARD) == bot_turn:  # Computer won the game
            print('\nYou lose. BOT WON')

        elif self.is_winner(self.__BOARD) == 'TIE':  # Nobody won i.e TIE
            print('\nIts TIE')

        self.play_again()  # Wanting player to replay the game


if __name__ == '__main__':
    TIC_TAC_TOE().main()
