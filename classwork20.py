import requests
url = "https://opentdb.com/api.php?amount=10&type=multiple"
res = requests.get(url)
if res.status_code == 200:
    trivia=res.json()
    score=0
    for i , question_data in enumerate(trivia['results']):
        print(f"question {i+1}:{question_data['question']}")
        options = question_data['incorrect_answers']+ [question_data['correct_answer']]
        options=sorted(options)
        for j , option in enumerate(options):
            print(f"{j+1}.{option}")
        user_ans=input("your answer (1/2/3/4):")
        if options[int(user_ans)-1]==question_data['correct_answer']:
            print("correct answer")
            score+=1
        else:
            print(f"worng answer the correct answer was:{question_data['correct_answer']}")
            print("\n")
    print(f"for your final score{score}/{len(trivia['results'])}")
else:
    print("failed to retrive triva")
