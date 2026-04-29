import tkinter as tk
import tkinter.messagebox as mk
from PIL import Image, ImageDraw, ImageTk, ImageFont
import random
root =tk.Tk()
root.title('Uno')
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f'{width}x{height}')

buttonList = []
playerCards = []
opponentCards = []
turn = 1
numList = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]
cardList = [["red","1"],["red","2"],["red","3"],["red","4"],["red","5"],["red","6"],["red","7"],["red","8"],["red","9"],["red","0"]
            ,["green","1"],["green","2"],["green","3"],["green","4"],["green","5"],["green","6"],["green","7"],["green","8"],["green","9"],["green","0"]
            ,["blue","1"],["blue","2"],["blue","3"],["blue","4"],["blue","5"],["blue","6"],["blue","7"],["blue","8"],["blue","9"],["blue","0"]
            ,["yellow","1"],["yellow","2"],["yellow","3"],["yellow","4"],["yellow","5"],["yellow","6"],["yellow","7"],["yellow","8"],["yellow","9"],["yellow","0"]]
index = random.choice(numList)
topCard = cardList[index]
def generate_card(card):
    font = ImageFont.truetype("arial.ttf", 75)
    img = Image.new("RGB", (100, 150), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle((5, 5, 90, 140), fill=card[0])
    draw.text((30,40), card[1], fill = 'white', font = font,stroke_width = 3)
    return img

def backside():
    img = Image.new("RGB", (100, 150), "black")
    draw = ImageDraw.Draw(img)
    draw.rectangle((5, 5, 90, 140), fill='red')
    return img

font = ImageFont.truetype("arial.ttf", 30)
img = Image.new("RGB", (100, 150), "black")
draw = ImageDraw.Draw(img)
draw.rectangle((5, 5, 90, 140), fill='red')
draw.text((10,40), f'Draw\nCard', fill = 'white', font = font,stroke_width = 0.5)
drawCardImage = ImageTk.PhotoImage(img)
def opturn():
    global turn
    if turn == 2:
        root.after(500,opmove)

def opmove():    
    global turn
    global topCard
    for i in range(len(opponentCards)):
        if opponentCards[i][0] == topCard[0] or opponentCards[i][1] == topCard[1]:
            turn = 1
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
                    mk.showinfo("You Lost", "You'll get it next time")
            return
    drawCard(opponentCards, 1)

        
    
def playCard(card, button):
    global topCard
    global turn
    result = ''
    row = int(button.grid_info()['row'])
    column = int(button.grid_info()['column'])
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
                    mk.showinfo("You Won", "Congratulations")
                
                turn = 2
                opturn()
                    

def drawCard(player,num):
    global topCard
    global turn
    if (player == playerCards and turn == 1) or (player == opponentCards and turn == 2):
        if len(numList) > 0:
            index = random.choice(numList)
            if player == opponentCards:
                buttonList[index].configure(image = tk_image[1])
            buttonList[index].grid(row=num,column=len(player)+1, sticky='w')
            player.append(cardList[index])
            if not(cardList[index][0] == topCard[0] or cardList[index][1] == topCard[1]):
                if turn == 1:
                    turn = 2
                    opturn()
                elif turn == 2:
                    turn = 1
            elif turn == 2:
                opturn()
        
        else:
            deck.destroy()
    
    
    numList.remove(index)

deck = tk.Button(root, image = drawCardImage)
deck.configure(command = lambda p=playerCards,n=3: drawCard(p,n))
deck.grid(row=2,column=1)
for i in range(40):
    tk_image = [ImageTk.PhotoImage(generate_card(cardList[i])),ImageTk.PhotoImage(backside())]
    button = tk.Button(root, image = tk_image[0])
    button.configure(command=lambda c=cardList[i], b=button: playCard(c, b))
    button.image = tk_image
    buttonList.append(button)
for i in range(10):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)
buttonList[index].grid(row=2,column=4, sticky='w')
numList.remove(index)

for i in range(7):
    index = random.choice(numList)
    buttonList[index].grid(row=3,column=i+1, sticky='w')
    playerCards.append(cardList[index])
    numList.remove(index)
for i in range(7):
    index = random.choice(numList)
    buttonList[index].configure(image=tk_image[1])
    buttonList[index].grid(row=1,column=i+1, sticky = 'w')
    opponentCards.append(cardList[index])

    numList.remove(index)
    



root.mainloop()
