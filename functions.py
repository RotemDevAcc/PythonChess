from app import Actions, Colors ,MAXWIDTH,MAXHEIGHT
from Config import *
import os,time,random,threading



if USESOUNDS and os.name == "nt":
    import winsound
    def PlaySound(sound):
        #os.system(f"start {sound}")
        winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
elif USESOUNDS:
    USESOUNDS = False
    print("Sounds Disabled Because Your Not Using Windows")

def ClearConsole():
    os.system("cls" if os.name == "nt" else "clear")

def DrawActions():
    for action in Actions:
        print(f"\033[95m{action.name}\033[0m - \033[92m{action.value}\033[0m")

def StartMessage(message):
    Wait(200)
    print()
    print(message)

def Message(message):
    message_thread = threading.Thread(target=StartMessage, args=(message,))
    message_thread.start()

def ChooseColor():
    i = 1
    for color in Colors:
        print(f"{i}.{color.value}{color.name}{Colors['DEFAULT'].value}")
        i += 1

    # Creates Some Space Between The Options And The Input
    print()
    if USESOUNDS:
        PlaySound('sounds/blop.wav')
    chosencolor = input(f"{Colors['PURPLE'].value}Choose {Colors['RED'].value}Your {Colors['BLUE'].value}Player {Colors['GREEN'].value}Color By {Colors['CYAN'].value}Name: {Colors['DEFAULT'].value}")
    if(chosencolor and chosencolor != None): chosencolor = chosencolor.upper()
    found = False
    for color in Colors:
        if(chosencolor == color.name):
            chosencolor = color.value
            found = True
            break

    if(not found):
        return Colors['DEFAULT'].value
    
    return chosencolor


def DoInput():
    user_selection = input("Select Action: ")

    if user_selection.strip().isdigit():
        number = int(user_selection)
        if(number > len(Actions)):
            print(f"Action Must Not Be Above {len(Actions)}")
            return None
            

        return number
    else: 
        print(f"Action Must Be A Number Between 0 ~ {len(Actions)}")
        return None
    

def MoveY(y, IsForward):
    if IsForward:
        if y - 1 >= 0:  # Check if moving up is within boundaries
            y -= 1  # Move up
        else:
            Message("Can't Move Up Further")
    else:
        if y + 1 < MAXHEIGHT:  # Check if moving down is within boundaries
            y += 1  # Move down
        else:
            Message(f"Can't Move Down Further Than {MAXHEIGHT - 1} Steps From The Start")
    return y

def MoveX(x,IsRight):
    if(IsRight): 
        if(x + 1 >= MAXWIDTH):
            print(f"Cant Move Forward More Than {MAXWIDTH} Steps From The Start")
            return x
        x += 1
        return x
    else:
        if(x - 1 < 0):
            Message(f"Cant Move Backward More Than {0} Steps From The Start")
            return x
        x -= 1
        return x
    



def DoEat(y,x,table,king):
    if not table[y][x]:

        # Chances Of Eating Are {EATINGCHANCE} Unless Player Is A King Than its a 100%
        success = king or random.randint(1,100) > EATINGCHANCE

        if(success):
            Message(f"{Colors['GREEN'].value} Eaten Successfully{Colors['DEFAULT'].value}")
            PlaySound("sounds/eaten.wav")
            table[y][x] = True
        else: 
            PlaySound("sounds/blocked.wav")
            Message(f"{Colors['RED'].value}Eating This Cell Has Failed.{Colors['DEFAULT'].value}")
    else: Message(Colors['YELLOW'].value + "You've already eaten this cell." + Colors['DEFAULT'].value)

def Wait(miliseconds):
    if(not miliseconds):
        miliseconds = 1000

    time.sleep(miliseconds / 1000)