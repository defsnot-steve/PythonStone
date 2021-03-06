from pygame import *
from random import *

from Buff import *
from Buffs import *
from card import *
from Constants import *


foldername = getFoldername()
DISPLAYNUM = 4

RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
BOARD = (205,182,139)
LINDSAY = (255, 7, 162)


#Show all of the Cards on the Board
def showBoard(spots):
    screen  = getScreen()
    for i in range(0,2):
        for j in range(7):
            if (spots[i][j].getOccupied()):
                if i != 0:
                    showCard2(spots[i][j], screen, True)
                else:
                    showCard2(spots[i][j], screen, False)
                    
                    
# Show all of the cards in Hand of the current Player
# hands: each player's hand
# screen: the surface being projected onto
# turn: an int representation of who's turn it is		
def showHand(hands, turn):
    screen = getScreen()
    #The opposing Player's cards will be shown as cardbacks
    cardBack = image.load(foldername+"cardback.png")
    for i in range (2):
        for j in range (10):
            if i != turn:
                showHandCard(hands[i].getCards()[j], [i,j], screen)
            else:
                showCardBack(hands[i].getCards()[j], [j,i], screen, cardBack)

#Shows a cardBack		
def showCardBack(card, pos, screen, img):
    width = screen.get_width()
    height = screen.get_height()
    
    conversionx = width / 1600.0
    conversiony = height / 800.0
    
    if card.isNull() == False:
        img = transform.scale(img, (int(conversionx*140), int(conversiony*100)))
        imgRect = Rect(pos[0]*140*conversionx, 700*pos[1]*conversiony, conversionx*140, conversiony*100)
        screen.blit(img, imgRect)
    
	
# Show a card on the Board
# row1: A bool used to see what player the card belongs too       
def showCard2(spot, screen, row1):
    
    
    width = screen.get_width()
    height = screen.get_height()
    
    conversionx = width / 1600.0
    conversiony = height / 800.0
    
    nameFont = font.Font(None, int(24*conversionx))
    
    #Name Text
    name = nameFont.render(spot.getCard().getName() , True, (255, 255, 255), BOARD)
    nameRect = name.get_rect()
    nameRect.centerx = (spot.getPos()[0] +25 ) * conversionx
    if row1:
        nameRect.centery = (spot.getPos()[1] + 50) * conversiony
    else:
        nameRect.centery = (spot.getPos()[1] + 50) * conversiony
        
    #Power Toughness Text
    pts = str(spot.getCard().getPower()) + "                  " + str(spot.getCard().getToughness())
    pt = nameFont.render(pts, True, (255, 255, 255), BOARD)
    ptRect = pt.get_rect()
    ptRect.centerx = (spot.getPos()[0] + 30) * conversionx
    if row1:
        ptRect.centery = (spot.getPos()[1] + 150) * conversiony
    else:
        ptRect.centery = (spot.getPos()[1] + 150) * conversiony
        
        
    num = 0    
    if spot.getCard().getKeywords()[0]:
        num += 20*conversionx
        img = image.load(foldername+"taunt_symbol.png")
        img = transform.scale(img, (int(conversionx*20), int(conversiony*20)))
        imgRect = Rect(spot.getPos()[0]*conversionx, (spot.getPos()[1]+100)*conversiony, conversionx*20, conversiony*20)
        screen.blit(img, imgRect)
        
    if spot.getCard().getKeywords()[1]:
        
        img = image.load(foldername+"charge_symbol.png")
        img = transform.scale(img, (int(conversionx*20), int(conversiony*20)))
        imgRect = Rect(spot.getPos()[0]*conversionx +  num, (spot.getPos()[1]+100)*conversiony, conversionx*20, conversiony*20)
        num += 20*conversionx
        screen.blit(img, imgRect)
        
    if spot.getCard().getKeywords()[2]:
        
        img = image.load(foldername+"divine_symbol.png")
        img = transform.scale(img, (int(conversionx*20), int(conversiony*20)))
        imgRect = Rect(spot.getPos()[0]*conversionx +  num, (spot.getPos()[1]+100)*conversiony, conversionx*20, conversiony*20)
        num += 20*conversionx
        screen.blit(img, imgRect)
        
    if spot.getCard().getKeywords()[3]:
        
        img = image.load(foldername+"windfury_symbol.png")
        img = transform.scale(img, (int(conversionx*20), int(conversiony*20)))
        imgRect = Rect(spot.getPos()[0]*conversionx +  num, (spot.getPos()[1]+100)*conversiony, conversionx*20, conversiony*20)
        num += 20*conversionx
        screen.blit(img, imgRect)
        
    #Blit to Screen
    screen.blit(name, nameRect)
    screen.blit(pt, ptRect)

#Shows a hand card    
def showHandCard(card, pos, screen):
    width = screen.get_width()
    height = screen.get_height()
    
    conversionx = width / 1600.0
    conversiony = height / 800.0
    
    handFont = font.Font(None, int(15*conversionx)+2)
    if card.getName() != "Null":
        #Name Text
    	name = handFont.render(card.getName() , True, (255, 255, 255), BOARD)
    	nameRect = name.get_rect()
    	nameRect.centerx = (pos[1]*140 + 70)*conversionx
    	nameRect.centery = (pos[0]*700 + 20)*conversiony
    	
        #Cost Text
    	cost = handFont.render(str(card.getCost()) , True, (255, 255, 255), BOARD)
    	costRect = cost.get_rect()
    	costRect.centerx = (pos[1]*140 + 70)*conversionx
    	costRect.centery = (pos[0]*700 + 40)*conversiony
    	
        #Blit to Screen
    	screen.blit(name, nameRect)
    	screen.blit(cost, costRect)

#The main draw method, used to continuosly draw the board
# filename is the name of the current hovercard
# pos is the mouse position
# status is an int used to determine if the hovercard should be shown	
def drawGrid(filename, pos=[0,0], status=0):
    
    board = getBoard()
    screen = getScreen()
    
    #establish the players
    player1 = board.getPlayer1()
    player2 = board.getPlayer2()
    
    nameFont = font.Font(None, 30)
    
    width = screen.get_width()
    height = screen.get_height()
    
    widthInc = width/32.0
    heightInc = height/16.0
    
    tenth = width/11.42
    
    #Base coat of the board
    draw.rect(screen, BOARD, (0,0,width,height))
    
    #Player1 Portrait
    player1 = board.getPlayer1()
    portrait1 = image.load(player1.getPortrait())
    portrait1 = transform.scale(portrait1, (int(widthInc*6), int(heightInc*2)))
    port1Rect = Rect(widthInc*11, heightInc*2, widthInc*6, heightInc*2)
    screen.blit(portrait1, port1Rect)
    
    #Player2 Portrait
    player2 = board.getPlayer2()
    portrait2 = image.load(player2.getPortrait())
    portrait2 = transform.scale(portrait2, (int(widthInc*6), int(heightInc*2)))
    port2Rect = Rect(widthInc*11, heightInc*12, widthInc*6, heightInc*2)
    screen.blit(portrait2, port2Rect)
    
    #Player1 Armor
    crest = image.load("pics/armor.png")
    crest1Rect = Rect(widthInc*18, heightInc*3, 40, 45)
    screen.blit(crest, crest1Rect)
    
    #Player2 Armor
    crest = image.load("pics/armor.png")
    crest2Rect = Rect(widthInc*18, heightInc*13, 40, 45)
    screen.blit(crest, crest2Rect)
    
    #Player1 Health
    health1 = nameFont.render((str(player1.getLife()) +"    "+ str(player1.getArmor())) , True, (255, 255, 255), BOARD)
    health1Rect = health1.get_rect()
    health1Rect.centerx = widthInc*18
    health1Rect.centery = heightInc*2.4
    screen.blit(health1, health1Rect)
    
    #Player1 Weapon
    if player1.isArmed():
    	weapon = player1.getWeapon()
        
    	Weapon1 = nameFont.render((str(weapon.getPower()) +" / "+ str(weapon.getDurability())) , True, (255, 255, 255), BOARD)
    	Weapon1Rect = Weapon1.get_rect()
    	Weapon1Rect.centerx = widthInc*6
    	Weapon1Rect.centery = heightInc*3
    	screen.blit(Weapon1, Weapon1Rect)
	
    #Player2 Weapon
    if player2.isArmed():
    	weapon = player2.getWeapon()
        
    	Weapon2 = nameFont.render((str(weapon.getPower()) +" / "+ str(weapon.getDurability())) , True, (255, 255, 255), BOARD)
    	Weapon2Rect = Weapon2.get_rect()
    	Weapon2Rect.centerx = widthInc*6
    	Weapon2Rect.centery = heightInc*13
    	screen.blit(Weapon2, Weapon2Rect)
	
	#Player 2 Health
    health2 = nameFont.render((str(player2.getLife()) +"    "+ str(player2.getArmor())) , True, (255, 255, 255), BOARD)
    health2Rect = health1.get_rect()
    health2Rect.centerx = widthInc*18
    health2Rect.centery = heightInc*12.4
    screen.blit(health2, health2Rect)
    
    
    #Verticals
    for i in range (1,7):
        draw.line(screen, RED, ((widthInc*4)*i, heightInc*4) , ((widthInc*4)*i, heightInc*12))
        
    for i in range (1,10):
        draw.line(screen, RED, (tenth*i, 0) , (tenth*i, heightInc*2))
        draw.line(screen, RED, (tenth*i, heightInc*14) , (tenth*i, heightInc*16))
	
    #Horizontals
    draw.line(screen, RED, (0, height/8) , (width, height/8))
    draw.line(screen, RED, (0, height/4) , (width, height/4))
    draw.line(screen, RED, (0, height*0.75) , (width, height*0.75))
    draw.line(screen, RED, (0, 7*height/8) , (width, 7*height/8))
    
    
    #Hero Section 1
    draw.line(screen, RED, (widthInc*9, heightInc*2), (widthInc*9, heightInc*4))
    draw.line(screen, RED, (widthInc*9, heightInc*12), (widthInc*9, heightInc*14))
    draw.line(screen, RED, (widthInc*11, heightInc*2), (widthInc*11, heightInc*4))
    draw.line(screen, RED, (widthInc*11, heightInc*12), (widthInc*11, heightInc*14))
    
    #Hero Section 2
    draw.line(screen, RED, (widthInc*17, heightInc*2), (widthInc*17, heightInc*4))
    draw.line(screen, RED, (widthInc*17, heightInc*12), (widthInc*17, heightInc*14))
    draw.line(screen, RED, (widthInc*19, heightInc*2), (widthInc*19, heightInc*4))
    draw.line(screen, RED, (widthInc*19, heightInc*12), (widthInc*19, heightInc*14))
    
    #Hero Power Boxes
    draw.rect(screen, BLUE, (widthInc*19, heightInc*2, widthInc*2, heightInc*2))
    draw.rect(screen, BLUE, (widthInc*19, heightInc*12, widthInc*2, heightInc*2))
    
    
    #End Turn Button
    draw.rect(screen, (100, 100, 255), (widthInc*28, heightInc*8,150,100))
    name = nameFont.render("End Turn" , True, (155,155,255 ), (100, 100, 0))
    nameRect = name.get_rect()
    nameRect.centerx = widthInc*29 + widthInc/2 
    nameRect.centery = heightInc*9
    screen.blit(name, nameRect)
    
    #Player 1 Mana
    player1Mana = nameFont.render(str(player1.getCurMana()) +" "+ str(player1.getSpellDamage()) , True, (155,155,255 ), (0, 0, 0))
    manaRect = player1Mana.get_rect()
    manaRect.centerx = widthInc*29 + widthInc/2  
    manaRect.centery = heightInc*3
    screen.blit(player1Mana, manaRect)
    
    #Player 1 Power
    player1Power = nameFont.render(str(player1.getPower()) , True, (205,155,20), BOARD)
    powerRect = player1Power.get_rect()
    powerRect.centerx = widthInc*10
    powerRect.centery = heightInc*3
    screen.blit(player1Power, powerRect)
    
    #Player 2 Power
    player2Power = nameFont.render(str(player2.getPower()) , True, (205,155,20), BOARD)
    power2Rect = player2Power.get_rect()
    power2Rect.centerx = widthInc*10
    power2Rect.centery = heightInc*13
    screen.blit(player2Power, power2Rect)
    
    #Player 2 Mana
    player2Mana = nameFont.render(str(player2.getCurMana()) , True, (155,155,255 ), (0, 0, 0))
    mana2Rect = player2Mana.get_rect()
    mana2Rect.centerx = widthInc*29 + widthInc/2  
    mana2Rect.centery = heightInc*13
    screen.blit(player2Mana, mana2Rect)
    

#Shows a card image if mouse is hovering over the card    
def hoveredCard(screen, pos, status, filename):
        screen = getScreen()
        convx = screen.get_width() / 1600.0
        convy = screen.get_height() / 800.0
        if status == 1:
            img = image.load(filename)
            img = transform.scale(img, (int(307*convx), int(465*convy)))
            #Check where the card should go to not be off screen
            if pos[1] > 381*convy:
                imgRect = Rect(pos[0]*convx, (pos[1] - 300)*convy, 276*convx, 381*convy)
            else:
                imgRect = Rect(pos[0]*convx, pos[1]*convy, 276*convx, 381*convy)
            screen.blit(img, imgRect)
            display.flip()
            
#Draws the Screen selection Screen
# screen: surface that is being drawn on
# cards: Possible cards to add to deck
# background: The background colour
# start: the current position in the card list
# filename: the filename of an image to highlight
def showSelect(screen, cards, usedCards, num, background, start, filename, filename2):
    
    convx = screen.get_width() / 1600.0
    convy = screen.get_height() / 800.0
    
    
    nameFont = font.Font(None, int(30*convx))
    #Draws the background
    draw.rect(screen, BOARD, (0,0,1400*convx,800*convy))
    
    
    
    #Submit Deck button
    draw.rect(screen, RED, (1000*convx,600*convy, 200*convx, 70*convy), 5)
    name = nameFont.render("Submit Deck" , True, (50,50,50), BOARD)
    nameRect = name.get_rect()
    nameRect.centerx = 1100*convx 
    nameRect.centery = 635*convy
    screen.blit(name, nameRect)
    
    #Show 4 current Cards
    cooridinates = [[0, 0, 184*convx, 254*convy],[184*convx, 0, 184*convx, 254*convy],[0, 254*convy, 184*convx, 254*convy],[184*convx, 254*convy, 184*convx, 254*convy]]
    
    for i in range (start, min(start + DISPLAYNUM, len(cards))):
        file = foldername + cards[i].getFilename()
        img = image.load(file)
        img = transform.scale(img, (int(184*convx), int(254*convy)))
        imgRect = Rect(cooridinates[i - start][0], cooridinates[i - start][1], 184*convx, 254*convy)
        screen.blit(img, imgRect)
        
        
    # Show selected cards    
    draw.rect(screen, BLUE, (5*convx, 510*convy, 710*convx, 280*convy), 2)
    for i in range (len(usedCards)):
        name = nameFont.render(usedCards[i].getName(), True, (50,50,50), BOARD)
        nameRect = name.get_rect()
        if i < 10:
            nameRect.centerx = 120*convx 
            nameRect.centery = (530 + 25*i)*convy
        elif i < 20:
            nameRect.centerx = 340*convx 
            nameRect.centery = (530 + 25*(i-10))*convy
        else:
            nameRect.centerx = 570*convx 
            nameRect.centery = (530 + 25*(i-20))*convy
        screen.blit(name, nameRect)
    
    #Box of Card choices
    draw.rect(screen, GREEN, (400*convx, 80*convy, 250*convx, 190*convy), int(10*convx) )
    for i in range (start, min(start + DISPLAYNUM, len(cards))):
    	name = nameFont.render(cards[num*i].getName() , True, (50,50,50), BOARD)
    	nameRect = name.get_rect()
    	nameRect.centerx = 525*convx 
    	nameRect.centery = (100 + 50*(i - start))*convy
    	screen.blit(name, nameRect)
        
    #Hero Portrait
    img = image.load(filename2)
    img = transform.scale(img, (int(300*convx), int(100*convy)))
    imgRect = Rect(1050*convx, 100*convy, 300*convx, 100*convy)
    screen.blit(img, imgRect)
    
    
    #Left and right card selectors
    left = image.load(foldername+"/Left.png")
    left = transform.scale(left, (int(100*convx), int(100*convy)))
    leftRect = Rect(400*convx, 400*convy, 100*convx, 100*convy)
    screen.blit(left, leftRect)
    
    right = image.load(foldername+"/Right.png")
    right = transform.scale(right, (int(100*convx), int(100*convy)))
    rightRect = Rect(600*convx, 400*convy, 100*convx, 100*convy)
    screen.blit(right, rightRect)
    
    select = image.load(foldername+"/selectionMessage.png")
    select = transform.scale(select, (int(600*convx), int(130*convy)))
    selectRect = Rect(800*convx, 280*convy, 600*convx, 130*convy)
    screen.blit(select, selectRect)
    
    sub = image.load(foldername+"/submission.png")
    sub = transform.scale(sub, (int(600*convx), int(200*convy)))
    subRect = Rect(800*convx, 550*convy, 600*convx, 200*convy)
    screen.blit(sub, subRect)
    
    
    #Hover Card
    img = image.load(filename)
    img = transform.scale(img, (int(184*convx), int(254*convy)))
    imgRect = Rect(1400*convx, 0, 200*convx, 200*convy)
    screen.blit(img, imgRect)
    
def drawDeckChoice(screen, turn):
    convx = screen.get_width() / 1600.0
    convy = screen.get_height() / 800.0
    
    nameFont = font.Font(None, int(convx*30))
    questionFont = font.Font(None, int(convx*48))
    #Draws the background
    
    draw.rect(screen, BOARD, (0,0,1600*convx,800*convy))
    #Draw the question
    quest = questionFont.render("Player "+str(turn)+", Do you want to use a new deck or create your own?", True, (50,50,50), BOARD)
    questRect = quest.get_rect()
    questRect.centerx = 800*convx 
    questRect.centery = 50*convy
    screen.blit(quest, questRect)
    
    quest = nameFont.render("Create Quick Deck", True, (50,50,50), BOARD)
    questRect = quest.get_rect()
    questRect.centerx = 275*convx 
    questRect.centery = 260*convy
    screen.blit(quest, questRect)
    
    quest = nameFont.render("Create Saved Deck", True, (50,50,50), BOARD)
    questRect = quest.get_rect()
    questRect.centerx = 525*convx 
    questRect.centery = 260*convy
    screen.blit(quest, questRect)
    
    #Deck Selection
    draw.rect(screen, BLUE, (800*convx, 80*convy, 250*convx, 270*convy), 10)
    for i in range (0,2):
        Deck = open('deck'+str(i+1)+'.txt', 'r')
        name = nameFont.render(Deck.readline()[:-1]+": ("+Deck.readline()[:-1]+")", True, (50,50,50), BOARD)
        nameRect = name.get_rect()
        nameRect.centerx = 925*convx 
        nameRect.centery = (95 + 30*i)*convy
        screen.blit(name, nameRect)
        Deck.close()
        
    draw.rect(screen, RED, (150*convx, 200*convy, 250*convx, 120*convy), int(3*convx)+1)
    draw.rect(screen, RED, (400*convx, 200*convy, 250*convx, 120*convy), int(3*convx)+1) 
    
    #draw.rect(screen, RED, (200*convx, 200*convy, 200*convx, 200*convy))
    #draw.rect(screen, RED, (400*convx, 400*convy, 200*convx, 200*convy)) 
     
    img = image.load(foldername+"Title.png")
    img = transform.scale(img, (int(602*convx), int(387*convy)))
    imgRect = Rect(500*convx, 400*convy, 602*convx, 387*convy)
    screen.blit(img, imgRect)  
        