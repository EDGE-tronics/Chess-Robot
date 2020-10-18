
'''

chess.SQUARE_NAMES.index("h8")
print(chess.piece_name(board.piece_type_at(chess.A7)))

chess.piece_name(board.piece_type_at(chess.SQUARE_NAMES.index("e3")))

chess.square_file(chess.SQUARE_NAMES.index("e2")) #me da realmente la columna, el resiltado para este ejemplo es 4

chess.square_rank(chess.SQUARE_NAMES.index("e2")) #Da como resultado la fila, para este ejemplo es 1

board.piece_type_at(chess.SQUARE_NAMES.index("e3")) == None

'''

#CONSTRUIREMOS LAS FUNCIONES BASICAS PARA EL CASO DE JUGAR CON BLANCAS

#Modificar sistema de juego para en lugar de colocar la jugada, cologar un vector de casillas

import chess
import chess.engine

def showCheck(board):
    if board.is_check():
        print("CHECK!!")

def sequenceGenerator(uciMove, board):
    '''
    INPUT: 
        uciMove -> Move in UCI format to analyze it. 
        board -> Game state, this is a chess.Board() object.
    OUTPUT:
        result -> Is empty if a valid move is not detected, if it is detected then it is a dictionary data structure with two values:
            "seq": String with a sequence of chess coordinates to guide th robot movement.
            "type": String with type of movement, Castling-Promotion-Move-Capture-Passant.
    '''
    result = {}
    move = chess.Move.from_uci(uciMove)
    first = uciMove[:2]
    second = uciMove[2:4]
    last = uciMove[-1]
    graveyard = "k0"

    if last < '1' or last > '8': # Promotion Evaluation: Check if last char is a letter.
        if board.is_capture(move):
            result["seq"] = second + graveyard + first + second
        else:
            result["seq"] = first + second
        result["type"] = "Promotion"
    elif board.turn and uciMove == "e1g1" and chess.piece_name(board.piece_type_at(chess.SQUARE_NAMES.index("e1"))) == "king": #White King side castling
        result["seq"] = first + second + "h1f1"
        result["type"] = "White King Side Castling"
    elif board.turn and uciMove == "e1c1" and chess.piece_name(board.piece_type_at(chess.SQUARE_NAMES.index("e1"))) == "king": #White Queen side castling
        result["seq"] = first + second + "a1d1"
        result["type"] = "White Queen Side Castling"
    elif not board.turn and uciMove == "e8g8" and chess.piece_name(board.piece_type_at(chess.SQUARE_NAMES.index("e8"))) == "king": #Black King side castling
        result["seq"] = first + second + "h8f8"
        result["type"] = "Black King Side Castling"
    elif not board.turn and uciMove == "e8c8" and chess.piece_name(board.piece_type_at(chess.SQUARE_NAMES.index("e8"))) == "king": #Black Queen side castling
        result["seq"] = first + second + "a8d8"
        result["type"] = "White Queen Side Castling"
    elif board.is_en_passant(move): # En Passant
        if board.turn:
            squareFile = chess.square_file(chess.SQUARE_NAMES.index(first)) 
            squareRank = chess.square_rank(chess.SQUARE_NAMES.index(first))
            result["seq"] = chess.SQUARE_NAMES[chess.square(squareFile-1,squareRank)] + graveyard + first + second
            result["type"] = "Passant"
        else:
            squareFile = chess.square_file(chess.SQUARE_NAMES.index(first)) 
            squareRank = chess.square_rank(chess.SQUARE_NAMES.index(first))
            result["seq"] = chess.SQUARE_NAMES[chess.square(squareFile+1,squareRank)] + graveyard + first + second
            result["type"] = "Passant"
    elif board.is_capture(move): # Capture move
        result["seq"] = second + graveyard + first + second
        result["type"] = "Capture"
    else: # Normal move
        result["seq"] = uciMove
        result["type"] = "Move"  

    return result

def moveAnalysis (squares, board):
    '''
    INPUT: 
        squares -> Squares detected by the computer vision algorithm. 
        board -> State of game, this is a chess.Board() object.
    OUTPUT:
        result -> Is empty if a valid move is not detected, or on the contrary, a dictionary data structure with two values:
            "move": String with the valid movement in UCI format, for example "e2e4".
            "type": String with type of movement, Castling-Promotion-Move-Capture-Passant.

    NOTE: In case of promotion we must concatenate the new piece to UCI command, 
          before pushing the move to the board state, we ask the user which is the promoted piece.
    '''

    result = {}  # Move type, move coordinates
    kindOfMove = ""
    uciMove = ""

    elements =  len(squares)
    if elements < 5 and elements > 1:  # Lenght verification
        legalMoves = board.legal_moves

        if elements == 4: # Clastling evaluation
            if board.turn: # White Turn
                if ("e1" in squares) and ("h1" in squares): # Queen side castling evaluation
                    if chess.Move.from_uci("e1g1") in legalMoves:
                        result["move"] = "e1g1"
                        result["type"] = "Castling"
                if ("e1" in squares) and ("a1" in squares): # Queen side castling evaluation
                    if chess.Move.from_uci("e1c1") in legalMoves:
                        result["move"] = "e1c1"
                        result["type"] = "Castling"   
            else: # Black Turn
                if ("e8" in squares) and ("h8" in squares): # Queen side castling evaluation
                    if chess.Move.from_uci("e8g8") in legalMoves:
                        result["move"] = "e8g8"
                        result["type"] = "Castling"
                if ("e8" in squares) and ("a8" in squares): # Queen side castling evaluation
                    if chess.Move.from_uci("e8c8") in legalMoves:
                        result["move"] = "e8c8"
                        result["type"] = "Castling" 
        
        if not result:
            moveVector = [squares[0]+squares[1],squares[1]+squares[0]] # Instantiate the list with the two most probable movements
            if elements > 2:
                moveVector.append(squares[0]+squares[2])
                moveVector.append(squares[2]+squares[0])
                moveVector.append(squares[1]+squares[2])
                moveVector.append(squares[2]+squares[1])
            for uciMove in moveVector: # Move Validation
                move = chess.Move.from_uci(uciMove)
                if move in legalMoves:
                    result["move"] = uciMove
                    if board.is_en_passant(move):
                        result["type"] = "Passant"
                    elif board.is_capture(move):
                        result["type"] = "Capture"
                    else:
                        result["type"] = "Move"             
                    return result
                elif chess.Move.from_uci(uciMove+"q") in legalMoves:
                    result["move"] = uciMove
                    result["type"] = "Promotion"
                    return result

    return result