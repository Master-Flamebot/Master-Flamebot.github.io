

class Enemies:

    powerup_amount = 1
    num_of_enemies = 0

    def __init__(self, name, health, speed, damage):
        self.name = name
        self.health = health
        self.speed = speed
        self.damage = damage

        Enemies.num_of_enemies += 1

    @property
    def display_attributes(self):
        return '{} = health:{}, speed:{}, damage:{}'.format(self.name, self.health, self.speed, self.damage)

    def powerup_affect(self):
        self.damage = int(self.damage + self.powerup_amount)

    def __repr__(self):
        return "Enemies('{}', {}, {}, {})".format(self.name, self.health, self.speed, self.damage)

    @classmethod
    def set_powerup_amount(cls, amount):
        cls.powerup_amount = amount

class CommonGrunt(Enemies):
    powerup_amount = 2

    def __init__(self, name, health, speed, damage, weakness):
        Enemies.__init__(self, name, health, speed, damage)
        self.weakness = weakness

    def __repr__(self):
        return "CommonGrunt('{}', {}, {}, {}, '{}')".format(self.name, self.health, self.speed, self.damage, self.weakness)

Grunt_1 = CommonGrunt('first', 10, 1, 1, 'fire')
Grunt_2 = CommonGrunt('second', 20, .5, 2, 'fire')

print(Grunt_1.display_attributes)
print(Grunt_2.display_attributes)

