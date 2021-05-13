# Learning-Python

These are some of the codes I wrote while learning Python, those that seem more fun to me.

test_operations_new.py
----------------------
If you're like me, than learning something you try to understand every single bit and every hidden detail of that something. Obviously not a good approach for Python or anything as extensive as Python, but there was a time I was still trying to do that. After all, Python has hundreds if not thousands of libraries and modules, so I figured I should at least fully comprehend the Built-in module of the Standard library. This means understanding each and every operation, function and method, how exactly they work for each supported type and what the result/type would be for various arguments. Eventually I got tired of testing each function/method operation for all built-in types and realized I should automate it. So this file is a module with test functions that take dictionaries of objects and operations/functions/methods to test all for all. In particular, it has six main functions to test 1) unary operations, 2) binary operations, 3) unary methods, 4) binary methods, 5) functions taking one argument, 6) functions taking two arguments. It also has some mini helper functions used by the main tester functions for error handling, etc. The results are beautiful Excel spreadsheets with all arguments/operands lined along axes and operation/function/method results and respective type in the intersections.

roman_to_integer2.py
--------------------
A simple fun code to convert Roman numbers to integers. But I enjoyed making it the way to fully filter invalid Roman numbers with a beautiful regex check.

number_guesser_universal.py
---------------------------
Again a simple, quite popular game to code when learning Python. The task was to write it to guess a number between 1 and 1000 in 10 guesses and I wrote a universal thing to guess any number between any valid endpoints within minimum number of guesses.

Employee_class
--------------
The usual form for the HR to keep employee records. Might seem simple or boring, but just think of all the mishaps if any detail is missed. It should be open for adding employees and editing their info as it changes (after all people do get salary raises from time to time), but how to ensure that a woman does not accidentally become a man without any doctor appointment or not to make someone leave the company before they join? Also, it's easy to ensure that names are strings and phone numbers are numbers of specific format, and even easier to automatically construct corporate format email addresses from employee names and surnames. But wait! What if two or more people have the same name? Maybe we shouldn't hire the second one or ask them to change their name... Well, we won't for this code takes care of all that. As a bonus, we can compare employees by tenure and even form teams.

Summation_puzzle
----------------
I used to think I'm good at those. After all, it doesn't take a PHD to solve 'base + ball = games' and even 'Kyoto + Osaka = Tokyo'. But I challenged myself to code a universal solution for all possible summation problems. Can't insist my code works on all of them and in all languages but it worked on whatever I tested including the longest one according to Wikipedia (SO + MANY + MORE + MEN + SEEM + TO + SAY + THAT + THEY + MAY + SOON + TRY + TO + STAY + AT + HOME + SO + AS + TO + SEE + OR + HEAR + THE + SAME + ONE + MAN + TRY + TO + MEET + THE + TEAM + ON + THE + MOON + AS + HE + HAS + AT + THE + OTHER + TEN = TESTS). In case you'd like to test it yourself, be ready to wait a bit.

