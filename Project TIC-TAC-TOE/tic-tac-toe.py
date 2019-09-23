BOARD = [str(i) for i in range(1, 10)]
WAYS_TO_WIN = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def display_board():
    '''Display board each time after player and computer place their turn'''

    print('\n{} | {} | {}'.format(BOARD[0], BOARD[1], BOARD[2]))
    print('-' * 10)
    print('{} | {} | {}'.format(BOARD[3], BOARD[4], BOARD[5]))
    print('-' * 10)
    print('{} | {} | {}\n'.format(BOARD[6], BOARD[7], BOARD[8]))


def get_turns():
    '''Determine if player want to go first'''

    get_turn = input('\nDo you want to go first? (Y/n): ').lower()

    if get_turn == 'y':
        print('\nTake the first move. GOOD LUCK !')
        player_turn, computer_turn = 'X', 'O'

    else:
        print('\nI am taking the first move. Play Safe !')
        player_turn, computer_turn = 'O', 'X'

    return player_turn, computer_turn


def human_turn():
    '''Make human's move'''

    get_turn = int(input('\nYOUR TURN: '))

    if BOARD[get_turn - 1] == 'X' or BOARD[get_turn - 1] == 'O':   # Checking if the place is already occupied by X or O
        print('\nFoolish man. That place is already occupied.')
        display_board()
        human_turn()

    BOARD[get_turn - 1] = player


def computer_turn():
    '''Make computer's move'''

    test_board = BOARD[:]   # Make a copy of the original board
    possible_moves = [BOARD.index(mov) for mov in BOARD if mov != 'X' and mov != 'O']   # Getting the possible moves computer can make

    for move in possible_moves:  # If computer can win the game, then take the move.
        test_board[move] = computer

        if declare_winner(test_board) == computer:
            return move

        test_board[move] = str(move + 1)  # Undoing, if cannot be won

    for move in possible_moves:  # If player can win the game, then block the move
        test_board[move] = player

        if declare_winner(test_board) == player:
            return move

        test_board[move] = str(move + 1)  # Undoing, if cannot be won

    return possible_moves[0]


def declare_winner(Board):
    '''Determine winner'''

    for winner in WAYS_TO_WIN:
        if Board[winner[0]] == Board[winner[1]] == Board[winner[2]]:
            return Board[winner[0]]

    if len([valid_place for valid_place in BOARD if valid_place != 'X' and valid_place != 'O']) == 0:   # When no one wins
        return 'TIE'

    return None


def TIC_TAC_TOE():
    '''Playing TIC-TAC-TOE ...'''

    global player, computer, BOARD

    player, computer = get_turns()

    if player == 'X':
        display_board()
        human_turn()
        BOARD[computer_turn()] = computer  # Computer is making its move
        display_board()

    else:
        BOARD[computer_turn()] = computer  # Computer is making its move
        display_board()

    while not declare_winner(BOARD):
        human_turn()

        if len([valid_place for valid_place in BOARD if valid_place != 'X' and valid_place != 'O']) != 0:
            move = computer_turn()
            BOARD[move] = computer  # Computer is making its move
            display_board()

    if declare_winner(BOARD) == player:
        print('\nNo no no ... You cannot beat me.\nI swear it won\'t happen again')

    elif declare_winner(BOARD) == computer:
        print('\nCOMPUTER are superior than HUMAN since once upon a time.')

    elif declare_winner(BOARD) == 'TIE':
        print('A very lucky fellow, got TIE with me.')

    choice = input('\nDo you want to play again (Y/n)?').lower()

    if choice == 'y':
        BOARD = [str(i) for i in range(1, 10)]
        TIC_TAC_TOE()


if __name__ == '__main__':
    TIC_TAC_TOE()
