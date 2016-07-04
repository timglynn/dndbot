#!/usr/bin/env python

final_dict = dict()


num_of_fields = input('Number of columns in table: ')
output_file = input('Output filename is: ')

field_names = list()
for i in range(0, int(num_of_fields)):
    curr_name = input('What is the name of the %s field: ' %str(i + 1))
    field_names.append(curr_name)


loop_num = input("How many rows to add? ")

print("Building the file")


for loop in range(0, loop_num):
    key_name = input('What is the key name? ')

    final_dict[key_name] = dict()
    for name in field_names:
        final_dict[key_name][name] = input('Enter ' + name + ' for ' + \
                key_name + " : ")

with open(output_file, 'w') as ot:
    ot.write(str(final_dict))



