class TemperatureConversion:
    '''
    Convert given temperature to celsius, fahrenheit or kelvin

    Conversion equation:
        C - 0        F - 32       K - 273.15
       --------  =  --------  =  ------------
         100          180             100

    From above equation, we get:
        1. Celsius to Fahrenheit
                F = (180 / 100) * C + 32
                  = (9 / 5) * C + 32

        2. Celsius to Kelvin
                K = C + 273.15

        3. Fahrenheit to Celsius
                C = (100 / 180) * (F - 32)
                  = (5 / 9) * (F - 32)

        4. Fahrenheit to Kelvin
                K = (100 / 180) * (F - 32) + 273.15
                  = (5 / 9) * (F - 32) + 273.15

        5. Kelvin to Celsius
                C = (100 / 100) * (K - 273.15)
                  = K - 273

        6. Kelvin to Fahrenheit
                F = (180 / 100) * (K - 273.15) + 32
                  = (9 / 5) * (K - 273.15) + 32
    '''

    def __init__(self, temp):
        self.temp = temp

    def CelsiusToFahrenheit(self):
        converted = (9 / 5) * self.temp + 32
        return f'{self.temp}C = {converted}F'

    def CelsiusToKelvin(self):
        converted = self.temp + 273.15
        return f'{self.temp}C = {converted}K'

    def FahrenheitToCelsius(self):
        converted = (5 / 9) * (self.temp - 32)
        return f'{self.temp}F = {converted}C'

    def FahrenheitToKelvin(self):
        converted = (5 / 9) * (self.temp - 32) + 273.15
        return f'{self.temp}F = {converted}K'

    def KelvinToCelsius(self):
        converted = self.temp - 273.15
        return f'{self.temp}K = {converted}C'

    def KelvinToFahrenheit(self):
        converted = (9 / 5) * (self.temp - 273.15) + 32
        return f'{self.temp}K = {converted}F'


if __name__ == '__main__':
    temp_converted = TemperatureConversion(100)

    print(temp_converted.CelsiusToFahrenheit())
    print(temp_converted.CelsiusToKelvin(), end='\n\n')

    print(temp_converted.FahrenheitToCelsius())
    print(temp_converted.FahrenheitToKelvin(), end='\n\n')

    print(temp_converted.KelvinToCelsius())
    print(temp_converted.KelvinToFahrenheit())
