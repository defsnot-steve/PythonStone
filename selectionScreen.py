from DrawBoard import *
from Generator import *
from hover import *
from inputbox import *
from Messages import *


DISPLAYNUM = 4
BOARD = (205,182,139)

def selectScreen(player, screen, board, turn):
    deckCards = []
    selecting = True
    cardList = Generator(screen, board, player).getCards()
    start = 0
    filename = "pics/Abusive_sergeant.png"
    saved = False
    name = ""
    
    convx = screen.get_width() / 1600.0
    convy = screen.get_height() / 800.0
    
    while True:
        drawDeckChoice(screen, turn)
        for evnt in event.get():
                    if evnt.type == MOUSEBUTTONDOWN:
                        outcome = makeOrBreak(evnt.pos, convx, convy)
                        if outcome[0]:
                            if outcome[0] == "Custom":
                                choosePlayer(player)
                                cardList = skim(player, cardList)
                                saved = outcome[1]
                                if saved:
                                    name = ask(screen, "Please Name Your Deck")
                                #Select screen for Player1
                                while (selecting):
                                        showSelect(screen, cardList, deckCards, 1, (255,255,255), start, filename, player.getPortrait())
                                        for evnt in event.get():
                                                if evnt.type == MOUSEBUTTONDOWN:
                                                        selecting = checkExit(evnt, player, deckCards, convx, convy, screen)
                                                        newCard = addCard(evnt.pos, cardList, start, player, convx, convy)
                                                        if newCard:
                                                                if len(deckCards) < 30:
                                                                        deckCards.append(newCard)
                                                                else:
                                                                        ToManyCardsMessage = Message("Decks may only have 30 Cards", screen)
                                                                        ToManyCardsMessage.displayMessage()
                                                        start += updateList(evnt.pos, convx, convy)
                                                        start = max(start, 0)
                                                elif evnt.type == QUIT:
                                                        quit()
                                                elif evnt.type == MOUSEMOTION:
                                                        filename = hoverCard(filename, evnt.pos, cardList, start, convx, convy)
                                        display.flip()
                        
                            else:
                                deckData = []
                                readDeck = open('deck'+str(outcome[1] + 1)+'.txt', 'r')
                                for line in readDeck:
                                    deckData.append(line.strip('\n'))
                                readDeck.close()
                                
                                generator = Generator(screen, board, player)
                                cardDict = generator.getCardDict()
                                playerDict = generator.getPlayerDict()
                                
                                for i in deckData[2:]:
                                    deckCards.append(cardDict[i].copy())
                                playerData = playerDict[deckData[1]]
                                player.setPortrait(foldername + playerData[0])
                                player.setHP(playerData[1])
                                player.setRole(playerData[2])
                                
                            return player, deckCards, saved, name
                    elif evnt.type == QUIT:
                        quit()
        display.flip()
        

# Update the class that the player has picked on the deck selection screen.
def updateClass(player, pos, board, screen, convx, convy):
        classPort = [["guldan_portrait.jpg", WarlockPower(player), 'Warlock'], ["rexxar_portrait.jpg", HunterPower(player), 'Hunter'],
                                 ["garrosh_portrait.png", WarriorPower(player), 'Warrior'],["thrall_portrait.jpg", ShamanPower(player), 'Shaman']
                                 ,["uther_portrait.png", PaladinPower(player), 'Paladin'], ["jaina_portrait.jpg", MagePower(player), 'Mage'],
                                 ["anduin_portrait.png", PriestPower(player),'Priest'],["valeera_portrait.png", RoguePower(player),'Rogue'],
                                 ["malfurion_portrait.png", DruidPower(player), 'Druid']]
        for i in range (9):
            if 800*convx < pos[0] < 1050*convx and convy*(80+30*i) < pos[1] < convy*(80+(30*(i+1))):
                    player.setPortrait(foldername + classPort[i][0])
                    player.setHP(classPort[i][1])
                    player.setRole(classPort[i][2])
                    
                    
#Check to see if User wants to quit the application
def check_to_quit():
        for evnt in event.get(): # checks all events that happen
                keys = key.get_pressed()
                keyz= key.get_pressed ()
                if evnt.type == QUIT:
                        return False
        return True

# Shift the DISPLAYNUM
def updateList(pos, convx, convy):
        if 400*convx < pos[0] < 500*convx and 400*convy < pos[1] < 500*convy:
            return -DISPLAYNUM
        elif 600*convx < pos[0] < 700*convx and 400*convy < pos[1] < 500*convy:
            return DISPLAYNUM
        return 0

#Check to see if User wants to submit Deck
def checkExit(mouse, player, deck, convx, convy, screen):
        mx, my = mouse.pos
        if 800*convx < mx < 1400*convx and 550*convy < my < 750*convy:
                if not deck:
                        NoDeckMessage = Message("Please Select at least 1 Card", screen)
                        NoDeckMessage.displayMessage()
                        return True
                if player.getHP() == None:
                        NoDeckMessage = Message("Please Select a Character", screen)
                        NoDeckMessage.displayMessage()
                        return True
                return False
        else:
                return True
            
def makeOrBreak(pos, convx, convy):
    if 150*convx < pos[0] < 400*convx and 200*convy < pos[1] < 320*convy:
        return ["Custom", False]
    elif  400*convx < pos[0] < 650*convx and 200*convy < pos[1] < 320*convy:
        return ["Custom", True]
    for i in range (2):
        if 800*convx < pos[0] < 1050*convx and convy*(80+30*i) < pos[1] < convy*(80+(30*(i+1))):
            return ["Past", i]
    return [False]

# Assign a card to a player
# returns a new card assigned to player (Card)
def addCard(pos, cards, start, player, convx, convy):
    cooridinates = [[0, 0, 184*convx, 254*convy],[184*convx, 0, 368*convx, 254*convy],[0, 254*convy, 184*convx, 508*convy],[184*convx, 254*convy, 368*convx, 508*convy]]
    for i in range (4):
        if 400*convx < pos[0] < 650*convx and convy*(80+50*i) < pos[1] < convy*(80+(50*(i+1))) or (cooridinates[i][0] < pos[0] < cooridinates[i][2] and cooridinates[i][1] < pos[1] < cooridinates[i][3]):
            
            newCard = cards[i + start].copy()
            newCard.setPlayer(player)
            return newCard
        
    return None

def choosePlayer(player):
    screen = getScreen()
    convx = screen.get_width()/ 1600.0
    convy = screen.get_height()/ 800.0
    nameFont = font.Font(None, int(convx*30))
    classPort = [["guldan_portrait.jpg", WarlockPower(player), 'Warlock'], ["rexxar_portrait.jpg", HunterPower(player), 'Hunter'],
                                 ["garrosh_portrait.png", WarriorPower(player), 'Warrior'],["thrall_portrait.jpg", ShamanPower(player), 'Shaman']
                                 ,["uther_portrait.png", PaladinPower(player), 'Paladin'], ["jaina_portrait.jpg", MagePower(player), 'Mage'],
                                 ["anduin_portrait.png", PriestPower(player),'Priest'],["valeera_portrait.png", RoguePower(player),'Rogue'],
                                 ["malfurion_portrait.png", DruidPower(player), 'Druid']]
    keepGoing = True
    
    while keepGoing:
        draw.rect(screen, BOARD, (0,0, screen.get_width(), screen.get_height()) )
        draw.rect(screen, (180, 180, 200), (600*convx,20*convy, 300*convx, 630*convy) )
        draw.rect(screen, RED, (600*convx,20*convy, 300*convx, 630*convy), int(5*convx) )
        for i in range (9):
            draw.line(screen, RED, (600*convx, (20 +70*i)*convy), (900*convx, (20 +70*i)*convy) )
        classes = ["Warlock","Hunter","Warrior","Shaman","Paladin","Mage","Priest","Rogue","Druid"]
        for i in range (9):
            name = nameFont.render(classes[i], True, (50,50,50), (180,180,200))
            nameRect = name.get_rect()
            nameRect.centerx = 750*convx 
            nameRect.centery = (55+70*i)*convy
            screen.blit(name, nameRect)
        display.flip()
        for evnt in event.get():
            if evnt.type == MOUSEBUTTONDOWN:
                pos = evnt.pos
                for i in range (9):
                    if 600*convx < pos[0] < 900*convx and convy*(20+70*i) < pos[1] < convy*(20+(70*(i+1))):
                        player.setPortrait(foldername + classPort[i][0])
                        player.setHP(classPort[i][1])
                        player.setRole(classPort[i][2])
                        keepGoing = False
