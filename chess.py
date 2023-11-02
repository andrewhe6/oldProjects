import sys
import random
import time
from colorama import init, Back, Style
from termcolor import colored
from copy import deepcopy

init() # initializes colorama

# defines the class for the pieces, name is the name displayed on the board like 'P' for Pawn, color determines which player owns that piece
class Piece:
    def __init__(self, name, color):
        self.name = name
        self.color = color

class Pawn(Piece):
    pass
class Rook(Piece):
    pass
class Knight(Piece):
    pass
class Bishop(Piece):
    pass
class Queen(Piece):
    pass
class King(Piece):
    pass
class Empty(Piece):
    pass

# declared outside function so its value remains even if players play again, holds the number of wins of each player
whiteWin = 0
blackWin = 0


# functions controls the main game loop
def main():
    # creating board to keep track of moves used for calculations
    board = [
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
    ]

    # creating board that will actually be displayed to the player
    display = [
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
    ]

    # adds pieces into the board in the stndard chess position
    for col in range(8):
        board[1][col] = Pawn(" P ", "black")
        board[6][col] = Pawn(" P ", "white")
    for row in range(2, 6):
        for col in range(8):
            board[row][col] = Empty("   ", "empty")

    board[7][4] = King(" K ", "white")
    board[0][4] = King(" K ", "black")

    board[7][2] = Bishop(" B ", "white")
    board[7][5] = Bishop(" B ", "white")
    board[0][2] = Bishop(" B ", "black")
    board[0][5] = Bishop(" B ", "black")

    board[7][1] = Knight(" N ", "white")
    board[7][6] = Knight(" N ", "white")
    board[0][1] = Knight(" N ", "black")
    board[0][6] = Knight(" N ", "black")

    board[7][3] = Queen(" Q ", "white")
    board[0][3] = Queen(" Q ", "black")

    board[7][0] = Rook(" R ", "white")
    board[7][7] = Rook(" R ", "white")
    board[0][0] = Rook(" R ", "black")
    board[0][7] = Rook(" R ", "black")

    againstBot = False
    colorChoice = ""
    stalemate = False
    checkmate = False
    playerTurn = "white"
    turnCount = 1
    global enPassant
    enPassant = False
    global enPassantPosition
    enPassantPosition = ""
    global wShortCastle
    global wLongCastle
    global bShortCastle
    global bLongCastle
    wShortCastle = True
    wLongCastle = True
    bShortCastle = True
    bLongCastle = True
    global whiteWin
    global blackWin

    # prints out the rules, then waits 1 second before starting the game
    print("\n---Chess---")
    print("This is a recreation of Chess with all the major features. Put the enemy king in checkmate to win!")
    print("Format your input as '[coordinate of the piece you want to move] [coordinate of the square you want to move to]' ")
    print("Input with the letters first, then numbers. Eg: 'e2e4' moves the piece on e2 to the e4 square. Capitalization does not matter")
    print("If you need extra help with moves, type 'moves' to get a list of all possible moves in your current position")
    print("If you have never played Chess before, input 'help' and 'rules' to learn about the game, rules, and different pieces")
    time.sleep(1)

    # asks if the user wants to play against the bot, loops until the user inputs 1 or 2, 1 means playing against player, 2 means playing against the bot
    while againstBot != "1" or againstBot != "2":
        againstBot = input("\nDo you want to play against another player (find a real life partner) or an AI bot (bot plays randomly)? Type 1 or 2. \n1 - Player \n2 - Bot \n")
        againstBot = againstBot.replace(" ", "")
        if againstBot == "1":
            againstBot = False
            break
        elif againstBot == "2":
            againstBot = True
            # if the player chooses bot, loop until the player decides what color they want to play as
            while colorChoice != "white" or colorChoice != "black":
                colorChoice = input("\nDo you want to play as white or black? White always moves first. The bot will play as the other color. \nType white or black: ")
                colorChoice = colorChoice.lower().replace(" ", "")
                if colorChoice == "white":
                    print("\nYou will play as white.")
                    break
                elif colorChoice == "black":
                    print("\nYou will play as " + colored("black", "red") + ".")
                    break
            break

    while stalemate == False or checkmate == False:
        # updates the display board according to the positions of the pieces on the board
        update_display_board(board, display)
        print("\n   | a | b | c | d | e | f | g | h | Wins: " + str(blackWin))
        print("---+---+---+---+---+---+---+---+---+---")
        for row in range(8):
            # prints the number coordinates then prints a row of the display board
            print(" " + str(abs(8 - row)) + " |", end="")
            print("|".join(display[row]), end="")
            print("| " + str(abs(8 - row)))
            print(Style.RESET_ALL + "---+---+---+---+---+---+---+---+---+---")
        print("   | a | b | c | d | e | f | g | h | Wins: " + str(whiteWin) + "\n")

        # takes the current position and finds all the possible moves that the current player can make
        possibleMovesList = find_possible_moves(playerTurn, board)
        if len(possibleMovesList) == 0:
            # if the player has no legal moves, check if its checkmate or stalemate
            if check_king_attacked(playerTurn, board) == True:
                checkmate = True
                break
            else:
                stalemate = True
                break

        legalMove = False
        # loops until the player gives a legal move
        while legalMove == False:
            if againstBot == True:
                # prompts player for move on their turn, then checks if its one of the legal moves
                if colorChoice == playerTurn:
                    if playerTurn == "black":
                        playerMove = input("* Player " + colored(playerTurn, "red") + "'s move: ")
                    else:
                        playerMove = input("* Player " + playerTurn + "'s move: ")
                    playerMove = playerMove.replace(" ", "")
                    for possibleMove in possibleMovesList:
                        if playerMove == possibleMove:
                            legalMove = True
                            break
                    else:
                        print(help_menu(playerMove, playerTurn, display, againstBot, possibleMovesList))
                # if not player turn, have the bot play a move
                else:
                    time.sleep(0.25)
                    # prints black as a different text color when its blacks turn
                    if playerTurn == "black":
                        print("* AI Bot " + colored(playerTurn, "red") + " is thinking of a move: ")
                    else:
                        print("* AI Bot " + playerTurn + " is thinking of a move: ")
                    time.sleep(0.75)
                    # the bot chooses a random value from the list of possible moves and uses it as its move
                    randomMove = random.randint(0, len(possibleMovesList) - 1)
                    playerMove = possibleMovesList[randomMove]
                    print("AI Bot played " + playerMove)
                    time.sleep(1)
                    legalMove = True
                    break

            # prompts players for their move when playing against player, then checks if its one of the legal moves
            else:
                if playerTurn == "black":
                    playerMove = input("* Player " + colored(playerTurn, "red") + "'s move: ")
                else:
                    playerMove = input("* Player " + playerTurn + "'s move: ")
                playerMove = playerMove.replace(" ", "")
                for possibleMove in possibleMovesList:
                    if playerMove == possibleMove:
                        legalMove = True
                        break
                else:
                    print(help_menu(playerMove, playerTurn, display, againstBot, possibleMovesList))

        # converts the player move into list indexs then updates the board with the moves
        playerInitial, playerFinal = convert_to_usable(playerMove)
        # updates the board with the players move
        board = deepcopy(update_game_board(playerInitial, playerFinal, playerTurn, board))
        # check if the player moved the king/rook or if the opposite color captured it, then turns the corresponding castling side illegal
        if (playerTurn == "white" and playerInitial == "70") or (playerTurn == "black" and playerFinal == "70"):
            wLongCastle = False
        if (playerTurn == "white" and playerInitial == "77") or (playerTurn == "black" and playerFinal == "77"):
            wShortCastle = False
        if playerTurn == "white" and playerInitial == "74":
            wLongCastle = False
            wShortCastle = False
        if (playerTurn == "black" and playerInitial == "00") or (playerTurn == "white" and playerFinal == "00"):
            bLongCastle = False
        if (playerTurn == "black" and playerInitial == "07") or (playerTurn == "white" and playerFinal == "07"):
            bShortCastle = False
        if playerTurn == "black" and playerInitial == "04":
            wLongCastle = False
            wShortCastle = False

        # checks if the players initial move was a pawn at starting position and they moved 2 spaces and saves the position of the final move
        # then turns en passant true until the next turn, which turns it false unless player also moved 2 spaces
        if playerTurn == "white":
            for wPawnCol in range(8):
                if playerInitial == "6" + str(wPawnCol) and playerFinal == "4" + str(wPawnCol) and isinstance(board[int(playerFinal[0])][int(playerFinal[1])], Pawn):
                    enPassant = True
                    enPassantPosition = str(playerFinal) + str(wPawnCol)
                    break
            else:
                enPassant = False
                enPassantPosition = ""
        elif playerTurn == "black":
            for bPawnCol in range(8):
                if playerInitial == "1" + str(bPawnCol) and playerFinal == "3" + str(bPawnCol) and isinstance(board[int(playerFinal[0])][int(playerFinal[1])], Pawn):
                    enPassant = True
                    enPassantPosition = str(playerFinal) + str(bPawnCol)
                    break
            else:
                enPassant = False
                enPassantPosition = ""

        check_pawn_promotion(board)
        # adds to the turn count and changes the players turn
        turnCount += 1
        if turnCount % 2 == 0:
            playerTurn = "black"
        else:
            playerTurn = "white"
        if check_king_attacked(playerTurn, board) == True:
            print("Check! Your King is currently under attack!")

    # if the game ended, check whether it was by checkmate or stalemate, and adds a win if checkmate
    if checkmate == True:
        print("---CHECKMATE---")
        if playerTurn == "white":
            print("White is currently in check and any move white makes will result in a check.")
            print("Player " + colored("black", "red") + " is the winner!")
            blackWin += 1
        else:
            print(colored("Black", "red") + " is currently in check and any move " + colored("black", "red") + " makes will result in a check.")
            print("Player white is the winner!")
            whiteWin += 1
        print("---Game Ended---")
    if stalemate == True:
        print("---STALEMATE---")
        if playerTurn == "white":
            print("White is not currently in check and has no legal moves, as they all result in check. ")
        else:
            print(colored("Black", "red") + " is not in check and has no legal moves, as they all result in check.")
        print("---Game Ended---")

    prompt_rematch()


# function takes the move and converts it into list indexes to be used for calculations
def convert_to_usable(move):
    # convert to a list because strings are immutable
    move = list(move)
    # changes the move format from (col, row) into (row, col), inverting the row since player views it bottom to top while list index goes top to bottom
    initialRow = abs(int(move[1]) - 8)
    initialCol = ord(move[0].lower()) - 97
    finalRow = abs(int(move[3]) - 8)
    finalCol = ord(move[2].lower()) - 97
    # combines the converted moves into a string
    initial = str(initialRow) + str(initialCol)
    final = str(finalRow) + str(finalCol)
    return initial, final


# function takes the players moves and applies it to the game board and updates it
def update_game_board(initialMove, finalMove, playerColor, gameBoard):
    global enPassant
    global wShortCastle
    global wLongCastle
    global bShortCastle
    global bLongCastle
    # copies the board, then updates the final position with the piece of the initial position
    newGameBoard = deepcopy(gameBoard)
    newGameBoard[int(finalMove[0])][int(finalMove[1])] = newGameBoard[int(initialMove[0])][int(initialMove[1])]
    # if the player moved en passant, also turn the captured pawn spot empty
    if enPassant == True:
        if playerColor == "white" and int(initialMove[0]) == 3 and abs(int(initialMove[0]) - 1 == int(finalMove[0])) and abs(int(finalMove[1]) - int(initialMove[1])) == 1 and int(finalMove[1]) == int(enPassantPosition[1]):
            newGameBoard[int(finalMove[0]) + 1][int(finalMove[1])] = Empty("   ", "empty")
        if playerColor == "black" and int(initialMove[0]) == 5 and abs(int(initialMove[0]) + 1 == int(finalMove[0])) and abs(int(finalMove[1]) - int(initialMove[1])) == 1 and int(finalMove[1]) == int(enPassantPosition[1]):
            newGameBoard[int(finalMove[0]) - 1][int(finalMove[1])] = Empty("   ", "empty")
    # if the player castled, move the rook to the other side of the king
    if wShortCastle == True and initialMove == "74" and finalMove == "76":
        newGameBoard[7][5] = Rook(" R ", "white")
        newGameBoard[7][7] = Empty("   ", "empty")
    if wLongCastle == True and initialMove == "74" and finalMove == "72":
        newGameBoard[7][3] = Rook(" R ", "white")
        newGameBoard[7][0] = Empty("   ", "empty")
    if bShortCastle == True and initialMove == "04" and finalMove == "06":
        newGameBoard[0][5] = Rook(" R ", "black")
        newGameBoard[0][7] = Empty("   ", "empty")
    if bLongCastle == True and initialMove == "04" and finalMove == "02":
        newGameBoard[0][3] = Rook(" R ", "black")
        newGameBoard[0][0] = Empty("   ", "empty")
    # turns the initial positon empty since the piece just moved from there
    newGameBoard[int(initialMove[0])][int(initialMove[1])] = Empty("   ", "empty")
    return newGameBoard


# function takes the game board and translates it into another board that displays the pieces with color
def update_display_board(gameBoard, displayBoard):
    # loop through the board
    for row in range(8):
        for col in range(8):
            # calculates every other square of the board in order to color the lighter squares of the checkered pattern
            if (row + col) % 2 == 0:
                # check which piece is in each position of the board, then copies the name of the piece into the display board
                if isinstance(gameBoard[row][col], Pawn):
                    displayBoard[row][col] = Back.WHITE + Style.BRIGHT + colored(" P ", "white", attrs=["bold"])
                    # if the piece is black, it will change the color on the display to reflect it
                    if gameBoard[row][col].color == "black":
                        displayBoard[row][col] = Back.WHITE + colored(" P ", "red", attrs=["bold"])
                elif isinstance(gameBoard[row][col], Bishop):
                    displayBoard[row][col] = Back.WHITE + colored(" B ", "white", attrs=["bold"])
                    if gameBoard[row][col].color == "black":
                        displayBoard[row][col] = Back.WHITE + colored(" B ", "red", attrs=["bold"])
                elif isinstance(gameBoard[row][col], Knight):
                    displayBoard[row][col] = Back.WHITE + colored(" N ", "white", attrs=["bold"])
                    if gameBoard[row][col].color == "black":
                        displayBoard[row][col] = Back.WHITE + colored(" N ", "red", attrs=["bold"])
                elif isinstance(gameBoard[row][col], Rook):
                    displayBoard[row][col] = Back.WHITE + colored(" R ", "white", attrs=["bold"])
                    if gameBoard[row][col].color == "black":
                        displayBoard[row][col] = Back.WHITE + colored(" R ", "red", attrs=["bold"])
                elif isinstance(gameBoard[row][col], King):
                    displayBoard[row][col] = Back.WHITE + colored(" K ", "white", attrs=["bold"])
                    if gameBoard[row][col].color == "black":
                        displayBoard[row][col] = Back.WHITE + colored(" K ", "red", attrs=["bold"])
                elif isinstance(gameBoard[row][col], Queen):
                    displayBoard[row][col] = Back.WHITE + colored(" Q ", "white", attrs=["bold"])
                    if gameBoard[row][col].color == "black":
                        displayBoard[row][col] = Back.WHITE + colored(" Q ", "red", attrs=["bold"])
                elif isinstance(gameBoard[row][col], Empty):
                    displayBoard[row][col] = Back.WHITE + colored("   ", "white")
            # color the darker squares of the board
            else:
                # check which piece is in each position of the board, then copies the name of the piece into the display board
                if isinstance(gameBoard[row][col], Pawn):
                    displayBoard[row][col] = Back.GREEN + Style.BRIGHT + colored(" P ", "white", attrs=["bold"])
                    if gameBoard[row][col].color == "black":
                        displayBoard[row][col] = Back.GREEN + colored(" P ", "red", attrs=["bold"])
                elif isinstance(gameBoard[row][col], Bishop):
                    displayBoard[row][col] = Back.GREEN + colored(" B ", "white", attrs=["bold"])
                    if gameBoard[row][col].color == "black":
                        displayBoard[row][col] = Back.GREEN + colored(" B ", "red", attrs=["bold"])
                elif isinstance(gameBoard[row][col], Knight):
                    displayBoard[row][col] = Back.GREEN + colored(" N ", "white", attrs=["bold"])
                    if gameBoard[row][col].color == "black":
                        displayBoard[row][col] = Back.GREEN + colored(" N ", "red", attrs=["bold"])
                elif isinstance(gameBoard[row][col], Rook):
                    displayBoard[row][col] = Back.GREEN + colored(" R ", "white", attrs=["bold"])
                    if gameBoard[row][col].color == "black":
                        displayBoard[row][col] = Back.GREEN + colored(" R ", "red", attrs=["bold"])
                elif isinstance(gameBoard[row][col], King):
                    displayBoard[row][col] = Back.GREEN + colored(" K ", "white", attrs=["bold"])
                    if gameBoard[row][col].color == "black":
                        displayBoard[row][col] = Back.GREEN + colored(" K ", "red", attrs=["bold"])
                elif isinstance(gameBoard[row][col], Queen):
                    displayBoard[row][col] = Back.GREEN + colored(" Q ", "white", attrs=["bold"])
                    if gameBoard[row][col].color == "black":
                        displayBoard[row][col] = Back.GREEN + colored(" Q ", "red", attrs=["bold"])
                elif isinstance(gameBoard[row][col], Empty):
                    displayBoard[row][col] = Back.GREEN + colored("   ", "white")
    return displayBoard


# function generates all possible player inputs and checks which inputs can turn into legal moves
def find_possible_moves(playerColor, gameBoard):
    allPossibleMoves = []
    # generate 4 numbers and convert 2 of them into letters, then combines them in a variable to simulate a player inputted move and checks legality
    for letterInitial in range(0, 8):
        for numInitial in range(1, 9):
            for letterFinal in range(0, 8):
                for numFinal in range(1, 9):
                    testLetterInitial = chr(letterInitial + 97)
                    testLetterFinal = chr(letterFinal + 97)
                    testMove = str(testLetterInitial) + str(numInitial) + str(testLetterFinal) + str(numFinal)
                    testInitial, testFinal = convert_to_usable(testMove)
                    if check_legal_move(testInitial, testFinal, playerColor, gameBoard) == True:
                        # creates a new updated board using the test moves, then checks if the move will put the player in check
                        testBoard = deepcopy(update_game_board(testInitial, testFinal, playerColor, gameBoard))
                        if check_king_attacked(playerColor, testBoard) == False:
                            allPossibleMoves.append(testMove)
    return allPossibleMoves


# functions finds the current players king position, then scans the area around to see if an opposing piece is attacking it
def check_king_attacked(playerColor, gameBoard):
    if playerColor == "white":
        otherColor = "black"
    else:
        otherColor = "white"
    # tries to find the row and col of the current players king
    for kingRow in range(8):
        for kingCol in range(8):
            # find the king that is the same as the player color
            if isinstance(gameBoard[kingRow][kingCol], King) and gameBoard[kingRow][kingCol].color == playerColor:
                # loop through the board positions again to find the enemy king
                for otherKingRow in range(8):
                    for otherKingCol in range(8):
                        # gets the position of the other king
                        if isinstance(gameBoard[otherKingRow][otherKingCol], King) and gameBoard[otherKingRow][otherKingCol].color == otherColor:
                            # checks if the other king is 1 space away from player's king
                            if abs(otherKingRow - kingRow) == 1 and abs(otherKingCol - kingCol) == 0:
                                return True
                            elif abs(otherKingRow - kingRow) == 0 and abs(otherKingCol - kingCol) == 1:
                                return True
                            elif abs(otherKingRow - kingRow) == 1 and abs(otherKingCol - kingCol) == 1:
                                return True
                        else:
                            break

                rowIncrement = 1
                colIncrement = 1
                # scanning vertical axis up
                while kingRow - rowIncrement >= 0:
                    # if it meets a same color piece, the King is not in check in that direction so break from the loop
                    if gameBoard[kingRow - rowIncrement][kingCol].color == playerColor:
                        break
                    # check if it meets a opposite color piece
                    elif gameBoard[kingRow - rowIncrement][kingCol].color == otherColor:
                        # if its a rook or queen, the King is in check so return True
                        if isinstance(gameBoard[kingRow - rowIncrement][kingCol], Rook) or isinstance(gameBoard[kingRow - rowIncrement][kingCol], Queen):
                            return True
                        # if not, the King is not in check in that direction
                        else:
                            break
                    # if neither, its an empty square so move to check the next square
                    rowIncrement += 1
                    continue

                # reset the increments used for calculation
                rowIncrement = 1
                # scanning vertical axis down
                while kingRow + rowIncrement <= 7:
                    # if it meets a same color piece, the King is not in check in that direction so break from the loop
                    if gameBoard[kingRow + rowIncrement][kingCol].color == playerColor:
                        break
                    # check if it meets a opposite color piece
                    elif gameBoard[kingRow + rowIncrement][kingCol].color == otherColor:
                        # if its a rook or queen, the King is in check so return True
                        if isinstance(gameBoard[kingRow + rowIncrement][kingCol], Rook) or isinstance(gameBoard[kingRow + rowIncrement][kingCol], Queen):
                            return True
                        # if not, the King is not in check in that direction
                        else:
                            break
                    # if neither, its an empty square so move to check the next square
                    rowIncrement += 1
                    continue

                # reset the increments used for calculation
                rowIncrement = 1
                colIncrement = 1
                # scanning horizontal axis left
                while kingCol - colIncrement >= 0:
                    # if it meets a same color piece, the King is not in check in that direction so break from the loop
                    if gameBoard[kingRow][kingCol - colIncrement].color == playerColor:
                        break
                    # check if it meets a opposite color piece
                    elif gameBoard[kingRow][kingCol - colIncrement].color == otherColor:
                        # if its a rook or queen, the King is in check so return True
                        if isinstance(gameBoard[kingRow][kingCol - colIncrement], Rook) or isinstance(gameBoard[kingRow][kingCol - colIncrement], Queen):
                            return True
                        # if not, the King is not in check in that direction
                        else:
                            break
                    # if neither, its an empty square so move to check the next square
                    colIncrement += 1
                    continue

                # reset the increments used for calculation
                colIncrement = 1
                # scanning horizontal axis right
                while kingCol + colIncrement <= 7:
                    # if it meets a same color piece, the King is not in check in that direction so break from the loop
                    if gameBoard[kingRow][kingCol + colIncrement].color == playerColor:
                        break
                    # check if it meets a opposite color piece
                    elif gameBoard[kingRow][kingCol + colIncrement].color == otherColor:
                        # if its a rook or queen, the King is in check so return True
                        if isinstance(gameBoard[kingRow][kingCol + colIncrement], Rook) or isinstance(gameBoard[kingRow][kingCol + colIncrement], Queen):
                            return True
                        # if not, the King is not in check in that direction
                        else:
                            break
                    # if neither, its an empty square so move to check the next square
                    colIncrement += 1
                    continue

                # reset the increments used for calculation
                rowIncrement = 1
                colIncrement = 1
                # scanning top left diagonal
                while kingRow - rowIncrement >= 0 and kingCol - colIncrement >= 0:
                    # if it meets a same color piece, the King is not in check in that direction so break from the loop
                    if gameBoard[kingRow - rowIncrement][kingCol - colIncrement].color == playerColor:
                        break
                    # check if it meets a opposite color piece
                    elif gameBoard[kingRow - rowIncrement][kingCol - colIncrement].color == otherColor:
                        # if its a bishop or queen, the King is in check so return True
                        if isinstance(gameBoard[kingRow - rowIncrement][kingCol - colIncrement], Bishop) or isinstance(gameBoard[kingRow - rowIncrement][kingCol - colIncrement], Queen):
                            return True
                        # if not, the King is not in check in that direction
                        else:
                            break
                    # if neither, its an empty square so move to check the next square
                    rowIncrement += 1
                    colIncrement += 1
                    continue

                # reset the increments used for calculation
                rowIncrement = 1
                colIncrement = 1
                # scanning top right diagonal
                while kingRow - rowIncrement >= 0 and kingCol + colIncrement <= 7:
                    # if it meets a same color piece, the King is not in check in that direction so break from the loop
                    if gameBoard[kingRow - rowIncrement][kingCol + colIncrement].color == playerColor:
                        break
                    # check if it meets a opposite color piece
                    elif gameBoard[kingRow - rowIncrement][kingCol + colIncrement].color == otherColor:
                        # if its a bishop or queen, the King is in check so return True
                        if isinstance(gameBoard[kingRow - rowIncrement][kingCol + colIncrement], Bishop) or isinstance(gameBoard[kingRow - rowIncrement][kingCol + colIncrement], Queen):
                            return True
                        # if not, the King is not in check in that direction
                        else:
                            break
                    # if neither, its an empty square so move to check the next square
                    rowIncrement += 1
                    colIncrement += 1
                    continue

                # reset the increments used for calculation
                rowIncrement = 1
                colIncrement = 1
                # scanning bottom left diagonal
                while kingRow + rowIncrement <= 7 and kingCol - colIncrement >= 0:
                    # if it meets a same color piece, the King is not in check in that direction so break from the loop
                    if gameBoard[kingRow + rowIncrement][kingCol - colIncrement].color == playerColor:
                        break
                    # check if it meets a opposite color piece
                    elif gameBoard[kingRow + rowIncrement][kingCol - colIncrement].color == otherColor:
                        # if its a bishop or queen, the King is in check so return True
                        if isinstance(gameBoard[kingRow + rowIncrement][kingCol - colIncrement], Bishop) or isinstance(gameBoard[kingRow + rowIncrement][kingCol - colIncrement], Queen):
                            return True
                        # if not, the King is not in check in that direction
                        else:
                            break
                    # if neither, its an empty square so move to check the next square
                    rowIncrement += 1
                    colIncrement += 1
                    continue

                # reset the increments used for calculation
                rowIncrement = 1
                colIncrement = 1
                # scanning bottom right diagonal
                while (kingRow + rowIncrement) <= 7 and (kingCol + colIncrement) <= 7:
                    # if it meets a same color piece, the King is not in check in that direction so break from the loop
                    if gameBoard[kingRow + rowIncrement][kingCol + colIncrement].color == playerColor:
                        break
                    # check if it meets a opposite color piece
                    elif gameBoard[kingRow + rowIncrement][kingCol + colIncrement].color == otherColor:
                        # if its a bishop or queen, the King is in check so return True
                        if isinstance(gameBoard[kingRow + rowIncrement][kingCol + colIncrement], Bishop) or isinstance(gameBoard[kingRow + rowIncrement][kingCol + colIncrement], Queen):
                            return True
                        # if not, the King is not in check in that direction
                        else:
                            break
                    # if neither, its an empty square so move to check the next square
                    rowIncrement += 1
                    colIncrement += 1
                    continue

                # loop through the game board coordinates
                for knightRow in range(8):
                    for knightCol in range(8):
                        # checks for an opposing knight
                        if isinstance(gameBoard[knightRow][knightCol], Knight) and gameBoard[knightRow][knightCol].color == otherColor:
                            # checks if the knight is attacking the king using pythagorean thereom, 2 squares and 1 square away
                            if pow(abs(knightRow - kingRow), 2) + pow(abs(knightCol - kingCol), 2) == 5:
                                return True

                # scanning for black pawn if player is white
                if playerColor == "white" and kingRow > 1:
                    # ensures no index error
                    if kingCol < 7:
                        # check for black pawn on right side, a king on the last col cant be attacked by a right side pawn
                        if (gameBoard[kingRow - 1][kingCol + 1], Pawn) and gameBoard[kingRow - 1][kingCol + 1].color == "black":
                            return True
                    if kingCol > 0:
                        # check for black pawn on left side, a king on the first col cant be attacked by a left side pawn
                        if (gameBoard[kingRow - 1][kingCol - 1], Pawn) and gameBoard[kingRow - 1][kingCol - 1].color == "black":
                            return True
                # scanning for white pawn if player is black
                elif playerColor == "black" and kingRow < 7:
                    # ensures no index error
                    if kingCol < 7:
                        # check for white pawn on right side, a king on the last col cant be attacked by a right side pawn
                        if (gameBoard[kingRow + 1][kingCol + 1], Pawn) and gameBoard[kingRow + 1][kingCol + 1].color == "white":
                            return True
                    if kingCol > 0:
                        # check for white pawn on left side, a king on the first col cant be attacked by a left side pawn
                        if (gameBoard[kingRow + 1][kingCol - 1], Pawn) and gameBoard[kingRow + 1][kingCol - 1].color == "white":
                            return True
                # returns false is nothing is attacking the king
                return False
    return False


# function scans the board for any pawns on the end rows and prompts for promotion if there is
def check_pawn_promotion(gameBoard):
    for col in range(8):
        # checks for pawns on the top row
        if gameBoard[0][col].name == " P ":
            # continue prompting until the player correctly promotes
            while gameBoard[0][col].name == " P ":
                promotion = input("Type the piece you want to promote the pawn into. (Type 'B' 'N' 'R' or 'Q') \n")
                promotion = promotion.lower().replace(" ", "")
                # checks which piece the player inputted, then replaces the pawn with the new piece
                if promotion == "b":
                    gameBoard[0][col] = Bishop(" B ", "white")
                elif promotion == "n":
                    gameBoard[0][col] = Knight(" N ", "white")
                elif promotion == "r":
                    gameBoard[0][col] = Rook(" R ", "white")
                elif promotion == "q":
                    gameBoard[0][col] = Queen(" Q ", "white")
                else:
                    print("Invalid piece")

        # checks for pawns on the bottom row
        elif gameBoard[7][col].name == " P ":
            # continue prompting until the player correctly promotes
            while gameBoard[7][col].name == " P ":
                promotion = input("Type the piece you want to promote the pawn into. (Type 'B' 'N' 'R' or 'Q') \n")
                promotion = promotion.lower().replace(" ", "")
                # checks which piece the player inputted, then replaces the pawn with the new piece
                if promotion == "b":
                    gameBoard[7][col] = Bishop(" B ", "black")
                elif promotion == "n":
                    gameBoard[7][col] = Knight(" N ", "black")
                elif promotion == "r":
                    gameBoard[7][col] = Rook(" R ", "black")
                elif promotion == "q":
                    gameBoard[7][col] = Queen(" Q ", "black")
                else:
                    print("Invalid piece")
    return gameBoard


# function checks whether the input was correct, then calls the corresponding move function to ensure move was legal
def check_legal_move(initialMove, finalMove, playerColor, gameBoard):
    # ensures initial and final moves are different
    if initialMove != finalMove:
        # ensures the player is moving only their color pieces
        if gameBoard[int(initialMove[0])][int(initialMove[1])].color == playerColor:
            # checks which piece is being moved, then calls the corresponding function to check if it is legal
            if isinstance(gameBoard[int(initialMove[0])][int(initialMove[1])], Pawn):
                return check_pawn_move(initialMove, finalMove, playerColor, gameBoard)
            elif isinstance(gameBoard[int(initialMove[0])][int(initialMove[1])], Knight):
                return check_knight_move(initialMove, finalMove, playerColor, gameBoard)
            elif isinstance(gameBoard[int(initialMove[0])][int(initialMove[1])], Bishop):
                return check_bishop_move(initialMove, finalMove, playerColor, gameBoard)
            elif isinstance(gameBoard[int(initialMove[0])][int(initialMove[1])], Rook):
                return check_rook_move(initialMove, finalMove, playerColor, gameBoard)
            elif isinstance(gameBoard[int(initialMove[0])][int(initialMove[1])], Queen):
                return check_queen_move(initialMove, finalMove, playerColor, gameBoard)
            elif isinstance(gameBoard[int(initialMove[0])][int(initialMove[1])], King):
                return check_king_move(initialMove, finalMove, playerColor, gameBoard)
            else:
                return False
        else:
            return False
    else:
        return False


# function checks whether the king move is legal
def check_king_move(initialMove, finalMove, playerColor, gameBoard):
    global wShortCastle
    global wLongCastle
    global bShortCastle
    global bLongCastle
    # since a king can move up to 1 space around it, check if the change in position is either 1 or 0 for both directions
    if (abs(int(finalMove[0]) - int(initialMove[0])) == 1 or abs(int(finalMove[0]) - int(initialMove[0])) == 0) and (abs(int(finalMove[1]) - int(initialMove[1])) == 1 or abs(int(finalMove[1]) - int(initialMove[1])) == 0):
        if playerColor == "white" and (isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty) or gameBoard[int(finalMove[0])][int(finalMove[1])].color == "black"):
            return True
        elif playerColor == "black" and (isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty) or gameBoard[int(finalMove[0])][int(finalMove[1])].color == "white"):
            return True
        else:
            return False
    # checks for long castle if king moves 2 spaces left
    elif int(finalMove[0]) == int(initialMove[0]) and int(initialMove[1]) - 2 == int(finalMove[1]):
        # if white long castles, check that its legal and that all the spaces in between are empty
        if playerColor == "white" and wLongCastle == True and isinstance(gameBoard[7][1], Empty) and isinstance(gameBoard[7][2], Empty) and isinstance(gameBoard[7][3], Empty):
            return True
        # if black long castles, check that its legal and that all the spaces in between are empty
        elif playerColor == "black" and bLongCastle == True and isinstance(gameBoard[0][1], Empty) and isinstance(gameBoard[0][2], Empty) and isinstance(gameBoard[0][3], Empty):
            return True
        else:
            return False
    # checks for short castle if king moves 2 spaces right
    elif int(finalMove[0]) == int(initialMove[0]) and int(initialMove[1]) + 2 == int(finalMove[1]):
        # if white short castles, check that its legal and that all the spaces in between are empty
        if playerColor == "white" and wShortCastle == True and isinstance(gameBoard[7][5], Empty) and isinstance(gameBoard[7][6], Empty):
            return True
        # if black short castles, check that its legal and that all the spaces in between are empty
        elif playerColor == "black" and bShortCastle == True and isinstance(gameBoard[0][5], Empty) and isinstance(gameBoard[0][6], Empty):
            return True
        else:
            return False
    else:
        return False


# function checks whether the pawn move is legal
def check_pawn_move(initialMove, finalMove, playerColor, gameBoard):
    global enPassant
    global enPassantPosition
    if playerColor == "white":
        # check if the pawn moved 2 spaces, which is only possible if the pawn is still on its starting square
        if int(initialMove[0]) == 6 and int(finalMove[0]) == 4 and int(initialMove[1]) == int(finalMove[1]):
            # checks that the two squares in front are empty
            if isinstance(gameBoard[int(initialMove[0]) - 1][int(initialMove[1])], Empty) and isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty):
                return True
            else:
                return False
        # checks if the pawn moved 1 space forward in the same row and that the square its moving to is empty
        elif int(initialMove[0]) - 1 == int(finalMove[0]) and int(initialMove[1]) == int(finalMove[1]) and isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty):
            return True
        # checks if the pawn is capturing diagonally, which would change its col by 1 and move it forward 1
        elif gameBoard[int(finalMove[0])][int(finalMove[1])].color == "black":
            if int(initialMove[0]) - 1 == int(finalMove[0]) and abs(int(finalMove[1]) - int(initialMove[1])) == 1:
                return True
            else:
                return False
        # checks if the white pawn moved diagonally while en passant is true and that the white piece moves into the same row as the black piece that just moved
        elif enPassant == True and int(initialMove[0]) == 3 and abs(int(initialMove[0]) - 1 == int(finalMove[0])) and abs(int(finalMove[1]) - int(initialMove[1])) == 1 and int(finalMove[1]) == int(enPassantPosition[1]):
            return True
        else:
            return False

    # check legal movement for black
    else:
        # check if the pawn moved 2 spaces, which is only possible if the pawn is still on its starting square
        if int(initialMove[0]) == 1 and int(finalMove[0]) == 3 and int(initialMove[1]) == int(finalMove[1]):
            if isinstance(gameBoard[int(initialMove[0]) + 1][int(initialMove[1])], Empty) and isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty):
                return True
            else:
                return False
        # checks if the pawn moved 1 space forward in the same row and that the square its moving to is empty
        elif int(initialMove[0]) + 1 == int(finalMove[0]) and int(initialMove[1]) == int(finalMove[1]) and isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty):
            return True
        # checks if the pawn is capturing diagonally, which would change both axis by 1 space
        elif gameBoard[int(finalMove[0])][int(finalMove[1])].color == "white":
            if int(initialMove[0]) + 1 == int(finalMove[0]) and abs(int(finalMove[1]) - int(initialMove[1])) == 1:
                return True
            else:
                return False
        # checks if the black pawn moved diagonally while en passant is true and that the white piece moves into the same row as the white piece that just moved
        elif enPassant == True and int(initialMove[0]) == 5 and abs(int(initialMove[0]) + 1 == int(finalMove[0])) and abs(int(finalMove[1]) - int(initialMove[1])) == 1 and int(finalMove[1]) == int(enPassantPosition[1]):
            return True
        else:
            return False


# function checks whether the knight move is legal
def check_knight_move(initialMove, finalMove, playerColor, gameBoard):
    # since the movement is always 2 squares + 1 square, I used the Pythagorean theorem to ensure it equals 5 to be legal
    if pow(abs(int(finalMove[0]) - int(initialMove[0])), 2) + pow(abs(int(finalMove[1]) - int(initialMove[1])), 2) == 5:
        # ensures the final square is either empty or a piece of the opposite color
        if isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty):
            return True
        elif playerColor == "white" and gameBoard[int(finalMove[0])][int(finalMove[1])].color == "black":
            return True
        elif playerColor == "black" and gameBoard[int(finalMove[0])][int(finalMove[1])].color == "white":
            return True
        else:
            return False
    else:
        return False


# function checks whether the bishop move was legal
def check_bishop_move(initialMove, finalMove, playerColor, gameBoard):
    if playerColor == "white":
        otherColor = "black"
    else:
        otherColor = "white"
    squareIncrement = 1
    # ensures that both axis move by the same number of squares
    if abs(int(finalMove[0]) - int(initialMove[0])) == abs(int(finalMove[1]) - int(initialMove[1])):
        bishopSpaces = abs(int(finalMove[0]) - int(initialMove[0]))
        # top left diagonal
        if int(finalMove[0]) < int(initialMove[0]) and int(finalMove[1]) < int(initialMove[1]):
            while squareIncrement < bishopSpaces:
                # checks that all the squares diagonally between the final position is empty
                if isinstance(gameBoard[int(initialMove[0]) - squareIncrement][int(initialMove[1]) - squareIncrement], Empty):
                    squareIncrement += 1
                else:
                    return False
            # check that the final position is empty or capturing an opposite color
            if gameBoard[int(finalMove[0])][int(finalMove[1])].color == otherColor or isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty):
                return True
            else:
                return False

        # top right diagonal
        elif int(finalMove[0]) < int(initialMove[0]) and int(finalMove[1]) > int(initialMove[1]):
            while squareIncrement < bishopSpaces:
                # checks that all the squares diagonally between the final position is empty
                if isinstance(gameBoard[int(initialMove[0]) - squareIncrement][int(initialMove[1]) + squareIncrement], Empty):
                    squareIncrement += 1
                else:
                    return False
            # check that the final position is empty or capturing an opposite color
            if gameBoard[int(finalMove[0])][int(finalMove[1])].color == otherColor or isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty):
                return True
            else:
                return False

        # bottom left diagonal
        elif int(finalMove[0]) > int(initialMove[0]) and int(finalMove[1]) < int(initialMove[1]):
            while squareIncrement < bishopSpaces:
                # checks that all the squares diagonally between the final position is empty
                if isinstance(gameBoard[int(initialMove[0]) + squareIncrement][int(initialMove[1]) - squareIncrement], Empty):
                    squareIncrement += 1
                else:
                    return False
            # check that the final position is empty or capturing an opposite color
            if gameBoard[int(finalMove[0])][int(finalMove[1])].color == otherColor or isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty):
                return True
            else:
                return False

        # bottom right diagonal
        elif int(finalMove[0]) > int(initialMove[0]) and int(finalMove[1]) > int(initialMove[1]):
            while squareIncrement < bishopSpaces:
                # checks that all the squares diagonally between the final position is empty
                if isinstance(gameBoard[int(initialMove[0]) + squareIncrement][int(initialMove[1]) + squareIncrement], Empty):
                    squareIncrement += 1
                else:
                    return False
            # check that the final position is empty or capturing an opposite color
            if gameBoard[int(finalMove[0])][int(finalMove[1])].color == otherColor or isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty):
                return True
            else:
                return False
    else:
        return False


# function checks whether the rook move was legal
def check_rook_move(initialMove, finalMove, playerColor, gameBoard):
    if playerColor == "white":
        otherColor = "black"
    else:
        otherColor = "white"
    squareIncrement = 1
    # check if horizontal movement
    if (initialMove[0] == finalMove[0] and initialMove[1] != finalMove[1]):
        rookHorizontal = abs(int(finalMove[1]) - int(initialMove[1]))
        # calculates right side
        if int(finalMove[1]) > int(initialMove[1]):
            # loops to check if every square in between is empty
            while squareIncrement < rookHorizontal:
                if isinstance(gameBoard[int(initialMove[0])][int(initialMove[1]) + squareIncrement], Empty):
                    squareIncrement += 1
                else:
                    return False
            # ensures the ending position is empty square or capturing an opposite color piece
            if gameBoard[int(finalMove[0])][int(finalMove[1])].color == otherColor or isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty):
                return True
            else:
                return False
        # calculates left side
        elif int(finalMove[1]) < int(initialMove[1]):
            # loops to check if every square in between is empty
            while squareIncrement < rookHorizontal:
                if isinstance(gameBoard[int(initialMove[0])][int(initialMove[1]) - squareIncrement], Empty):
                    squareIncrement += 1
                else:
                    return False
            # ensures the ending position is empty square or capturing an opposite color piece
            if gameBoard[int(finalMove[0])][int(finalMove[1])].color == otherColor or isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty):
                return True
            else:
                return False
    # check if vertical movement
    elif (initialMove[0] != finalMove[0] and initialMove[1] == finalMove[1]):
        rookVertical = abs(int(finalMove[0]) - int(initialMove[0]))
        # calculates down side
        if int(finalMove[0]) > int(initialMove[0]):
            # loops to check if every square in between is empty
            while squareIncrement < rookVertical:
                if isinstance(gameBoard[int(initialMove[0]) + squareIncrement][int(initialMove[1])], Empty):
                    squareIncrement += 1
                else:
                    return False
            # ensures the ending position is empty square or capturing an opposite color piece
            if gameBoard[int(finalMove[0])][int(finalMove[1])].color == otherColor or isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty):
                return True
            else:
                return False
        # calculates up side
        elif int(finalMove[0]) < int(initialMove[0]):
            # loops to check if every square in between is empty
            while squareIncrement < rookVertical:
                if isinstance(gameBoard[int(initialMove[0]) - squareIncrement][int(initialMove[1])], Empty):
                    squareIncrement += 1
                else:
                    return False
            # ensures the ending position is empty square or capturing an opposite color piece
            if gameBoard[int(finalMove[0])][int(finalMove[1])].color == otherColor or isinstance(gameBoard[int(finalMove[0])][int(finalMove[1])], Empty):
                return True
            else:
                return False
    else:
        return False


# function checks whether the queen move was legal
def check_queen_move(initialMove, finalMove, playerColor, gameBoard):
    # the queens movement is the same as bishop + rook combined
    if check_bishop_move(initialMove, finalMove, playerColor, gameBoard) == True or check_rook_move(initialMove, finalMove, playerColor, gameBoard) == True:
        return True
    else:
        return False


# function handles errors and print different messages depending on user input
def help_menu(action, playerColor, displayBoard, againstBot, possibleMovesList):
    # turns it lowercase and removes any spaces
    action = action.lower().replace(" ", "")
    if action == "help":
        message = "---HELP--- \n"
        message += "Format your moves as '[initialSquare] [finalSquare]' with letter coordinate first, then number. Spaces and capitalization do not matter. \n"
        message += "EXAMPLE: 'd3d4' moves the piece from position D3 to position D4, as long as the movement is legal for the piece you move. \n"
        message += "--LIST OF PIECES--\n"
        message += "* Pawn or 'P' can move 1 space forward. It can only capture top diagonally 1 space, which means it can be blocked if a piece is directly in front. \n"
        message += "If the Pawn has not moved yet, it can move 2 spaces forward instead of 1. If it reaches the end, it can promote to any piece except for the King. \n"
        message += "En Passant - If an enemy pawn moves 2 spaces and your pawn is directly left/right, you can move behind the pawn and capture it ONLY the turn after. \n"
        message += "* Knight or 'N' can only move/capture in an L shape. 2 spaces in a direction, turn, 1 space. It is the only piece that can jump over other pieces. \n"
        message += "* Bishop or 'B' can only move/capture in a diagonal. Basically, the Bishop can only stay on other squares of the same color as its initial square. \n"
        message += "* Rook or 'R' can only move/capture in a straight horizontal/vertical line. \n"
        message += "* Queen or 'Q' can move/capture in a straight horizontal/vertical line OR diagonally. Its like a rook and bishop combined, making it a strong piece. \n"
        message += "* King or 'K' can only move/capture 1 space in any direction. The King should always be protected as you will lose if your side's King is captured. \n"
        message += "Castling - ONLY IF your King and one of your Rooks has not moved yet and the squares in between are empty, your King can move 2 spaces left or right. \n"
        message += "Castling left side is called 'long castle' while castling right side is called 'short castle.' This moves the Rook to the other side of the King. \n"
        message += "---------- \n"
    elif action == "rules":
        message = "---RULES--- \n"
        message += "To win, you must put the enemy King in Checkmate, where any move results in check. If your King is in sight of an opposing piece, you are in 'Check'. \n"
        message += "You must put your king out of danger by either capturing the attacking piece, moving out of the attack, or blocking the attack with another piece. \n"
        message += "It is Stalemate if the player has no legal moves and is not currently in Check. There is info on special moves like En Passant by inputting 'help'. \n"
        message += "----------- \n"
    elif action == "board":
        # prints the board again for the player if they inputted board
        print("\n   | a | b | c | d | e | f | g | h | Wins: " + str(blackWin))
        print("---+---+---+---+---+---+---+---+---+---")
        for row in range(8):
            print(" " + str(abs(8 - row)) + " |", end="")
            print("|".join(displayBoard[row]), end="")
            print("| " + str(abs(8 - row)))
            print(Style.RESET_ALL + "---+---+---+---+---+---+---+---+---+---")
        print("   | a | b | c | d | e | f | g | h | Wins: " + str(whiteWin))
        return ""
    elif action == "move" or action == "moves":
        print("Possible Moves: " + ", ".join(possibleMovesList))
        return ""
    elif action == "end":
        print("---PROGRAM TERMINATED--- \n")
        sys.exit(1)
    elif action == "draw":
        prompt_draw(playerColor, againstBot)
        return ""
    elif action == "resign":
        prompt_resign(playerColor, againstBot)
        return ""
    # if nothing, print a generic error message
    else:
        message = "---ERROR--- \n"
        message += "There was a mistake with your input. Please try again. Input 'help' or 'rules' if you need help formatting your input or learning how each piece moves. \n"
        message += "If you are struggling to type moves, input 'moves' to get a list of legal moves in your position, then choose one and input it as your move. \n"
        message += "You may input 'draw' to offer the other player a draw (AI Bot will decline draw offers) or 'resign' to immediately forfeit the game and have the other player win. \n"
        message += "If the terminal gets filled with too much text, you can input 'board' to print the board again. \n"
        message += "In case of error, input 'end' to immediately end and terminate the program. \n"
        message += "----------- \n"
    return message


# function checks if the players want to draw
def prompt_draw(playerColor, againstBot):
    global whiteWin
    global blackWin
    if againstBot == True:
        print("AI Bot has declined the draw offer. You can not offer a draw to the AI Bot!")
        return 1
    else:
        if playerColor == "white":
            otherColor = colored("black", "red")
        else:
            playerColor = colored("black", "red")
            otherColor = "white"
        print("Player " + playerColor + " is offering a draw.")
        # continuously prompts the player input until their either accept or decline
        while True:
            decision = input("Player " + otherColor + " do you 'accept' or 'decline'? ")
            decision = decision.lower().replace(" ", "")
            # check if the player wants to accept the draw
            if decision == "accept":
                print("Player " + otherColor + " has accepted the draw offer. Neither player wins. ")
                print("---Game ended. DRAW!--- \n")
                whiteWin += 0.5
                blackWin += 0.5
                prompt_rematch()
            elif decision == "decline":
                # returns 1 to continue the game
                print("Player " + otherColor + " has declined the draw offer. The game will continue. ")
                return 1


# function checks if the player wants to resign
def prompt_resign(playerColor, againstBot):
    global whiteWin
    global blackWin
    if playerColor == "white":
        otherColor = colored("black", "red")
    else:
        playerColor = colored("black", "red")
        otherColor = "white"
    print("Player " + playerColor + " has resigned.")
    # prints a different text depending if player was playing against ai bot
    if againstBot == True:
        print("---AI Bot " + otherColor + " is the winner!--- \n")
    else:
        print("---Player " + otherColor + " is the winner!--- \n")
    if playerColor == "white":
        blackWin += 1
    else:
        whiteWin += 1
    prompt_rematch()


# function prompts the players if they want to rematch
def prompt_rematch():
    print("CURRENT SCORE: " + str(whiteWin) + "-" + str(blackWin) + "\n")
    rematch = input("Would you like to play again? Type 'yes' or 'no': ")
    rematch = rematch.lower().replace(" ", "")
    if rematch == "yes":
        # if the players want to play again, call the main function again which also resets the board
        print("\033c")
        print("Restarting game \n")
        time.sleep(0.5)
        main()
    else:
        print("Ending Program")
        sys.exit(0)


# calls the main function to start the game loop
if __name__ == "__main__":
    main()