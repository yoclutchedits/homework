import requests
import time
from colorama import Fore, Style, init
init(autoreset=True)
def get_trivia():
    url = "https://opentdb.com/api.php?amount=5&type=multiple"
    res = requests.get(url, timeout=10)
    if res.status_code == 200:
        trivia=res.json()
        score=0
        for i , question_data in enumerate(trivia['results']):
            print(Fore.MAGENTA + f"Category: {question_data['category']}")
            print(Fore.YELLOW + f"Question {i+1}: {question_data['question']}")
            options = question_data['incorrect_answers']+ [question_data['correct_answer']]
            options=sorted(options)
            for j , option in enumerate(options):
                print(Fore.YELLOW + f"{j+1}.{option}")
            user_ans=input(Fore.CYAN + "your answer (1/2/3/4):")
            while user_ans not in ['1','2','3','4']:
                print(Fore.RED + f"invalid input, please enter 1, 2, 3, or 4")
                user_ans=input(Fore.CYAN + "your answer (1/2/3/4):")
            if options[int(user_ans)-1]==question_data['correct_answer']:
                print(Fore.GREEN + "correct answer")
                score+=1
            else:
                print(Fore.RED + f"wrong answer the correct answer was:{question_data['correct_answer']}")
                print("\n")
        print(Fore.CYAN + f"calculating your score...")
        time.sleep(2)
        print(Fore.CYAN+ f"too pass the quiz you need at least 3 correct answers")
        print(Fore.CYAN+"revaluating your answers...")
        time.sleep(2)
        print(Fore.YELLOW + f"for your final score {score}/{len(trivia['results'])}")
        if score >= 3:
            print(Fore.GREEN + "Congratulations! You passed the quiz.")
        else:
            print(Fore.RED + "Sorry, you did not pass the quiz.")
    else:
        print(Fore.RED + f"failed to retrieve trivia")
    y=input(Fore.CYAN + f"do you want to play again? (y/n):").lower()
    while y not in ['y','n']:
        print("invalid input, please enter y or n")
        y=input(Fore.CYAN + "do you want to play again? (y/n):").lower()
    if y=='y':
        get_trivia()
    print(Fore.GREEN + "Goodbye!")
if __name__ == "__main__":
    get_trivia()