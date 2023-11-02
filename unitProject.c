// SCOPE - libraries
#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

// code taken from https://stackoverflow.com/questions/3585846/color-text-in-terminal-applications-in-unix
// NEW FEATURE - colored text
#define RED   "\x1B[31m"
#define RESET "\x1B[0m"

// defining variables
// SCOPE - variables
string white = RESET "o" RED;
string whiteKing = RESET "W" RED;
string red = RED "o";
string redKing = RED "W";
string empty = " ";
int initialLetter = 0;
int initialNumber = 0;
int finalLetter = 0;
int finalNumber = 0;
string playerMove;
string moveColor;
int turnCounter = 1;
int whiteCount = 1; // piece counter
int redCount = 1;
string errorMessage;
bool legalMove = false;
bool gameOver = false;

// SCOPE - array
// used for updating game board
string boardPiece[8][4];


// declaring functions, definitions are after main()
// SCOPE - functions
bool check_legal_move(string input);
string create_error_message(string message);
string update_board(string move, string board[8][4]);


int main(void)
{
    // initiating the setup pieces into the array
    // SCOPE - loops
    for (int c = 0; c < 4; c = c + 1)
    {
        // fills the top 3 rows with white
        for (int b = 0; b < 8; b = b + 1)
        {
            if (b < 3)
            {
                boardPiece[b][c] = white;
            }

            // fills the middle 2 rows with empty
            if (b >=3 && b < 5)
            {
                boardPiece[b][c] = empty;
            }

            // fills the bottom 3 rows with red
            if (b >= 5)
            {
                boardPiece[b][c] = red;
            }
        }
    }

    do
    {
        // prints the board with all the board pieces
        printf(RESET "--+---------------------------------+ \n");
        printf("H | " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "| \n", boardPiece[0][0], boardPiece[0][1], boardPiece[0][2], boardPiece[0][3]);
        printf("  |                                 | \n");
        printf("G |" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ] | \n", boardPiece[1][0], boardPiece[1][1], boardPiece[1][2], boardPiece[1][3]);
        printf("  |                                 | \n");
        printf("F | " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "| \n", boardPiece[2][0], boardPiece[2][1], boardPiece[2][2], boardPiece[2][3]);
        printf("  |                                 | \n");
        printf("E |" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ] | \n", boardPiece[3][0], boardPiece[3][1], boardPiece[3][2], boardPiece[3][3]);
        printf("  |                                 | \n");
        printf("D | " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "| \n", boardPiece[4][0], boardPiece[4][1], boardPiece[4][2], boardPiece[4][3]);
        printf("  |                                 | \n");
        printf("C |" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ] | \n", boardPiece[5][0], boardPiece[5][1], boardPiece[5][2], boardPiece[5][3]);
        printf("  |                                 | \n");
        printf("B | " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "| \n", boardPiece[6][0], boardPiece[6][1], boardPiece[6][2], boardPiece[6][3]);
        printf("  |                                 | \n");
        printf("A |" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ]" RED " [%s] " RESET "[ ] | \n", boardPiece[7][0], boardPiece[7][1], boardPiece[7][2], boardPiece[7][3]);
        printf("--+---------------------------------+ \n");
        printf("  |  1   2   3   4   5   6   7   8  | \n\n");

        // prints the current number of turns
        printf("--TURN %i-- \n", turnCounter);

        // checks whether its red's or white's move
        // SCOPE - conditional logic
        if (turnCounter % 2 == 1)
        {
            moveColor = RED "RED" RESET;
        } else {
            moveColor = RESET "WHITE";
        }

        do
        {
            // prompts player input of moves until the move is legal or until they end the game
            printf("%s", moveColor);
            // SCOPE - interactive element
            playerMove = get_string("s Move: ");

            // checks if player inputted end, then ends the program
            if (strcmp(playerMove, "end") == 0)
            {
                printf("----------\n");
                printf("GAME ENDED\n");
                printf("----------\n");
                return 1;
            }

            // checks if the players move if legal
            check_legal_move(playerMove);
            if (legalMove == false)
            {
                // if not legal move, gives the player an error message depending on what they wrote
                create_error_message(playerMove);
                printf("%s\n", errorMessage);
            }
        // keep prompting until they make a legal move
        } while (legalMove == false);

        // updates the gameboard to reflect the move
        update_board(playerMove, boardPiece);

        // checks if a piece is able to turn into a king piece
        for (int a = 0; a < 4; a = a + 1)
        {
            // checks if red piece is at the top end of the board
            if (boardPiece[0][a] == red)
            {
                // promotes that piece to king
                boardPiece[0][a] = redKing;
            }
            // checks if white piece is at the bottom of the board
            if (boardPiece[7][a] == white)
            {
                // promotes that piece to king
                boardPiece[7][a] = whiteKing;
            }
        }

        // reset legal move for the function
        legalMove = false;

        printf("--------- \n\n\n");
        // adds 1 to the turn counter SCOPE - math
        turnCounter = turnCounter + 1;

        // loops through board pieces to check if all the pieces of a color are still alive
        for (int x = 0; x < 8; x = x + 1)
        {
            for (int y = 0; y < 4; y = y + 1)
            {
                // checks for red pieces
                // SCOPE - logical operator
                if (boardPiece[x][y] == red || boardPiece[x][y] == redKing)
                {
                    redCount = redCount + 1;
                }
                // checks for white pieces
                if (boardPiece[x][y] == white || boardPiece[x][y] == whiteKing)
                {
                    whiteCount = whiteCount + 1;
                }
            }
        }

        // if a certain color no longer has any pieces, set gameOver to true
        if (redCount == 0 || whiteCount == 0)
        {
            gameOver = true;
        } else {
            // resets piece counts for the next loop
            redCount = 0;
            whiteCount = 0;
        }

    // continue until game is over and one side has no more pieces
    } while (gameOver == false);

    // prints the color of the winner then ends the program
    printf("----- GAME OVER -----\n");
    printf("%s is the winner! \n", moveColor);
    printf("---------------------\n");
    return 0;
}

// function checks if the selected piece can legally move to a selected position
bool check_legal_move(string input)
{
    // input should only have 5 characters
    if (strlen(input) == 5)
    {
        // check whether the correct datatypes were inputted
        if (isalpha(input[0]) && isdigit(input[1]) && isblank(input[2]) && isalpha(input[3]) && isdigit(input[4]) && atoi(&input[1]) <= 8 && atoi(&input[4]) <=8)
        {
            initialLetter = abs(toupper(input[0]) - 72);
            initialNumber = floor((atoi(&input[1]) + 1) / 2) - 1;
            finalLetter = abs(toupper(input[3]) - 72);
            finalNumber = floor((atoi(&input[4]) + 1) / 2) - 1;
            // printf("initial letter %i\n", initialLetter); // printtest
            // printf("initial number %i\n", initialNumber); // printtest
            // printf("final letter %i\n", finalLetter); // printtest
            // printf("final number %i\n", finalNumber); // printtest

            // if the initial or final number is 4, minus 1 to ensure index doesnt break
            if (initialNumber == 4)
            {
                initialNumber = initialNumber - 1;
            }
            if (finalNumber == 4)
            {
                finalNumber = finalNumber - 1;
            }
        } else {
            return legalMove = false;
        }

        // checks if it is reds turn SCOPE - complex logic
        if (turnCounter % 2 == 1)
        {
            for (int side = 1; side < 8; side = side + 2)
            {
                // checks if there a red piece/king on the far left odd side
                if (initialLetter == side && initialNumber == 0 && ((boardPiece[side][0] == red && boardPiece[initialLetter][initialNumber] == red) || (boardPiece[side][0] == redKing && boardPiece[initialLetter][initialNumber] == redKing)))
                {
                    // check red piece side movement
                    if (boardPiece[initialLetter][initialNumber] == red && boardPiece[finalLetter][finalNumber] == empty && initialLetter - 1 == finalLetter && initialNumber == finalNumber)
                    {
                        return legalMove = true;

                    // check red king side movement
                    } else if (boardPiece[initialLetter][initialNumber] == redKing && boardPiece[finalLetter][finalNumber] == empty && (initialLetter + 1 == finalLetter || initialLetter - 1 == finalLetter) && initialNumber == finalNumber) {
                        return legalMove = true;

                    // check if side piece is capturing
                    } else if ((boardPiece[initialLetter][initialNumber] == red || boardPiece[initialLetter][initialNumber] == redKing) && abs(initialLetter - 2) == finalLetter && initialNumber + 1 == finalNumber) {
                        // checks if diagonal piece is white
                        if (boardPiece[initialLetter - 1][initialNumber] == white || boardPiece[initialLetter - 1][initialNumber] == whiteKing)
                        {
                            return legalMove = true;
                        } else {
                            return legalMove = false;
                        }

                    } else {
                        return legalMove = false;
                    }
                }
            }

            // ensures initial position is red piece and final position is empty
            if (boardPiece[initialLetter][initialNumber] == red && boardPiece[finalLetter][finalNumber] == empty)
            {
                // check red piece movement
                if (initialLetter - 1 == finalLetter && (initialNumber == finalNumber || abs(initialNumber - 1) == finalNumber))
                {
                    return legalMove = true;

                // check red piece even movement
                } else if (initialLetter % 2 == 0 && initialLetter - 1 == finalLetter && (initialNumber == finalNumber || initialNumber + 1 == finalNumber)) {
                    return legalMove = true;

                // check red piece capture
                } else if (abs(initialLetter - 2) == finalLetter && (initialNumber + 1 == finalNumber || abs(initialNumber - 1) == finalNumber)) {
                    // check ODD left side
                    if (initialLetter % 2 == 1 && finalNumber + 1 == initialNumber && (boardPiece[initialLetter - 1][initialNumber - 1] == white || boardPiece[initialLetter - 1][initialNumber - 1] == whiteKing))
                    {
                        return legalMove = true;

                    // check odd and right side capture
                    } else if (initialLetter % 2 == 1 && finalNumber - 1 == initialNumber && (boardPiece[initialLetter - 1][initialNumber] == white || boardPiece[initialLetter - 1][initialNumber] == whiteKing)) {
                        return legalMove = true;

                    // check EVEN left side
                    } else if (initialLetter % 2 == 0 && finalNumber + 1 == initialNumber && (boardPiece[initialLetter - 1][initialNumber] == white || boardPiece[initialLetter - 1][initialNumber] == whiteKing)) {
                        return legalMove = true;

                    // check EVEN right side
                    } else if (initialLetter % 2 == 0 && finalNumber - 1 == initialNumber && (boardPiece[initialLetter - 1][initialNumber + 1] == white || boardPiece[initialLetter - 1][initialNumber + 1] == whiteKing)) {
                        return legalMove = true;

                    } else {
                        return legalMove = false;
                    }

                } else {
                    return legalMove = false;
                }

            // ensures initial position is red KING and final position is empty
            } else if (boardPiece[initialLetter][initialNumber] == redKing && boardPiece[finalLetter][finalNumber] == empty) {
                for (int let = 0; let < 8; let = let + 1)
                {
                    // check red king movement on odd letters
                    if (let % 2 == 1 && (initialNumber == finalNumber || abs(initialNumber - 1) == finalNumber) && (initialLetter + 1 == finalLetter || abs(initialLetter - 1) == finalLetter))
                    {
                        return legalMove = true;

                    // check red king movement on even letters
                    } else if ((initialNumber == finalNumber || initialNumber + 1 == finalNumber) && (initialLetter + 1 == finalLetter || abs(initialLetter - 1) == finalLetter)) {
                        return legalMove = true;

                    }
                }

                 // check red king capture
                if ((initialLetter + 2 == finalLetter || initialLetter - 2 == finalLetter) && (initialNumber + 1 == finalNumber || initialNumber - 1 == finalNumber))
                {
                    // EVEN top left
                    if (initialLetter % 2 == 0 && finalNumber + 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber] == white || boardPiece[initialLetter - 1][initialNumber] == whiteKing))
                    {
                        return legalMove = true;

                    // EVEN top right
                    } else if (initialLetter % 2 == 0 && finalNumber - 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber + 1] == white || boardPiece[initialLetter - 1][initialNumber + 1] == whiteKing)) {
                        return legalMove = true;

                    // EVEN bottom left
                    } else if (initialLetter % 2 == 0 && finalNumber + 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber] == white || boardPiece[initialLetter + 1][initialNumber] == whiteKing)) {
                        return legalMove = true;

                    // EVEN bottom right
                    } else if (initialLetter % 2 == 0 && finalNumber - 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber + 1] == white || boardPiece[initialLetter + 1][initialNumber + 1] == whiteKing)) {
                        return legalMove = true;

                    // ODD top left
                    } else if (initialLetter % 2 == 1 && finalNumber + 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber - 1] == white || boardPiece[initialLetter - 1][initialNumber - 1] == whiteKing)) {
                        return legalMove = true;

                    // ODD top right
                    } else if (initialLetter % 2 == 1 && finalNumber - 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber] == white || boardPiece[initialLetter - 1][initialNumber] == whiteKing)) {
                        return legalMove = true;

                    // ODD bottom left
                    } else if (initialLetter % 2 == 1 && finalNumber + 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber - 1] == white || boardPiece[initialLetter + 1][initialNumber - 1] == whiteKing)) {
                        return legalMove = true;

                    // ODD bottom right
                    } else if (initialLetter % 2 == 1 && finalNumber - 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber] == white || boardPiece[initialLetter + 1][initialNumber] == whiteKing)) {
                        return legalMove = true;

                    } else {
                        return legalMove = false;
                    }

                } else {
                    return legalMove = false;
                }

            } else {
                return legalMove = false;
            }

        // else move for white
        } else {
            for (int side = 0; side < 8; side = side + 2)
            {
                // checks if there a white piece/king on the far right odd side
                if (initialLetter == side && initialNumber == 3 && ((boardPiece[side][3] == white && boardPiece[initialLetter][initialNumber] == white) || (boardPiece[side][3] == whiteKing && boardPiece[initialLetter][initialNumber] == whiteKing)))
                {
                    // check white piece side movement
                    if (boardPiece[initialLetter][initialNumber] == white && boardPiece[finalLetter][finalNumber] == empty && initialLetter + 1 == finalLetter && initialNumber == finalNumber)
                    {
                        return legalMove = true;

                    // check white side king movement
                    } else if (boardPiece[initialLetter][initialNumber] == whiteKing && boardPiece[finalLetter][finalNumber] == empty && (initialLetter + 1 == finalLetter || initialLetter - 1 == finalLetter) && initialNumber == finalNumber) {
                        return legalMove = true;

                    // check if side piece is capturing
                    } else if ((boardPiece[initialLetter][initialNumber] == white || boardPiece[initialLetter][initialNumber] == whiteKing) && initialLetter + 2 == finalLetter && initialNumber - 1 == finalNumber) {
                        if (boardPiece[initialLetter + 1][initialNumber] == red || boardPiece[initialLetter - 1][initialNumber] == redKing)
                        {
                            return legalMove = true;
                        } else {
                            return legalMove = false;
                        }

                    } else {
                        return legalMove = false;
                    }
                }
            }

            // ensures initial position is white piece and final position is empty
            if (boardPiece[initialLetter][initialNumber] == white && boardPiece[finalLetter][finalNumber] == empty)
            {
                // check white piece/king movement
                if (initialLetter + 1 == finalLetter && (initialNumber == finalNumber || initialNumber + 1 == finalNumber))
                {
                    return legalMove = true;

                // check white piece odd movement
                } else if (initialLetter % 2 == 1 && initialLetter + 1 == finalLetter && (initialNumber == finalNumber || initialNumber - 1 == finalNumber)) {
                    return legalMove = true;

                // check white piece capture
                } else if (initialLetter + 2 == finalLetter && (initialNumber + 1 == finalNumber || abs(initialNumber - 1) == finalNumber)) {
                    // check ODD left side
                    if (initialLetter % 2 == 1 && finalNumber + 1 == initialNumber && (boardPiece[initialLetter + 1][initialNumber - 1] == red || boardPiece[initialLetter + 1][initialNumber - 1] == redKing))
                    {
                        return legalMove = true;

                    // check ODD right
                    } else if (initialLetter % 2 == 1 && finalNumber - 1 == initialNumber && (boardPiece[initialLetter + 1][initialNumber] == red || boardPiece[initialLetter + 1][initialNumber] == redKing)) {
                        return legalMove = true;

                    // check EVEN left
                    } else if (initialLetter % 2 == 0 && finalNumber + 1 == initialNumber && (boardPiece[initialLetter + 1][initialNumber] == red || boardPiece[initialLetter + 1][initialNumber] == redKing)) {
                        return legalMove = true;

                    // check EVEN right
                    } else if (initialLetter % 2 == 0 && finalNumber - 1 == initialNumber && (boardPiece[initialLetter + 1][initialNumber - 1] == red || boardPiece[initialLetter + 1][initialNumber - 1] == redKing)) {
                        return legalMove = true;

                    } else {
                        return legalMove = false;
                    }

                } else {
                    return legalMove = false;
                }

            // ensures initial position is white king and final position is empty
            } else if (boardPiece[initialLetter][initialNumber] == whiteKing && boardPiece[finalLetter][finalNumber] == empty) {
                for (int let = 0; let < 8; let = let + 1)
                {
                    // check white king movement on odd letters
                    if (let % 2 == 1 && (initialNumber == finalNumber || abs(initialNumber - 1) == finalNumber) && (initialLetter + 1 == finalLetter || abs(initialLetter - 1)))
                    {
                        return legalMove = true;

                    // check white king movement on even letters
                    } else if ((initialNumber == finalNumber || initialNumber + 1 == finalNumber) && (initialLetter + 1 == finalLetter || abs(initialLetter - 1) == finalLetter)) {
                        return legalMove = true;

                    }
                }

                // check white king capture
                if ((initialLetter + 2 == finalLetter || initialLetter - 2 == finalLetter) && (initialNumber + 1 == finalNumber || initialNumber - 1 == finalNumber))
                {
                    // EVEN top left
                    if (initialLetter % 2 == 0 && finalNumber + 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber] == red || boardPiece[initialLetter - 1][initialNumber] == redKing))
                    {
                        return legalMove = true;

                    // EVEN top right
                    } else if (initialLetter % 2 == 0 && finalNumber - 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber + 1] == red || boardPiece[initialLetter - 1][initialNumber + 1] == redKing)) {
                        return legalMove = true;

                    // EVEN bottom left
                    } else if (initialLetter % 2 == 0 && finalNumber + 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber] == red || boardPiece[initialLetter + 1][initialNumber] == redKing)) {
                        return legalMove = true;

                    // EVEN bottom right
                    } else if (initialLetter % 2 == 0 && finalNumber - 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber + 1] == red || boardPiece[initialLetter + 1][initialNumber + 1] == redKing)) {
                        return legalMove = true;

                    // ODD top left
                    } else if (initialLetter % 2 == 1 && finalNumber + 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber - 1] == red || boardPiece[initialLetter - 1][initialNumber - 1] == redKing)) {
                        return legalMove = true;

                    // ODD top right
                    } else if (initialLetter % 2 == 1 && finalNumber - 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber] == red || boardPiece[initialLetter - 1][initialNumber] == redKing)) {
                        return legalMove = true;

                    // ODD bottom left
                    } else if (initialLetter % 2 == 1 && finalNumber + 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber - 1] == red || boardPiece[initialLetter + 1][initialNumber - 1] == redKing)) {
                        return legalMove = true;

                    // ODD bottom right
                    } else if (initialLetter % 2 == 1 && finalNumber - 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber] == red || boardPiece[initialLetter + 1][initialNumber] == redKing)) {
                        return legalMove = true;

                    } else {
                        return legalMove = false;
                    }

                } else {
                    return legalMove = false;
                }
            }
        }

    } else {
        // return error if letters arent A-H or numbers arent 1-8
        return legalMove = false;
    }

    return legalMove = false;
}

// function chooses which message to display
string create_error_message(string message)
{
    // turns the message lower case
    for (int m = 0; m < strlen(message); m = m + 1)
    {
        message[m] = tolower(message[m]);
    }

    // check if player typed rules
    if (strcmp((message), "rules") == 0)
    {
        // print rules message
        errorMessage = "---RULES--- \nPieces can only move forward diagonally and capture diagonally. Unlike real Checkers, capture is not forced and only one piece can be captured at a time. \nIf your piece (o) makes it to the other side, it becomes a king (W) and can now move forwards or backwards. \nTake turns until one side has no remaining pieces left.";
    // check if player typed help
    } else if (strcmp((message), "help") == 0) {
        // print help message
        errorMessage = "---HELP---\nPieces can only move forward diagonally unless they are a king (can move backwards). Put your moves with letter first, \nthen the number like [Initial position] space [Final Position]. Example C3 D2. Capitalization doesnt matter. \nIf capturing, [Final Pos] will be the square behind the enemy piece. \nCapture is not forced and only one piece can be captured at a time. Example C3 E5";
    } else {
        // print generic error message
        errorMessage = "Unknown move. Type 'help' to help format input, 'rules' to learn how to play, or 'end' to end the program.";
    }
    return errorMessage;
}

// function takes player moves and updates the board
string update_board(string move, string board[8][4])
{
    // check if it was a capture
    if (initialLetter + 2 == finalLetter || initialLetter - 2 == finalLetter)
    {
        // check if red piece did the capture
        if (boardPiece[initialLetter][initialNumber] == red)
        {
            // check odd left side
            if (initialLetter % 2 == 1 && finalNumber + 1 == initialNumber && (boardPiece[initialLetter - 1][initialNumber - 1] == white || boardPiece[initialLetter - 1][initialNumber - 1] == whiteKing))
            {
                boardPiece[initialLetter - 1][initialNumber - 1] = empty;

            // check odd and right side capture
            } else if (initialLetter % 2 == 1 && finalNumber - 1 == initialNumber && (boardPiece[initialLetter - 1][initialNumber] == white || boardPiece[initialLetter - 1][initialNumber] == whiteKing)) {
                boardPiece[initialLetter - 1][initialNumber] = empty;

            // check EVEN left side
            } else if (initialLetter % 2 == 0 && finalNumber + 1 == initialNumber && (boardPiece[initialLetter - 1][initialNumber] == white || boardPiece[initialLetter - 1][initialNumber] == whiteKing)) {
                boardPiece[initialLetter - 1][initialNumber] = empty;

            // check EVEN right side
            } else if (initialLetter % 2 == 0 && finalNumber - 1 == initialNumber && (boardPiece[initialLetter - 1][initialNumber + 1] == white || boardPiece[initialLetter - 1][initialNumber + 1] == whiteKing)) {
                boardPiece[initialLetter - 1][initialNumber + 1] = empty;
            }

            boardPiece[finalLetter][finalNumber] = red;
        }

        // check if red king is capturing
        if (boardPiece[initialLetter][initialNumber] == redKing)
        {
            // EVEN top left
            if (initialLetter % 2 == 0 && finalNumber + 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber] == white || boardPiece[initialLetter - 1][initialNumber] == whiteKing))
            {
                boardPiece[initialLetter - 1][initialNumber] = empty;

            // EVEN top right
            } else if (initialLetter % 2 == 0 && finalNumber - 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber + 1] == white || boardPiece[initialLetter - 1][initialNumber + 1] == whiteKing)) {
                boardPiece[initialLetter - 1][initialNumber + 1] = empty;

            // EVEN bottom left
            } else if (initialLetter % 2 == 0 && finalNumber + 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber] == white || boardPiece[initialLetter + 1][initialNumber] == whiteKing)) {
                boardPiece[initialLetter + 1][initialNumber] = empty;

            // EVEN bottom right
            } else if (initialLetter % 2 == 0 && finalNumber - 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber + 1] == white || boardPiece[initialLetter + 1][initialNumber + 1] == whiteKing)) {
                boardPiece[initialLetter + 1][initialNumber + 1] = empty;

            // ODD top left
            } else if (initialLetter % 2 == 1 && finalNumber + 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber - 1] == white || boardPiece[initialLetter - 1][initialNumber - 1] == whiteKing)) {
                boardPiece[initialLetter - 1][initialNumber - 1] = empty;

            // ODD top right
            } else if (initialLetter % 2 == 1 && finalNumber - 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber] == white || boardPiece[initialLetter + 1][initialNumber] == whiteKing)) {
                boardPiece[initialLetter - 1][initialNumber] = empty;

            // ODD bottom left
            } else if (initialLetter % 2 == 1 && finalNumber + 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber - 1] == white || boardPiece[initialLetter + 1][initialNumber - 1] == whiteKing)) {
                boardPiece[initialLetter + 1][initialNumber - 1] = empty;

            // ODD bottom right
            } else if (initialLetter % 2 == 1 && finalNumber - 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber] == white || boardPiece[initialLetter + 1][initialNumber] == whiteKing)) {
                boardPiece[initialLetter + 1][initialNumber] = empty;
            }

            boardPiece[finalLetter][finalNumber] = redKing;
        }

        // check if white piece did the move
        if (boardPiece[initialLetter][initialNumber] == white)
        {
            // check ODD left
            if (initialLetter % 2 == 1 && finalNumber + 1 == initialNumber && (boardPiece[initialLetter + 1][initialNumber - 1] == red || boardPiece[initialLetter + 1][initialNumber - 1] == redKing))
            {
                boardPiece[initialLetter + 1][initialNumber - 1] = empty;

            // check ODD right
            } else if (initialLetter % 2 == 1 && finalNumber - 1 == initialNumber && (boardPiece[initialLetter + 1][initialNumber] == red || boardPiece[initialLetter + 1][initialNumber] == redKing)) {
                boardPiece[initialLetter + 1][initialNumber] = empty;

            // check EVEN left
            } else if (initialLetter % 2 == 0 && finalNumber + 1 == initialNumber && (boardPiece[initialLetter + 1][initialNumber] == red || boardPiece[initialLetter + 1][initialNumber] == redKing)) {
                boardPiece[initialLetter + 1][initialNumber] = empty;

            // check EVEN right
            } else if (initialLetter % 2 == 0 && finalNumber - 1 == initialNumber && (boardPiece[initialLetter + 1][initialNumber - 1] == red || boardPiece[initialLetter + 1][initialNumber - 1] == redKing)) {
                boardPiece[initialLetter + 1][initialNumber - 1] = empty;
            }

            boardPiece[finalLetter][finalNumber] = white;
        }

        // checks if white king did the capture
        if (boardPiece[initialLetter][initialNumber] == whiteKing)
        {
            // checks for a red piece/king in the direction of capture and turn that position empty
            // EVEN top left
            if (initialLetter % 2 == 0 && finalNumber + 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber] == red || boardPiece[initialLetter - 1][initialNumber] == redKing))
            {
                boardPiece[initialLetter - 1][initialNumber] = empty;

            // EVEN top right
            } else if (initialLetter % 2 == 0 && finalNumber - 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber + 1] == red || boardPiece[initialLetter - 1][initialNumber + 1] == redKing)) {
                boardPiece[initialLetter - 1][initialNumber + 1] = empty;

            // EVEN bottom left
            } else if (initialLetter % 2 == 0 && finalNumber + 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber] == red || boardPiece[initialLetter + 1][initialNumber] == redKing)) {
                boardPiece[initialLetter + 1][initialNumber] = empty;

            // EVEN bottom right
            } else if (initialLetter % 2 == 0 && finalNumber - 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber + 1] == red || boardPiece[initialLetter + 1][initialNumber + 1] == redKing)) {
                boardPiece[initialLetter + 1][initialNumber + 1] = empty;

            // ODD top left
            } else if (initialLetter % 2 == 1 && finalNumber + 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber - 1] == red || boardPiece[initialLetter - 1][initialNumber - 1] == redKing)) {
                boardPiece[initialLetter - 1][initialNumber - 1] = empty;

            // ODD top right
            } else if (initialLetter % 2 == 1 && finalNumber - 1 == initialNumber && initialLetter - 2 == finalLetter && (boardPiece[initialLetter - 1][initialNumber] == red || boardPiece[initialLetter - 1][initialNumber] == redKing)) {
                boardPiece[initialLetter - 1][initialNumber] = empty;

            // ODD bottom left
            } else if (initialLetter % 2 == 1 && finalNumber + 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber - 1] == red || boardPiece[initialLetter + 1][initialNumber - 1] == redKing)) {
                boardPiece[initialLetter + 1][initialNumber - 1] = empty;

            // ODD bottom right
            } else if (initialLetter % 2 == 1 && finalNumber - 1 == initialNumber && initialLetter + 2 == finalLetter && (boardPiece[initialLetter + 1][initialNumber] == red || boardPiece[initialLetter + 1][initialNumber] == redKing)) {
                boardPiece[initialLetter + 1][initialNumber] = empty;
            }

            boardPiece[finalLetter][finalNumber] = whiteKing;
        }

    // regular movement
    } else {
        // checks the color of initial position, then turns final position into that color
        if (board[initialLetter][initialNumber] == red)
        {
            board[finalLetter][finalNumber] = red;
        }
        if (board[initialLetter][initialNumber] == redKing)
        {
            board[finalLetter][finalNumber] = redKing;
        }
        if (board[initialLetter][initialNumber] == white)
        {
            board[finalLetter][finalNumber] = white;
        }
        if (board[initialLetter][initialNumber] == whiteKing)
        {
            board[finalLetter][finalNumber] = whiteKing;
        }
    }

    // turns the piece in the initial position empty after the piece moves to a new spot
    board[initialLetter][initialNumber] = empty;

    // exits the function
    return 0;
} // perfectly 700 lines :)
