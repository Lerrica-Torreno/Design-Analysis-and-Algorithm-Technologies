# 3x8 chess board using backtracking algorithm

# outer function (board, starts algorithm)
def knightMoves():
    # items will be stored as tuple (col,row)
    moves = [] 
    LMoves = [(2, 1), (-2, 1), (2, -1), (-2, -1), # possible L-moves (+ DOWN/right, - UP/right)   
            (1, 2), (-1, 2), (1, -2), (-1, -2)] # (x - vertical movement) & (y - horizontal movement) 

    # inner function (main, recursive backtracking)
    def backTrack(row, col, moveCount):
        # nonlocal - to access variable from outer function
        nonlocal moves, LMoves 
        # adds current position to moves (list)
        moves.append((row, col)) 
        
        # if it completes all squares it will print the result
        if moveCount == 24: 
            output = "moves: \n"
            #print("moves: ")
            # knight's move will be stored in moves (list)
            for move in moves: 
                # (+=) will continuously display new output every run in txt file 
                # printed in this format (1-col, 0-row)
                output += f"{move[1]}{move[0]}\n"
            
            # saves output to txt file 
            with open("chessOutput.txt", "a") as file:
                file.write(output)
                print(output)
            return True

        # loops in every LMoves
        for x, y in LMoves: 
            # col converted to ord (ASCII) + y converted back to chr
            # 97:a, 98:b, 99:c
            nextRow, nextCol = row + x, chr(ord(col) + y) # row/col = current row/col, x/y = from LMove

            # nextRow = 1-8, nextCol = a-c, no repeat of combination (x,y) in moves
            if 1 <= nextRow <= 8 and 'a' <= nextCol <= 'c' and (nextRow, nextCol) not in moves:
                # repeats function and adds score in moveCount
                if backTrack(nextRow, nextCol, moveCount + 1): 
                    return True 
        
        # removes move if conditions are not met 
        moves.pop()
        return False 
    
    # starting row and column 
    startRow, startCol = 1, 'a'

    # error handling for row 
    if startRow < 1 or startRow > 9:
        # writes error output in txt 
        with open("chessOutput.txt", "a") as file: 
            file.write(f"Invalid starting row {startRow}. Start from 1-8 only.\n") 
        # prints output 
        print(f"Invalid starting row {startRow}. Start from 1-8 only.\n") 
        return
    
    # error handling for column 
    if startCol < 'a' or startCol > 'c':
        # writes error output in txt 
        with open("chessOutput.txt", "a") as file:
            file.write(f"Invalid starting column {startCol}. Start in a, b, or c only.\n") 
        # prints output 
        print(f"Invalid starting column {startCol}. Start in a, b, or c only.")
        return 
    
    # calls functions 
    backTrack(startRow, startCol, 1)
knightMoves()

