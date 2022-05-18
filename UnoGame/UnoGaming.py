import random
import time



color = ('VERMELHO','VERDE','AZUL','AMARELO')
value = ('0','1','2','3','4','5','6','7','8','9','Pula','Inverte','Compra2','Compra4','Muda')
type_card = {'0':'number','1':'number','2':'number','3':'number','4':'number','5':'number','6':'number',
            '7':'number','8':'number','9':'number','Pula':'action','Inverte':'action','Compra2':'action',
            'Compra4':'action_nocolor','Muda':'action_nocolor'}

class Card:
    def __init__(self, color, value):
        self.value = value
        if type_card[value] == 'number':
            self.color = color
            self.cardtype = 'number'
        elif type_card[value] == 'action':
            self.color = color
            self.cardtype = 'action'
        else:
            self.color = None
            self.cardtype = 'action_nocolor'

    def __str__(self):
        if self.color == None:
            return self.value
        else:
            return self.color + " " + self.value

class Deck:
    def __init__(self):
        self.deck = []
        for i in color:
            for j in value:
                if type_card[j] != 'action_nocolor':
                    self.deck.append(Card(i, j))
                    self.deck.append(Card(i, j))
                else:
                    self.deck.append(Card(i, j))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'O Deck tem ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def Draw(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.cardsstr = []
        self.number_cards = 0
        self.action_cards = 0

    def add_card(self, card):
        self.cards.append(card)
        self.cardsstr.append(str(card))
        if card.cardtype == 'number':
            self.number_cards += 1
        else:
            self.action_cards += 1

    def remove_card(self, place):
        self.cardsstr.pop(place - 1)
        return self.cards.pop(place - 1)

    def cards_in_hand(self):
        for i in range(len(self.cardsstr)):
            print(f' {i + 1}.{self.cardsstr[i]}')

    def single_card(self, place):
        return self.cards[place - 1]

    def no_of_cards(self):
        return len(self.cards)


def choose_first():
    if random.randint(0,1)==0:
        return 'Jogador'
    else:
        return 'Computador'

def single_card_check(top_card,card):
    if card.color==top_card.color or top_card.value==card.value or card.cardtype=='action_nocolor':
        return True
    else:
        return False

def full_hand_check(hand,top_card):
    for c in hand.cards:
        if c.color==top_card.color or c.value == top_card.value or c.cardtype=='action_nocolor':
            return hand.remove_card(hand.cardsstr.index(str(c))+1)
    else:
        return 'sem carta'

def win_check(hand):
    if len(hand.cards)==0:
        return True
    else:
        return False

def last_card_check(hand):
    for c in hand.cards:
        if c.cardtype!='number':
            return True
        else:
            return False

while True:
    print('********************     UNO    ********************')
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    for i in range(7):
        player_hand.add_card(deck.Draw())
    pc_hand = Hand()
    for i in range(7):
        pc_hand.add_card(deck.Draw())
    top_card = deck.Draw()
    if top_card.cardtype != 'number':
        while top_card.cardtype != 'number':
            top_card = deck.Draw()
    print('\nCarta no topo: {}'.format(top_card))
    time.sleep(1)
    playing = True

    turn = choose_first()
    print(turn + ' joga primeiro')
    name=input("Nome do jogador: ")
    while playing:
        if turn == 'Jogador':
            print('\n----------------------------------------------------\n')
            print('\nCarta na mesa: ' + str(top_card)+ '\n')
            print('Suas cartas:\n ')
            player_hand.cards_in_hand()
            if player_hand.no_of_cards() == 1:
                if last_card_check(player_hand):
                    print('Ultima carta não é uma ação \nAdiciona uma carta')
                    player_hand.add_card(deck.Draw())
                    print('Suas cartas: ')
                    player_hand.cards_in_hand()
            choice = input("\nJogar (j) ou Comprar (c) ?: ")
            if choice == 'j':
                pos = int(input('Escolha sua carta pelo indice: '))
                temp_card = player_hand.single_card(pos)
                if single_card_check(top_card, temp_card):
                    if temp_card.cardtype == 'number':
                        top_card = player_hand.remove_card(pos)
                        turn = 'Computador'
                    else:
                        if temp_card.value == 'Pula':
                            turn = 'Jogador'
                            top_card = player_hand.remove_card(pos)
                        elif temp_card.value == 'Inverte':
                            turn = 'Jogador'
                            top_card = player_hand.remove_card(pos)
                        elif temp_card.value == 'Compra2':
                            pc_hand.add_card(deck.Draw())
                            pc_hand.add_card(deck.Draw())
                            top_card = player_hand.remove_card(pos)
                            turn = 'Jogador'
                        elif temp_card.value == 'Compra4':
                            for i in range(4):
                                pc_hand.add_card(deck.Draw())
                            top_card = player_hand.remove_card(pos)
                            draw4color = input('Escolha uma cor, use caps: ')
                            if draw4color != draw4color.upper():
                                draw4color = draw4color.upper()
                            top_card.color = draw4color
                            turn = 'Jogador'
                        elif temp_card.value == 'Muda':
                            top_card = player_hand.remove_card(pos)
                            wildcolor = input('Escolha uma cor, use caps: ')
                            if wildcolor != wildcolor.upper():
                                wildcolor = wildcolor.upper()
                            top_card.color = wildcolor
                            turn = 'Computador'
                else:
                    print('Carta não pode ser usada')
            elif choice == 'c':
                temp_card = deck.Draw()
                print('Você comprou: ' + str(temp_card))
                time.sleep(1)
                if single_card_check(top_card, temp_card):
                    player_hand.add_card(temp_card)
                else:
                    print('Não pode usar esta carta')
                    player_hand.add_card(temp_card)
                    turn = 'Computador'
            if win_check(player_hand):
                print('\n***** ',name,' Venceu ******!!')
                playing = False
                break

        if turn == 'Computador':
            print('\n----------------------------------------------------\n')
            if pc_hand.no_of_cards() == 1:
                if last_card_check(pc_hand):
                    time.sleep(1)
                    print('Computador adiciona cartas a mão')
                    pc_hand.add_card(deck.Draw())
            temp_card = full_hand_check(pc_hand, top_card)
            time.sleep(1)
            if temp_card != 'sem carta':
                print(f'\nComputador joga: {temp_card}')
                time.sleep(1)
                if temp_card.cardtype == 'number':
                    top_card = temp_card
                    turn = 'Jogador'
                else:
                    if temp_card.value == 'Pula':
                        turn = 'Computador'
                        top_card = temp_card
                    elif temp_card.value == 'Inverte':
                        turn = 'Computador'
                        top_card = temp_card
                    elif temp_card.value == 'Compra2':
                        player_hand.add_card(deck.Draw())
                        player_hand.add_card(deck.Draw())
                        top_card = temp_card
                        turn = 'Computador'
                    elif temp_card.value == 'Compra4':
                        for i in range(4):
                            player_hand.add_card(deck.Draw())
                        top_card = temp_card
                        draw4color = pc_hand.cards[0].color
                        print('Muda cor para: ', draw4color)
                        top_card.color = draw4color
                        turn = 'Computador'
                    elif temp_card.value == 'Muda':
                        top_card = temp_card
                        wildcolor = pc_hand.cards[0].color
                        print("Muda cor para: ", wildcolor)
                        top_card.color = wildcolor
                        turn = 'Jogador'
            else:
                print('\nComputador compra carta')
                time.sleep(1)
                temp_card = deck.Draw()
                if single_card_check(top_card, temp_card):
                    print(f'Computador joga: {temp_card}')
                    time.sleep(1)
                    if temp_card.cardtype == 'number':
                        top_card = temp_card
                        turn = 'Jogador'
                    else:
                        if temp_card.value == 'Pula':
                            turn = 'Computador'
                            top_card = temp_card
                        elif temp_card.value == 'Inverte':
                            turn = 'Computador'
                            top_card = temp_card
                        elif temp_card.value == 'Compra2':
                            player_hand.add_card(deck.Draw())
                            player_hand.add_card(deck.Draw())
                            top_card = temp_card
                            turn = 'Computador'
                        elif temp_card.value == 'Compra4':
                            for i in range(4):
                                player_hand.add_card(deck.Draw())
                            top_card = temp_card
                            draw4color = pc_hand.cards[0].color
                            print('Mudou cor para: ', draw4color)
                            top_card.color = draw4color
                            turn = 'Computador'
                        elif temp_card.value == 'Muda':
                            top_card = temp_card
                            wildcolor = pc_hand.cards[0].color
                            print('Mudou cor para: ', wildcolor)
                            top_card.color = wildcolor
                            turn = 'Jogador'
                else:
                    print('\nComputador não tem carta')
                    time.sleep(1)
                    pc_hand.add_card(temp_card)
                    turn = 'Jogador'
            print('\nComputador tem {} cartas na mão'.format(pc_hand.no_of_cards()))
            time.sleep(1)
            if win_check(pc_hand):
                print('\n****** Computador venceu, tente novamente *******!!')
                playing = False

    newGame = input('Gostaria de jogar novamente? (s/n)')
    if newGame == 's':
        continue
    else:
        print('\nObrigado por jogar!!')
        break
