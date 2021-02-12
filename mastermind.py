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
Main launcher for the game
'''

from engine import Engine

if __name__ == "__main__":
    inp = "y"
    while inp == "y":
        engine = Engine()
        engine.start()
        print("Game Over")
        inp = raw_input("Play again (y/n): ")
