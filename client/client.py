import os

print("------Welcome to the Premier League Games Predictor!------"
      "\nIn this application, you will be able to predict"
      "\nthe outcome of upcoming Premier League matches based on"
      "\nhistorical data and team performance."
      "\nor data provided by you.")

program_state = 0
while program_state != -1:
    case = program_state
    if case == 0:
        print("\n\nPress 1 to get started or 0 to exit the program.")
        user_input = input("Choose wisely: ")
        if user_input == '1':
            program_state = 1

        elif user_input == '0':
            print("Thanks for using the app. Goodbye!")
            program_state = -1

        else:
            print("Invalid input. Please try again.")
            program_state = 0

    elif case == 1:
        print("Program booting... Please wait.")
        start_model = os.system(
            'python server/src/data/getdata/start_dataset.py'
            )
        start_model = os.system(
            'python server/src/data/processdata/process_dataset.py'
            )
        program_state = 2

    elif case == 2:
        print("\n\nChoose how you would like to proceed:"
              "\n1 - Fetch upcoming Premier League matches from the web"
              "\n2 - Provide your own data"
              "\n0 - Exit the program")
        user_input = input("Make up your choice: ")

        if user_input == '1':
            print("Fetching upcoming matches...")
            program_state = 3

        elif user_input == '2':
            print("Please provide your data in the required format.")
            print("Write down the last 5 games data to predict:")
            program_state = 4

        elif user_input == '0':
            print("Thanks for using the app. Goodbye!")
            program_state = -1

        else:
            print("Invalid input. Please try again.")
            program_state = 2

    elif case == 3:
        print("\n\n Upcoming matches:")
        print("Select which match you want to predict:")
        print("0 - Return to main menu")
        user_input = input("Choose your next move: ")
        if user_input == '0':
            program_state = 2
        elif user_input in ['1', '2', '3', '4', '5']:
            '''upcoming_matches_index'''
            program_state = 5
        else:
            print("Invalid input. Please try again.")
            program_state = 3

    elif case == 4:
        print("Write down the last 5 games data to predict:")
        print("1 - To proceed")
        print("0 - Return to main menu")
        user_input = input("I don't have all day...: ")
        if user_input == '0':
            program_state = 2
        elif user_input == '1':
            program_state = 6
        else:
            print("Invalid input. Please try again.")
            program_state = 4

    elif case == 5:
        print("Predicting match outcome based on given data...")
        # predict_match_from_web(upcoming_matches_index[user_input])
        print("\n2 - Build another match")
        print("\n1 - Predict another match")
        print("\n0 - Return to main menu")
        user_input = input("Your choice: ")
        if user_input == '0':
            program_state = 2
        elif user_input == '1':
            program_state = 3
        elif user_input == '2':
            program_state = 4
        else:
            print("Invalid input. Please try again.")
            program_state = 5

    elif case == 6:
        print("Give me the information about your game")
        print("\n 1 - Predict this match")
        print("\n 0 - Go back")
        user_input = input("Your choice: ")
        if user_input == '0':
            program_state = 4
        elif user_input == '1':
            program_state = 5

        else:
            print("Invalid input. Please try again.")
            program_state = 6
