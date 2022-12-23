import os

os.system('cls' if os.name == 'nt' else 'clear')

while True:
    user_input = input('>>> ')
    os.system('cls' if os.name == 'nt' else 'clear')

    if user_input == 'exit' or user_input == 'e' or user_input == 'quit' or user_input == 'q':
        print('exiting...')
        break
    elif user_input == 'help' or user_input == 'h':
        print("""
        usage: [action] [modifier] [value] [value_2]
        valid actions:
         - add
           ↳ semester
           ↳ class
         - delete
           ↳ semester
           ↳ class
           ↳ all
         - reset
           ↳ semester
           ↳ all
         - scan
         - list
           ↳ semester
           ↳ class
           ↳ all
           ↳ objects
         - exit
         - help
         """)
    else:
        os.system('python3 gen.py ' + user_input)
