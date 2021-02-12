'''
 * Copyright (C) 2021 Florin Petriuc. All rights reserved.
 * Initial release: Florin Petriuc <petriuc.florin@gmail.com>
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License version
 * 2 as published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
'''

'''
Main engine functionality for the game
'''

from random import randint

class Engine:
    def __init__(self):
        self.__valid_rows = [6, 8, 12, 19]
        self.__code_len_min = 4
        self.__code_len_max = 6
        self.__game_over = False
        self.__win = False
        self.__rows = 0
        self.__crt_row = 0
        self.__variations = 0
        self.__code = []

    '''
    Validates the input string and assigns the value to the __rows variable
    '''
    def __validate_and_assign_rows(self, rows):
        try:
            self.__rows = int(rows)
        except Exception as e:
            print("Invalid input: " + rows + " (" + str(e) + ")")
            print("Try again")
            return False
        if self.__rows == 0:
            print("Invalid input: 0 (Number is not supported)")
            print("Try again")
            return False
        if self.__rows not in self.__valid_rows:
            self.__rows = 0
            print("Invalid input: " + rows + " (Number is not supported)")
            print("Try again")
            return False
        return True

    '''
    Validates the input string and assigns the value to the __variations variable
    '''
    def __validate_and_assign_variations(self, variations):
        try:
            self.__variations = int(variations)
        except Exception as e:
            print("Invalid input: " + variations + " (" + str(e) + ")")
            print("Try again")
            return False
        # It makes no sense to have 1 or less variations
        # 1 variation means all the elements in the code array must have the same value
        if self.__variations < 2:
            self.__variations = 0
            print("Invalid input: " + variations + " (Number is not supported)")
            print("Try again")
            return False
        return True

    '''
    Validates the input string and assigns the __code array
    If the input string is empty, a random array is generated for code
    '''
    def __validate_and_assign_code(self, code):
        if code == "":
            self.__code = [randint(0, self.__variations - 1) for i in range(randint(self.__code_len_min, self.__code_len_max))]
        else:
            try:
                self.__code = [int(c) for c in code.split()]
            except Exception as e:
                print("Invalid input " + code + "(" + str(e) + ")")
                print("Try again")
                return False
            l = len(self.__code)
            if l < self.__code_len_min or l > self.__code_len_max:
                print("Invalid input (Invalid number of entries " + str(l) + ")")
                print("Try again")
                self.__code = []
                return False
            for c in self.__code:
                if c < 0:
                    print("Invalid input (Code number must be positive)")
                    print("Try again")
                    self.__code = []
                    return False
                if c >= self.__variations:
                    print("Invalid input (Code number must not be greater than variations)")
                    self.__code = []
                    return False
        return True

    '''
    Validates and returns the current pegs input from the user as an int array
    '''
    def __validate_and_return_pegs(self, pegs):
        ret = pegs.split()
        if len(ret) != len(self.__code):
            print("Invalid input " + pegs + " (You must input " + str(len(self.__code)) + " numbers)")
            return None
        try:
            ret = [int(x) for x in ret]
        except Exception as e:
            print("Invalid input " + pegs + "(" + str(e) + ")")
            return None
        for peg in ret:
            if peg >= self.__variations:
                print("Invalid input " + pegs + " (Peg must not be greater than variations))")
                return None
            if peg < 0:
                print("Invalid input " + pegs + " (Peg must be a psotive number))")
                return None
        return ret

    '''
    Returns the number of full matches from a guess
    '''
    def __get_full_matches(self, pegs):
        ret = 0
        for i in range(0, len(pegs)):
            if self.__code[i] == pegs[i]:
                ret += 1
        return ret

    '''
    Returns the number of partial matches from a guess
    '''
    def __get_partial_matches(self, pegs):
        ret = 0
        _code = [c for c in self.__code]
        for i in range(0, len(self.__code)):
            if self.__code[i] == pegs[i]:
                # full match
                continue
            for j in range(0, len(self.__code)):
                if self.__code[j] == pegs[j]:
                    # full match
                    continue
                if pegs[i] == _code[j]:
                    _code[j] = -1
                    ret += 1
                    # break on first match to avoid multiple matches for 1 peg
                    break
        return ret

    '''
    Iterates the game based on the pegs input
    '''
    def __game_iterate(self, pegs):
        self.__crt_row += 1
        full_matches = self.__get_full_matches(pegs)
        partial_matches = 0
        if full_matches == len(self.__code):
            self.__win = True
            self.__game_over = True
        else:
            partial_matches = self.__get_partial_matches(pegs)
        if self.__crt_row >= self.__rows:
            self.__game_over = True
        return { "full_matches": full_matches, "partial_matches": partial_matches }

    '''
    Reads input for rows from stdin
    '''
    def __init_rows(self):
        valid_rows = ",".join([str(r) for r in self.__valid_rows])
        rows = raw_input("Number of rows (" + valid_rows + "): ")
        while self.__validate_and_assign_rows(rows) == False:
            rows = raw_input("Number of rows (" + valid_rows + "): ")

    '''
    Reads input for variations from stdin
    '''
    def __init_variations(self):
        variations = raw_input("Number of variations: ")
        while self.__validate_and_assign_variations(variations) == False:
            variations = raw_input("Number of variations: ")

    '''
    Reads input for code from stdin
    '''
    def __init_code(self):
        format = "%d %d ... %d - between " + str(self.__code_len_min) + " and " + str(self.__code_len_max)
        code = raw_input("Code (leave empty for random, format is " + format + "): ")
        while self.__validate_and_assign_code(code) == False:
            code = raw_input("Code (leave empty for random, format is " + format + "): ")

    '''
    Read the current pegs guess from stdin
    '''
    def __input_pegs(self):
        pegs = raw_input("Pegs " + str(self.__crt_row) + ": ")
        ret = self.__validate_and_return_pegs(pegs)
        while ret is None:
            pegs = raw_input("Pegs " + str(self.__crt_row) + ": ")
            ret = self.__validate_and_return_pegs(pegs)
        return ret

    '''
    Starts the game
    '''
    def start(self):
        self.__init_rows()
        self.__init_variations()
        self.__init_code()
        # Clear the console to hide the code
        print("\033[H\033[J")
        print("Number of pegs per row: " + str(len(self.__code)))
        print("Variations " + str(self.__variations))
        while self.__game_over == False:
            pegs = self.__input_pegs()
            result = self.__game_iterate(pegs)
            print("You got " + str(result["full_matches"]) + " black pegs and " + str(result["partial_matches"]) + " white pegs")
        if self.__win:
            print("You won!")
        else:
            print("You lost!")
            print("Code was " + " ".join([str(x) for x in self.__code]))
