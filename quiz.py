import json
import os
from json.decoder import JSONDecodeError

student_name = ''
student_roll = ''
QUIZ_FILE = r"./data/quiz.json"
SCORE_FILE = r"./data/score.json"



def teacher_mode():
    clear_screen()

    print("You are a Teacher\n\n\n")

    print("1. Press 1 for list all questrion\n")
    print("2. Press 2 for add new question\n")
    print("3. Press 0 for Exit!\n")

    command = get_user_command([1,2, 0])

    if command == 1:
        list_questions()

    if command == 2:
        add_new_question()
    
    else:
        exit_program()


def student_mode():
    global student_name, student_roll
    clear_screen()

    if(student_name == '' or student_roll == ''):
        student_roll = input("Enter your roll: ")
        student_name = input("Enter your name: ")
        clear_screen()

    print("You are a Student\n\n\n")

    print("1. Press 1 for answer questrions\n")
    print("2. Press 0 for Exit!\n")

    command = get_user_command([1, 0])

    if command == 1:
        answer_questions()

    else:
        exit_program()


def answer_questions():
    global QUIZ_FILE
    clear_screen()

    quizs = get_json_data(QUIZ_FILE)
    if quizs is None:
        quizs = []
        print("There are not question for answer, please contact your teacher for add new question.")
        exit()

    else:
        score = 0
        for item in quizs:
            clear_screen()
            print("{}. {}\n".format(item["id"], item["question"]))
            for option in item['options']:
                print("\t{}. {}\n".format(option['key'], option['value']))
            answer = input("Enter your choice: ")
            # answer = input("")
            if(answer == item['answer']):
                score += 1
        clear_screen()

        store_score(score)


        print("Your score is: {} out of {}\n\n".format(score, len(quizs)))

        print("1. Press 1 for back\n")
        print("2. Press 0 for Exit!\n")

        command = get_user_command([1, 0])

        if command == 1:
            student_mode()
        else:
            exit_program()


def store_score(score):
    global student_roll, student_name, SCORE_FILE

    data = get_json_data(SCORE_FILE)
    if data is None:
        data = []

    new_score = {
        "roll": student_roll,
        "name": student_name,
        "score": score
    }
    
    data.append(new_score)
    store_json_data(SCORE_FILE, data)


# Add new question
def add_new_question():
    global QUIZ_FILE
    question = input("Enter question:\n")
    option_a = input("Enter option A: ")
    option_b = input("Enter option B: ")
    option_c = input("Enter option C: ")
    option_d = input("Enter option D: ")
    print("\n")

    correct_answer = ''
    while(True):
        correct_answer = input("Enter correct option: ")
        if correct_answer in ['A','B', 'C', 'D']:
            break
        else:
            print("Please enter a valid option\n")

    data = get_json_data(QUIZ_FILE)
    if data is None:
        data = []

    id = 1
    if(len(data)):
        last_item = data[-1];
        id = last_item['id'] + 1

    new_question = {"id": id, "question": question, "options": [
            {"key":"A", "value": option_a},
            {"key":"B", "value": option_b},
            {"key":"C", "value": option_c},
            {"key":"D", "value": option_d}
        ], "answer": correct_answer}
    
    data.append(new_question)
    store_json_data(QUIZ_FILE, data)

    teacher_mode()


# Liar all questions
def list_questions():
    global QUIZ_FILE
    clear_screen()


    quizs = get_json_data(QUIZ_FILE)
    if quizs is None:
        quizs = []
    
    for item in quizs:
        print("{}. {}".format(item["id"], item["question"]))
    
    print("\n\n\n")
    print("1. Press 1 for delete question\n")
    print("2. Press 2 for back\n")
    print("3. Press 0 for Exit!\n")

    command = get_user_command([1,2, 0])

    if(command == 1):
        # Delete question
        print("Enter question number for delete\n")
        id = int(input())
        delete_question_by_id(id)
        print("Question {} delete successfully!\n".format(id))

        list_questions()

    if(command == 2):
        teacher_mode()
    else:
        exit_program()

def get_files_in_a_directory(directory):
    files = []

    for path in os.scandir(directory):
        if path.is_file():
            files.append(path.name)

    return files


# Get data from json file
def get_json_data(filename):
  with open(filename, 'r+') as json_file:
    try:
        data = json.load(json_file)
        return data
    except JSONDecodeError:
        pass
#Store text data to json file
def store_json_data(filename, data):
    with open(filename, 'w+') as outfile:
         json.dump(data, outfile)


# Delete question by id
def delete_question_by_id(id):
    global QUIZ_FILE

    data = get_json_data(QUIZ_FILE)
    if data is not None:
        for item in data:
            if item.get('id') == id:
                data.remove(item)
                break

        store_json_data(QUIZ_FILE, data)


#Get command input from user
def get_user_command(options):
    command = ''
    while(True):
        command = int(input())

        if  command in options:
            break
        else:
            print("You entered wrong value, please enter correct value")
    return command


# Clear console screen     
def clear_screen():
    #for windows
    if os.name == 'nt':   
        _ = os.system('cls')   

    # for mac and linux(here, os.name is 'posix')   
    else:   
        _ = os.system('clear')   


#Exit the program
def exit_program():
    print("\n\n")
    print("\t\t\t\tGood Bey!\t\t\t\t")
    exit();


def main():
    print("\t\t\t\t\tWelcome to QUIZ App\t\t\t\t")
    print("\n\n")

    print("1. Press 1 for Teacher\n")
    print("2. Press 2 for Student\n")
    print("3. Press 0 for Exit!\n")

    command = get_user_command([0,1,2])

    if(command == 1):
        teacher_mode()
    elif command == 2:
        student_mode()
    else:
        exit_program()

if __name__ == "__main__":
    main()