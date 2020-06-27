class Temperature_convertedersion:
    '''Convert given temperature to celsius, fahrenheit or kelvin'''

    def __init__(self, temp):
        self.temp = temp

    def celsius_to_fahrenheit(self):
        converted = (9 / 5) * self.temp + 32

        return f'{self.temp}C = {converted}F'

    def celsius_to_kelvin(self):
        converted = self.temp + 273

        return f'{self.temp}C = {converted}K'

    def fahrenheit_to_celsius(self):
        converted = (5 / 9) * self.temp - 32

        return f'{self.temp}F = {converted}C'

    def fahrenheit_to_kelvin(self):
        converted = (5 * self.temp - 2617) / 9

        return f'{self.temp}F = {converted}K'

    def kelvin_to_celsius(self):
        converted = self.temp - 273

        return f'{self.temp}K = {converted}C'

    def kelvin_to_fahrenheit(self):
        converted = (9 * self.temp + 2167) / 5

        return f'{self.temp}K = {converted}F'


if __name__ == '__main__':
    temp_converted = Temperature_convertedersion(100)

    print(temp_converted.celsius_to_fahrenheit())
    print(temp_converted.celsius_to_kelvin(), end='\n\n')

    print(temp_converted.fahrenheit_to_celsius())
    print(temp_converted.fahrenheit_to_kelvin(), end='\n\n')

    print(temp_converted.kelvin_to_celsius())
    print(temp_converted.kelvin_to_fahrenheit())
