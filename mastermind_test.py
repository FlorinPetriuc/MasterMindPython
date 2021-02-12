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
Unit tests for the game engine functionality
'''

import sys
from engine import Engine

'''
Generic function for printing results
'''
def test_validate(msg, expected, result):
    print(msg + ": "),
    if result == expected:
        print("PASSED")
    else:
        print("FAILED (" + str(expected) + " vs " + str(result) + ")")
        sys.exit()

'''
Test rows input
'''
def test_valid_rows():
    e = Engine()
    test_validate("Testing validate rows with invalid char", False, e._Engine__validate_and_assign_rows("a"))
    test_validate("Testing validate rows with 0 rows", False, e._Engine__validate_and_assign_rows("0"))
    for rows in range(1, 100):
        r = str(rows)
        test_validate("Testing validate rows with number " + r, rows in e._Engine__valid_rows, e._Engine__validate_and_assign_rows(r))

'''
Test variations input
'''
def test_valid_variations():
    e = Engine()
    test_validate("Testing validate variations with invalid char", False, e._Engine__validate_and_assign_variations("a"))
    for variations in range(1, 100):
        v = str(variations)
        test_validate("Testing validate variations with number " + v, variations >= 2, e._Engine__validate_and_assign_variations(v))

'''
Test code input
'''
def test_valid_code():
    e = Engine()
    e._Engine__variations = 50
    test_validate("Testing validate code with invalid char", False, e._Engine__validate_and_assign_code("a b c"))

    arr_too_short = [x for x in range(0, e._Engine__code_len_min - 1)]
    arr_too_sort_s = " ".join([str(a) for a in arr_too_short])
    test_validate("Testing validate code with an array too short", False, e._Engine__validate_and_assign_code(arr_too_sort_s))

    arr_too_long = [x for x in range(0, e._Engine__code_len_max + 1)]
    arr_too_long_s = " ".join([str(a) for a in arr_too_long])
    test_validate("Testing validate code with an array too long", False, e._Engine__validate_and_assign_code(arr_too_long_s))

    arr = [x for x in range(0, 100)]
    for i in range(e._Engine__code_len_min, e._Engine__code_len_max + 1):
        for idx in range(0, 100, i):
            subarr = arr[idx:idx + i]
            subarr_s = " ".join([str(x) for x in subarr])
            test_validate("Testing validate code with " + subarr_s, subarr[len(subarr) - 1] <= e._Engine__variations, e._Engine__validate_and_assign_code(subarr_s))

'''
Test that the random numbers for code follow the restrictions
'''
def test_valid_random_code():
    e = Engine()
    e._Engine__variations = 50
    for i in range(0, 100):
        e._Engine__validate_and_assign_code("")
        res = True
        for c in e._Engine__code:
            if c >= e._Engine__variations:
                res = False
        if len(e._Engine__code) < e._Engine__code_len_min:
            res = False
        if len(e._Engine__code) > e._Engine__code_len_max:
            res = False
        code_s = " ".join([str(x) for x in e._Engine__code])
        test_validate("Testing validate code with no input (" + code_s + ")", True, res)

'''
Test that the pegs input is validated properly
'''
def test_valid_pegs():
    e = Engine()
    e._Engine__variations = 50
    e._Engine__code = [0, 1, 2, 3]
    test_validate("Testing validate pegs with an array too short", True, e._Engine__validate_and_return_pegs("0 1 2") is None)
    test_validate("Testing validate pegs with an array too long", True, e._Engine__validate_and_return_pegs("0 1 2 3 4") is None)
    test_validate("Testing validate pegs with an invalid char", True, e._Engine__validate_and_return_pegs("0 1 2 a") is None)
    test_validate("Testing validate pegs with a negative number", True, e._Engine__validate_and_return_pegs("0 1 2 -1") is None)
    test_validate("Testing validate pegs with a number too large", True, e._Engine__validate_and_return_pegs("0 1 2 50") is None)
    test_validate("Testing validate pegs with a valid input", True, e._Engine__validate_and_return_pegs("0 1 2 49") is not None)

'''
Test the full matches function
'''
def test_full_matches():
    e = Engine()
    e._Engine__code = [1, 2, 3, 4]
    test_validate("Testing full matches with 1 match", 1, e._Engine__get_full_matches([1, 3, 2, 5]))
    test_validate("Testing full matches with 2 matches", 2, e._Engine__get_full_matches([1, 3, 3, 5]))
    test_validate("Testing full matches with 3 matches", 3, e._Engine__get_full_matches([1, 3, 3, 4]))
    test_validate("Testing full matches with 4 matches", 4, e._Engine__get_full_matches([1, 2, 3, 4]))

'''
Test the partial matches function
'''
def test_partial_matches():
    e = Engine()
    e._Engine__code = [1, 2, 3, 4]
    test_validate("Testing partial matches with 1 match", 1, e._Engine__get_partial_matches([1, 4, 3, 3]))
    test_validate("Testing partial matches with 2 matches", 2, e._Engine__get_partial_matches([1, 4, 3, 2]))
    test_validate("Testing partial matches with 3 matches", 3, e._Engine__get_partial_matches([3, 4, 0, 2]))
    test_validate("Testing partial matches with 4 matches", 4, e._Engine__get_partial_matches([3, 4, 1, 2]))

'''
Test the game iterate function when winning
'''
def test_game_iterate_win():
    e = Engine()
    e._Engine__code = [1, 2, 3, 4]
    e._Engine__rows = 4
    res = e._Engine__game_iterate([0, 1, 2, 3])
    test_validate("Testing full matches at 1st win iteration", 0, res["full_matches"])
    test_validate("Testing partial matches at 1st win iteration", 3, res["partial_matches"])
    test_validate("Testing game over at 1st win iteration", False, e._Engine__game_over)
    test_validate("Testing win at 1st win iteration", False, e._Engine__win)
    test_validate("Testing game row at 1st win iteration", 1, e._Engine__crt_row)
    res = e._Engine__game_iterate([1, 1, 2, 3])
    test_validate("Testing full matches at 2nd win iteration", 1, res["full_matches"])
    test_validate("Testing partial matches at 2nd win iteration", 2, res["partial_matches"])
    test_validate("Testing game over at 2nd win iteration", False, e._Engine__game_over)
    test_validate("Testing win at 2nd win iteration", False, e._Engine__win)
    test_validate("Testing game row at 2nd win iteration", 2, e._Engine__crt_row)
    res = e._Engine__game_iterate([1, 2, 2, 3])
    test_validate("Testing full matches at 3rd win iteration", 2, res["full_matches"])
    test_validate("Testing partial matches at 3rd win iteration", 1, res["partial_matches"])
    test_validate("Testing game over at 3rd win iteration", False, e._Engine__game_over)
    test_validate("Testing win at 3rd win iteration", False, e._Engine__win)
    test_validate("Testing game row at 3rd win iteration", 3, e._Engine__crt_row)
    res = e._Engine__game_iterate([1, 2, 3, 4])
    test_validate("Testing full matches at 4th win iteration", 4, res["full_matches"])
    test_validate("Testing partial matches at 4th win iteration", 0, res["partial_matches"])
    test_validate("Testing game over at 4th win iteration", True, e._Engine__game_over)
    test_validate("Testing win at 4th win iteration", True, e._Engine__win)
    test_validate("Testing game row at 4th win iteration", 4, e._Engine__crt_row)

'''
Test the game iterate function when losing
'''
def test_game_iterate_lose():
    e = Engine()
    e._Engine__code = [1, 2, 3, 4]
    e._Engine__rows = 4
    res = e._Engine__game_iterate([4, 3, 2, 1])
    test_validate("Testing full matches at 1st lose iteration", 0, res["full_matches"])
    test_validate("Testing partial matches at 1st lose iteration", 4, res["partial_matches"])
    test_validate("Testing game over at 1st lose iteration", False, e._Engine__game_over)
    test_validate("Testing win at 1st lose iteration", False, e._Engine__win)
    test_validate("Testing game row at 1st lose iteration", 1, e._Engine__crt_row)
    res = e._Engine__game_iterate([0, 3, 1, 2])
    test_validate("Testing full matches at 2nd lose iteration", 0, res["full_matches"])
    test_validate("Testing partial matches at 2nd lose iteration", 3, res["partial_matches"])
    test_validate("Testing game over at 2nd lose iteration", False, e._Engine__game_over)
    test_validate("Testing win at 2nd lose iteration", False, e._Engine__win)
    test_validate("Testing game row at 2nd lose iteration", 2, e._Engine__crt_row)
    res = e._Engine__game_iterate([1, 2, 2, 3])
    test_validate("Testing full matches at 3rd lose iteration", 2, res["full_matches"])
    test_validate("Testing partial matches at 3rd lose iteration", 1, res["partial_matches"])
    test_validate("Testing game over at 3rd lose iteration", False, e._Engine__game_over)
    test_validate("Testing win at 3rd lose iteration", False, e._Engine__win)
    test_validate("Testing game row at 3rd lose iteration", 3, e._Engine__crt_row)
    res = e._Engine__game_iterate([1, 2, 3, 0])
    test_validate("Testing full matches at 4th lose iteration", 3, res["full_matches"])
    test_validate("Testing partial matches at 4th lose iteration", 0, res["partial_matches"])
    test_validate("Testing game over at 4th lose iteration", True, e._Engine__game_over)
    test_validate("Testing win at 4th lose iteration", False, e._Engine__win)
    test_validate("Testing game row at 4th lose iteration", 4, e._Engine__crt_row)

if __name__ == "__main__":
    test_valid_rows()
    test_valid_variations()
    test_valid_code()
    test_valid_random_code()
    test_valid_pegs()
    test_full_matches()
    test_partial_matches()
    test_game_iterate_win()
    test_game_iterate_lose()
