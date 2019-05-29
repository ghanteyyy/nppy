import random


def game():
    ''' Let's play guessing game

        Guess a number between 1-100
        Your guess must not exceed 100 and must not be less than 1 '''

    try:

        name = input('Enter name:\t').title()
        print('Welcome {}\n'.format(name))

        found = False
        number_of_tries = 0        # Track number of tries
        random_number = random.randint(1, 100)   # You need to guess this random number

        while not found:
            user_guess = int(input('\nGuess a number:'))   # Asking user to enter their guess

            if user_guess == random_number:   # Checking if user guess and random number equal
                print("You have guessed in {} tries".format(number_of_tries))
                found = True

                choice = input('\nDo you want to continue (y/n)?:').lower()

                if choice == 'y':
                    game()    # Calling function to restart the game

                else:
                    print('\nGoodbye! Have a nice day ...')
                    break

            elif user_guess > random_number:   # Checking if user guess is greater than random number
                print('Guess Lower')

            elif user_guess < random_number:   # Checking if user guess is higher than random number
                print('Guess Higher')

            elif user_guess > 100:             # Checking if user guess is more than 100
                print('Guess Lower than 100')

            elif user_guess < 1:               # Checking if user guess is less than 1
                print('Guess Higher than 0')

            number_of_tries += 1

    except ValueError:
        print('Integer value was expected\n')
        game()

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    game()
