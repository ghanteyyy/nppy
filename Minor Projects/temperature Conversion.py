def Celsius_to_Fahrenheit(Tc):
    # Celsius to Fahrenheit = (9 / 5) * Temperature in celsius + 32

    Tf = (9 / 5) * Tc + 32
    print('The Fahrenheit scale of {} is {}'.format(Tc, Tf))


def Fahrenheit_to_Celsius(Tf):
    # Fahrenheit to Celsius = (5 / 9) * Temperature in Fahrenheit - 32

    Tc = (5 / 9) * Tf - 32
    print('The Celsius scale of {} is {}'.format(Tf, Tc))


if __name__ == '__main__':
    try:
        Celsius_to_Fahrenheit(float(input('Give Temperature in Celsius scale:')))
        Fahrenheit_to_Celsius(float(input('\n\nGive Temperature in Fahrenheit scale:')))

    except (ValueError, NameError):
        print('Integer was expected')
