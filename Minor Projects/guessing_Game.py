import random


class Guessing_Game:
    def __init__(self, low=0, high=100):
        self.low = low
        self.high = high

    def is_guess_within_range(self, guess):
        '''Check if the guess is within the range of self.low and self.high'''

        return self.low <= guess <= self.high

    def get_user_guess(self):
        '''Ask user to enter their guess until the valid guess is entered.'''

        guess = None

        while not guess:
            try:
                guess = int(input(f'\nGuess a number between {self.low}-{self.high}: '))

                if not self.is_guess_within_range(guess):
                    print(f'Your guess must be in {self.low}-{self.high}')
                    guess = None

            except ValueError:
                print('Your guess is not valid. Guess was expected in integer')

        return guess

    def play_again(self):
        '''Ask user if they want to play the game again.'''

        check = input('\nDo you want to play again (y/n)?').lower()

        return check == 'y'

    def random_number(self):
        '''Returns random number which has to be guessed by the user'''

        return random.randint(self.low, self.high)

    def main(self):
        '''Playing the game'''

        play = True

        while play:
            count = 1
            is_guessed = False
            to_guess = self.random_number()

            while not is_guessed:   # Until user guesses the random_number
                user_guess = self.get_user_guess()

                if user_guess == to_guess:
                    is_guessed = True
                    print(f'You have guessed in {count} guesses')

                    if not self.play_again():
                        play = False

                elif user_guess > to_guess:
                    print('Your guess is high')

                elif user_guess < to_guess:
                    print('Your guess is low')

                count += 1


if __name__ == '__main__':
    guess = Guessing_Game()
    guess.main()
