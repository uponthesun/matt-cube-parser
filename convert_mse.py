import sys
from zipfile import ZipFile

usage = \
"""
Usage: 
python convert_mse.py input_file.csv

input_file.csv should be an input file in the format of Matt's custom cube spreadsheet, exported as csv.
The output of the script is two files:
output.mse-set - Magic Set Editor file.
failed.txt - Text file containing the input lines which failed to be parsed, likely because of being
improperly formatted, or possibly because of a bug in the script.
"""

if len(sys.argv) < 2 or sys.argv[1] == 'help' or sys.argv[1] == '--help':
    print(usage)
    exit()

debug = False
input_file_name = sys.argv[1]

with open(input_file_name, 'rb') as f:
    raw_input_string = f.read().decode('utf-8')

# The spreadsheet format has the mana cost, P/T, and rules text all in one cell, separated by
# newlines. Google Spreadsheets saves those in-cell newlines as \n, and uses \r\n to separate
# rows. Therefore, we do some processing here to replace \n with |, and split on \r\n to,
# so we have a list where each line is a string representing a single card with no newlines in it.
rules_text_delimiter = '|'
raw_cards = raw_input_string \
    .replace('\n', rules_text_delimiter) \
    .split('\r{0}'.format(rules_text_delimiter))

# Filter out empty rows.
raw_cards = list(filter(lambda x: len(x.strip(',').strip()) > 0, raw_cards))

# Files with parts of the MSE output format.
with open('header.txt', 'r') as f:
    header = ''.join(f.readlines())
with open('footer.txt', 'r') as f:
    footer = ''.join(f.readlines())
with open('card_template.txt', 'r') as f:
    template = ''.join(f.readlines())

def parse_card(card):
    card_split = card.split(',')
    name, type = card_split[0:2]
    text = ','.join(card_split[2:]).replace('"', '')

    if debug:
        print("name: " + str(name))
        print("type: " + str(type))
        print("text: " + str(text))

    text_split = text.split(rules_text_delimiter)
    if 'Creature' in type:
        cost, pt = text_split[0:2]
        rules_text = '\n\t\t'.join(text_split[2:])
        power, toughness = pt.split('/')
    else:
        cost = text_split[0]
        rules_text = '\n\t\t'.join(text_split[1:])
        power, toughness = '', ''
    
    if debug:
        print("cost: " + str(cost))
        print("power: " + str(power))
        print("toughness: " + str(toughness))
        print("rules text: " + str(rules_text))
    
    result = template.replace('{name}', name.strip()) \
                            .replace('{cost}', cost.strip()) \
                            .replace('{rules}', rules_text.strip()) \
                            .replace('{power}', power.strip()) \
                            .replace('{toughness}', toughness.strip()) \
                            .replace('{type}', type.strip())
    return result

output = []
failed_lines = []

for card in raw_cards:
    try:
        output.append(parse_card(card))
    except Exception as e:
        if debug: 
            print(e)
        failed_lines.append(card)

# A .mse-set file is just a .zip archive with a single text file called 'set' in it.
set_filename = 'set'
with open(set_filename, 'w') as f:
    f.write(header + '\n')
    for line in output:
        f.write(line + '\n')
    f.write(footer)
with ZipFile('output.mse-set', 'w') as z:
    z.write(set_filename)

# Write a file containing failed lines so it's easier to correct invalid input.
with open('failed.txt', 'w') as f:
    for line in failed_lines:
        f.write(line + '\n')
        
print("Successfully processed {0} cards; {1} failed cards.".format(len(output), len(failed_lines)))