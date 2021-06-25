import random

guest_number = int(input("Enter the number of friends joining (including you):\n"))
guest_dict = {}


class Guest:
    def __init__(self, name, value=0):
        self.name = name
        self.value = value

    def __repr__(self):
        return '{}'.format(self.name)


print("Enter the name of every friend (including you), each on a new line:")
for i in range(guest_number):
    guest = Guest(name=input())
    guest_dict[guest.name] = guest.value

bill = float(input("Enter the total bill value:\n"))
choice = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n')
if choice == 'No':
    print("No one is going to be lucky")
    if guest_number > 0:
        portion = round(bill / guest_number, 2)
        for k, v in guest_dict.items():
            guest_dict[k] = portion
        print(guest_dict)
    else:
        print({})
if choice == "Yes":
    lucky = random.choice(list(guest_dict))
    print(f'{lucky} is the lucky one!')
    portion = round(bill / (guest_number - 1), 2)
    for k, v in guest_dict.items():
        if k == lucky:
            pass
        else:
            guest_dict[k] = portion
    print(guest_dict)
