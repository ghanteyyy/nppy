class Fighter(object):
    def __init__(self, name, health, damage_per_attack):
        self.name = name
        self.health = health
        self.damage_per_attack = damage_per_attack

    def __str__(self):
        return "Fighter({}, {}, {})".format(self.name, self.health, self.damage_per_attack)

    __repr__ = __str__


def declare_winner(fighter1, fighter2, first_attacker):
    if fighter1.name == first_attacker:
        fn, fh, fd = fighter1.name, fighter1.health, fighter1.damage_per_attack
        sn, sh, sd = fighter2.name, fighter2.health, fighter2.damage_per_attack

    else:
        fn, fh, fd = fighter2.name, fighter2.health, fighter2.damage_per_attack
        sn, sh, sd = fighter1.name, fighter1.health, fighter1.damage_per_attack

    while True:
        sh -= fd

        if sh <= 0:
            return fn

        fh -= sd

        if fh <= 0:
            return sn


print(declare_winner(Fighter("Lew", 10, 2), Fighter("Harry", 5, 4), "Lew"))           # "Lew")
print(declare_winner(Fighter("Lew", 10, 2), Fighter("Harry", 5, 4), "Harry"))         # "Harry")
print(declare_winner(Fighter("Harald", 20, 5), Fighter("Harry", 5, 4), "Harry"))      # "Harald")
print(declare_winner(Fighter("Harald", 20, 5), Fighter("Harry", 5, 4), "Harald"))     # "Harald")
print(declare_winner(Fighter("Jerry", 30, 3), Fighter("Harald", 20, 5), "Jerry"))     # "Harald")
print(declare_winner(Fighter("Jerry", 30, 3), Fighter("Harald", 20, 5), "Harald"))    # "Harald")
