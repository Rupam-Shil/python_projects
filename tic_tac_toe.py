import itertools

game = [[2, 0, 2],
        [2, 0, 0],
        [1, 1, 1],
        ]


def win(current_game):
    def all_same(l):
        if l.count(l[0]) == len(l) and l[0] != 0:
            return True
        else:
            return False

    # Horizontal
    for row in game:
        print(row)
        if all_same(row):
            print("Player {}  is the winner horizontally".format(row[0]))
            return True
    # diagoanal
    diags = []
    for col, row in enumerate(reversed(range(len(game)))):
        diags.append(game[row][col])
    if all_same(diags):
        print("Player {}  is the winner diagonally".format(diags[0]))
        return True
    diags = []
    for ix in range(len(game)):
        diags.append(game[ix][ix])
    if all_same(diags):
        print("Player {}  is the winner diagonally".format(diags[0]))
        return True

    # Vertical
    for col in range(len(game)):
        check = []
        for row in game:
            check.append(row[col])
        if all_same(check):
            print("Player {}  is the winner vertically".format(check[0]))
            return True

    return False


def game_board(game_map, player=0, row=0, column=0, just_display=False):
    try:
        if game_map[row][column] != 0:
            print("This position is occupied")
            return game_map, False
        print("   " + "  ".join(str(i) for i in range(len(game_map))))
        if not just_display:
            game_map[row][column] = player

        for index, row in enumerate(game_map):
            print(index, row)
        return game_map, True

    except IndexError as e:
        print("Something went wrong! Did you enter row/column as 0 or 2?", e)
        return game_map, False
    except Exception as e:
        print("Something went very wrong", e)
        return game_map, False


play = True
players = [1, 2]
while play:
    game = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            ]
    game_won = False
    game, _ = game_board(game, just_display=True)
    player_choice = itertools.cycle([1, 2])
    while not game_won:
        current_player = next(player_choice)
        print(f"Current Player is no: {current_player}")
        played = False

        while not played:
            column_choice = int(input('''What column you want play?(0,1,2): '''))
            row_choice = int(input('''What row you want to play (0,1,2): '''))
            game, played = game_board(game,
                                      current_player,
                                      row_choice,
                                      column_choice)

        if win(game):
            game_won = True
            again = input("""The game is over , would you like to play again(y/n)""")
            if again.casefold() == "y":
                print("restarting...")
            elif again.lower() == "n":
                print("Byee")
                play = False
            else:
                print("Not a valid answer,So see you later")

# game = game_board(game, just_display=True)
# game = game_board(game, player=1, row=10, column=1)
# game = game_board(game, 2, 1, 2)
