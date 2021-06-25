from math import log
from math import pow
from math import ceil
from math import floor
import argparse


def annuity_chooser():
    if args.principal is not None and args.periods is not None and args.interest is not None:
        annuity_payment()
    elif args.payment is not None and args.periods is not None and args.interest is not None:
        principle()
    elif args.principal is not None and args.payment is not None and args.interest is not None:
        number_of_payments()
    else:
        print("Incorrect parameters")


def number_of_payments():
    principal = int(args.principal)
    payment = int(args.payment)
    interest = float(args.interest)
    rate = (interest / 100) / (12 / 1)
    n = -(-log(payment / (payment - rate * principal), 1 + rate) // 1)
    over = payment * n - principal
    if n <= 2:
        print("It will take 1 month to repay this loan!")
        print("Overpayment = " + str(int(over)))
        exit()
    elif n < 12:
        print("It will take " + str(int(n)) + " months to repay this loan!")
        print("Overpayment = " + str(int(over)))
        exit()
    elif n == 12:
        print("It will take 1 year to repay this loan!")
        print("Overpayment = " + str(int(over)))
        exit()
    elif n % 12 != 0:
        m = n % 12
        y = (n - m) / 12
        if y < 2 and m == 1:
            print("it will take 1 year and 1 month to repay this loan!")
            print("Overpayment = " + str(int(over)))
            exit()
        else:
            print("It will take 1 year and " + str(int(m)) + " months to repay this loan!")
            print("Overpayment = " + str(int(over)))
            exit()
        if y > 1 and m == 1:
            print("It will take " + str(int(y)) + " years and 1 month to repay this loan!")
            print("Overpayment = " + str(int(over)))
            exit()
        else:
            print("it will take " + str(int(y)) + " years and " + str(int(m)) + " months to repay this loan!")
            print("Overpayment = " + str(int(over)))
            exit()
    else:
        t = n / 12
        print("It will take " + str(int(t)) + " years to repay this loan!")
        print("Overpayment = " + str(int(over)))
        exit()


def annuity_payment():
    principal = int(args.principal)
    periods = int(args.periods)
    interest = float(args.interest)
    if principal is not None and periods is not None and interest is not None:
        rate = interest / 12 / 100
        a = ceil(principal * ((rate * pow(1 + rate, periods)) / (pow(1 + rate, periods) - 1)))
        over = a * periods - principal
        print("Your annuity payment = " + str(int(a)) + "!")
        print("Overpayment = " + str(int(over)))
        exit()
    else:
        print("Incorrect parameters")


def principle():
    payment = float(args.payment)
    periods = int(args.periods)
    interest = float(args.interest)
    rate = interest / 12 / 100
    principal = floor(payment / ((rate * pow(1 + rate, periods)) / (pow(1 + rate, periods) - 1)))
    over = payment * periods - principal
    print("Your loan principal = " + str(round(principal)) + "!")
    print("Overpayment = " + str(int(over)))
    exit()


def differential():
    principal = int(args.principal)
    periods = int(args.periods)
    interest = float(args.interest)
    total = 0
    if principal is not None and periods is not None and interest is not None:
        i = 1
        rate = interest / 12 / 100
        while i <= periods:
            pay = ceil((principal / periods) + rate * (principal - (principal * (i - 1) / periods)))
            total += pay
            print("Month " + str(i) + " payment is " + str(int(pay)))
            i += 1
        over = total - principal
        print()
        print("Overpayment = " + str(int(over)))
        exit()
    else:
        print("Incorrect parameters")


# print("What do you want to calculate?")
# print("""type "n" for number of monthly payments,""")
# print("""type "a" for annuity monthly payment amount,""")
# print("""type "p" for loan principal:""")
# choice = input()
# if choice == "n":
    # number_of_payments()
# elif choice == "a":
    # annuity_payment()
# elif choice == "d":
    # differential()
# else:
    # principle()
parser = argparse.ArgumentParser()
parser.add_argument('--type')
parser.add_argument('--principal')
parser.add_argument('--interest')
parser.add_argument('--periods')
parser.add_argument('--payment')
args = parser.parse_args()
args_list = []
for arg in vars(args):
    if getattr(args, arg) is not None:
        args_list.append(getattr(args, arg))
if args.interest is None or args.type not in ("diff", "annuity") or len(args_list) != 4:
    print("Incorrect parameters")
else:
    if 'annuity' in args_list:
        annuity_chooser()
    else:
        differential()
