from functions import *
from tiles import *
from players import *
from games import *

#Initialize the root

root = Tk() 
root.resizable(0,0)
root.title("Scrabble")
root.geometry("%dx%d%+d%+d" % (300, 300, 0, 0))

#Initialize variables
global playing #To tell if the player is currently playing; for the save game function
playing = 0

#Initialize subdictionaries for CPU
try:
  open("resources/AI.txt")
except:
  print("Initializing subdictionaries")
  import diphthin
  
  
#Tiles in "bag"
global distribution
#distribution = ["a", "a", "a", "a", "a", "a", "a", "a", "a", "b", "b", "c", "c", "d", "d", "d", "d", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "f", "f", "g", "g", "g", "h", "h", "i", "i", "i", "i", "i", "i", "i", "i", "i", "j", "k", "l", "l", "l", "l", "m", "m", "n", "n", "n", "n", "n", "n", "o", "o", "o", "o", "o", "o", "o", "o", "p", "p", "q", "r", "r", "r", "r", "r", "r","s", "s", "s", "s", "t", "t", "t", "t", "t", "t", "u", "u", "u", "u", "v", "v", "w", "w", "x", "y", "y", "z", "?", "?"]
distribution = ["a", "a", "a", "a", "a", "a", "a", "a", "a", "b", "b", "c", "c", "d", "d", "d", "d", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "f", "f", "g", "g", "g", "h", "h", "i", "i", "i", "i", "i", "i", "i", "i", "i", "j", "k", "l", "l", "l", "l", "m", "m", "n", "n", "n", "n", "n", "n", "o", "o", "o", "o", "o", "o", "o", "o", "p", "p", "q", "r", "r", "r", "r", "r", "r","s", "s", "s", "s", "t", "t", "t", "t", "t", "t", "u", "u", "u", "u", "v", "v", "w", "w", "x", "y", "y", "z"]

               # "?", "?", "?", "?", "?", "?", "?", "?","?", "?","?", "?", "?", "?"] #Just for fun :)
               #"?" is a blank tile, can be any letter.
###############Start of playing algorithms: instructions, mode1questions, mode2questions, play, mode1VarSwitch, mode2VarSwitch, check, checkData, scrabbleDestroy, exitGame.###############
def instructions():
    """Needs to be updated"""
    text = """Instructions for Scrabble:

    You get a rack of 7 tiles to start the game. You must play words with these
    7 tiles so that each word formed vertically and horizontally is a word.
    
    \tNote: Whenever you play a word, make sure that it touches at least
    \tone other letter on the board (not diagonally.)
    \tThe first move must touch the star in the middle of the board.
    
    To play a tile, click and drag the tile to the board.
    \tNote: When you play a tile, make sure that it snaps into a space.
    \tIf it doesn't, then it didn't place and you have to do it again.
    "?" tiles are blank tiles. They can be played as any letter.

    If you can't find any words to make, you can exchange. Exchanging 
    You get a certain amount of points based on the letters you played.
    Special Score Tiles:
    \tTWS (triple word score): Multiplies your score for that turn by 3.
    \tDWS (double word score): Multiplies your score for that turn by 2.
    \tTLS (triple letter score): Multiplies your score for that letter by 3.
    \tDLS (double letter score): Multiplies your score for that letter by 2.
    
    Once you play a word, you draw tiles until you have seven again.
    The game ends when there are no tiles left in the bag.

    Modes:
    Normal: wrong word -> continue
    Hardcore: wrong word -> lose turn

    Normal: play until no tiles in bag
    Short: play to 75 points"""

    instructionsWindow = Toplevel(root, height=root.winfo_screenheight(), width=root.winfo_screenwidth())
    instructionsWindow.title("Instructions")
    instructionsLabel = Label(instructionsWindow, text=text, justify=LEFT)
    instructionsLabel.place(x=300, y=10, height=750, width=500)
    closeButton = Button(instructionsLabel, text="Close", command=instructionsWindow.destroy)
    closeButton.place(x=225, y=600)
    
def mode1questions():
    text="""Normal: wrong word --> continue
    Hardcore: wrong word --> lose turn."""
    popup(root, "Mode 1 Description", text, root.winfo_screenheight(), root.winfo_screenwidth())
    
def mode2questions():
    text="""Normal: play until bag and one of the player's racks are empty
    Short: play until one person reaches 75 points.\n\n\n
    Note: normal play can take at least an hour, but short play is very fast."""
    popup(root, "Mode 2 Description", text, root.winfo_screenheight(), root.winfo_screenwidth())
    
def play():
    global enterWindow, name1Var, name2Var, mode1Var, mode2Var, playing

    playing = 1
    enterWindow = Toplevel(root, height = root.winfo_screenheight(),\
                           width = root.winfo_screenwidth())
    enterWindow.wm_title("Enter Names and Modes")

    label1 = Label(enterWindow, text = "Enter name 1:")
    label1.place(x = 50, y = 50, height = 20, width = 95)
    name1Var = StringVar()
    name1Var.set("Joe")
    name1 = Entry(enterWindow, textvariable=name1Var)
    name1.place(x = 150, y = 50, height = 20, width = 100)

    label2 = Label(enterWindow, text = "Enter name 2:")
    label2.place(x = 50, y = 175, height = 20, width = 95)
    name2Var = StringVar()
    name2Var.set("CPU")
    name2 = Entry(enterWindow, textvariable=name2Var)
    name2.place(x = 150, y = 175, height = 20, width = 100)

    cpuRemindLabel = Label(enterWindow, text = """Note: If name 2 is CPU, the computer
will play for that player.""")
    cpuRemindLabel.place(x=50, y=215, height=30, width=250)
 #   cpuRemindLabel.pack()
    
    mode1Label = Label(enterWindow, text = "Enter mode 1 (normal or hardcore):")
    mode1Label.place(x = 50, y = 295, height = 20, width = 210)
    mode1Var = StringVar()
    mode1Var.set("normal")
    mode1 = Entry(enterWindow, textvariable=mode1Var)
    mode1.place(x = 270, y = 295, height = 20, width = 100)

    mode1Questions = Button(enterWindow, text= "?", command = mode1questions)
    mode1Questions.place(x=370, y=280, height=50, width=50)

    mode1Switch = Button(enterWindow, text = "Switch", command = mode1VarSwitch)
    mode1Switch.place(x=430,  y=280, height=50, width=75)
    
    mode2Label = Label(enterWindow, text = "Enter mode 2 (normal or short):")
    mode2Label.place(x = 50, y = 465, height = 20, width = 200)
    mode2Var = StringVar()
    mode2Var.set("normal")
    mode2 = Entry(enterWindow, textvariable=mode2Var)
    mode2.place(x = 270, y = 465, height = 20, width = 100)

    mode2Questions = Button(enterWindow, text = "?", command = mode2questions)
    mode2Questions.place(x=370, y=450, height=50, width=50)

    mode2Switch = Button(enterWindow, text = "Switch", command = mode2VarSwitch)
    mode2Switch.place(x=430, y=450, height=50, width = 75)
    
    enterButton = Button(enterWindow, text = "Enter data", command = checkData)
    enterButton.place(x = 100, y = 500)

def mode1VarSwitch():
    if mode1Var.get() == "normal":
        mode1Var.set("hardcore")
    else:
        mode1Var.set("normal")

def mode2VarSwitch():
    if mode2Var.get() == "normal":
        mode2Var.set("short")
    else:
        mode2Var.set("normal")
        
def check(string, validInputs, popupHeader, popupText):
    if string in validInputs:
        return True
    else:
        popup(root, popupHeader, popupText, root.winfo_screenheight(), root.winfo_screenwidth())
        return False
    
def checkData():
    if check(mode1Var.get(), ['n', 'h', 'N', 'H', 'normal', 'hardcore'], "Invalid Mode 1", "Invalid Mode 1"):
        if check(mode2Var.get(), ['n', 's', 'N', 'S', 'normal', 'short'], "Invalid Mode 2", "Invalid Mode 2"):
            playing = 1
            enterWindow.destroy()
            popup(root, "Pass Device", "Pass Device to %s\n\n" % name1Var.get(), \
                  500, 500)
            global scrabble
            if name2Var.get() == "CPU":
                scrabble = GameWithCPU(name1Var.get(), mode1Var.get(), mode2Var.get())
            else:
                scrabble = Game(name1Var.get(), name2Var.get(), mode1Var.get(), mode2Var.get())
            scrabble.startGame()
            scrabble.main()
            playing = 0
            
def scrabbleDestroy():
    #DESTROY THE SCRABBLE
    #if you are playing, it
    #writes the game to the save file, then destroys the root of the scrabble
    #and the scrabble comes crashing down
    if playing:
        try:
            writeAllGames([scrabble, scrabble])
            scrabble.root.destroy()
        except NameError:
            pass
        
def exitGame():
    scrabbleDestroy()
    root.destroy()
    print("Thanks for playing! Hope you enjoyed! Have a nice day.")
    end()

###############Main interface###############
root.config(bg=generateRandomColor())

welcomeLabel = Label(root, text = "Welcome to Scrabble in Python!")
instructionsButton = Button(root, text = "Instructions", command = instructions)
playButton = Button(root, text = "Play", command = play)
playSavedButton = Button(root, text = "Play Saved Game", command = playSavedGame)
exitButton = Button(root, text = "Exit", command = exitGame)

welcomeLabel.place(x = 40, y = 0)
instructionsButton.place(x = 90, y = 50)
playButton.place(x = 110, y = 100)
playSavedButton.place(x = 76, y = 150)
exitButton.place(x = 112, y = 200)

if __name__ == "__main__": #Looks cooler :)
    root.mainloop()