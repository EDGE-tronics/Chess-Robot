import PySimpleGUI as sg
import ChessLogic as cl
import time
import os
import copy
import threading
import time


'''
styles:

BlueMono
GreenTan
LightGreen
Black
Dark
'''
CHESS_PATH = 'pieces_images'  # path to the chess pieces

BLANK = 0  # piece names
PAWNB = 1
KNIGHTB = 2
BISHOPB = 3
ROOKB = 4
KINGB = 5
QUEENB = 6
PAWNW = 7
KNIGHTW = 8
BISHOPW = 9
ROOKW = 10
KINGW = 11
QUEENW = 12

initial_board = [[ROOKB, KNIGHTB, BISHOPB, QUEENB, KINGB, BISHOPB, KNIGHTB, ROOKB],
                 [PAWNB, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [PAWNW, ] * 8,
                 [ROOKW, KNIGHTW, BISHOPW, QUEENW, KINGW, BISHOPW, KNIGHTW, ROOKW]]

psg_board = copy.deepcopy(initial_board)

blank = os.path.join(CHESS_PATH, 'blank.png')
bishopB = os.path.join(CHESS_PATH, 'nbishopb.png')
bishopW = os.path.join(CHESS_PATH, 'nbishopw.png')
pawnB = os.path.join(CHESS_PATH, 'npawnb.png')
pawnW = os.path.join(CHESS_PATH, 'npawnw.png')
knightB = os.path.join(CHESS_PATH, 'nknightb.png')
knightW = os.path.join(CHESS_PATH, 'nknightw.png')
rookB = os.path.join(CHESS_PATH, 'nrookb.png')
rookW = os.path.join(CHESS_PATH, 'nrookw.png')
queenB = os.path.join(CHESS_PATH, 'nqueenb.png')
queenW = os.path.join(CHESS_PATH, 'nqueenw.png')
kingB = os.path.join(CHESS_PATH, 'nkingb.png')
kingW = os.path.join(CHESS_PATH, 'nkingw.png')

images = {BISHOPB: bishopB, BISHOPW: bishopW, PAWNB: pawnB, PAWNW: pawnW, KNIGHTB: knightB, KNIGHTW: knightW,
          ROOKB: rookB, ROOKW: rookW, KINGB: kingB, KINGW: kingW, QUEENB: queenB, QUEENW: queenW, BLANK: blank}


graveyard = 'k0'
userColor = True
playing =  False
blackSquareColor = '#B58863'
whiteSquareColor = '#F0D9B5'
Debug = False
sequence = []
state = "stby"


def timer():
   now = time.localtime(time.time())
   print (now.tm_hour)
   print (now.tm_min)
   print (now.tm_sec)
   return now

def render_square(image, key, location):
    if (location[0] + location[1]) % 2:
        color =  blackSquareColor
    else:
        color = whiteSquareColor
    return sg.Button('', image_filename=image, size=(1, 1),
                          border_width=0, button_color=('white', color),
                          pad=(0, 0), key=key)

def redrawBoard():
    columns = 'abcdefgh'
    global userColor
    if userColor:
        for i in range(8):
            window.FindElement(key = str(8-i)+"r").Update("   "+str(8-i))
            window.FindElement(key = str(8-i)+"l").Update(str(8-i)+"   ")
            for j in range(8):
                window.FindElement(key = columns[j]+"t").Update(columns[j])
                window.FindElement(key = columns[j]+"b").Update(columns[j])    
                color = blackSquareColor if (i + j) % 2 else whiteSquareColor
                piece_image = images[initial_board[i][j]]
                elem = window.FindElement(key=(i, j))
                elem.Update(button_color=('white', color),
                            image_filename=piece_image, )
    else:
        for i in range(8):
            window.FindElement(key = str(8-i)+"r").Update("   "+str(i+1))
            window.FindElement(key = str(8-i)+"l").Update(str(i+1)+"   ")
            for j in range(8):
                window.FindElement(key = columns[j]+"t").Update(columns[7-j])
                window.FindElement(key = columns[j]+"b").Update(columns[7-j]) 
                color = blackSquareColor if (i + j) % 2 else whiteSquareColor
                piece_image = images[initial_board[7-i][7-j]]
                elem = window.FindElement(key=(i, j))
                elem.Update(button_color=('white', color),
                            image_filename=piece_image, )

def updateBoard(window, move):
    global userColor
    for cont in range(0,len(move["seq"]),4):
        squareCleared = move["seq"][cont:cont+2]
        squareOcuped = move["seq"][cont+2:cont+4]
        y = cl.chess.square_file(cl.chess.SQUARE_NAMES.index(squareCleared))
        x = 7 - cl.chess.square_rank(cl.chess.SQUARE_NAMES.index(squareCleared))

        piece_image = images[psg_board[x][y]] 
        piece = psg_board[x][y]
        psg_board[x][y] = BLANK
        color = blackSquareColor if (x + y) % 2 else whiteSquareColor
        if userColor:
            elem = window.FindElement(key=(x, y))
        else:
            elem = window.FindElement(key=(7-x, 7-y))
        elem.Update(button_color=('white', color),
                    image_filename=blank, )  

        if squareOcuped != graveyard:
            y = cl.chess.square_file(cl.chess.SQUARE_NAMES.index(squareOcuped))
            x = 7 - cl.chess.square_rank(cl.chess.SQUARE_NAMES.index(squareOcuped))
            psg_board[x][y] = piece
            color = blackSquareColor if (x + y) % 2 else whiteSquareColor
            if userColor:
                elem = window.FindElement(key=(x, y))
            else:
                elem = window.FindElement(key=(7-x, 7-y))    
            elem.Update(button_color=('white', color),
                        image_filename=piece_image, )         

def newGameWindow ():
    global userColor
    global playing
    windowName = "Configuration"
    initGame = [[sg.CBox('Play As White', key='userWhite', default = userColor)], [sg.Submit("Save")]]
    windowNewGame = sg.Window(windowName, default_button_element_size=(12,1), auto_size_buttons=False, icon='kingb.ico').Layout(initGame)
    while True:
        button,value = windowNewGame.Read()
        if button == "Save":
            playing = True
            userColor = value["userWhite"]
            break
        if button in (None, 'Exit'): #MAIN WINDOW
            break   
    windowNewGame.close() 

def quitGameWindow ():
    global playing
    global window
    windowName = "Configuration"
    quitGame = [[sg.Text('Are you sure?',justification='center', size=(30, 1), font='Any 13')], [sg.Submit("Yes",  size=(15, 1)),sg.Submit("No", size=(15, 1))]]
    if playing:
        while True:
            windowNewGame = sg.Window(windowName, default_button_element_size=(12,1), auto_size_buttons=False, icon='kingb.ico').Layout(quitGame)
            button,value = windowNewGame.Read()
            if button == "Yes":
                playing = False
                break
            if button in (None, 'Exit', "No"): #MAIN WINDOW
                break   
    windowNewGame.close()   

def mainBoardLayout():
    # ------ Menu Definition ------ #      
    menu_def = [['Properties'],      
                ['Help', 'About...'], ]  


    # ------ Layout ------ # 
    # sg.SetOptions(margins=(0,0))
    sg.ChangeLookAndFeel('Dark')
    # create initial board setup
    board = copy.deepcopy(initial_board)
    # the main board display layout
    board_layout = [[sg.T(' '*12)] + [sg.T('{}'.format(a), pad=((0,47),0), font='Any 13', key = a+'t') for a in 'abcdefgh']]
    # loop though board and create buttons with images
    for i in range(8):
        numberRow = 8-i 
        row = [sg.T(str(numberRow)+'   ', font='Any 13', key = str(numberRow)+"l")]
        for j in range(8):
            piece_image = images[board[i][j]]
            row.append(render_square(piece_image, key=(i,j), location=(i,j)))
        row.append(sg.T('   '+str(numberRow), font='Any 13', key = str(numberRow)+"r"))
        board_layout.append(row)
    # add the labels across bottom of board
    board_layout.append([sg.T(' '*12)] + [sg.T('{}'.format(a), pad=((0,47),0), font='Any 13', key = a+'b') for a in 'abcdefgh'])

    board_controls = [[sg.RButton('New Game', key='newGame', size=(13, 2), font=('courier', 16))],
                        [sg.RButton('Quit', key='quit', size=(6, 2), font=('courier', 16), disabled = True),sg.RButton('Draw', key='draw', size=(6, 2), font=('courier', 16), disabled = True)],
                        [sg.InputText('' , size=(12, 1))],
                        [sg.InputText('' , size=(12, 1))],
                        [sg.InputText('' , size=(12, 1))],
                        [sg.InputText('' , size=(12, 1))],
                        [sg.Button("Send",key='seqButton', size=(13, 2), font=('courier', 16))]]

    layout = [[sg.Menu(menu_def, tearoff=False)], 
                [sg.Column(board_layout),sg.VerticalSeparator(pad=None),sg.Column(board_controls)]]

    return layout

def pcTurn(board,engine):
    global sequence
    global state
    pcMove = engine.play(board, cl.chess.engine.Limit(time=1))
    sequence = cl.sequenceGenerator(pcMove.move.uci(), board)
    board.push(pcMove.move)
    state = "updatePcMove"
    updateBoard(window, sequence)


def playerTurn(board,squares):
    result = cl.moveAnalysis(squares, board)
    if result:
        if result["type"] == "Promotion":
            result["move"] += "q"
        sequence = cl.sequenceGenerator(result["move"], board)
        board.push_uci(result["move"])
        updateBoard(window, sequence)
        return True
    else:
        return False

def startGame():
    global psg_board
    window.FindElement("newGame").Update(disabled=True)
    window.FindElement("draw").Update(disabled=False)
    window.FindElement("quit").Update(disabled=False)
    psg_board = copy.deepcopy(initial_board)
    redrawBoard()


def quitGame():
    #engine.quit()
    window.FindElement("newGame").Update(disabled=False)
    window.FindElement("draw").Update(disabled=True)
    window.FindElement("quit").Update(disabled=True)

def chessThread ():
    if not board.is_game_over() and playing and (not userColor == board.turn):
        pcTurn(board,engine)
    elif board.is_game_over() and playing:
        quitGame(engine)
        print("GAME OVER")

def test(num1,num2):
    suma = num1+num2
    print(suma)
    return suma


layout = mainBoardLayout()
window = sg.Window('ChessRobot', default_button_element_size=(12,1), auto_size_buttons=False, icon='kingb.ico').Layout(layout)


'''
def main():
    
    squares = []
    global playing
    global psg_board
    board = cl.chess.Board()
    chessThread = threading.Thread(name='chessThread', target=test, args=(1,3,))
    while True:
        button, value = window.Read(timeout=100)

        if button =="newGame" and not playing:
            print("entro en new")
            #window.Disable()
            newGameWindow()
            #window.Enable()
            if playing:
                board, engine = startGame()
                refTime = time.time()
                button, value = window.Read(timeout=100)
                

        if button =="quit" and playing:
            print("entro en quit")
            quitGameWindow()
            if not playing:
                quitGame(engine) 
                button, value = window.Read(timeout=100)  
     

        if button == "seqButton":
            print("entro en send")
            print(button,value)
            squares.append(value[1])
            squares.append(value[2])
            squares.append(value[3])
            squares.append(value[4])
            print(squares)
            if not board.is_game_over() and playing and (userColor == board.turn):
                playerTurn(board, squares)
            elif board.is_game_over() and playing:
                quitGame(engine)
                print("GAME OVER")
            print(board)
            squares.clear()
            button, value = window.Read(timeout=100)
        
        if playing:
            now = time.time() - refTime
            time_string = time.strftime("%H:%M:%S", time.gmtime(now))
            window["seqButton"].Update(time_string)
            print(time_string)

        if button in (None, 'Exit'): #MAIN WINDOW
            break      


    window.close()    
'''

def main():
    global userColor
    global state
    global playing
    global sequence
    board = cl.chess.Board()
    engine = cl.chess.engine.SimpleEngine.popen_uci("stockfishX64.exe")
    squares = []
    
    while True:
        button, value = window.Read(timeout=100)
        
        if button =="newGame":
            print("entro en new")
            state = "startMenu"
        
        if button =="quit":
            print("entro en quit")
            quitGameWindow()
            if not playing:
                state = "returnPos"

        if board.is_game_over() and playing:
            quitGame()
            playing = False
            print("GAME OVER")
            state = "returnPos"


        if state == "stby": #stby
            print(state)

        elif state == "startMenu": #Start Menu
            print(state)
            newGameWindow()
            if playing:
                startGame()
                board = cl.chess.Board()
                engine = cl.chess.engine.SimpleEngine.popen_uci("stockfishX64.exe")
                if userColor:
                    state = "playerTurn"
                else:
                    state = "pcTurn"
            else:
                state = "stby"

        elif state == "playerTurn": #Player Turn
            print(state)
            
            if button == "seqButton":
                print("entro en send")
                state = "moveDetection"

        elif state == "moveDetection": #Computer vision movement detection and move Validation
            print(state)
            print(button,value)
            squares.append(value[1])
            squares.append(value[2])
            if value[3]:
                squares.append(value[3])
            if value[4]:
                squares.append(value[4])
            print(squares)
            if playerTurn(board, squares):
                state = "pcTurn"
            else:
                print("INVALID MOVE")
                state = "playerTurn"
            print(board)
            squares.clear()
        
        elif state == "pcTurn": #PC turn
            print(state)
            processThread = threading.Thread(target=pcTurn, args=(board,engine,), daemon=True)
            processThread.start()
            state = "stby" #need wait for pc movment, the deamon change the state

        elif state == "updatePcMove": #PC turn
            print(state)
            state = "robotMove"

        elif state == "robotMove": #Move of piece by robot
            print(state)
            state = "playerTurn"

        elif state == "returnPos": #Return robotic Arm to zero position
            print(state)
            state = "showGameResult"

        elif state == "showGameResult":
            print(state)
            quitGame()
            state = "stby"
            
            


        if button in (None, 'Exit'): #MAIN WINDOW
            break      

    window.close() 


if __name__ == "__main__":
    main()