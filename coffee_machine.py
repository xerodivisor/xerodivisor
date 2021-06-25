class CoffeeMachine:
    def __init__(self):
        self.water = 400
        self.milk = 540
        self.beans = 120
        self.cups = 9
        self.money = 550

    def display_inventory(self):
        print('The coffee machine has:', f'{self.water} of water', f'{self.milk} of milk',
              f'{self.beans} of coffee beans', f'{self.cups} of disposable cups',
              f'{self.money} of money', f'', sep='\n')
        self.do_action()

    def get_espresso(self):
        self.water -= 250
        self.beans -= 16
        self.cups -= 1
        self.money += 4

    def get_latte(self):
        self.water -= 350
        self.milk -= 75
        self.beans -= 20
        self.cups -= 1
        self.money += 7

    def get_cappuccino(self):
        self.water -= 200
        self.milk -= 100
        self.beans -= 12
        self.cups -= 1
        self.money += 6

    def check_inventory(self, coffee_type):
        if coffee_type == '1':
            if self.water < 250:
                print('Sorry, not enough water!\n')
                self.do_action()
            if self.beans < 16:
                print('Sorry, not enough beans!\n')
                self.do_action()
            if self.cups < 1:
                print('Sorry, not enough cups!\n')
                self.do_action()
            else:
                print('I have enough resources, making you a coffee!\n')
                self.get_espresso()
        elif coffee_type == '2':
            if self.water < 250:
                print('Sorry, not enough water!\n')
                self.do_action()
            if self.milk < 75:
                print('Sorry, not enough milk!\n')
                self.do_action()
            if self.beans < 20:
                print('Sorry, not enough beans!\n')
                self.do_action()
            if self.cups < 1:
                print('Sorry, not enough cups!\n')
                self.do_action()
            else:
                print('I have enough resources, making you a coffee!\n')
                self.get_latte()
        elif coffee_type == '3':
            if self.water < 200:
                print('Sorry, not enough water!\n')
                self.do_action()
            if self.milk < 100:
                print('Sorry, not enough milk!\n')
                self.do_action()
            if self.beans < 12:
                print('Sorry, not enough beans!\n')
                self.do_action()
            if self.cups < 1:
                print('Sorry, not enough cups!\n')
                self.do_action()
            else:
                print('I have enough resources, making you a coffee!\n')
                self.get_cappuccino()
        self.do_action()

    def get_coffee(self):
        coffee_type = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n')
        if coffee_type == '1':
            self.check_inventory(coffee_type)
        elif coffee_type == '2':
            self.check_inventory(coffee_type)
        elif coffee_type == '3':
            self.check_inventory(coffee_type)
        else:
            pass
        self.do_action()

    def fill_inventory(self):
        self.water += int(input('Write how many ml of water do you want to add:\n'))
        self.milk += int(input('Write how many ml of milk do you want to add:\n'))
        self.beans += int(input('Write how many grams of coffee beans do you want to add:\n'))
        self.cups += int(input('Write how many disposable cups of coffee do you want to add:\n'))
        self.do_action()

    def take_money(self):
        print(f'I gave you ${self.money}\n')
        self.money = 0
        self.do_action()

    def do_action(self):
        action = input('Write action (buy, fill, take, remaining, exit):\n')
        if action == 'buy':
            print()
            self.get_coffee()
        elif action == 'fill':
            print()
            self.fill_inventory()
        elif action == 'take':
            print()
            self.take_money()
        elif action == 'remaining':
            print()
            self.display_inventory()
        else:
            exit()


if __name__ == '__main__':
    coffee_machine = CoffeeMachine()
    coffee_machine.do_action()
