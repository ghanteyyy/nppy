import os


def sort_details():
    '''Sort content of a file alphabetically'''

    with open('phonebook.txt', 'r+') as phbk:
        lines = phbk.readlines()
        lines.sort()
        phbk.seek(0)

        for line in lines:
            phbk.write(line)


def check_exists(name, number):
    '''Check if name and number exists in file'''

    with open('phonebook.txt', 'r') as phbk:
        lines = phbk.readlines()
        check = '{}: {}\n'.format(name.ljust(20), number)

        if check in lines:
            return True

        else:
            return False


def search_by():
    '''Search by name or number'''

    print('''\n1. Search by name\n2. Search by number\nAny key to quit ...\n''')
    choice = input('Search by: ')

    if choice == '1' or choice == 'name':
        search_by_name()

    elif choice == '2' or choice == 'num':
        search_by_number()


def search_by_name():
    '''when user want to search by name'''

    while True:
        name = input('\nEnter name: ').title()
        found = False

        with open('phonebook.txt', 'r+') as phbk:
            lines = phbk.readlines()

            if len(name) == 0:
                print('\nPlease, do not enter empty name')

            elif len(name) != 0:
                for line in lines:
                    split = line.split()

                    if split[0] == name:
                        print(split[-1])
                        found = True

                else:
                    if found is False:
                        print('Contact not found')
                        choice = input('\nDo you want to add it? (Y/n): ').lower()

                        if choice == 'y':
                            number = input('\nEnter number for {}: '.format(name))

                            if not check_exists(name, number):
                                phbk.write('{} : {}\n'.format(name.ljust(20), number))
                                print('\n' + name + '\n' + number)

                            else:
                                print('Details already exists. Try again with different name or number ...')

                        elif choice == 'n':
                            search_by()

                        else:
                            print('Invalid Input')
                            search_by_name()
        sort_details()


def search_by_number():
    '''when user want to search by number'''

    while True:
        number = input('\nEnter number: ')
        found = False

        with open('phonebook.txt', 'r+') as phbk:
            lines = phbk.readlines()

            if len(number) == 0:
                print('\nPlease, do not enter empty number')

            elif len(number) != 0:
                for line in lines:
                    split = line.split()

                    if number == split[-1]:
                        print(split[-1])
                        found = True

                else:
                    if found is False:
                        print('Contact not found')
                        choice = input('\nDo you want to add it? (Y/n): ').lower()

                        if choice == 'y':
                            name = input('\nEnter name for {}: '.format(number))

                            if not check_exists(name, number):
                                phbk.write('{} : {}\n'.format(name.ljust(20), number))
                                print(name + '\n' + number)

                            else:
                                print('Details already exists. Try again with different name or number ...')

                        elif choice == 'n':
                            search_by()

                        else:
                            print('Invalid Input')
                            search_by_name()
        sort_details()


def main():
    if not os.path.exists('phonebook.txt'):
        with open('phonebook.txt', 'w'):
            pass

    search_by()


if __name__ == '__main__':
    main()
