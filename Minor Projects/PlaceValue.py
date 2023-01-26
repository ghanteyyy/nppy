class PlaceValue:
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
        '''
        Group number of length 3

        If user enters 1234567890 then this function returns [[1], [234], [567], [890]]
        '''

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
        '''
        Getting the number in words with respect to their place value
        '''

        in_words = ''
        length = len(value)

        if length == 1:
            if value == '0':
                if not self.in_words:
                    in_words = 'Zero'

            else:
                in_words += self.map_num[value]

        elif length == 2:
            if value[0] == '1' or value[1] == '0':
                in_words += self.map_num[value]

            else:
                in_words += f'{self.map_num[value[0] + "0"]}-{self.map_num[value[1]]}'

        if len(value) == 3:
            if value[1:] == '00':
                in_words += f'{self.map_num[value[0]]} hundred'

            elif value[1] == '0':
                in_words += f'{self.map_num[value[0]]} hundred and {self.map_num[value[2]]}'

            elif value[1] == '1' or value[-1] == '0':
                in_words += f'{self.map_num[value[0]]} hundred and {self.map_num[value[1:]]}'

            else:
                in_words += f'{self.map_num[value[0]]} hundred and {self.map_num[value[1] + "0"]}-{self.map_num[value[2]]}'

        return in_words

    def main(self):
        place_value = self.place_value[:len(self.num)][::-1]

        # Grouping number and their place_value of length 3
        num_group = self.make_group(self.num)[::-1]
        place_value_group = self.make_group(place_value)[::-1]

        for index, value in enumerate(num_group):
            value = str(int(value))

            if index < len(num_group) - 1:
                self.in_words += f'{self.getting_in_words(value)} {place_value_group[index][-1]} '

            else:
                self.in_words += self.getting_in_words(value)

        return self.in_words.lower()


if __name__ == '__main__':
    try:
        value = str(int(input('Enter a number: ')))
        in_words = PlaceValue(value).main()
        print(in_words)

    except ValueError:
        print('Entered value is not a valid number')
