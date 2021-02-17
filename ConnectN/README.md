##TODO

- create a new minmax function that adds alpha beta pruning (don't delete the old one) Orlando
- modify training.py to print out a COMPLETE analysis JEREMY
    tokens_to_win = 3
    depth = 4
    H X W   Win/Loss/Ties (win/match)
    6 X 7       2/3/6
    7 X 9       0.5
    1 X 2       0.0
    5 X 5       0.92

    tokens_to_win = 4
    depth = 4
    Depth   Win/Loss
    H X W   Win/Loss
    6 X 7       0.3
    7 X 9       0.5
    1 X 2       0.9
    5 X 5       0.92

    tokens_to_win = 5
    depth = 4
    Depth   Win/Loss
    H X W   Win/Loss
    6 X 7       0.3
    7 X 9       0.5
    1 X 2       0.9
    5 X 5       0.92

- modify training.py to log to file every board where the AI Lost (Include all params, h, w, time_limit, tokens_to_win) JEREMY


    Future:
- Apply defensive_scalar to many parts of the AI (use it in a bunch of evaluation functions) <- use this offense 
- Learn by tuning
- Make a GOD API <-- Orlando
-
-
-




