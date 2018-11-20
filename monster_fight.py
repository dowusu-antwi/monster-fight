#!/usr/bin/env python

"""
Monster Fight Game

Created on Wed Feb 24 15:20:00 2016

@author: dowusu

"""
import random
import time
from sys import stdout

#initialize dict of weapons, values: [hitpoint, tries]
WEAPONS = {'sword': [3,2], 'axe': [4,2], 'bow and arrow': [3,4], 'dagger': [2,4], 'bo staff':[1,5]} #'HAND-TO-HAND': [1,1] 

#other necessary functionss
#-------------print by letter
def quickPrint(string,state=0):
    #change quickPrint to allow for raw_input
    """
    Print each character of a string one at a time.
    Simulates classic video game message output.
    
    can take input string of raw_input (''), make state True
    
    FIX PRINTING ON SAME LINE, CHARACTER AT A TIME
    """
    #figure out a way dependent on actual time
    #   rather than time based on processing speed
    string = str(string)
    for char in string:
        if char in '.!?':
            try:
                charInd = string.index(char)
                if string[charInd+1] == '.' or string[charInd-1] == '.':
                    stdout.write(char)
		    stdout.flush()
                    time.sleep(0.05)  
                elif string[charInd-1] == '.' and string[charInd-2] == '.':
		    stdout.write(char)
		    time.sleep(1.5) 
		    stdout.flush()
		else:                      
                    stdout.write(char)
                    time.sleep(0.05)
            except IndexError:
                stdout.write(char)
		stdout.flush()
                time.sleep(0.5)    
        elif char.lower() not in 'abcdefghijklmnopqrstuvwxyz':
            stdout.write(char)
        else:
            time.sleep(0.05)          
            stdout.write(char)
	    stdout.flush()
    if char == string[len(string)-1]:
        stdout.flush()
        if state:
            out = raw_input('')
            return out.lower()
        else: 
            print ''
#----------choose weapon
def getWeaponList(weaponFile):
    """
    Create list of weapons
    """
    openFile = open(weaponFile, 'r')
    fileLines = openFile.readlines()
    monsterList = []    
    for line in fileLines:
        prev = []
        monster = []
        health = []
        loot = []
        for char in line:
            # add ':' or ',' to prev
            # if empty list weapon, only ':' power, if ':' and ',' hitpoints
            if char == '#' and char == line[0]:
                break            
            if (char == ':' or char == ',') and prev != [':',',']:
                prev.append(char)            
            else:
                if prev == []:
                    monster.append(char)
                elif prev == [':']:
                    health.append(char)
                else:
                    loot.append(char)
        if prev != []:
            name = ''.join(weapon)
            healthPoints = int(''.join(power))
            hitpoints = ''.join(hitpoints).strip().replace('\t','').split(',')
            # add weapon object to weapon list
            weapon = Weapon()
    return monsterList

#-------create monster
def getMonsterList(monsterFile):
    openFile = open(monsterFile, 'r')
    fileLines = openFile.readlines()
    monsterList = []    
    for line in fileLines:
        prev = []
        monster = []
        health = []
        loot = []
        for char in line:
            # add ':' or ',' to prev
            # if empty list monster, only ':' health, if ':' and ',' loot
            if char == '#' and char == line[0]:
                break            
            if (char == ':' or char == ',') and prev != [':',',']:
                prev.append(char)            
            else:
                if prev == []:
                    monster.append(char)
                elif prev == [':']:
                    health.append(char)
                else:
                    loot.append(char)
        if prev != []:
            name = ''.join(monster)
            healthPoints = int(''.join(health))
            loot = ''.join(loot).strip().replace('\t','').split(',')
            # calculate power and speed for each monster using health
            power = (float(healthPoints)/4)+2
            speed = (power/healthPoints)*10
            # add monster object to monsterList
            monster = Monster(name,healthPoints,power,speed,loot)
            monsterList.append(monster)
    return monsterList

def getRandMonster(monsterList):
    return random.choice(monsterList)

def createPopulation(predator, prey, population):
    ## create's dynamic population of monsters (predator v. prey)
    ## predator, prey - Creature objects
    ## population - total number of creatures
    prey_count = population/2
    predator_count = population/2
    
    
#### ---- necessary functions end ---- ####
        
#create creature class (subclasses: fighter, monster)
class Creature(object):
    def __init__(self,name,health,power,speed):
        self.name = name.upper()
        self.health = int(health)
        self.power = int(power)
        self.speed = int(speed) #out of 10
        self.stats = {'health': health, 'power': power, 'speed': speed}
        self.alive = True   
        
class Fighter(Creature):
    def __init__(self,name,health,power,speed):
        # preset health of every user
        Creature.__init__(self,name,health,power,speed)        
        # weapon is object       
        self.start_heath = self.health        
        weapon = self.chooseWeapon(WEAPONS)
        inventory = {}
	inventory["WEAPON: " + weapon.name.upper()] = "--> Hitpoints: " + str(weapon.hitpoints) + " Tries: " + str(float(weapon.tries))
	self.weapon = weapon
	self.inventory = inventory
	
    def __str__(self):
        return "NAME: " + self.name + " WEAPON:" + str(self.weapon)
    def chooseWeapon(self,weapons):
        """
        Return object WEAPON, chosen by user
        1. Ask user to choose WEAPON
        2. Tell user what WEAPON they chose
        3. Get HITPOINTS, TRIES for WEAPON from .txt file
        4. Pass WEAPON object into user's FIGHTER class
        """
        while(True):
            weapon_choices = weapons.keys()
            try:
                ans = quickPrint("Choose your weapon, " + self.name + ": " + str(weapon_choices) + "--> ",1)
                if ans in weapons.keys():
                    quickPrint("You have chosen the " + ans.upper() + ". A valiant choice, warrior.")
                    break
                elif ans == 'NONE':
                    quickPrint("I see...you are indeed one of the bravest. Then you shall proceed with HAND-TO-HAND combat as your weapon of choice.")
                else:
                    quickPrint("Alas, that is not one of the weapons you may wield.")
            except:
                quickPrint("That is no weapon, fool. Try again...on your life.")
        if ans == 'NONE':
            weapon_stats = [1,1]
            hitpoints = weapon_stats[0];
            tries = weapon_stats[1];
            return Weapon('HAND-TO-HAND',hitpoints,tries)
        else:
            weapon_stats = WEAPONS[ans]
            hitpoints = weapon_stats[0];
            tries = weapon_stats[1];
            return Weapon(ans,hitpoints,tries)
    def attack(self, opponent, WEAPONS):
        """
        Takes in:
            opponent CREATURE object
            WEAPONS dictionary - weapon: weapon_power
        Reduces HEALTH attribute with prob based on rand element
        Returns loot on CREATURE, doesn't remove loot
        """
        attack_power = self.power
        opponent_health = opponent.health
        weaponName = self.weapon.name
        hit = attack_power + WEAPONS[weaponName][0]
        tries = 0
        while(tries < WEAPONS[weaponName][1]):
            probability = random.random()
            quickPrint("You attack the " + str(opponent.name) + ".")
            if probability < 0.7:
                opponent_health -= hit
                # if opponent still alive, change opponents health
                if opponent_health > 0:
                    quickPrint("A direct hit! The " + str(opponent.name) + " now has health " + str(opponent_health) + ".")
                    opponent.health = opponent_health
                else:
                    quickPrint("A fatal blow! You have killed the " + str(opponent.name) + ".")
                    opponent.health = 0
                    opponent.alive = False
                    break
            else:
                quickPrint("You missed! Your aim must be true, warrior - lest you die!")
            tries += 1
    def flee(self,monster):
        """
        Take in:
            Current HEALTH, START_HEALTH
            MONSTER (speed used)            
            some random element 
        1. Determine likelihood of escape
            Larger percentage of start health -> better chance of escape
        2. Return True or False for escape chance
        """    
        health_prcnt = self.health/(self.start_health)
        speed_prcnt = (self.speed - monster.speed)/10
        probability = random.random()
        chance = (health_prcnt + probability + speed_prcnt)/3        
        if chance > 0.3:
            return True
        else:
            return False
    def checkInventory(self):
        check_inven = ''
        while(check_inven != 'no' and check_inven != 'yes'):
                check_inven = quickPrint("Would you like to check your inventory? (yes/no): ",1)
                if check_inven == 'yes':
                    if self.inventory == {}:
                         quickPrint("You carry only your will and your wits about you. Your INVENTORY is empty.")
                    else:
                        print("INVENTORY:")
			print "Loot\t\t\t\tAmount"
                    	for item in self.inventory:
                        	quickPrint("  " + item + "\t" + str(self.inventory[item]))
                    	quickPrint("Use your items wisely. Now, continue on your quest!")
                elif check_inven == 'no':
                    quickPrint("Then you shall continue on...")
                    break
                else:
                    quickPrint("You fool! A real warrior must follow directions.")
        return True
    def pickUpLoot(self,monster):
        """
        1. Uses Monster.getLoot() to get loot dict.
        2. Ask fighter to choose loot items to pick up (none if necessary)
        3. Adds loot items to fighter's inventory.
        4. returns new modified fighter inventory
        """        
        quickPrint("Available Loot: ")
        monster_loot_dict = monster.getLoot()
        valid_loot_names = monster_loot_dict.keys()
        loot_vals = monster_loot_dict.values()
        print "Loot\t\t\t\t\tAmount"
        count = 1        
        # PRINT OUT AMOUNT OF LOOT AT TABBED SPACE BASED ON LENGTH OF MONSTER NAME
        for name in valid_loot_names:
            quickPrint(str(count) + '. ' + name + "\t\t\t\t" + str(loot_vals[count-1]))
            count += 1
        # ask user for loot preference
        ans = quickPrint("Which of the items would you like to pick up? (Enter loot items separated by commas (',') "
			 "or 'NONE' if you don't want any loot or 'ALL' if you want all loot): ",1)
        user_loot = self.inventory
	inventory_filled = False
	while ans != 'none':
	    # check if user is putting in wrong loot            
            if ans != 'all':
	    	mod_ans = ans.strip()
            	mod_ans = mod_ans.split(',')
	    		
		# Validates loot names before adding to inventory
		valid_loot = True
		invalid_inds = []
		for loot in mod_ans:
			print("Validating  "+loot.strip()+" of "+str(len(mod_ans))+ " items...")
	                if loot not in valid_loot_names:
               			valid_loot = False
				current_ind = mod_ans.index(loot)
				invalid_inds.append(current_ind)
			# Removes whitespace in loot names
			loot = loot.strip()
			mod_ans[current_ind] = loot

		# Adds valid loot names to inventory
		if valid_loot:
			print("Preparing  "+loot+"...")
		    	# modify user's inventory and return dict
		   	print("Modifying user's inventory: ") 	
                    	if loot in user_loot.keys():
                        	user_loot[loot] += monster_loot_dict[loot]
				quickPrint("You have picked up extra " + str(loot).upper())
                    	# else, add monster.loot key-val pairs to user.loot dict
                    	else:
                    	   	user_loot[loot] = monster_loot_dict[loot]  
		    		quickPrint('You have picked up ' + str(loot).upper())          
			inventory_filled = True 
		else:
			invalid_loot = ""
			count = 0
			for ind in invalid_inds:
				invalid_loot = invalid_loot + str(mod_ans[ind]) + ", "
				count += 1
			invalid_loot = invalid_loot[0:len(invalid_loot)-2]
			if count != 1:
				interject = "are"
			else:	
				interject = "is"
			ans = quickPrint("You fool! " + invalid_loot.upper() + " " + interject + " not available for pickup! "
					 "(Enter loot items separated by commas (',') or 'NONE' if you don't want any loot): ",1)
	    elif ans == "all":
		for loot in monster_loot_dict.keys():
			if loot in user_loot.keys():
				user_loot[loot] += monster_loot_dict[loot]
				quickPrint("You have picked up extra " + str(loot).upper())	
			else:
				user_loot[loot] = monster_loot_dict[loot]
				quickPrint("You have picked up " + str(loot).upper())
		inventory_filled = True
	    else:
		ans = quickPrint("You imbecile! A true warrior follows directions...",1)
  	    
	    if inventory_filled:
	    	# updates user's inventor, returns inventory dict	
	    	self.inventory = user_loot
   	    	return self.inventory
 
        # user decides against any loot, return current inventory
        quickPrint("You leave the loot to rot. Hopefully, you already possess what you will need...")
        return self.inventory
    
    def tameMonster(monster):
        """
        Allows Fighter to capture weak Monster and make it a companion
	- Adds monster to INVENTORY
	- Changes monster class instance to make WEAPON (of sorts)
        """
        pass
    def fuseItems(monster,weapon):
        """
        Allows Fighter to fuse Monster and weapon
        - certain chance of success/failure, based on stats
        - can only fuse certain monsters and weapons - no knowledge of which combos work
        """
        pass
# end of Fighter class
  
#create weapon class
class Weapon(object):
    def __init__(self,name,hitpoints,tries):
        self.name = name.lower()
        self.hitpoints = float(hitpoints)
        self.tries = int(tries)
    def __str__(self):
        """
        Display the name of the WEAPON
        """
        return self.name

class Monster(Creature):
    def __init__(self,name,health,power,speed,loot):
        Creature.__init__(self,name,health,power,speed)
        meat_loot = ['monster meat']
        meat_loot.extend(loot)        
        self.loot = meat_loot
    def __str__(self):
        return self.name
    def attack(self, opponent, WEAPONS):
        """
        Takes in:
            opponent CREATURE object
            WEAPONS dictionary - weapon: weapon_power
        Reduces HEALTH attribute stochastically (with prob based on rand element)
        """
        attack_power = self.power
        opponent_health = opponent.health
        opponent_health -= attack_power
        # if opponent still alive, change opponents health
        if opponent_health > 0:
            opponent.health = opponent_health
            quickPrint("The " + self.name + " attacks you! Your health is now " + str(opponent_health) + ".")
        # otherwise, kill opponent
        else:
            opponent.health = 0
            opponent.alive = False
            quickPrint("The " + self.name + " kills you!")
    def getLoot(self):
        """
        returns loot dictionary based on self.loot
        AMOUNT and RARITY of loot based on health of MONSTER
        varies within and between monster species
        generated after each monster dies
        loot dictionary = {NAME: # PIECES of loot}
        """        
        loot_names = self.loot        
        loot_dict = {}        
        if self.health < 30:
            loot_dict[loot_names[0]] = 3
        else:
            loot_dict[loot_names[0]] = 5
        for ind in range(1,len(loot_names)):
            loot_dict[loot_names[ind]] = 1
        return loot_dict

class Fusion(Creature):
    """
    Fusion is combination of two classes:
        1. Monster subclass
        2. Weapon subclass
    Fusion has all characteristics of Monster and Weapon
    Fusion has combine stats, and new properties
    """
    def __init__(self,monster,weapon,speed,loot):
        fuseStats(monster,weapon)
        self.monster = monster #Monster class
        self.weapon = weapon #Weapon object
        Creature.__init__(self,name,health,power,speed,loot)
    def fuseStats(monster,weapon):
        name = monster.name + "-" + weapon.name
        self.name = name
        self.health = monster.health + weapon.tries
        self.power = monster.power + weapon.hitpoints
                
#-------initialize monster fight game
def readNarrative(lines):
	"""
	Read array of narrative lines
	Print out to dislplay using (mod?)  quickPrint()

	lines: array of strings to read dynamically
	e.g.	(...) > wait for 3 Sec
		! ! ! > wait for 1 Sec
		etc. ...
	"""
	pass

def playGame():
    # include self healing factor (based on time)
    # add items to inventory, include other WEAPONS
    # allow for wandering of user
    # base monster population on a growth/decay model

    quickPrint("Welcome to the game of Monster Fight!")
    quickPrint("To take on such a challenge...")
    name = quickPrint("You must be a brave warrior. What is your name, warrior? ",1)
    quickPrint(name.upper() + "? ...A fool's name. But you will fight to give it worth.")    
    user = Fighter(name.upper(),1000,30,3) #name,health,power,speed
    while(user.alive):
        monsterList = getMonsterList('monsters.txt')
        monster = getRandMonster(monsterList)
        quickPrint("Look, over yonder! A monster approaches...you must fight!")
        quickPrint("Your health is currently " + str(user.health) + ".")
        quickPrint("The monster is a " + monster.name + " with health " + str(monster.health) + ".")
        # monster attacks user, user fights back        
        while(monster.alive):
            if user.alive:
                monster.attack(user, WEAPONS)
                if user.alive:
                    user.attack(monster, WEAPONS)
                else:
                    quickPrint("You are dead! The world of Monster Fight was too much for your weak soul. GAME OVER.")
                    break
            else:
                quickPrint("You are dead! The world of Monster Fight was too much for your weak soul. GAME OVER.")
                break
        # user has won, give user option to pick up loot
        if user.alive:
            choice = quickPrint("Do you want to inspect the loot? (yes/no): ",1)
            if choice == "yes":
                # update pickUpLoot function, modify inventory from within function                
                user.pickUpLoot(monster)
            else:
                quickPrint("You leave the loot to rot.")
            ans = quickPrint("Would you like to leave Monster Fight? (yes/no): ",1)
        else:
            ans = ''
        # find out if user still wants to play
        while(user.alive and (ans != 'no' or ans != 'yes')):        
            if ans == 'no':
                quickPrint("Then you shall continue on your quest of bravery!")
                user.checkInventory()
                break
            elif ans == 'yes':
                quickPrint("Yes? Well then...it seems the world of Monster Fight was too much for your weak soul.")
                quickPrint("But...you live to fight another day.")
                user.alive = False
                break
            else:
                quickPrint("You imbecile! A true warrior follows directions!")
                ans = quickPrint("Would you like to leave Monster Fight? (yes/no): ",1)                
playGame()
