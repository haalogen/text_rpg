# -*- coding: utf-8 -*-
from sys import exit
from random import randint, random
import os
import time



class Player(object):
    def __init__(self):
        while True:
            print "Please, choose your hero's name: "
            self.name = raw_input('> ')
            print "You choose %r. Are you sure? (y/n)" % self.name
            answer = raw_input('> ')
            print
            if answer in ['y', 'yes', 'Y', 'YES']:
                print "Live long and prosper, %s !" % self.name
                break
        
        self.health = 100
        self.strength = 10
        self.agility = 0.2
        
        self.weapon = None
        self.shield = None
        self.armor = None
        self.potionCount = 0
        self.money = 5
        
        self.level = 1
        self.maxHealth = 100
        self.experience = 0
        self.maxExperience = 100
        
        self.blocking = False
        
        # for debug purposes ;)
        if self.name == 'debug':
            print "~~~Debug mode~~~"
            self.money = 500
    
    
    
    def info(self):
        print """
=== Player's info: ===

Name:   %s
Level:  %r      Exp: %r / %r

== Stats ==
* health   -- %r / %r
* strength -- %r
* agility  -- %r

== Items ==
* weapon -- %r
* shield -- %r
* armor  -- %r

* health potions -- %r

* money: %r $
        """ % (self.name, self.level, 
               self.experience, self.maxExperience,
               self.health, self.maxHealth, 
               self.strength, self.agility,
               self.weapon, self.shield, self.armor,
               self.potionCount, self.money)




class Enemy(object):
    def __init__(self, enemyType):
        self.enemyType = enemyType
        
        
        if self.enemyType == 'sand-crab':
            # init sand crab
            self.health = 30
            self.strength = 10
            self.agility = 0.1
        
        elif self.enemyType == 'demon':
            # init demon
            self.health = 100
            self.strength = 30
            self.agility = 0.2
        
        elif self.enemyType == 'dragon':
            # init dragon
            self.health = 400
            self.strength = 60
            self.agility = 0.3
        
        elif self.enemyType == 'giant-cucumber':
            # init giant cucumber (boss)
            self.health = 2000
            self.strength = 200
            self.agility = 0.4
        
        
        tmp = self.health
        self.money = randint(tmp / 5, tmp / 2)




class Scene(object):
    def __init__(self):
        self.sceneName = 'scene'
    
    
    def enter(self):
        print "This scene is not yet configured.",
#        exit(1)       
    
    
    def print_map(self):
        print """
Choose where to go next:

1 - Shop
2 - Beach
3 - Coal mine
4 - Volcano crater
5 - Boss Dungeon
6 - Home
        """
    
    
    def buy(self):
        prices = self.prices
        
        print """
What do you want to buy?

1 - health potion [restores  80 hp]         -- %r $
2 - steel sword   ( + 100%% strength )       -- %r $
3 - wooden shield ( + 100%% agility  )       -- %r $
4 - leather armor ( +  70%% health   )       -- %r $

You have %r $
        """ % (prices['1'], prices['2'], prices['3'], prices['4'],
                player.money)
        
        
        what = raw_input('> ')
        
        if what in ['1', '2', '3', '4']:
            
            print "How many do you want to buy?"
            
            try:
                num = int( raw_input('> ') )
                
                if num > 0:
                    price = prices[what]
                    
                    
                    if player.money >= num * price:
                        
                        if what == '1':
                            player.potionCount += num
                        
                        elif what == '2' and player.weapon == None:
                            player.weapon = 'steel sword'
                            player.strength *= 2
                        
                        elif what == '3' and player.shield == None:
                            player.shield = 'wooden shield'
                            player.agility *= 2
                        
                        elif what == '4' and player.armor == None: 
                            player.armor = 'leather armor'
                            player.maxHealth = \
                                        int(1.7 * player.maxHealth)
                        
                        else: 
                            print "You can't buy 2nd sword"+\
                                                "/shield/armor!"    
                            return # !!! 
                        
                        
                        player.money -= num * price
                        
                        print "You have bought %r %r!" \
                                        % (num, self.itemNames[what])
                        
                    else:
                        print "Money don't grow on trees, man!",
                        print " Go earn some!"
                    
            except ValueError:
                print "Enter a valid number, you little bitch!"
        
        else:
            print "Command not recognized."
            print "Where will I find \'" + what + "\' ?"
    
    
    
    
    def handle_actions(self, availableCmds):
        
        next_scene = None
        while next_scene == None:
            
            command = raw_input('> ')
            
            if command == 'buy':
                # buy smth
                self.buy()
            
            elif command == 'info':
                # show player info
                player.info()
            
            elif command == 'map':
                next_scene = self.move_next()
                return next_scene
            
            elif command == 'fight':
                # fight enemy
                self.fight()
                
                if player.health > 0:
                    next_scene = self.sceneName
                
                else:
                    next_scene = 'death'
                
                return next_scene
            
            else:
                print "Command not recognized. \n"
                print "Available commands: ", availableCmds
            
    
    
    
    def fight(self):
        enemyTypes = {'beach'           : 'sand-crab',
                      'coal_mine'       : 'demon',
                      'volcano_crater'  : 'dragon',
                      'boss_dungeon'    : 'giant-cucumber'}
        
        cooldowns = {'punch' : 1,
                     'kick'  : 2,
                     'swing' : 3,
                     'slash' : 4,
                     'block' : 0}
        
        currentCooldowns = {'punch' : 0,
                            'kick'  : 0,
                            'swing' : 0,
                            'slash' : 0,
                            'block' : 0}
        
        damage = {'punch' : 0.5 * player.strength,
                  'kick'  : 1.0 * player.strength,
                  'swing' : 2.0 * player.strength,
                  'slash' : 3.0 * player.strength}
        
        enemy = Enemy(enemyTypes[self.sceneName])
        
        log = ""
        
        while player.health > 0 and enemy.health > 0:
            
            if os.name == 'nt': # windows
                os.system('cls')
            
            else:
                os.system('clear')
            
            
            print """
===Fight===

Player: %20r            Enemy: %20r
HP:     %4r / %4r                     HP: %5r

==Available actions==

1 - punch       | cooldown  %r 
2 -  kick       | cooldown  %r    
3 - swing       | cooldown  %r
4 - slash       | cooldown  %r
5 - block       | cooldown  %r
6 - potion(%r)

==Log==

%s
            """ %  (player.name, enemyTypes[self.sceneName],
                player.health, player.maxHealth, enemy.health,
                currentCooldowns['punch'], currentCooldowns['kick'],
                currentCooldowns['swing'], currentCooldowns['slash'],
                currentCooldowns['block'], player.potionCount, log) 
            
            
            action = raw_input('> ')
            
            timeStr = time.asctime()
            
            enemyEvades = ( random() < enemy.agility )
            
            player.blocking = False
            
            dmg = 0
            
            if action == '1':
                #punch
                if currentCooldowns['punch'] == 0:
                    
                    if not enemyEvades:
                        dmg = damage['punch']
                    
                    
                    log += timeStr + " Punch! (Enemy HP: - %r)\n" \
                                        % dmg
                    
                    # inflict damage to enemy
                    enemy.health -= dmg
                    
                    # setup cooldown for action
                    currentCooldowns['punch'] = cooldowns['punch']
            
                else:
                    print "Action's on cooldown!"
                    time.sleep(1)
                    continue
                
            
            elif action == '2':
                #kick
                if currentCooldowns['kick'] == 0:
                    
                    if not enemyEvades:
                        dmg = damage['kick']
                    
                    log += timeStr + " Kick! (Enemy HP: - %r)\n" \
                                        % dmg
                    
                    # inflict damage to enemy
                    enemy.health -= dmg
                    
                    # setup cooldown for action
                    currentCooldowns['kick'] = cooldowns['kick']
                    
                else:
                    print "Action's on cooldown!"
                    time.sleep(1)
                    continue
                
            
            elif action == '3':
                #swing sword
                if player.weapon and currentCooldowns['swing'] == 0:
                    
                    if not enemyEvades:
                        dmg = damage['swing']
                    
                    
                    log += timeStr + " Swing! (Enemy HP: - %r)\n" \
                                        % dmg
                    
                    # inflict damage to enemy
                    enemy.health -= dmg
                    
                    # setup cooldown for action
                    currentCooldowns['swing'] = cooldowns['swing']
                    
                
                elif not player.weapon: # weapon == None
                    print "You need a sword to do this!"
                    time.sleep(1)
                    continue
                
                elif currentCooldowns['swing'] != 0:
                    print "Action's on cooldown!"
                    time.sleep(1)
                    continue
                
            
            elif action == '4':
                #slash sword
                if player.weapon and currentCooldowns['slash'] == 0:
                    
                    if not enemyEvades:
                        dmg = damage['slash']
                    
                    
                    log += timeStr + " Slash! (Enemy HP: - %r)\n" \
                                        % dmg
                    
                    # inflict damage to enemy
                    enemy.health -= dmg
                    
                    # setup cooldown for action
                    currentCooldowns['slash'] = cooldowns['slash']
                    
                
                elif not player.weapon:
                    print "You need a sword to do this!"
                    time.sleep(1)
                    continue
                
                elif currentCooldowns['slash'] != 0:
                    print "Action's on cooldown!"
                    time.sleep(1)
                    continue
                
            
            elif action == '5':
                #block
                if currentCooldowns['block'] == 0:
                    
                    log += timeStr + " Block! (Player agility x2)\n"
                    
                    # setup player's "blocking" state
                    player.blocking = True
                    
                    # setup cooldown for action
                    currentCooldowns['block'] = cooldowns['block']
                
            
            elif action == '6':
                #potion
                if player.potionCount > 0:
                    
                    log += timeStr + " Potion(-1). Player(+80 HP).\n"
                    
                    # Player's HP+80;
                    if player.health + 80 > player.maxHealth:
                        player.health = player.maxHealth
                    
                    else:
                        player.health += 80
                    
                    player.potionCount -= 1
                    continue
                
                else:
                    print "No potions!"
                    time.sleep(1)
                    continue
                
            
            else:
                print "UNKNOWN ACTION %r !!!" % action
                time.sleep(1)
                continue
            
            
            # enemy's attack starts here
            agi = player.agility
            
            if player.blocking:
                agi *= 2
            
            dmg = 0
            
            if random() > agi:
                dmg = enemy.strength
            
            log += timeStr + "\t Attack! (Player HP: - %r) \n" % dmg
            
            player.health -= dmg
            
            # decrementing cooldowns
            for action in ['punch', 'kick', 'swing', 'slash']:
                
                if currentCooldowns[action] > 0:
                    currentCooldowns[action] -= 1
                
        
        # the last fight view (after the fight is over)    
        if os.name == 'nt': # windows
            os.system('cls')
        
        else:
            os.system('clear')
        
        
        print """===Fight===

Player: %20r            Enemy: %20r
HP:     %4r / %4r                     HP: %5r

==Available actions==

1 - punch       | cooldown  %r 
2 -  kick       | cooldown  %r    
3 - swing       | cooldown  %r
4 - slash       | cooldown  %r
5 - block       | cooldown  %r
6 - potion(%r)

==Log==

%s      """ %  (player.name, enemyTypes[self.sceneName],
                player.health, player.maxHealth, enemy.health,
                currentCooldowns['punch'], currentCooldowns['kick'],
                currentCooldowns['swing'], currentCooldowns['slash'],
                currentCooldowns['block'], player.potionCount, log) 
        
        
        if player.health > 0: # player won
            # get exp
            exp = 2 * enemy.strength
            
            print "You've got %r exp!" % exp
            
            player.experience += exp
            
            if player.experience > player.maxExperience:
                
                print "<<< Level up! >>>"
                
                player.level += 1
                player.maxExperience *= 2
                player.maxHealth *= 2
                player.strength *= 2
            
            
            # take loot
            print "You have looted %r $ !" % enemy.money
            player.money += enemy.money
            print "You now have: %r $" % player.money
    
    
    
    def move_next(self):
        forever = True
        
        while forever:
            self.print_map()
            
            command = raw_input("> ")
            print 
            
            # check chosen way
            way = command
            if way == '1':
                # go to the shop
                print 'Gonna spend some cash... $)'
                return 'shop'
            
            elif way == '2':
                # go to the beach
                print "It's time for the beach, bitches!"
                return 'beach'
            
            elif way == '3':
                # go to the coal mine
                print "Gonna check out what's going on down there..."
                return 'coal_mine'
            
            elif way == '4':
                # go to the volcano crater
                print "I was always fond of extreme traveling..."
                return 'volcano_crater'
            
            elif way == '5':
                # go to the boss dungeon
                print "What do these huge gates hide? I wonder..."
                return 'boss_dungeon'
            
            elif way == '6':
                # go home
                print 'Walking home...'
                return 'home'
            
            else:
                print "Command not recognized."
                print "What is \'" + command + "\' ?"




class Death(Scene):
    def __init__(self):
        self.sceneName = 'death'
    
    quips = [
"Then wild animals raped your body.",
"A flock of beautiful butterflies layed eggs in your eyes.",
"Your body became a life-saving meal for a family of rats.",
"A rattlesnake took a shelter in your anus.",
"A bear took a shit upon your face."
            ]
    
    
    
    def enter(self):
        print "You died."
        print Death.quips[ randint(0, len(Death.quips) - 1) ]
        
        raw_input("Press Enter to try again.")
        
        return 'home'




class Shop(Scene):
    def __init__(self):
        self.sceneName = 'shop'
        
        self.prices = {'1' : 10,      # potion
                       '2' : 100,     # sword
                       '3' : 50,     # shield
                       '4' : 70}     # armor
        self.itemNames = {'1' : 'health potion(s)',  # potion
                          '2' : 'steel sword',       # sword
                          '3' : 'wooden shield',     # shield
                          '4' : 'leather armor'}     # armor
        
        self.availableCmds = ['buy', 'map', 'info']
    
    def enter(self):
        prices = self.prices
        
        print """
The shop looks pretty neat and friendly.
The coolest shit could be bought here:

* health potion (restores  80 hp ) -- %r $
* steel sword   (+ 100 %% strength) -- %r $
* wooden shield (+ 100 %% agility ) -- %r $
* leather armor (+  70 %% health  ) -- %r $

You have: %r $ 
        """ % (prices['1'], prices['2'], prices['3'], prices['4'],
                player.money)
        
        
        next_scene = self.handle_actions(self.availableCmds)
        return next_scene




class Beach(Scene):
    def __init__(self):
        self.sceneName = 'beach'
    
    def enter(self):
        print "Beach"
        
        availableCmds = ['map', 'info', 'fight']
        
        next_scene = self.handle_actions(availableCmds)
        return next_scene




class CoalMine(Scene):
    def __init__(self):
        self.sceneName = 'coal_mine'
    
    def enter(self):
        print "CoalMine"
        
        availableCmds = ['map', 'info', 'fight']
        
        next_scene = self.handle_actions(availableCmds)
        return next_scene




class VolcanoCrater(Scene):
    def __init__(self):
        self.sceneName = 'volcano_crater'
    
    def enter(self):
        print "VolcanoCrater"
        
        availableCmds = ['map', 'info', 'fight']
        
        next_scene = self.handle_actions(availableCmds)
        return next_scene




class Home(Scene):

    def enter(self):
        print """
You are at home. 
A great place to rest from battles and save your progress.
        """
        #restore HP
        player.health = player.maxHealth
        
        # save game
        # if game was saved successfully
        # print "Game was saved."
        
        availableCmds = ['map', 'info']
        
        next_scene = self.handle_actions(availableCmds)
        return next_scene




class BossDungeon(Scene):
    def __init__(self):
        self.sceneName = 'boss_dungeon'
    
    def enter(self):
        print "BossDungeon"
        
        availableCmds = ['map', 'info', 'fight']
        
        next_scene = self.handle_actions(availableCmds)
        
        if next_scene != 'death':
            next_scene = 'finished'
         
        return next_scene




class Finished(Scene):
    def enter(self):
        print """
CONGLATURATIONS!
YOU HAVE WON IN THE BEST RPG EVER.
        """
        
        raw_input("Press enter to exit.")




class Map(object):
    
    scenes = {
        'death'          : Death(),
        'shop'           : Shop(),
        'beach'          : Beach(),
        'coal_mine'      : CoalMine(),
        'volcano_crater' : VolcanoCrater(),
        'home'           : Home(),
        'boss_dungeon'   : BossDungeon(),
        'finished'       : Finished(),
    }
    def __init__(self, start_scene):
        self.start_scene = start_scene




class Engine(object):
    
    def __init__(self, scene_map):
            self.scene_map = scene_map
    
    
    def play(self):
        current_scene = self.scene_map.start_scene
        
        while not current_scene == 'finished':
            
            # playing scenes
            if current_scene in self.scene_map.scenes:
                
                scene_map = self.scene_map
                
                next_scene_object = scene_map.scenes[current_scene]
                
                next_scene = next_scene_object.enter()
                
                current_scene = next_scene
            
            else:
                print "There is no such scene."
            
        # be sure to show final scene
        self.scene_map.scenes[current_scene].enter()



player = Player()
a_map = Map('home')
a_game = Engine(a_map)
a_game.play()


