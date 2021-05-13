def k_combs(k):
    nums = set(range(10))
    if k == 1:
        return [[i] for i in nums]
    return [el + [i] for el in k_combs(k-1) for i in nums.difference(el)]

def calc(pr_res, operator, operand):
    if operator == '+':
        return pr_res + operand
    elif operator == '-':
        return pr_res - operand

def word_to_num(word,lookup_dict):
    number = ''.join(str(lookup_dict[ch]) for ch in word)
    return number

def sum_puzzle(text):
    letters = {ch for ch in text if ch.isalpha()}
    if len(letters) > 10:
        print('Too many distinct letters (>10).')
        return
    operands = [[]]
    operators = []
    for ch in text:
        if ch.isalpha():
            operands[-1].append(ch)
        elif ch in {'+', '-'}:
            operands.append([])
            operators.append(ch)
        elif ch == '=':
            operands.append([])
    combs = k_combs(len(letters))
    res = []
    for comb in combs:
        mapping = dict(zip(letters, comb))
        # if mapping == {'T':9, 'R':8, 'A':7, 'N':6, 'H':5, 'Y':4, 'S':3, 'M':2, 'O':1, 'E':0}:
        #     print('here')
        zero_start = 0
        num_operands = []
        for operand in operands:
            num_operand = word_to_num(operand, mapping)
            if num_operand[0] == 0:
                zero_start = 1
                break
            else:
                num_operands.append(int(num_operand))
        if zero_start == 0:
            result = num_operands[0]
            for i in range(len(operators)):
                result = calc(result, operators[i], num_operands[i+1])
            if result == num_operands[-1]:
                res.append(mapping)
    return res

a = sum_puzzle('''SO+MANY+MORE+MEN+SEEM+TO+SAY+THAT+THEY+MAY+SOON+TRY+TO+STAY+AT+HOME+
                SO+AS+TO+SEE+OR+HEAR+THE+SAME+ONE+MAN+TRY+TO+MEET+THE+TEAM+ON+THE+
                MOON+AS+HE+HAS+AT+THE+OTHER+TEN=TESTS''')
print(a, len(a))