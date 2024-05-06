import random

STARTING_MONEY = 1000

class Player:
    def __init__(self, dealer=False):
        self.money = STARTING_MONEY
        self.hand = []
        self.dealer = dealer
        self.name = "Dealer"
        if not self.dealer:
            self.name = input("What's your name? ")

    def deal(self, card):
        self.hand.append(card)

    def cardDisplay(self):
        cards = ""
        for i in range(len(self.hand[0].art)):
            for card in self.hand:
                cards += f"{card.art[i]} "
            cards += "\n"
        cards = cards[:-1]
        return cards

class Card:
    def __init__(self, suite, value):
        self.suite = suite
        self.value = value
        self.cardMap = {1: "A ", 2: "2 ", 3:"3 ", 4:"4 ", 5:"5 ", 6:"6 ", 7:"7 ", 8:"8 ", 9:"9 ", 10:"10", 11:"J ", 12:"Q ", 13:"K "}
        self.suiteMap = {0: "♣", 1:"\x1b[31m♦\x1b[0m", 2:"\x1b[31m♥\x1b[0m", 3:"♠"}
        self.art = f""" ___ 
|{self.suiteMap[self.suite]}  |
| {self.cardMap[self.value]}|
|  {self.suiteMap[self.suite]}|
 --- """.split("\n")

deck = []

def resetDeck(deck):
    for _ in range(6):
        for i in range(4):
            for j in range(1, 14):
                deck.append(Card(i, j))
    random.shuffle(deck)

resetDeck(deck)
player = Player()
dealer = Player(True)

def calculateHandValue(hand):
    handValue = 0
    for card in hand:
        if card.value != 1:
            handValue += card.value if card.value < 11 else 10
    for card in hand:
        if card.value == 1:
            handValue += 11 if handValue + 11 <= 21 else 1
    return handValue

def nextRound(deck, player, dealer):
    player.hand = []
    dealer.hand = []
    bet = int(input(f"How much do you want to bet? (\x1b[4m{player.money}\x1b[0m in bank): "))
    if bet > player.money:
        bet = player.money
    for _ in range(2):
        player.deal(deck.pop())
        dealer.deal(deck.pop())
    playerValue = calculateHandValue(player.hand)
    dealerValue = calculateHandValue(dealer.hand)

    while True:
        dealerString = "\x1b[91mDealer's Cards:\x1b[0m\n{}\x1b[0m"
        playerString = "\x1b[32mYour cards:\x1b[0m\n{}\x1b[0m"
        dealerScore = "\x1b[91mDealer's Score: {}"
        playerScore = "\x1b[32m{}'s score: {}\x1b[0"
        print(f"{dealerString.format(dealer.cardDisplay())}\n{dealerScore.format(dealerValue)}\n{playerString.format(player.cardDisplay())}\n{playerScore.format(player.name, playerValue)}")
        print("\x1b[33m_\x1b[0m" * 50)
        getNewCard = input("Get new card? (y/n): ")
        if getNewCard == "y":
            player.deal(deck.pop())
            playerValue = calculateHandValue(player.hand)
        else:
            while dealerValue < playerValue:
                dealer.deal(deck.pop())
                dealerValue = calculateHandValue(dealer.hand)
            if dealerValue > 21:
                player.money += bet
                print(dealerString.format(dealer.cardDisplay()))
                print(f"You won! :) Money: {player.money}")
                break
            else:
                player.money -= bet
                print(dealerString.format(dealer.cardDisplay()))
                print(f"You lost. :( Money: {player.money}")
                break
        if playerValue > 21:
            player.money -= bet
            print(playerString.format(player.cardDisplay()))
            print(f"You busted. :( Money: {player.money}")
            break
    print("\x1b[35m_\x1b[0m" * 60)

while player.money > 0 and player.money < STARTING_MONEY * 100:
    if len(deck) < 52:
        resetDeck(deck)
    nextRound(deck, player, dealer)
if player.money <= 0:
    print("Your lost all of your money.")
else:
    print("You were thrown out the casino and were accused of cheating. :D")

