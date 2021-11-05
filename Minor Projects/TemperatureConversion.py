class TemperatureConversion:
    '''Convert given temperature to celsius, fahrenheit or kelvin'''

    def __init__(self, temp):
        self.temp = temp

    def CelsiusToFahrenheit(self):
        converted = (9 / 5) * self.temp + 32
        return f'{self.temp}C = {converted}F'

    def CelsiusToKelvin(self):
        converted = self.temp + 273
        return f'{self.temp}C = {converted}K'

    def FahrenheitToCelsius(self):
        converted = (5 / 9) * self.temp - 32
        return f'{self.temp}F = {converted}C'

    def FahrenheitToKelvin(self):
        converted = (5 * self.temp - 2617) / 9
        return f'{self.temp}F = {converted}K'

    def KelvinToCelsius(self):
        converted = self.temp - 273
        return f'{self.temp}K = {converted}C'

    def KelvinToFahrenheit(self):
        converted = (9 * self.temp + 2167) / 5
        return f'{self.temp}K = {converted}F'


if __name__ == '__main__':
    temp_converted = TemperatureConversion(100)

    print(temp_converted.CelsiusToFahrenheit())
    print(temp_converted.CelsiusToKelvin(), end='\n\n')

    print(temp_converted.FahrenheitToCelsius())
    print(temp_converted.FahrenheitToKelvin(), end='\n\n')

    print(temp_converted.KelvinToCelsius())
    print(temp_converted.KelvinToFahrenheit())
