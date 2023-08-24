# Functions.py
from functions import *

# Game Settings Config.py
from Config import *

from enum import Enum



class Actions(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    EAT = 5
    RESTART = 6
    QUIT = 7

class Colors(Enum):
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DEFAULT = '\033[0m'




coordx = 0
coordy = MAXHEIGHT - 1
Running = 0
isKing = False
playerColor = "\033[0m"


# Made By GPT
# Initialize the game grid
game_grid = [[' ' for _ in range(MAXWIDTH)] for _ in range(MAXHEIGHT)]
eaten_grid = [[False for _ in range(MAXWIDTH)] for _ in range(MAXHEIGHT)]

# Function to print the game grid
def print_game_grid(player_x, player_y):

    # Iterate through the game grid and print each cell
    global isKing
    player_icon = "👑" if isKing else f"{playerColor}P{Colors['DEFAULT'].value}"

    for y in range(MAXHEIGHT):
        for x in range(MAXWIDTH):
            if x == player_x and y == player_y:
                # Print the player character at the player's position
                print(game_grid[player_y][player_x], end=''+player_icon)
            else:
                # Print the contents of the cell (e.g., ' ' for empty)
                if(eaten_grid and eaten_grid[y][x]):
                    print(game_grid[y][x], end='\033[91mX\033[0m')
                else:
                    print(game_grid[y][x], end='\033[94mO\033[0m')

        # Start a new line for the next row
        print()

def SetKing(Kingmode):
    global isKing
    isKing = Kingmode
    if USESOUNDS and isKing: 
        PlaySound('sounds/king.wav')
    
    Message(f"{Colors['YELLOW'].value} Congratz, You Are Now A King{Colors['DEFAULT'].value}")

def Restart():
    global coordx,coordy,Running,isKing
    ClearConsole()
    coordx = 0
    coordy = MAXHEIGHT - 1
    Running = 0
    isKing = False
    print(f"{Colors['RED'].value}Restarting Game, Please Wait...{Colors['DEFAULT'].value}")
    Wait(1000)
    Running = 1
    RunStart()

def Quit():
    global coordx,coordy,Running,isKing
    ClearConsole()
    coordx = 0
    coordy = MAXHEIGHT - 1
    Running = 0
    isKing = False
    print(f"{Colors['RED'].value}Game Stopped, Cya Later.{Colors['DEFAULT'].value}")


# End GPT
def RunStart():
    global Running

    # Play the audio
    

    while Running == 1:
        input("Press \033[93mEnter\033[0m To \033[96mStart The Game\033[0m:")

        Running = 2
        timer = STARTCD
        for x in range(STARTCD):
            ClearConsole()
            if USESOUNDS:
                PlaySound('sounds/bell.wav')
            print(f"Starting The Game In: \033[93m{timer}\033[0m")

            Wait(1000)
            timer -= 1

        ClearConsole()
        RunApp()

        

def RunApp():
    global Running,playerColor
    print(f"{Colors['RED'].value}G{Colors['GREEN'].value}a{Colors['BLUE'].value}m{Colors['YELLOW'].value}e {Colors['PURPLE'].value}Started{Colors['DEFAULT'].value}")

    playerColor = ChooseColor()
    if USESOUNDS:
        PlaySound("sounds/success.wav")
    ClearConsole()
    while Running:
        DrawActions()
        global coordx,coordy
        print_game_grid(coordx,coordy)
        user_selection = DoInput()
        if user_selection == None: continue

        user_selection = Actions(user_selection)

        if user_selection == Actions.FORWARD:
            coordy = MoveY(coordy,True)
            if(coordy == 0 and not isKing):
                SetKing(True)
        elif user_selection == Actions.BACKWARD:
            coordy = MoveY(coordy,False)
        elif user_selection == Actions.LEFT:
            coordx = MoveX(coordx,False)
        elif user_selection == Actions.RIGHT:
            coordx = MoveX(coordx,True)
        elif user_selection == Actions.EAT:
            DoEat(coordy,coordx,eaten_grid,isKing)
        elif user_selection == Actions.RESTART:
            Restart()
        elif user_selection == Actions.QUIT:
            Quit()
            return
        



if __name__ == "__main__":
    Running = 1
    RunStart()
