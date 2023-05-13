import json
import os
from json.decoder import JSONDecodeError




def teacher_mode():
    clear_screen()

    print("You are a Teacher\n")

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


# Add new question
def add_new_question():
    question = input("Enter question:\n")
    option_a = input("Enter option A: ")
    option_b = input("Enter option B: ")
    option_c = input("Enter option C: ")
    option_d = input("Enter option D: ")
    print("\n")

    correct_answer = ''
    while(True):
        correct_answer = input("Enter correct option:\n")
        if correct_answer in ['A','B', 'C', 'D']:
            break
        else:
            print("Please enter a valid option\n")
    
    filename = r"./data/quiz.json"
    data = get_json_data(filename)
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
    store_json_data(filename, data)


# Liar all questions
def list_questions():
    clear_screen()

    filename = r"./data/quiz.json"

    quizs = get_json_data(filename)
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


def student_mode():
    clear_screen()

    print("You are a Student\n")


# Get data from json file
def get_json_data(filename):
  with open(filename, 'w+') as json_file:
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
    filename = r"./data/quiz.json"
    data = get_json_data(filename)
    if data is not None:
        for item in data:
            if item.get('id') == id:
                data.remove(item)
                break

        store_json_data(filename, data)


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
    print("Good Bey!")
    exit();


def main():
    print("\t\t\t\t\tWelcome to QUIZ App\t\t\t\t\n")
    print("\n\n")

    print("1. Press 1 for Teacher\n")
    print("2. Press 2 for Student\n")
    print("3. Press 0 for Exit!\n")

    command = get_user_command([0,1,2])

    print("You entered {}".format(command))

    if(command == 1):
        teacher_mode()
    elif command == 2:
        student_mode()
    else:
        exit_program()

if __name__ == "__main__":
    main()