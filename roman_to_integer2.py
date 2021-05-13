import re


def rom_2_int(roman_num):
    if not re.search('^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$', roman_num):
        raise ValueError('Invalid literal for a Roman number')

    conv_table = dict(M=1000, D=500, C=100, L=50, X=10, V=5, I=1)
    fin_num = 0
    for i in range(len(roman_num) - 1):
        if conv_table[roman_num[i]] < conv_table[roman_num[i + 1]]:
            fin_num -= conv_table[roman_num[i]]
        else:
            fin_num += conv_table[roman_num[i]]
    fin_num += conv_table[roman_num[-1]]

    return fin_num


roman_number = input('Please, enter a Roman number: ')
if roman_number == '':
    print('No input provided.')
else:
    print(rom_2_int(roman_number))
