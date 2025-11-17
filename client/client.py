import os

print("------Welcome to the Premier League Games Predictor!------"
      "\nIn this application, you will be able to predict"
      "\nthe outcome of upcoming Premier League matches based on"
      "\nhistorical data and team performance.")

program_state = 0
while program_state != -1:
    case = program_state
    if case == 0:
        print("\n\nPress 1 to get started or 0 to exit the program.")
        user_input = input("Choose wisely: ")
        if user_input == '1':
            program_state = 1

        elif user_input == '0':
            print("Thanks for the visit. Goodbye!")
            program_state = -1

        else:
            print("Invalid input. Please try again.")
            program_state = 0
    elif case == 1:
        print("Program booting... Please wait.")
        start_model = os.system('python server/src/data/getdata/start_model.py')
        start_model = os.system('python server/src/data/processdata/process_data.py')
        program_state = -1

