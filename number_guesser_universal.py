def number_guesser_main(low, high, guesses, guess=1):
    guess_num = (high + low) // 2
    print(f'My guess number {guess}: {guess_num}')
    guess += 1
    ans = input()
    if ans == '0':
        print(f'I guessed in {guess - 1} steps!')
    elif guess > guesses:
        print(f'I couldn’t guess in {guess - 1} steps! This means you cheated!')
    elif ans == '1':
        number_guesser_main(guess_num + 1, high, guesses, guess)
    elif ans == '-1':
        number_guesser_main(low, guess_num - 1, guesses, guess)
    else:
        print('''Please, enter a valid answer:
                - 0, if my guess is true
                - 1, if my guess is smaller than your number
                - -1, if my guess is larger than your number.''')
        number_guesser_main(low, high, guesses, guess - 1)


def number_guesser(low, high):
    if not isinstance(low, (int, float)) or not isinstance(high, (int, float)):
        raise TypeError('"high" and "low" should be numbers.')
    if low < 1 or high < 1 or high < low:
        raise ValueError('"low" and "high" should be positive numbers and "high" should be larger than "low".')
    nums_length = high - low + 1
    guesses = 1
    while nums_length / 2 >= 1:
        nums_length /= 2
        guesses += 1
    if input(f'''Think of a number between {low} and {high} and I'll guess it in maximum {guesses} steps.
Input 0 once you’re ready to play.\n''') == '0':
        number_guesser_main(low, high, guesses)
    else:
        print('Guesser stopping.')


number_guesser(9, 12)
