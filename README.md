# Checkers

### Alpha-Beta Pruning (checkers.py)

Play against a checkers AI powered by a tree search with alpha-beta pruning. On your turn, use the left and right arrow keys to select a move, and press up to execute. Once the computer moves, press space to advance to your turn.

To adjust how many moves ahead the computer analyzes, adjust MAXDEPTH near the beginning of the source code.

### Neural Net (parser.py, CheckersTraining.ipynb)

A neural net trained to predict the outcome of a checkers game from the current board configuration

Running the parser script on game_data_raw.txt (downloaded from http://www.fierz.ch/download.php) produces an output file game_data_processed.csv which stores each board configuration from each game as a 33 component vector.  The first 32 components tell for each of the 32 accessible squares which piece is on the square (+/- for black/red with an absolute value of 1 for a regular piece, 2 for a king, and 0 for an empty square).  See http://www.bobnewell.net/nucleus/checkers.php?itemid=289 for details about the board numbering.  The final component is 1 or -1 corresponding respectively to a win for black or red.  (Draws are ommitted by the parser.)

Then running CheckersTraining.ipynb trains a neural net saved as checkers_net.pt.  My best validation accuracy so far (corresponding to the file on GitHub) is 73%, but I hope to improve this and possibly at a later time combine this with the alpha-beta pruning project, using the neural net as the heuristic when the maximum recursion depth is attained.  Curiously, removing the early game boards (as there is likely to be not much predictive power for these) only leads to a 3% improvement in the validation accuracy.
