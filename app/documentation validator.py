import json
import os

# change current working directory to file directory name
os.chdir(os.path.dirname(__file__))

# default items
json_default = {'metadata': [{}],
                'data': [list]}

header_default = {'type': ['header'],
                  'name': [str],
                  'size': [int],
                  'size type': ['bit', 'byte'],

                  'offset': [int, str],
                  'repeats': [int, str],
                  "condition": [bool, str],
                  'content': [list]}

content_default = {'type': ['data'],
                   'name': [str],
                   'size': [int],
                   'size type': ['bit', 'byte'],

                   'value type': ['unsigned integer',
                                  'signed integer'
                                  'floating point value',
                                  'string',
                                  'boolean'],
                   'comment': [str]}


# Looking for JSON syntax errors
def load_file(file_name):
    """Reads JSON file and if there are no error, formats it"""
    with open(file_name, 'r') as file:  # opens file as read
        print('Looking for JSON syntax errors...')
        try:  # tests if json has valid syntax
            json_input = json.load(file)
            print('JSON syntax errors not found\n')
        except Exception as e:  # prints what is wrong
            print('JSON syntax error found:', e)
            print('Exiting program')
            exit()

    with open(file_name, 'w') as file:  # opens file as write
        # formats (pretty prints) JSON file
        json_output = json.dumps(json_input, indent='\t')
        file.write(json_output)
    return json_input


json_file = load_file('example.json')


# Looking for Key errors
def compare_keys(d_dict, r_dict):
    """Compares dictionaries keys"""
    d_keys = d_dict.keys()
    r_keys = r_dict.keys()
    if d_keys == r_keys:  # if keys are identical - skip all comparison
        pass
    else:
        for r_key in r_keys:  # checks if there are undocumented dictionary
            if r_key not in d_keys:
                print('Key error found:', r_key, 'should not be in',
                      r_dict['name'])
        for d_key in d_keys:  # checks if there are missing dictionary
            if d_key not in r_keys:
                print('Key error found:', d_key, 'should be in',
                      r_dict['name'])
                # exit()


def key_loop(item):
    """"loops around it self for content"""
    try:  # tries to see if it has 'content'
        content_dict = item['content']
        for content_item in content_dict:
            if content_item['type'] == 'data':
                compare_keys(content_default, content_item)
                # loops around it self
                key_loop(content_item)
            elif content_item['type'] == 'header':
                compare_keys(header_default, content_item)
                # loops around it self
                key_loop(content_item)
            else:
                print('cia')
    except KeyError:
        pass


print('Looking for Key errors...')
# iterates all keys in root
compare_keys(json_default, json_file)
# iterates all keys in 'data'
data_dict = json_file['data']
for data_item in data_dict:
    # print('header')
    compare_keys(header_default, data_item)
    key_loop(data_item)
print()


def compare_values():
    real_values = json_file['data']
    for r_value in real_values:
        # print(r_value['name'])
        # every real value type and default values list
        for item in r_value:
            found = False
            # print(item)
            # every default value in single key
            for d_value in header_default[item]:
                # if it founds it - exit local loop
                if type(r_value[item]) == d_value:
                    found = True
                    break
                # if it string - compare not type, but real values
                elif r_value[item] == d_value:
                    found = True
            if found:
                # print('found')
                pass
            else:
                # print('not found')
                pass
            # print()
            if type(r_value[item]) == list:
                pass
                # print('got it')


def value_loop(item):
    """"loops around it self for content"""
    try:  # tries to see if it has 'content'
        content_dict = item['content']
        for content_item in content_dict:
            if content_item['type'] == 'data':
                compare_keys(content_default, content_item)
                # loops around it self
                value_loop(content_item)
            elif content_item['type'] == 'header':
                # print('header')
                compare_keys(header_default, content_item)
                # loops around it self
                value_loop(content_item)
    except KeyError:
        pass


# compare_values()

"""
Looking for JSON syntax errors...
JSON syntax errors not found
JSON syntax error found: e
Exiting program

Looking for Key errors....
Key errors not found
Key error found: k should not be in l
Key error found: k should be in l
Exiting program

Looking for Value errors...
Value errors not found
Value error found: v should be v in l

"""
