#imports
import tkinter as tk
import tkinter.messagebox as mk
from PIL import Image, ImageDraw, ImageTk, ImageFont
import random

#creating the window
root =tk.Tk()
root.title('Siete')
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f'{width}x{height}')

#Global Variables
buttonList = []
playerCards = []
opponentCards = []
turn = 1
uno_state = False
penalty = False

numList = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]
cardList = [["red","1"],["red","2"],["red","3"],["red","4"],["red","5"],["red","6"],["red","7"],["red","8"],["red","9"],["red","0"]
            ,["green","1"],["green","2"],["green","3"],["green","4"],["green","5"],["green","6"],["green","7"],["green","8"],["green","9"],["green","0"]
            ,["blue","1"],["blue","2"],["blue","3"],["blue","4"],["blue","5"],["blue","6"],["blue","7"],["blue","8"],["blue","9"],["blue","0"]
            ,["yellow","1"],["yellow","2"],["yellow","3"],["yellow","4"],["yellow","5"],["yellow","6"],["yellow","7"],["yellow","8"],["yellow","9"],["yellow","0"]]

#The card at the top of the pile
index = random.choice(numList)
topCard = cardList[index]

#returns the images of the front side of the cards
def generate_card(card):
    font = ImageFont.truetype("arial.ttf", 75)
    img = Image.new("RGB", (100, 150), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle((5, 5, 90, 140), fill=card[0])
    draw.text((30,40), card[1], fill = 'white', font = font,stroke_width = 3)
    return img

#returns the images of the back side of the cards
def backside():
    img = Image.new("RGB", (100, 150), "black")
    draw = ImageDraw.Draw(img)
    draw.rectangle((5, 5, 90, 140), fill='red')
    return img

#creates the image of the deck
font = ImageFont.truetype("arial.ttf", 30)
img = Image.new("RGB", (100, 150), "black")
draw = ImageDraw.Draw(img)
draw.rectangle((5, 5, 90, 140), fill='red')
draw.text((10,40), f'Draw\nCard', fill = 'white', font = font,stroke_width = 0.5)
drawCardImage = ImageTk.PhotoImage(img)

#calls function opmove() after 1.1 seconds
def opturn():
    global turn
    if turn == 2:
        root.after(1100,opmove)

#Moves the opponents cards
def opmove():    
    global turn
    global topCard
    global uno_state
    for i in range(len(opponentCards)):
        if opponentCards[i][0] == topCard[0] or opponentCards[i][1] == topCard[1]:
            uno_state = False
            index = cardList.index(opponentCards[i])
            btn = buttonList[index]
            btn.grid(row=2,column=4)
            btn.lift()
            topCard = opponentCards[i]
            opimg = ImageTk.PhotoImage(generate_card(opponentCards[i]))
            btn.configure(image = opimg)
            for j in range(len(opponentCards)-(i+1)):
                crd = cardList.index(opponentCards[len(opponentCards)-(j+1)])
                btn = buttonList[crd]
                btn.grid(row=1, column = len(opponentCards)-(j+1))
            opponentCards.remove(opponentCards[i])
            if opponentCards == []:
                    mk.showinfo("You Lost", "The opponent placed down all of their cards.")
            if len(opponentCards) == 1:
                
                root.after(1000, lambda p = opponentCards, n = 1: check_uno(p,n))
                
            turn = 1
            return
    drawCard(opponentCards, 1)

#If the player incorrectly calls out Uno, this function distributes three cards to the player.
def false_uno():
    global uno_state
    global penalty
    for i in range(6):
        uno_state = False
        penalty = True
        drawCard(playerCards, 3)
    penalty = False

#This function changes the variable uno_state to true of either of the player's number of cards goes down to one
def call_uno():
    global uno_state
    if len(playerCards) == 1 or len(opponentCards) == 1:
        uno_state = True  
    else:
        false_uno() 

    
    
    
        
#this function places down the card the user clicks if the rules allow it
def playCard(card, button):
    global topCard
    global turn
    global uno_state
    row = int(button.grid_info()['row'])
    column = int(button.grid_info()['column'])
    uno_state = False
    if card[0] == topCard[0] or card[1] == topCard[1]:
        if card[0] != topCard[0] or card[1] != topCard[1]:
            if turn == 1:
                button.grid(row=2,column=4)
                button.lift()
                topCard = card
                index = playerCards.index(card)
                for i in range(len(playerCards)-(index+1)):
                    crd = cardList.index(playerCards[len(playerCards)-(i+1)])
                    btn = buttonList[crd]
                    btn.grid(row=3, column = len(playerCards)-(i+1))
                playerCards.remove(card)
                if playerCards == []:
                    mk.showinfo("You Won", "Congratulations, you placed all of your cards.")
                if len(playerCards) == 1:
                    root.after(1000, lambda p = playerCards, n = 3: check_uno(p,n))
                    
                turn = 2
                opturn()
                    
#This function distributes a card from the deck to either of the players depending on its arguments
def drawCard(player,num):
    global topCard
    global turn
    global uno_state
    if (player == playerCards and turn == 1) or (player == opponentCards and turn == 2):
        if len(numList) > 0:
            index = random.choice(numList)
            if player == opponentCards:
                buttonList[index].configure(image = tk_image[1])
            buttonList[index].grid(row=num,column=len(player)+1, sticky='w')
            player.append(cardList[index])
            if not(cardList[index][0] == topCard[0] or cardList[index][1] == topCard[1]) and not uno_state and not penalty:
                if turn == 1:
                    turn = 2
                    opturn()
                elif turn == 2:
                    turn = 1
            elif turn == 2 and not uno_state and not penalty:
                opturn()
            numList.remove(index)
        else:
            deck.destroy()
            
    
#This function checks if uno was called when there is one card left for either player and distributes three cards depending on if it was called on time.
def check_uno(player, num):
    global uno_state, penalty, turn
    if player == opponentCards and uno_state and len(opponentCards) == 1:
        saved_turn = turn
        turn = 2  
        for i in range(6):
            drawCard(opponentCards, 1)
        turn = saved_turn
    elif player == playerCards and not uno_state and len(playerCards) == 1:
        saved_turn = turn
        turn = 1  
        penalty = True
        for i in range(6):
            drawCard(playerCards, 3)
        turn = saved_turn
    uno_state = False
    penalty = False
    
        
#Creates the Deck button and places it down
deck = tk.Button(root, image = drawCardImage)
deck.configure(command = lambda p=playerCards,n=3: drawCard(p,n))
deck.grid(row=2,column=1)
#Creates the Uno button and places it down.
unoButton = tk.Button(root, text="Siete!", font=("arial", 20), bg="red", fg="white",command=lambda: call_uno())
unoButton.grid(row=2, column=6)
#Creates all the cards
for i in range(40):
    tk_image = [ImageTk.PhotoImage(generate_card(cardList[i])),ImageTk.PhotoImage(backside())]
    button = tk.Button(root, image = tk_image[0])
    button.configure(command=lambda c=cardList[i], b=button: playCard(c, b))
    button.image = tk_image
    buttonList.append(button)
#Creates the grid for all the widgets to be placed
for i in range(10):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)
buttonList[index].grid(row=2,column=4, sticky='w')
numList.remove(index)

#Gives the user all of their cards
for i in range(7):
    index = random.choice(numList)
    buttonList[index].grid(row=3,column=i+1, sticky='w')
    playerCards.append(cardList[index])
    numList.remove(index)

#Gives the opponent all of their cards
for i in range(7):
    index = random.choice(numList)
    buttonList[index].configure(image=tk_image[1])
    buttonList[index].grid(row=1,column=i+1, sticky = 'w')
    opponentCards.append(cardList[index])

    numList.remove(index)
    
mk.showinfo('Rules', 'This game is similar to the popular game Uno. ' \
            ' The goal is to run out of all of your cards, your cards being the ones in the third row. ' \
            ' You can place down cards if it is your turn, and you can only place down cards if the specific card has the same color or number as the card in the center. ' \
            'After you place down a card, it is now your opponent\'s turn. ' \
            'If you cannot place any cards down and it is your turn, you may draw a card from the deck. ' \
            'If the card that you drew is playable, you may place it. If not, it is now the opponent\'s turn. ' \
            'Once you or your opponent are down to your last card, you have to press the siete button within 1 second. ' \
            'If you are on your last card and fail to press it, you gain six cards from the deck.' \
            'If your opponent is on their last card and you press the siete button in time, they gain six cards from the deck. ' \
            'If you press the siete button while no one has only one card left, you gain six cards from the deck. ')

root.mainloop()
