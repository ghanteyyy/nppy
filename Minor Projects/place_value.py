class Place_Value:
    def __init__(self, num):
        self.num = num
        self.in_words = ''
        self.map_num = {'1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine', '10': 'ten',
                        '11': 'elevan', '12': 'twelve', '13': 'thirteen', '14': 'fourteen', '15': 'fifteen', '16': 'sixteen', '17': 'seventeen',
                        '18': 'eighteen', '19': 'nineteen', '20': 'twenty', '30': 'thirty', '40': 'forty', '50': 'fifty', '60': 'sixty', '70': 'seventy',
                        '80': 'eighty', '90': 'ninety'}

        self.place_value = ['Ones', 'Tens', 'Hundred', 'Thousand', 'Ten Thousand', 'Hundred Thousand', 'Million', 'Ten Million', 'Hundred Million', 'Billion',
                            'Ten Billion', 'Hundred Billion', 'Trillion', 'Ten Trillion', 'Hundred Trillion', 'Quadrillion', 'Ten Quadrillion', 'Hundred Quadrillion',
                            'Quintillion', 'Ten Quintillion', 'Hundred Quintillion', 'Hextillion', 'Ten Hextillion', 'Hundred Hextillion', 'Septillion',
                            'Ten Septillion', 'Hundred Septillion', 'Octillion', 'Ten Octillion', 'Hundred Octillion', 'Nonillion', 'Ten Nonillion',
                            'Hundred Nonillion', 'Decillion', 'Ten Decillion', 'Hundred Decillion', 'Undecillion', 'Ten Undecillion', 'Hundred Undecillion',
                            'Duodecillion', 'Ten Duodecillion', 'Hundred Duodecillion', 'Tredecillion', 'Ten Tredecillion', 'Hundred Tredecillion',
                            'Quattuordecillion', 'Ten Quattuordecillion', 'Hundred Quattuordecillion', 'Quindecillion', 'Ten Quindecillion', 'Hundred Quindecillion',
                            'Hexdecillion', 'Ten Hexdecillion', 'Hundred Hexdecillion', 'Septendecillion', 'Ten Septendecillion', 'Hundred Septendecillion',
                            'Octodecillion', 'Ten Octodecillion', 'Hundred Octodecillion', 'Novemdecillion', 'Ten Novemdecillion', 'Hundred Novemdecillion',
                            'Vigintillion', 'Ten Vigintillion', 'Hundred Vigintillion', 'Unvigintillion', 'Ten Unvigintillion', 'Hundred Unvigintillion',
                            'Duovigintillion', 'Ten Duovigintillion', 'Hundred Duovigintillion', 'Trevigintillion', 'Ten Trevigintillion', 'Hundred Trevigintillion',
                            'Quattourvigintillion', 'Ten Quattourvigintillion', 'Hundred Quattourvigintillion', 'Quinvigintillion', 'Ten Quinvigintillion',
                            'Hundred Quinvigintillion', 'Hexvigintillion', 'Ten Hexvigintillion', 'Hundred Hexvigintillion', 'Septenvigintillion',
                            'Ten Septenvigintillion', 'Hundred Septenvigintillion', 'Octovigintillion', 'Ten Octovigintillion', 'Hundred Octovigintillion',
                            'Novemvigintillion', 'Ten Novemvigintillion', 'Hundred Novemvigintillion', 'Trigintillion', 'Ten Trigintillion', 'Hundred Trigintillion',
                            'Untrigintillion', 'Ten Untrigintillion', 'Hundred Untrigintillion', 'Duotrigintillion', 'Ten Duotrigintillion', 'Hundred Duotrigintillion',
                            'Googol', 'Ten Googol', 'Hundred Googol', 'Centillion', 'Ten Centillion', 'Hundred Centillion', 'Googolplex', 'Ten Googolplex',
                            'Hundred Googolplex']

    def make_group(self, values):
        '''Group number of length 3.
            If user enters 1234567890 then this function returns [[1], [234], [567], [890]] '''

        groups = []
        loop_for = len(values) // 3 if len(values) % 3 == 0 else len(values) // 3 + 1

        for i in range(loop_for):
            if len(values) <= 3:
                groups.append(values)
                values = ''

            else:
                groups.append(values[-3:])
                values = values[:-3]

        return groups

    def getting_in_words(self, value):
        '''Getting the number in words with respect to their place value'''

        in_words = ''

        if len(value) == 1:  # If single digit number is inputed
            in_words += self.map_num[value[:]]

        elif len(value) == 2:  # If double digit number is inputed i.e ones and tenth place only
            if value[0] == '1' or value[1] == '0':  # If a double digit number starts with '1' i.e. 10-19
                in_words += self.map_num[value[:]]

            else:  # If a double digit number is between 10-99
                in_words += f'{self.map_num[value[0] + "0"]}-{self.map_num[value[1]]}'

        elif value[:2] == '00' and value[2] != '0':  # If a number between 001-009 is inputed
            in_words += self.map_num[value[2]]

        elif value[0] == value[2] == '0' and value[1] != '0':  # If a number between 010-090 is inputed
            in_words += self.map_num[value[1:]]

        elif value[0] == '0' and value[1] != '0' and value[2] != '0':  # If a number between 011-099 is inputed
            if value[1] == '1':  # If number between 011-019 is inputed i.e '1' in tenth place
                in_words += self.map_num[value[1:]]

            else:  # If a number between 021-099 is inputed
                in_words += f'{self.map_num[value[1] + "0"]}-{self.map_num[value[2]]}'

        elif value[1:] == '00' and value[0] != '0':  # If a number where last two digits are '0' i.e 100, 200, 700, etc.
            in_words += self.map_num[value[0]] + ' hundred'

        elif value[1] == '0' and value[0] != '0' and value[2] != '0':  # If a number between 101, 907, 503, etc are inputed i.e '0' at the tenth place
            in_words += f'{self.map_num[value[0]]} hundred {self.map_num[value[2]]}'

        elif value[0] != '0' and (value[1] == '1' or value[2] == '0'):  # If a number whose last value is 0 or second last value starts with '1'
            in_words += f'{self.map_num[value[0]]} hundred {self.map_num[value[1:]]}'

        else:  # If a number has no any '0's
            in_words += f'{self.map_num[value[0]]} hundred {self.map_num[value[1] + "0"]}-{self.map_num[value[2]]}'

        return in_words

    def main(self):
        place_value = self.place_value[:len(self.num)][::-1]  # Slicing place_value as per the length of the given number

        # Grouping number and their place_value of length 3
        num_group = self.make_group(self.num)[::-1]
        place_value_group = self.make_group(place_value)[::-1]

        for index, value in enumerate(num_group):
            if index < len(num_group) - 1:  # Checking if the loops has not reached to the last index of num_group
                if value != '000':  # If the value is not '000' except in last-index
                    self.in_words += f'{self.getting_in_words(value)} {place_value_group[index][-1]} '

            else:
                # If the loop is at the last index of num_group

                if value in ['0', '00', '000']:  # If last three digit of a number is '0'
                    if not self.in_words:
                        self.in_words += 'Zero'

                else:  # If the last three number is between 001-999
                    self.in_words += self.getting_in_words(value)

        return self.in_words.lower()


if __name__ == '__main__':
    try:
        value = str(int(input('Enter a number: ')))
        pv = Place_Value(value)
        in_words = pv.main()
        print(in_words)

    except ValueError:
        print('Entered value is not a valid number')
