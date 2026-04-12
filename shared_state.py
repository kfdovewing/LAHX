#add your very global variables here
# chars = {"cat" : "assets/buddies/cat.png", "froggy" : "assets/buddies/froggy.png", "hat_guy" : "assets/buddies/hat_guy.png", "party_guy" : "assets/buddies/party_guy.png"}
buddy = "hi"
money = 0
food = 0
hunger = 0
happiness = 100

def cat():
    global buddy
    buddy = "assets/buddies/cat.png"

def frog():
    global buddy
    buddy = "assets/buddies/froggy.png"

def hat():
    global buddy
    buddy = "assets/buddies/hat_guy.png"

def party():
    global buddy
    buddy = "assets/buddies/party_guy.png"