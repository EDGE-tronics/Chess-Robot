import os
import ChessLogic as cl
import VisionModule as vm

Debug = True

# Test route:
route = os.getcwd() + '/'
print("The route is: ",route)

## TEST FUNCTION FOR MOVEMENT SEQUENCE GENERATION
def main():  
    board = cl.chess.Board()
    print(board)
    squares = []
    square = ""

    # SETUP
    cbPattern = vm.cv2.imread(route+'cbPattern.jpg', vm.cv2.IMREAD_GRAYSCALE)
    ## calibrateCam
    input("Please place the chessboard without the chess pieces and press enter\n")
    img1 = vm.cv2.imread(route + 'board.png')
    retIMG, homMat = vm.findTransformation(img1,cbPattern)
    ## findWhite
    input("Please place the chess pieces, press enter, check image and press enter\n")
    img2 = vm.cv2.imread(route+'0.png') 
    warpIMG2 = vm.cv2.warpPerspective(img2, homMat, (cbPattern.shape[1], cbPattern.shape[0]))
    # Draw quadrants and numbers on image
    vm.drawQuadrants(warpIMG2)
    # Get rotation matrix
    rotMat = vm.findRotation()
    if rotMat.any() != 0:
        warpIMG2 = vm.cv2.warpAffine(warpIMG2, rotMat, cbPattern.shape[1::-1], flags=vm.cv2.INTER_LINEAR)

    hsv2 = vm.cv2.cvtColor(warpIMG2, vm.cv2.COLOR_BGR2HSV)
    H2,S2,V2 = vm.cv2.split(hsv2)

    while not board.is_game_over():
        H1 = H2.copy()
        newImg = input("\nNew move image: ")
        img2 = vm.cv2.imread(route+newImg+'.png')

        # For testing
        vm.cv2.imshow("Window 1", warpIMG2)

        while img2 is None:
            newImg = input("\nSelect a valid image: ")
            img2 = vm.cv2.imread(route+newImg+'.png')
        warpIMG2 = vm.cv2.warpPerspective(img2, homMat, (cbPattern.shape[1], cbPattern.shape[0]))

        if rotMat.any() != 0:
            warpIMG2 = vm.cv2.warpAffine(warpIMG2, rotMat, cbPattern.shape[1::-1], flags=vm.cv2.INTER_LINEAR)

        hsv2 = vm.cv2.cvtColor(warpIMG2, vm.cv2.COLOR_BGR2HSV)
        H2,S2,V2 = vm.cv2.split(hsv2)

        # For testing
        vm.cv2.imshow("Window 2", warpIMG2)
        
        # Check which squares had the biggest change in color
        squares = vm.findMoves(H1, H2)

        result = cl.moveAnalysis(squares, board)
        while result:
            print("Move detected: ")
            print(result)
            if result["type"] == "Promotion":
                result["move"] += "q"
            print("Move sequence: ")
            sequence = cl.sequenceGenerator(result["move"], board)
            print(sequence)
            board.push_uci(result["move"])
            print("White turn: ", board.turn)
            print(board)
        else:
            print("Invalid move!")
        squares.clear()

        vm.cv2.waitKey()
        vm.cv2.destroyAllWindows()

if __name__ == "__main__":
    main()