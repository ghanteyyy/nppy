import random


def play_game():
    '''
    Game Rule:

        If a rock and scissors are formed, the rock wins, because a rock can smash scissors.
        If scissors and paper are formed, the scissors win, because scissors can cut paper.
        If paper and a rock are formed, the paper wins, because a sheet of paper can cover a rock. '''

    print('scissors (s) or paper (p) or rock (r) \n')
    choices = ['s', 'p', 'r']

    try:
        while True:
            random_choice = random.choice(choices)
            user_input = str(input('Whats your choice?:'))

            if user_input == '' or user_input == ' ':
                print('Blank input... scissors (s) or paper (p) or rock (r) was expected ...\n')

            elif user_input == 's' and random_choice == 'p':
                print('You Own!\n')

            elif user_input == 'p' and random_choice == 'r':
                print('You Own!\n')

            elif user_input == 'r' and random_choice == 's':
                print('You Own!\n')

            elif user_input == 'p' and random_choice == 's':
                print('You Lost! \n')

            elif user_input == 'r' and random_choice == 'p':
                print('You Lost! \n')

            elif user_input == 's' and random_choice == 'r':
                print('You Lost! \n')

            elif user_input == random_choice:
                print('Draw \n')

            elif user_input != 's' or user_input != 'p' or user_input != 'r':
                print('scissors (s) or paper (p) or rock (r) was expected ...')

            print('Press "Ctrl + c" to exit .... \n')

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    play_game()
