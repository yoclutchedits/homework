import random
from colorama import init, Fore
init(autoreset=True)

print('Welcome to Rock, Paper, Scissors!')

def get_difficulty():
    d = input(f'{Fore.MAGENTA}Choose the difficulty (medium, hard): ').lower()
    if d not in ['medium', 'hard']:
        print('Invalid choice, choose again.')
        return get_difficulty()


def rock_paper_scissors():
    choice = ['rock', 'paper', 'scissors']
    d = get_difficulty()

    while True:
        c = input(f'{Fore.MAGENTA}What do you choose rock, paper or scissors? ').lower()

        if c not in choice:
            print(f'{Fore.RED}Invalid choice. Please choose again.')
            continue

        if d == 'medium':
            ai = random.choice(choice)
        else:  # hard
            if c == 'rock':
                ai = 'paper'
            elif c == 'paper':
                ai = 'scissors'
            else:
                ai = 'rock'

        print(f'You chose: {c}')
        print(f'AI chose: {ai}')

        if c == ai:
            print(f"{Fore.YELLOW}It's a tie!")
        elif (
            (c == 'rock' and ai == 'scissors') or
            (c == 'paper' and ai == 'rock') or
            (c == 'scissors' and ai == 'paper')
        ):
            print(f'{Fore.GREEN}You win!')
        else:
            print(f'{Fore.RED}AI wins!')

        play = input('Do you want to play again? (yes/no): ').lower()
        if play != 'yes':
            print(f'{Fore.GREEN}Thanks for playing!')
            break

if __name__ == "__main__":
    rock_paper_scissors()
