import random


class Guessing_Game:
    def __init__(self, low=0, high=100):
        self.low = low
        self.high = high

    def is_guess_within_range(self, guess):
        '''Check if the guess is within the range of self.low and self.high'''

        if self.low <= guess <= self.high:
            return True

        return False

    def get_user_guess(self):
        '''Ask user to enter their guess until the valid guess is entered.'''

        try:
            guess = int(input(f'\nGuess a number between {self.low}-{self.high}: '))

            if not self.is_guess_within_range(guess):
                print(f'Your guess is not between {self.low}-{self.high}')

            else:
                return guess

        except ValueError:
            print('Your guess is not valid. Guess was expected in integer')

    def play_again(self):
        '''Ask user if they want to play the game again.'''

        check = input('\nDo you want to play again (y/n)?').lower()

        if check == 'y':
            return True

        return False

    def random_number(self):
        '''Returns random number which has to be guessed by the user'''

        return random.randint(self.low, self.high)

    def main(self):
        '''Playing the game'''

        count = 0
        is_guessed = False
        is_valid_guess = False
        to_guess = self.random_number()

        while not is_guessed:   # Until user guesses the random_number
            while not is_valid_guess:  # Until users enters valid guess
                user_guess = self.get_user_guess()

                if user_guess:
                    is_valid_guess = True

            if user_guess == to_guess:
                is_guessed = True
                print(f'You have guessed in {count} guesses')

                if self.play_again():
                    self.main()

            elif user_guess > to_guess:
                print('Your guess is high')

            elif user_guess < to_guess:
                print('Your guess is low')

            count += 1
            is_valid_guess = False


if __name__ == '__main__':
    guess = Guessing_Game()
    guess.main()
