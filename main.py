import random, time


########################################################################################
########## Global Variables
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

onGame = True

########################################################################################
########## Classes
class Card:
   def __init__(self,suit,rank):
      self.suit = suit
      self.rank = rank

   def __str__(self):
      return f"{self.rank} of {self.suit}"


class Deck:
   def __init__(self):
      self.deck = []
      for suit in suits:
         for rank in ranks:
            self.deck.append(Card(suit, rank))

   def __str__(self):
      return str([str(card) for card in self.deck])

   def __len__(self):
      return len(self.deck)

   def shuffle(self):
      random.shuffle(self.deck)
   
   def deal(self):
      #return Card instance
      return self.deck.pop()


class Hand:
   def __init__(self):
      self.cards = []
      self.value = 0
      self.aces = 0

   def add_card(self,card):
      '''
      Argument: Card Instance by using deal() method
      '''
      self.cards.append(card)
      self.value += values[card.rank]
      if card.rank == 'Ace':
         self.aces += 1
      
   def adjust_for_ace(self):
      if self.aces and self.value > 21:
         self.value -= 10
         self.aces -= 1

   def __str__(self):
      return str([str(card) for card in self.cards])


class Chips:
   def __init__(self):
      self.total = 100
      self.bet = 0
   
   def win_bet(self):
      self.total += self.bet

   def lose_bet(self):
      self.total -= self.bet

   def __str__(self):
      return f"Your bet amount is {self.bet} and balance is {self.total}"

########################################################################################
########## Methods

def take_bet(chips):
   while True:
      try:
         chips.bet = int(input("Enter your bet amount: "))
      except ValueError:
         print("Looks like you did not enter an integer!")
      else:
         if chips.bet > chips.total:
            print("Sorry, your bet can't exceed ", chips.total)
         else:
            break


def hit(deck,hand):
   hand.add_card(deck.deal())
   hand.adjust_for_ace()


def hit_or_stand(deck,hand):
   global onGame

   while True:
      ans = input("Enter 'h' for HIT or 's' for STAND: ").lower()
      
      if ans[0] == 'h':
         hit(deck,hand)
      elif ans[0] == 's':
         print("Player stands. Dealer is playing.\n")
         onGame = False
      else:
         print("Sorry. Please enter again")
         continue
      break
         

def show_some(player,dealer):
   print(f"Dealer's Hand: ['Hidden'], {[str(card) for card in dealer.cards[1:]]}")
   print(f"Dealer's Sum: {values[dealer.cards[1].rank]}")
   print(f"Your Hand: {[str(card) for card in player.cards]}")
   print(f"Your Sum: {player.value}")
   print("")


def show_all(player,dealer):
   print(f"Dealer's Hand: {[str(card) for card in dealer.cards]}")
   print(f"Dealer's Sum: {dealer.value}")
   print(f"Your Hand: {[str(card) for card in player.cards]}")
   print(f"Your Sum: {player.value}")
   print("")


def player_busts(chips):
   chips.lose_bet()
   print("Player Busts!")

def player_wins(chips):
   chips.win_bet()
   print("Player Wins!")

def dealer_busts(chips):
   chips.win_bet()
   print("Dealer Busts!")

def dealer_wins(chips):
   chips.lose_bet()
   print("Dealer Wins!")

def push():
   print("Dealer and Player tie! It's a push.\n")

def timeSleep(sec, message = ".."):
   print(message)
   for i in range(sec, 0, -1):
      time.sleep(1)
      print(i)
   time.sleep(1)

def replay(chips):
   return input(f"Now you have {chips.total}.\nDo you want to play again?? Enter Y or N: ").lower().startswith('y')

def quit():
   return input("If you want to (R)estart or (Q)uit the game??: ").lower().startswith('r')




########################################################################################
########## Main Program

while True:
   print("Welcome to BlackJack!!!")   
   
   # Player was given chips
   print("You now have 100 Chips!")
   chip = Chips()

   # Game Round
   while True:
      print("The dealer is shuffling a deck")
      # timeSleep(3, '(shuffling..)')

      print("The deck has been shuffled!")
      deck = Deck()
      deck.shuffle()

      take_bet(chip)
      
      # timeSleep(2, '(distributing cards..)')

      print("You and the dealer have received two cards, respectively.\n")
      playerHand = Hand()
      dealerHand = Hand()
      for i in range(2):
         playerHand.add_card(deck.deal())
         dealerHand.add_card(deck.deal())

      isPlayerBust = False
      
      # Ask player hit or stand
      while onGame:
         show_some(playerHand,dealerHand)

         # If the player busts
         if playerHand.value > 21:
            show_some(playerHand,dealerHand)
            player_busts(chip)
            isPlayerBust = True
            break
         # Continue to hit
         else:
            # If the player's hand equals to 21.
            if playerHand.value == 21:
               break
            hit_or_stand(deck,playerHand)
            continue
         
      # Dealer's turn
      while not isPlayerBust:
         
         # If dealer busts
         if dealerHand.value > 21:
            show_all(playerHand,dealerHand)
            dealer_busts(chip)
            break
         # If dealer sum is between 21 and 17
         elif 17 <= dealerHand.value <= 21:
            show_all(playerHand,dealerHand)
            print("Dealer Stands")
            if dealerHand.value > playerHand.value:
               dealer_wins(chip)
            elif dealerHand.value < playerHand.value:
               player_wins(chip)
            else:
               push()
            break
         else:
            hit(deck,dealerHand)
            continue
         
      onGame = True
      if not replay(chip):
         break

   if not quit():
      break

   

