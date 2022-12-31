import sys
import json
import pickle
import os
import glob
import mistune
import shutil

print('ahmer\'s notes utility')

# check if user entered enough arguments
if len(sys.argv) < 2:
    print('usage: python generate.py <action> <modifier> <value> <value_2>')
    exit()

print('')

# store arguments for easy access
action = sys.argv[1]
print('action = ' + action)
if len(sys.argv) > 2:
    modifier = sys.argv[2]
    print('modifier = ' + modifier)
if len(sys.argv) > 3:
    value = sys.argv[3]
    print('value = ' + value)
if len(sys.argv) > 4:
    value_2 = sys.argv[4]
    print('optional value = ' + value_2)

print('')

original_umask = os.umask(0o777)

# open input PKL and output JSON files
config_json_file = open('docs/config.json.js', 'w')
data_json_file = open('docs/data.json.js', 'w')
config_pkl_file_in = open('data/config.pkl', 'rb')
data_pkl_file_in = open('data/data.pkl', 'rb')

print('opened files '
      + str(config_json_file.name) + ', '
      + str(data_json_file.name) + ', '
      + str(config_pkl_file_in.name) + ', '
      + str(data_pkl_file_in.name) + '\n')

# read PKL files
config_pkl = config_pkl_file_in.read()
data_pkl = data_pkl_file_in.read()

# if PKL files are empty, create new objects
if config_pkl == b'' or data_pkl == b'':
    config_obj = {"root": "notes", "classes": {}}
    data_obj = {"files": []}
    print('no existing data found; created new objects')
# otherwise, load existing objects from PKL files
else:
    config_pkl_file_in.seek(0)
    data_pkl_file_in.seek(0)

    config_obj = pickle.load(config_pkl_file_in)
    data_obj = pickle.load(data_pkl_file_in)
    print('existing data found; loaded objects from PKL files')

if config_obj['root'] == '':
    config_obj['root'] = 'notes'
if config_obj == {}:
    config_obj = {"root": "notes", "classes": {}}
if data_obj == {}:
    data_obj = {"files": []}

print('config_obj = ' + str(config_obj))
print('data_obj = ' + str(data_obj))

print('\n----------------------------------------\n')

try:
    # if action is to create something
    if action == 'add' or action == 'a':
        # if modifier is 'semester'
        if modifier == 'semester' or modifier == 's':
            # if semester already exists
            if value in config_obj['classes']:
                # print error and exit
                print('semester "' + value + '" already exists')
            # if semester does not exist
            else:
                # create new semester
                print('creating new semester "' + value + '"')
                config_obj['classes'][value] = []
                # create a directory in docs for the semester
                os.makedirs('docs/' + value)
                os.makedirs('notes/' + value)
        # if modifier is 'class'
        elif modifier == 'class' or modifier == 'c':
            # if class already exists
            if value in config_obj['classes'][value_2]:
                # print error and exit
                print('class "' + value + '" already exists')
            # if class does not exist
            else:
                # try to add class to semester
                # if semester does not exist
                if value_2 not in config_obj['classes']:
                    # print error and exit
                    print('semester "' + value_2 + '" does not exist')
                # if semester exists
                else:
                    # create new class
                    print('creating new class "' + value + '"')
                    config_obj['classes'][value_2].append(value)
                    # create a directory in docs for the class
                    os.makedirs('docs/' + value_2 + '/' + value)
                    os.makedirs('notes/' + value_2 + '/' + value)
    # if action is to delete something
    elif action == 'delete' or action == 'd':
        # if modifier is 'semester'
        if modifier == 'semester' or modifier == 's':
            # if semester does not exist
            if value not in config_obj['classes']:
                # print error and exit
                print('semester "' + value + '" does not exist')
            # if semester exists
            else:
                # delete semester
                print('deleting semester "' + value + '"')
                del config_obj['classes'][value]
                # delete directory in docs for the semester
                os.rmdir('docs/' + value)
                os.rmdir('notes/' + value)
        # if modifier is 'class'
        elif modifier == 'class' or modifier == 'c':
            # if semester does not exist
            if value_2 not in config_obj['classes']:
                # print error and exit
                print('semester "' + value_2 + '" does not exist')
            # elif class does not exist
            elif value not in config_obj['classes'][value_2]:
                # print error and exit
                print('class "' + value + '" does not exist')
            # if class exists
            else:
                # delete class
                print('deleting existing class "' + value + '"')
                config_obj['classes'][value_2].remove(value)
                # delete directory in docs for the class
                os.rmdir('docs/' + value_2 + '/' + value)
                os.rmdir('notes/' + value_2 + '/' + value)
        # if invalid modifier is given
        else:
            print('invalid modifier "' + modifier + '"')
    # if action is to reset a semester
    elif action == 'reset' or action == 'r':
        # if modifier is 'semester'
        if modifier == 'semester' or modifier == 's':
            # if semester does not exist
            if value not in config_obj['classes']:
                # print error and exit
                print('semester "' + value + '" does not exist')
            # if semester exists
            else:
                # reset semester
                print('resetting semester "' + value + '"')
                # delete all class directories in docs for the semester
                for class_name in config_obj['classes'][value]:
                    os.rmdir('docs/' + value + '/' + class_name)
                    os.rmdir('notes/' + value + '/' + class_name)
                config_obj['classes'][value] = []
        # if modifier is 'all'
        elif modifier == 'all' or modifier == 'a':
            # reset all
            print('resetting all')
            config_obj = {"root": "notes", "classes": {}}
            data_obj = {"files": []}
            # delete all directories in docs
            for semester in os.listdir('docs'):
                # if semester is a directory
                if os.path.isdir('docs/' + semester):
                    shutil.rmtree('docs/' + semester)
            # delete all directories in notes
            for semester in os.listdir('notes'):
                # if semester is a directory
                if os.path.isdir('notes/' + semester):
                    shutil.rmtree('notes/' + semester)
        # if invalid modifier is given
        else:
            # print error and exit
            print('invalid modifier "' + modifier + '"')
    # if action is to scan for notes
    elif action == 'scan' or action == 's':
        notes = glob.glob(config_obj['root'] + '/**/*.md', recursive=True)
        style = open('docs/index.css', 'r').read()
        for note in notes:
            content = open(note, 'r').read()
            html_content = f'<!DOCTYPE html><html><head><title>{note.split("/")[-1].split(".")[0]}</title><style>{style}</style></head><body>' + \
                mistune.html(content) + '</body></html>'
            html_file = 'docs/' + \
                note.replace('.md', '.html').replace('notes/', '')
            open(html_file, 'w+').write(html_content)
            print('scanned ' + note + ', wrote to ' + 'docs/' +
                  note.replace('.md', '.html').replace('notes/', ''))
            data_obj['files'].append(html_file)
    # if action is to list the contents of something
    elif action == 'list' or action == 'l':
        # if modifier is 'semester'
        if modifier == 'semester' or modifier == 's':
            # if semester does not exist
            if value not in config_obj['classes']:
                # print error and exit
                print('semester "' + value + '" does not exist')
            # if semester exists
            else:
                # list semester
                print('listing semester "' + value + '"')
                print(config_obj['classes'][value])
        # if modifier is 'class'
        elif modifier == 'class' or modifier == 'c':
            # if semester does not exist
            if value_2 not in config_obj['classes']:
                # print error and exit
                print('semester "' + value_2 + '" does not exist')
            # if class does not exist
            elif value not in config_obj['classes'][value_2]:
                # print error and exit
                print('class "' + value + '" does not exist')
            # if class exists
            else:
                # list class
                print('listing class "' + value + '"')
                print(data_obj[value_2][value])
        # if modifier is 'all'
        elif modifier == 'all' or modifier == 'a':
            # list all
            print('listing all semesters and classes')
            print(config_obj['classes'])
        # if modifier is 'objects'
        elif modifier == 'objects' or modifier == 'o':
            # list all objects
            print('listing all objects')
            print('config_obj = ' + json.dumps(config_obj))
            print('data_obj = ' + json.dumps(data_obj))
        # if invalid modifier is given
        else:
            # print error and exit
            print('error: invalid modifier "' + modifier + '"')
            print('usage: python generate.py <action> <modifier> <value> <value_2>')
    # if an invalid action is given
    else:
        # print error and exit
        print('error: invalid action "' + action + '"')
        print('usage: python generate.py <action> <modifier> <value> <value_2>')
except NameError:
    # print error and exit
    print('error: too few arguments')
    print('usage: python generate.py <action> <modifier> <value> <value_2>')

# write JSON files
config_json_file.write('const config = ' + json.dumps(config_obj) + ';')
data_json_file.write('const data = ' + json.dumps(data_obj) + ';')

# open and write PKL files
config_pkl_file_in.close()
data_pkl_file_in.close()
config_pkl_file_out = open('data/config.pkl', 'wb')
data_pkl_file_out = open('data/data.pkl', 'wb')

pickle.dump(config_obj, config_pkl_file_out, protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(data_obj, data_pkl_file_out, protocol=pickle.HIGHEST_PROTOCOL)

print('\n----------------------------------------\n')

print('wrote JSON and PKL files')

# close files
config_json_file.close()
data_json_file.close()
config_pkl_file_out.close()
data_pkl_file_out.close()

os.umask(original_umask)
