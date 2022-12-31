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
        valid actions & modifiers:
         - (a)dd: adds new module
           ↳ (s)emester
           ↳ (c)lass
         - (d)elete: deletes existing module(s)
           ↳ (s)emester
           ↳ (c)lass
           ↳ (a)ll
         - (r)eset: resets content of existing module(s)
           ↳ (s)emester
           ↳ (a)ll
         - (s)can: scans for new notes in existing module(s)
         - (l)ist: lists existing module(s) and their contents
           ↳ (s)emester
           ↳ (c)lass
           ↳ (a)ll
           ↳ (o)bjects
         - (e)xit / (q)uit: exits the CLI
         - (h)elp: displays this message
         """)
    else:
        os.system('python3 gen.py ' + user_input)
