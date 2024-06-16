# Battleship-on-Python

## Description
Battleship (also Battleships or Sea Battle) is a guessing game for two players. It is played on ruled grids
(paper or board) on which the players' fleets of ships (including battleships) are marked. The locations of
the fleet are concealed from the other player. Players alternate turns calling `shots' at the other player's
ships, and the objective of the game is to destroy the opposing player's fleet.

Battleship is known worldwide as a pencil and paper game which dates from World War I. It was
published by various companies as a pad-and-pencil game in the 1930s, and was released as a plastic board
game by Milton Bradley in 1967. The game has spawned electronic versions, video games, smart device apps
and a film. (from the Wikipedia article on Battleship (the game)).


## Game-of-battleship

Battleship is a classic two person game, originally played with pen and paper.

On a grid (typically 10 x 10), players ’hide’ ships of mixed length; horizontally or vertically (not diagonally) without any overlaps. The exact types and number of ships varies by rule, but for this posting, I’m using ships of lengths: 5, 4, 3, 3, 2 (which results in 17 possible targets out of the total of 100 squares).

Note: even though ships cannot overlap, there is nothing in the rules to say they cannot touch. (In fact, some players consider this a strategy to confuse an opponent by obfuscating the true layout of ships. If there are five ‘hits’ in a row, a naive player might consider this to be the successful destruction of an aircraft carrier of length 5, but actually it could be the sinking of a battleship of length 4, and part of a cruiser of length 3)

## Simple Game Rules

We’ll start with a description of the simplified method of play:

After each player has hidden his fleet, players alternate taking shots at each other by specifying the coordinates of the target location. After each shot, the opponent responds with either a call HIT! or MISS! indicating whether the target coordinates have hit part of a boat, or open water. An example of a game in progress is show on the left.

## Game Stratergy

### Sinking Stratergy

Initially, shots can be fired at random, but once part of a ship has been hit, it's possible to search up, down, left and right looking for more of the same ship.

A simple implementation of this refined strategy is to create a stack of potential targets. Initially, the computer is in Hunt mode, firing at random. Once a ship has been 'winged' then the computer switches to Target mode. After a hit, the four surrounding grid squares are added to a stack of 'potential' targets (or less than four if the cell was on an edge/corner).

Cells are only added if they have not already been visited (there is no point in re-visiting a cell if we already know that it is a Hit or Miss).

Once in Target mode the computer pops off the next potential target off the stack, fires a salvo at this location, acts on this (either adding more potential targets to the stack, or popping the next target location off the stack), until either all ships have been sunk, or there are no more potential targets on the stack, at which point it returns to Hunt mode and starts firing at random again looking for another ship.

Even though far from elegant, this algorithm produces signifincantly better results than random firing. It is, however, a long way from efficient as it has no concept of what constitutes a ship, and blindly needs to walk around all surrounding edges of every hit pixel (with the exception of the last hit one), making sure there are no more ships touching.

![]([https://github.com/ashwani-mittal/Battleship-Game-Simulator/blob/master/Battleship.png](https://github.com/ashwani-mittal/Battleship-Game-Simulator/blob/main/Battleship.png))

### Hunting Stratergy

Now that we will be told when a ship is sunk, we know which ships (and even more importantly what the lengths of the ships) are still active. These facts are very valuable in determining which location we search next.

Our new algorithm will calculate the most probably location to fire at next based on a superposition of all possible locations the enemy ships could be in.

At the start of every new turn, based on the ships still left in the battle, we’ll work out all possible locations that every ship could fit (horizontally or vertically).

Initially, this will be pretty much anywhere, but as more and more shots are fired, some locations become less likely, and some impossible. Every time it’s possible for a ship to be placed in over a grid location, we’ll increment a counter for that cell. The result will be a superposition of probabilities


## Reference
http://www.datagenetics.com/blog/december32011/
