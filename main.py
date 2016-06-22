#Main  HS game
#To Lindsay
from pygame import *
from card import *
from cards import *
from random import *
from Turn import *
from DrawBoard import *
from Damage import *
from heroPower import *
from Board import *
from spawn import *

RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
BOARD = (205,182,139)
LINDSAY = (255, 7, 162)
#BOARD = LINDSAY
turn = 0
foldername = "pics/"

DISPLAYNUM = 4
filename = "abusive_sergeant.png"


def check_to_quit():
    for evnt in event.get(): # checks all events that happen
        keys = key.get_pressed()
        keyz= key.get_pressed ()
        if evnt.type == QUIT:
            return False
    return True



def checkExit(mouse):
    mx, my = mouse.pos
    if 1000 < mx < 1200 and 600 < my < 670:
	return False
    return  True

def addCard(pos, cards, start, player):
    for i in range (4):
	if 400 < pos[0] < 650 and 80+50*i < pos[1] < 80+(50*(i+1)):
	    newCard = cards[i + start].copy()
	    newCard.setPlayer(player)
	    return newCard
    return None

def checkHeroPower(pos, turn):
    if turn  == 1:
	if 950 < pos[0] < 1050 and 100 < pos[1] < 200:
	    player1.doHeroPower()
    else:
	if 950 < pos[0] < 1050 and 600 < pos[1] < 700:
	    player2.doHeroPower()

def updateClass(player, pos):
    classPort = [["guldan_portrait.jpg", WarlockPower(player)], ["rexxar_portrait.jpg", HunterPower(player)],
                 ["garrosh_portrait.png", WarriorPower(player)],["thrall_portrait.jpg", WarlockPower(player)]
                 ,["uther_portrait.png", PaladinPower(player, board)], ["jaina_portrait.jpg", MagePower(player, screen, board)],
                 ["anduin_portrait.png", WarlockPower(player)],["valeera_portrait.png", RoguePower(player)], 
                 ["malfurion_portrait.png", DruidPower(player)]]
    for i in range (9):
	if 800 < pos[0] < 1050 and 80+30*i < pos[1] < 80+(30*(i+1)):
	    player.setPortrait(foldername + classPort[i][0])
	    player.setHP(classPort[i][1])

def hoverCard(filename, pos, cards, start):
    for i in range (min(len(cards) - start, 4)):
	if 400 < pos[0] < 650 and 80+50*i < pos[1] < 80+(50*(i+1)):
	    return foldername + cards[i + start].getFilename()
    return filename

def hoverCardMain(filename, pos, spots, hands):
    for i in range (0,10):
	if pos[1] < 100 and pos[0]> i*140 and pos[0] < (i+1)*140:
	    return foldername + hands[0].getCards()[i].getFilename(), 1
	if pos[1] > 700 and pos[0]> i*140 and pos[0] < (i+1)*140:
	    return foldername + hands[1].getCards()[i].getFilename(), 1
    for i in range (0,7):
	if pos[1] > 200 and pos[1] < 400 and pos[0]> i*200 and pos[0] < (i+1)*200:
	    if spots[1][i].getOccupied():
		return foldername + spots[1][i].getCard().getFilename(), 1
	if pos[1] < 700 and pos[1] > 400 and pos[0]> i*200 and pos[0] < (i+1)*200:
	    if spots[0][i].getOccupied():
		return foldername + spots[0][i].getCard().getFilename(), 1
    return filename, 0

def updateList(pos):
    if 400 < pos[0] < 500 and 400 < pos[1] < 500:
	    return -DISPLAYNUM
    elif 600 < pos[0] < 700 and 400 < pos[1] < 500:
	    return DISPLAYNUM
    return 0
    
    
def highlight(pos, screen, selcted, square):
    for i in range (0,10):
	if pos[1] < 100 and pos[0]> i*140 and pos[0] < (i+1)*140:
	    xcor = pos[0] % 140
	    draw.rect(screen, GREEN, (140*i,0, 140, 100), 10)
	if pos[1] > 700 and pos[0]> i*140 and pos[0] < (i+1)*140:
	    xcor = pos[0] % 140
	    draw.rect(screen, GREEN, (140*i,700, 140, 100), 10)
    for i in range (0,7):
	if pos[1] > 200 and pos[1] < 400 and pos[0]> i*200 and pos[0] < (i+1)*200:
	    draw.rect(screen, GREEN, (200*i,200, 200, 200), 10)
	if pos[1] < 600 and pos[1] > 400 and pos[0]> i*200 and pos[0] < (i+1)*200:
	    draw.rect(screen, GREEN, (200*i,400, 200, 200), 10)
    for i in range (2):
	if 550 < pos[0] < 850 and 100 + 500*i < pos[1] < 200 + 500*i:
	    draw.rect(screen, GREEN, (550,100 + 500*i, 300, 100), 10)
	    
	if 950 < pos[0] < 1050 and 100 + 500*i < pos[1] < 200 + 500*i:
	    draw.rect(screen, GREEN, (950,100 + 500*i, 100, 100), 10)
	    
    if selected != None:
	square0 = abs(1-square[0])
	draw.rect(screen, (0,255,255), (square[1], square0, square[2], square[3]), 10)
	    
    
		
	
		
def select(mouseObj, spots, current, state, hands):
    global filename
    if current  == None:
	mx, my = mouseObj.pos
	for i in range (0,2):
	    for j in range(0,7):
		if 200*j < mx < 200*(j+1) and 200 + 200*(i) < my < 200 + 200*(i+1):
		    square = [i,j]
		    reversei = abs(1-i)
		    if spots[reversei][j].getOccupied():
			if spots[reversei][j].getCard().getTired() == False:
			    filename = spots[reversei][j].getCard().getFilename()
			    return spots[reversei][j], [i*200 + 200, j*200, 200, 200], "B"
	    for j in range(0,10):
		if 140*j < mx < 140*(j+1) and 0 < my < 100 :
		    square = [i,j]
		    print j, i
		    if turn == 1:
			filename = hands[0].getCards()[j].getFilename()
			return [hands[0].getCards()[j], [0,j]], [0, j*140, 140, 100], "H"
		
	    for j in range(0,10):
		if 140*j < mx < 140*(j+1) and 700 < my < 800 :
		    square = [i,j]
		    print j, i
		    if turn == 0:
			newfilename = hands[1].getCards()[j].getFilename()
			filename = newfilename
			print filename
			return [hands[1].getCards()[j], [1,j]], [700, j*140, 140, 100], "H"
	    murn = abs(1 - turn)
	    if 550 < mx < 850 and 100 + 500*murn < my < 200 + 500*murn and board.getCurrentPlayer().getPower() > 0 and board.getCurrentPlayer().isReady():
		return 1, [100 + 500*murn,550, 300, 100], "C"
	    elif 550 < mx < 850 and 100 + 500*murn < my < 200 + 500*murn and board.getCurrentPlayer().getPower() > 0:
		return  None, None, None
		
    else:
	mx, my = mouseObj.pos
	for i in range (0,2):
	    for j in range(0,7):
		if 200*j < mx < 200*(j+1) and 200 + 200*(i) < my < 200 + 200*(i+1):
		    i = abs(1-i)
		    if state == "B":
			
			if spots[i][j].getOccupied():
			    fight(spots[i][j], current, board)
			    current = None
			    state = None
			else:
			    return None, None, None
		    #Play Card
		    elif state == "H":
			if spots[i][j].getOccupied() == False:
			    return playCard(board.getCurrentPlayer(), board.getCurrentPlayer().getCurMana(), current[0], spots[i][j], 
			                    hands[current[1][0]], current[1][1])
			else:
			    prevCard = spots[i][j].getCard()
			    canRight = checkRight([i,j], spots)
			    canLeft = checkLeft([i,j], spots)
			    if canLeft or canRight:
				playCard(board.getCurrentPlayer(), board.getCurrentPlayer().getCurMana(), current[0], spots[i][j], 
			                    hands[current[1][0]], current[1][1])
			    
			    if mx > 200*j + 100 and canRight:
				shiftRight([i,j], spots, prevCard)
			    elif canLeft:
				shiftLeft([i,j], spots, prevCard)
			    elif canRight:
				shiftRight([i,j], spots, prevCard)
			    return None, None, None
		    #Hero attack
		    elif state == "C":
			attacker = board.getCurrentPlayer()
			if spots[i][j].getOccupied():
			    faceGo(attacker, spots[i][j], board)
			    attacker.setReady(False)
			    if attacker.isArmed():
				weapon = attacker.getWeapon()
				if weapon.attackCheck():
				    attacker.unarmed()
				    attacker.setWeapon(None)
			return None, None, None
	if state == "B":		
	    if 550 < mx < 850 and 100 < my  < 200 and not (current.getCard().getTired()):
		goFace(current.getCard(), player1)
		return None, None, None
	    elif 550 < mx < 850 and 600 < my  < 700 and not (current.getCard().getTired()):
		goFace(current.getCard(), player2)
		return None, None,  None
	elif state == "C":
	    if 550 < mx < 850 and 100 < my  < 200 and player2.isReady():
		faceToFace(player1, player2)
		return None, None, None
	    elif 550 < mx < 850 and 600 < my  < 700 and player1.isReady():
		faceToFace(player2, player1)
		return None, None,  None
	
    return current, [i,j, 200, 250], state
    
def playCard(player, mana, card, spot, hand1, hand2):
    if card.getCost() <= player.getCurMana():
	player.changeCurMana(-card.getCost())
	spot.setCard(card)
	spot.setOccupied(True)
	hand1.setNull(hand2)
	
	if card.hasBattleCry():
	    card.battleCry()
				
	if card.hasEffect():
	    card.doEffect()
	    board.playedCreature(card)
    display.flip()
    return None, None, None


    

	    
    
init()    
size =(1600,800)
screen= display.set_mode (size)
nameFont = font.Font(None, 30)
handFont = font.Font(None, 15)
selected = None
square = None
display.flip()
breaker = True
board = Board()
spots = board.getSpots()
hands = board.getHands()
player1 = board.getPlayer1()
player2 = board.getPlayer2()


twice = 0

state = None
x = 0
selecting = True
cardList = [CH_YETI(), FL_JUG(), RIV_CROC(), MUR_RAID(), ABU_SRG(board, screen), LNC_CAR(board, screen), IRN_OWL(board, screen), ELF_ARC(board, screen),
            GRM_MUR(board, screen), NOV_ENG(board, screen), LOT_HRD(board, screen)]
deck1Cards = []
deck2Cards = []
start = 0
while (selecting):
    showSelect(screen, cardList, 1, (255,255,255), start, filename)
    for evnt in event.get():
	if evnt.type == MOUSEBUTTONDOWN:
	    selecting = checkExit(evnt)
	    newCard = addCard(evnt.pos, cardList, start, player1)
	    updateClass(player1, evnt.pos)
	    if newCard:
		deck1Cards.append(newCard)
	    start += updateList(evnt.pos)
	elif evnt.type == QUIT:
	    quit()
	elif evnt.type == MOUSEMOTION:
	    filename = hoverCard(filename, evnt.pos, cardList, start)
    display.flip()
selecting = True 

while (selecting):
    showSelect(screen, cardList, 1, (200, 200, 200), start, filename)
    for evnt in event.get():
	if evnt.type == MOUSEBUTTONDOWN:
	    selecting = checkExit(evnt)
	    newCard = addCard(evnt.pos, cardList, start, player2)
	    updateClass(player2, evnt.pos)
	    if newCard:
		deck2Cards.append(newCard)
	    start += updateList(evnt.pos)
	elif evnt.type == QUIT:
	    quit()
	elif evnt.type == MOUSEMOTION:
	    filename = hoverCard(filename, evnt.pos, cardList, start)
    display.flip()

deck1, deck2 = board.simpleDecks(deck1Cards,deck2Cards, player1, player2)
hands[0].initialize(deck1)
hands[1].initialize(deck2)    
lastpos = [1400, 0]    
stat = 0
curpos = [1200, 0]
while (breaker):
    breaker = check_to_quit()
    drawGrid(screen, board, filename, lastpos, stat)
    highlight(mouse.get_pos(), screen, selected, square)


    showBoard(spots, screen)
    showHand(hands, screen, turn)
    time.wait(10)
    for newEvent in event.get():
	if newEvent.type == MOUSEBUTTONDOWN:
	    
	    selected, square, state = select(newEvent, spots, selected, state, hands)
	    checkHeroPower(newEvent.pos, turn)
	    turn = endTurn(newEvent.pos, turn, board)
	    filename, stat = hoverCardMain(filename, newEvent.pos, spots, hands)
	elif newEvent.type == MOUSEMOTION:
	    lastpos = newEvent.pos
	    filename, stat = hoverCardMain(filename, newEvent.pos, spots, hands)
	    curpos = newEvent.pos
	else:
	    if newEvent.type == QUIT: 
		breaker = False
    hoveredCard(screen, curpos, stat, filename)
    display.flip()
quit()