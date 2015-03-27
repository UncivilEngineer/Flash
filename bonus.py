########################
##Bonus game mode for FLASH
########################

import procgame.game 
from procgame import * 
import pinproc  
import random 
import time 
import sys 
import locale
from player import *
import logging

class BonusGameMode(game.Mode): 
    
    ###Global variables
    rollOverStatus1 = False
    rollOverStatus2 = False
    rollOverStatus3 = False
    rollOverStatus4 = False
    rollOverValue = 0
    
    def __init__(self, game, priority):  
        super(BonusGameMode, self).__init__(game, priority)

        #######set up logging#######
        self.log = logging.getLogger('flash.bonusgamemode')	
        self.log.info("Bonus Game initialized")

    def mode_started(self):
        logging.info("bonus game mode started")
        self.bonusReset()

    def bonusReset(self):
        self.log.info("bonus values reset")
        self.game.utilities.set_player_stats('bonus', 0, 'set')
        self.game.utilities.set_player_stats('bonus_x', 1, 'set')
        self.game.utilities.set_player_stats('rollOverValue', 0, 'set')
        self.rollOverStatus1 = False        
        self.rollOverStatus2 = False
        self.rollOverStatus3 = False
        self.rollOverStatus4 = False
        self.rollOverValue = 0
        

###################################################
### bonus light updating function #################
###################################################
        
    def update_bonus_lights_basic(self):
        bonusValue = self.game.utilities.get_player_stats('bonus')
        bonusX = self.game.utilities.get_player_stats('bonus_x')
        self.update_bonus_lights(bonusValue, bonusX)

    def update_bonus_lights(self, bonusValue, bonusMult):

    ###################################################
    ### This method can be called without arguments
    ### and it will default to the players bonus value.
    ### otherwise, you can specify a value to light up
    ###################################################

       # self.log.info('bonus lights update called')

    ###################################################
    ### I put the bonus light in the circle in a list
    ### in order to make them easier to cycle on
    ###################################################

        bonuslights = [ self.game.lamps.bonus1000,
                        self.game.lamps.bonus2000, 
                        self.game.lamps.bonus3000, 
                        self.game.lamps.bonus4000, 
                        self.game.lamps.bonus5000, 
                        self.game.lamps.bonus6000, 
                        self.game.lamps.bonus7000, 
                        self.game.lamps.bonus8000, 
                        self.game.lamps.bonus9000,
                        self.game.lamps.bonus10000 ]

    ####################################
    ### first thing, turn off bonus lights
    ####################################

        self.game.lamps.x2.disable()
        self.game.lamps.x3.disable()
        self.game.lamps.bonus20000.disable()
        for lamps in bonuslights:
            lamps.disable()

    ####################################
    ### now start turning things on again
    ####################################

    ######multiplier lights handler####


        if bonusMult >= 4:
            self.game.lamps.x2.schedule(schedule=0xff00ff00ff, cycle_seconds=0, now=False)
            self.game.lamps.x3.disable()
        elif bonusMult == 3:
            self.game.lamps.x3.enable()
            self.game.lamps.x2.disable()
        elif bonusMult == 2:
            self.game.lamps.x3.disable()
            self.game.lamps.x2.enable()
        else:
            self.game.lamps.x3.disable()
            self.game.lamps.x2.disable()

    ######bonus counter lamps##########

        ##### if the bonus is over 40K, blink all bonus lights
        ##### otherwise we set the 10k and 20k light, and then 
        ##### use lampcounter variable to turn on the cirlce lights
       
        if bonusValue >= 40000:
            for lamps in bonuslights:
                lamps.schedule(schedule = 0xff00ff00ff, cycle_seconds=0, now=true)

            self.game.lamps.bonus20000(schedule = 0xff00ff00ff, cycle_seconds=0, now=true)

        elif bonusValue >= 30000 and bonusValue < 40000:
            self.game.lamps.bonus10000.enable()
            self.game.lamps.bonus20000.enable()
            lampcounter = (bonusValue / 1000) - 30

        elif bonusValue >= 20000 and bonusValue < 30000:
            self.game.lamps.bonus10000.disable()
            self.game.lamps.bonus20000.enable()
            lampcounter = (bonusValue / 1000) - 20

        elif bonusValue >= 10000 and bonusValue < 20000:
            self.game.lamps.bonus10000.enable()
            self.game.lamps.bonus20000.disable()
            lampcounter = (bonusValue / 1000) - 10

        elif bonusValue < 10000:
            self.game.lamps.bonus10000.disable()
            self.game.lamps.bonus20000.disable()
            lampcounter = (bonusValue / 1000)

    ### this should light up the circle of bonus values
   
        for x in range(0, lampcounter):    
            bonuslights[x].enable()


######################################################
### Award bonus section ##############################
######################################################

    def award_bonus(self):
        self.log.info("Bonus award reached")
    
    ### we have to hold these value now, because the stats
    ### are used to update the lights

        bonusValue = self.game.utilities.get_player_stats('bonus')
        bonusMult  = self.game.utilities.get_player_stats('bonus_x')
        playerScore = self.game.utilities.currentPlayerScore()
        bonusList = [0,0]


         #### for each bonus mulitiplier, it counts down
        for x in range(bonusMult, 0, -1):
            bonusList[0] = x

            for y in range(bonusValue, 0, -100):
                bonusList[1] = y
                self.game.utilities.score(100)
                 ##### it should call for display update here
                #self.game.bonus.update_bonus_lights(bonusValue, bonusMult)
                self.delay("bonus", delay=.25, handler = self.bonusloop, param= bonusList)
        
        self.game.bonus.bonusReset()
        self.game.bonus.update_bonus_lights_basic()
    
    def bonusloop(self, bonusList):
        self.game.bonus.update_bonus_lights(bonusList[1], bonusList[0])
        self.log.info("bonsu light delay called")
        
            

########################################################
### Roll Over Advance X check ##########################
########################################################

    def checkRollOver(self):
        self.log.info('roll over check called')
        if self.rollOverValue == 4:
            self.game.utilities.set_player_stats('bonus_x', 1, 'add')
            self.game.lamps.rollOver1.schedule(schedule = 0xff00ff00ff, cycle_seconds=2, now=True)
            self.game.lamps.rollOver2.schedule(schedule = 0xff00ff00ff, cycle_seconds=2, now=True)
            self.game.lamps.rollOver3.schedule(schedule = 0xff00ff00ff, cycle_seconds=2, now=True)
            self.game.lamps.rollOver4.schedule(schedule = 0xff00ff00ff, cycle_seconds=2, now=True)
            self.rollOverValue = 0
            self.rollOverStatus1 = False
            self.rollOverStatus2 = False
            self.rollOverStatus3 = False
            self.rollOverStatus4 = False
        else:
            pass

########################################################
#### Bonus switch handlers #############################
########################################################

    def sw_rightFRLane_active_for_10ms(self, sw):
        self.game.utilities.score(1000)
        self.game.utilities.set_player_stats('bonus', 1000, 'add')
        self.update_bonus_lights_basic()

    def sw_leftFRLane_active_for_10ms(self, sw):
        self.game.utilities.score(1000)
        self.game.utilities.set_player_stats('bonus', 1000, 'add')
        self.update_bonus_lights_basic()

#########################################################
### Bonus roll over handlers  ###########################
#########################################################


    def sw_rollover1_active_for_10ms(self, sw):
        if self.rollOverStatus1 == False:
            self.rollOverValue = self.rollOverValue + 1
            self.game.lamps.rollOver1.enable()
            self.rollOverStatus1 = True
            self.checkRollOver()
        else:
            self.game.utilities.score(1000)
        
        self.game.utilities.set_player_stats('bonus', 1000, 'add')
        self.update_bonus_lights_basic()


            
    def sw_rollover2_active_for_10ms(self, sw):
        if self.rollOverStatus2 == False:
            self.rollOverValue = self.rollOverValue + 1
            self.game.lamps.rollOver2.enable()
            self.rollOverStatus2 = True
            self.checkRollOver()
        else:
            self.game.utilities.score(2000) 

        self.game.utilities.set_player_stats('bonus', 1000, 'add')
        self.update_bonus_lights_basic()           
        

    def sw_rollover3_active_for_10ms(self, sw):
        if self.rollOverStatus3 == False:
            self.rollOverValue = self.rollOverValue + 1
            self.game.lamps.rollOver3.enable()
            self.rollOverStatus3 = True
            self.checkRollOver()
        else:
            self.game.utilities.score(3000)
 
        self.game.utilities.set_player_stats('bonus', 1000, 'add')
        self.update_bonus_lights_basic()


    def sw_rollover4_active_for_10ms(self, sw):
        if self.rollOverStatus4 == False:
            self.rollOverValue = self.rollOverValue + 1
            self.game.lamps.rollOver4.enable()
            self.rollOverStatus4 = True
            self.checkRollOver()
        else:
            self.game.utilities.score(4000) 
         
        self.game.utilities.set_player_stats('bonus', 1000, 'add')
        self.update_bonus_lights_basic()