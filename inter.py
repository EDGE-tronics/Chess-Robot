import PySimpleGUI as sg
import os
import copy
import time
'''
styles:

BlueMono
GreenTan
LightGreen
Black
Dark
'''

conf = False

def render_square(image, key, location):
    if (location[0] + location[1]) % 2:
        color =  '#B58863'
    else:
        color = '#F0D9B5'
    return sg.Button('', image_filename=image, size=(1, 1),
                          border_width=0, button_color=('white', color),
                          pad=(0, 0), key=key)

def newGameWindow (state):
    if state == "OPEN":
        menu_def2 = [['Properties'],      
            ['Help', 'About...'], ]
        board_controls2 = [[sg.RButton('New Game', key='New Game')],
                    [sg.CBox('Play As White', key='_white_')],
                    ]

        layoutNewGame= [[sg.Menu(menu_def2, tearoff=False)], 
            [sg.Column(board_controls2)]]
        windowNewGame = sg.Window('Chess', default_button_element_size=(12,1), auto_size_buttons=False, icon='kingb.ico').Layout(layoutNewGame)
        b,v = windowNewGame.Read()
        conf =  True  
        return b,v  
    elif state == "CLOSE":
        windowNewGame.close()
        conf = False


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

# ------ Menu Definition ------ #      
menu_def = [['Properties'],      
            ['Help', 'About...'], ]  


# ------ Layout ------ # 
# sg.SetOptions(margins=(0,0))
sg.ChangeLookAndFeel('Dark')
# create initial board setup
board = copy.deepcopy(initial_board)
# the main board display layout
board_layout = [[sg.T(' '*6)] + [sg.T('{}'.format(a), pad=((23,27),0), font='Any 13') for a in 'abcdefgh']]
# loop though board and create buttons with images
for i in range(8):
    row = [sg.T(str(8-i)+'   ', font='Any 13')]
    for j in range(8):
        piece_image = images[board[i][j]]
        row.append(render_square(piece_image, key=(i,j), location=(i,j)))
    row.append(sg.T(str(8-i)+'   ', font='Any 13'))
    board_layout.append(row)
# add the labels across bottom of board
board_layout.append([sg.T(' '*6)] + [sg.T('{}'.format(a), pad=((23,27),0), font='Any 13') for a in 'abcdefgh'])

board_controls = [[sg.RButton('New Game', key='newGame')]]

layout = [[sg.Menu(menu_def, tearoff=False)], 
            [sg.Column(board_layout),sg.VerticalSeparator(pad=None),sg.Column(board_controls)]]



window = sg.Window('Chess', default_button_element_size=(12,1), auto_size_buttons=False, icon='kingb.ico').Layout(layout)

def main():
    while True:
        button, value = window.Read()
        if button == "newGame":
            b,v = newGameWindow("OPEN")
        if conf and b in (None, "Exit"):
            newGameWindow("CLOSE")
            
        
        if button in (None, 'Exit'):
            break    

    window.close()    

if __name__ == "__main__":
    main()