import argparse

try:
    basestring
except NameError:
    raw_input = input

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from kian import model

parser = argparse.ArgumentParser(description='Initiate a model.')
parser.add_argument('--name', '-n', nargs='?',
                    help='name of the model. No space character!')
parser.add_argument('--wiki', '-w', nargs='?',
                    help='code of Wiki, e.g. enwiki, fawikivoyage')
parser.add_argument('--prop', '-p', nargs='?',
                    help='Number or id of property, e.g. P31, P17')
parser.add_argument('--value', '-v', nargs='?',
                    help='value of the property. e.g. Q31, Q183')

args = parser.parse_args()
if args.name:
    name = args.name
else:
    name = str(
        raw_input('Please provide a name. No space character:')).strip()
if args.wiki:
    wiki = args.wiki
else:
    wiki = str(raw_input('Code of Wiki, e.g. enwiki, fawikivoyage:')).strip()
if args.prop:
    property_name = args.prop
else:
    property_name = str(
        raw_input('Number or id of property, e.g. P31, P17:')).strip()
if args.value:
    value = args.value
else:
    value = str(raw_input('value of the property. e.g. Q31, Q183:')).strip()

if ' ' in name:
    name = name.replace(' ', '_')
if 'wiki' not in wiki:
    raise ValueError('Name of wiki is not valid.')
if not property_name.startswith('P'):
    try:
        int(property_name)
    except:
        raise ValueError('Invalid property name')
    else:
        property_name = 'P' + property_name
try:
    int(property_name[1:])
except:
    raise ValueError('Invalid property name')
if not value.startswith('Q'):
    try:
        int(value)
    except:
        raise ValueError('Invalid value')
    else:
        property_name = 'Q' + property_name
try:
    int(property_name[1:])
except:
    raise ValueError('Invalid value')

# TODO: Further settings.

model = model.Model(name=name, wiki=wiki, property_name=property_name,
                    value=value)
try:
    model.write_file()
except RuntimeError:
    print('The model with the same name already exists')
    choice = str(input('Overwrite?[Y]es, [N]ew name:'))
    if choice.lower().strip() == 'y':
        model.write_file(force=True)
    elif choice.lower.strip() == 'n':
        choice = str(input('New name:'))
        model.name = choice.strip().replace(' ', '_')
        model.write_model()
    else:
        raise ValueError('Not a valid option')
