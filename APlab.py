# Original Board
matrix = [
    ["#", "2", "2", "2", "#"],
    ["1", "*", "*", "*", "*"],
    ["1", "*", "*", "*", "*"],
    ["1", "*", "*", "*", "*"],
    ["#", "*", "*", "*", "#"]
]


def can_move(player_id: int, bead_num: int, board: list):  # Checking the ability for moving
    if player_id == 1:
        index = 0
        for i in range(5):
            if board[bead_num][i] == "1":
                index = i
                break
        if index == 4:
            return 0
        if index + 1 < 5 and board[bead_num][index + 1] == "2":
            if index + 2 < 5 and board[bead_num][index + 2] == "2":
                return 0
            return 2
        return 1
    else:
        index = 0
        for i in range(5):
            if board[i][bead_num] == "2":
                index = i
                break
        if index == 4:
            return 0
        if index + 1 < 5 and board[index + 1][bead_num] == "1":
            if index + 2 < 5 and board[index + 2][bead_num] == "1":
                return 0
            return 2
        return 1


def move(player_id: int, bead_num: int, board: list):  # Move the decided bead in the direction we want
    can_move_parameter = can_move(player_id, bead_num, board)
    if player_id == 1:
        i = 0
        index = 0
        while i < 5:
            if board[bead_num][i] == "1":
                index = i
                break
            i += 1
        if can_move_parameter == 1:
            board[bead_num][index + 1], board[bead_num][index] = board[bead_num][index], board[bead_num][index + 1]
        elif can_move_parameter == 2:
            board[bead_num][index + 2], board[bead_num][index] = board[bead_num][index], board[bead_num][index + 2]
    else:
        i = 0
        index = 0
        while i < 5:
            if board[i][bead_num] == "2":
                index = i
                break
            i += 1
        if can_move_parameter == 1:
            board[index + 1][bead_num], board[index][bead_num] = board[index][bead_num], board[index + 1][bead_num]
        elif can_move_parameter == 2:
            board[index + 2][bead_num], board[index][bead_num] = board[index][bead_num], board[index + 2][bead_num]
    return board


def check_lock(player_id: int, board: list):  # Checking if all the 3 beads for one player is locked
    flag = False
    if can_move(player_id, 1, board) == can_move(player_id, 2, board) == can_move(player_id, 3, board) == 0:
        flag = True
    return flag


def publish(board: list):  # Prints the board in the form we want
    print("----------")
    for i in board:
        print(*i)
    print("----------")


def check_win(board):  # Checks if one of the players has won
    flag = False
    if board[1][4] == board[2][4] == board[3][4] == "1":
        flag = True
    if board[4][1] == board[4][2] == board[4][3] == "2":
        flag = True
    return flag


def board_evaluation(player_id: int, board: list):  # Evaluates the board
    # Base case
    if player_id == 1:
        if board[1][4] == board[2][4] == board[3][4] == "1":
            return True
        if board[4][1] == board[4][2] == board[4][3] == "2":
            return False
    else:
        if board[4][1] == board[4][2] == board[4][3] == "2":
            return True
        if board[1][4] == board[2][4] == board[3][4] == "1":
            return False

    # Check if the player is locked, then returns the opposite value of the opponent player
    if check_lock(player_id, board):
        if player_id == 1:
            return not board_evaluation(2, board)
        else:
            return not board_evaluation(1, board)

    # Backtracking ( THE CORE PART OF THE CODE! )
    for i in range(1, 4):
        if can_move(player_id, i, board) != 0:
            board_copy1 = [board[0].copy(), board[1].copy(), board[2].copy(), board[3].copy(), board[4].copy()]
            board_copy1 = move(player_id, i, board_copy1)
            if player_id == 1:
                opponent_id = 2
                if not board_evaluation(opponent_id, board_copy1):
                    return True
            if player_id == 2:
                opponent_id = 1
                if not board_evaluation(opponent_id, board_copy1):
                    return True
    return False


def best_move(player_id: int):  # Returns the best move using board_evaluation
    for i in range(1, 4):
        if can_move(player_id, i, matrix) != 0:
            board_copy = [matrix[0].copy(), matrix[1].copy(), matrix[2].copy(), matrix[3].copy(), matrix[4].copy()]
            board_copy = move(player_id, i, board_copy)
            if player_id == 1:
                if not board_evaluation(2, board_copy):
                    return i
            else:
                if not board_evaluation(1, board_copy):
                    return i
    for i in range(1, 4):
        if can_move(player_id, i, matrix) != 0:
            return i


publish(matrix)
player_side = int(input("Please choose your side,\n1 or 2 ?: "))
while player_side != 1 and player_side != 2:
    player_side = int(input("Your given input is False.\nPlease choose 1 or 2: "))

turn = 1

while not check_win(matrix):  # It runs until one of the players wins
    if turn == 1:
        if player_side == 1:
            if not check_lock(1, matrix):
                bead = int(input("Please choose your bead,\n1, 2 or 3? :"))
                # Handling wrong input
                while bead != 1 and bead != 2 and bead != 3:
                    bead = int(input("Your given input is False.\nPlease enter 1, 2 or 3: "))
                while can_move(1, bead, matrix) == 0:
                    bead = int(input("Your decided bead can't move.\nPlease choose another one: "))
                move(1, bead, matrix)
                publish(matrix)
            else:
                print("You can not move any of your beads.\n YOU'RE LOCKED!")
        else:
            if board_evaluation(1, matrix):
                move(1, best_move(1), matrix)
                publish(matrix)
            else:  # When we don't have any best move, we choose the first bead we can
                for bead in range(1, 4):
                    if can_move(1, bead, matrix) != 0:
                        move(1, bead, matrix)
                        publish(matrix)
                        break
        turn = 2
    else:
        if player_side == 2:
            if not check_lock(2, matrix):
                bead = int(input("Please choose your bead,\n1, 2 or 3? :"))
                while bead != 1 and bead != 2 and bead != 3:
                    bead = int(input("Your given input is False.\nPlease enter 1, 2 or 3: "))
                while can_move(2, bead, matrix) == 0:
                    bead = int(input("Your decided bead can't move.\nPlease choose another one: "))
                move(2, bead, matrix)
                publish(matrix)
            else:
                print("You can not move any of your beads.\n YOU'RE LOCKED!")
        else:
            if board_evaluation(2, matrix):
                move(2, best_move(2), matrix)
                publish(matrix)
            else:
                for bead in range(1, 4):
                    if can_move(2, bead, matrix) != 0:
                        move(2, bead, matrix)
                        publish(matrix)
                        break
        turn = 1

# Winning
if matrix[1][4] == matrix[2][4] == matrix[3][4] == "1":
    if player_side == 1:
        print("You won the game.\nCongratulations!❤🎉")
    else:
        print("You lost💔")
if matrix[4][1] == matrix[4][2] == matrix[4][3] == "2":
    if player_side == 2:
        print("You won the game.\nCongratulations!❤🎉")
    else:
        print("You lost💔")
