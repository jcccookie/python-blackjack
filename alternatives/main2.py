import random

################################################################################
#Global Variables
suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

onGame = True
################################################################################
#Classes
class Card:
   def __init__(self,suit,rank):
      self.suit = suit
      self.rank = rank

   def __str__(self):
      return self.rank + ' of ' + self.suit

class Deck:
   def __init__(self):
      self.deck = []
      for suit in suits:
         for rank in ranks:
            self.deck.append(Card(suit,rank))
   
   def shuffle(self):
      random.shuffle(self.deck)

   def __str__(self):
      dec_comp = ''
      for card in self.deck:
         dec_comp += '\n' + card.__str__()
      return 'The deck has: ' + dec_comp

   def deal(self):
      return self.deck.pop()

class Hand:
   def __init__(self):
      self.cards = []
      self.value = 0
      self.ace = False

   def addCard(self,card):
      self.cards.append(card)
      self.value += values[card.rank]
      if card.rank == 'Ace':
         self.ace = True

   def adjustAce(self):
      if self.ace and self.value > 21:
         self.value -= 10
         self.ace = False

class Chip:
   def __init__(self):
      self.total = 100
      self.bet = 0
   
   def winBet(self):
      self.total += self.bet

   def loseBet(self):
      self.total -= self.bet

   def __str__(self):
      return f"You have {self.total} chips." 


################################################################################
#Methods

def takeBet(chip):
   while True:   
      try:
         chip.bet = int(input("How many chips do you want to bet?: "))
      except ValueError:
         print("It seems that it is not an integer!")
      else:
         if chip.bet > chip.total:
            print(f"The number of chips is not sufficient!\nNow you have {chip.total} chips")
         else:
            break

def hit(deck,hand):
   hand.addCard(deck.deal())
   hand.adjustAce()

def askHitOrStand(deck,hand):
   global onGame

   while True:
      ans = input("Do you want to (h)it or (s)tand?: ").lower()
      # If player hits
      if ans[0] == 'h':
         hit(deck,hand)
      elif ans[0] == 's':
         print("Player Stands. Now dealer is playing...")
         onGame = False
      else:
         print("Input is not valid.")
         continue
      break
      

def showSome(player,dealer):
   print("Dealer's Hand:")
   print(" <Hidden Card>")
   print("", dealer.cards[1])
   print(f" Sum: {values[dealer.cards[1].rank]}")
   print("Player's Hand:", *player.cards, sep="\n ")
   print(f" Sum: {player.value}")

def showAll(player,dealer):
   print("Dealer's Hand:", *dealer.cards, sep="\n ")
   print(f" Sum: {dealer.value}")
   print("Player's Hand:", *player.cards, sep="\n ")
   print(f" Sum: {player.value}")

def replay(chip):
   return input(f"You have {chip.total}.\nDo you want to replay the game? Enter 'Y' or 'N': ").lower().startswith('y')

def restart():
   return input("Do you want to (R)estart or (Q)uit the game?: ").lower().startswith('r')

################################################################################
print("Welcome to Blackjack!!")
#Program Starts
while True:
   player_chip = Chip()
   print(f"You now have {player_chip.total}")

   #Game Round Starts
   while True:
      #Shuffle a deck
      deck = Deck()
      deck.shuffle()

      print("Deck has been shuffled!")

      #Take a bet
      takeBet(player_chip)
      
      #Deal cards to player and dealer
      playerHand = Hand()
      dealerHand = Hand()

      playerHand.addCard(deck.deal())
      playerHand.addCard(deck.deal())
      dealerHand.addCard(deck.deal())
      dealerHand.addCard(deck.deal())

      isPlayerBusts = False
      
      # Player is playing
      while onGame:
         # Display Cards on hands
         showSome(playerHand,dealerHand)
         # Ask a player to hit or stand
         askHitOrStand(deck,playerHand)

         # Player busts
         if playerHand.value > 21:
            isPlayerBusts = True
            player_chip.loseBet()
            showSome(playerHand,dealerHand)
            print("Player busts!")
            break
      
      # Dealer is playing
      if not isPlayerBusts:
         # Deal the card until the number reaches 17
         while dealerHand.value < 17:
            hit(deck,dealerHand)
         showAll(playerHand,dealerHand)

         # Dealer busts
         if dealerHand.value > 21:
            print("Dealer busts!")
         # Player wins
         elif dealerHand.value < playerHand.value:
            print("Player wins!!")
            player_chip.winBet()
         # Dealer wins
         elif dealerHand.value > playerHand.value:
            print("Dealer wins!!")
            player_chip.loseBet()
         # Ties
         else:
            print("Player and dealer tie! It's a push")

      onGame = True
      if not replay(player_chip):
         break

   if not restart():
      break