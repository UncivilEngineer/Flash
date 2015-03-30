########################
##Drop Targets game mode for FLASH
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
from flash import *

class DropTargetMode(game.Mode):
    
    bank5index = 0
    bank5lights = []
    bank5hold = False
    
    bank3index = 0
    bank3lights=[]
    bank3hold = False
    
    
    def __init__(self, game, priority):  
            super(DropTargetMode, self).__init__(game, priority)
    
            #######set up logging#######
            self.log = logging.getLogger('flash.droptargetmode')	
            self.log.info("Drop Targets initialized")
            
            ## set up the light list for bank 5
            self.bank5lights.append(self.game.lamps.fiveBank1Arrow)
            self.bank5lights.append(self.game.lamps.fiveBank2Arrow)
            self.bank5lights.append(self.game.lamps.fiveBank3Arrow)
            self.bank5lights.append(self.game.lamps.fiveBank4Arrow)
            self.bank5lights.append(self.game.lamps.fiveBank5Arrow)
    
    def mode_started(self):
        logging.info("Drop Target mode started")
        #self.dropTargetsReset()
        
    def dropTargetsReset(self):
        #self.game.coils.bank3reset.pulse(50)
        self.game.coils.bank5reset1to3.future_pulse(50,45)
        self.game.coils.bank5reset4to5.future_pulse(50,80)
        self.bank5index = 0
        self.bank5blink()
        #self.bank3blink()
        
    def bank5blink(self):
        ###First check if we are in hold mode
        if self.bank5hold == False:
            ### first thing to do is turn off the old lights
            for lamps in self.bank5lights:
                    lamps.disable()        
        
            ### then turn on the next lamp, based on the index value
            if self.bank5index <= 3:
                self.bank5index = self.bank5index +1
                self.bank5lights[self.bank5index].enable()
                ## call to the delay for next lamp
                self.delay('5bankdelay', delay = 1, handler = self.bank5blinkdelay)
            else:
                ### gets called if index is greater than 4
                ### reset the index back to 0, then enable the light
                self.bank5index = 0
                self.bank5lights[self.bank5index].enable()
                ## call to the delay for next lamp
                self.delay('5bankdelay', delay = 1, handler = self.bank5blinkdelay)
        else:
            pass
        
    def bank5blinkdelay(self):
        if self.bank5hold == False:
            ### this method is basically a copy of bank5blink
            ### both methods are used in sequense to create
            ### a moving target effect
            ### first thing to do is turn off the old lights
            for lamps in self.bank5lights:
                lamps.disable()
                ### then turn on the next lamp, based on the index value
            if self.bank5index <= 3:
                self.bank5index = self.bank5index +1
                self.bank5lights[self.bank5index].enable()
                ## call to the delay for next lamp
                self.delay('5bankdelay', delay = 1, handler = self.bank5blink)
            else:
                ### gets called if index is greater than 4
                ### reset the index back to 0
                self.bank5index = 0
                self.bank5lights[self.bank5index].enable()
                ## call to the delay for next lamp
                self.delay('5bankdelay', delay = 1, handler = self.bank5blink)        
        else:
            pass
    
    def bank5scorecheck(self, index):
        self.game.utilities.set_player_stats('bonus', 1000, 'add')
        if self.bank5index == index:
            ###pause the target lights
            ### and cancel the delay chain
            self.bank5hold == True
            self.cancel_delayed('5bankdelay')
            ### do a short blink ###
            self.bank5lights[self.bank5index].schedule(schedule = 0xff00ff00, cycle_seconds = 2, now = False)
            self.game.utilities.score(5000)
            #### pause for 1.5 seconds before restarting the target lights
            self.delay('bank5hold', delay = 1.5, handler =self.bank5resume)
        else:
            self.game.utilities.score(1000)
            
    def bank5resume(self):
        self.bank5hold = False
        ### after this pause, it resumes the target lights
        self.bank5blink()
    
    def updateEjectHoleLights(self):
        #### shut down all eject hole lights
        self.game.lamps.ejectHole5000.disable()
        self.game.lamps.ejectHole10000.disable()
        self.game.lamps.extraBallEjectHole.disable()
        
        ### set lamps based on eject_hole
        eject_hole = self.game.utilities.get_player_stats('eject_hole')
        
        if eject_hole == 1:
            self.game.lamps.ejectHole5000.enable()
        elif eject_hole == 2:
            self.game.lamps.ejectHole10000.enable()
        elif eject_hole == 3:
            self.game.lamps.extraBallEjectHole.enable()
        
########################################
####  drop target switch handlers ######
########################################
        
    def sw_fiveBankDT1_active(self,sw):
        ###send the index associated with switch to the checker
        self.bank5scorecheck(0)
            
    def sw_fiveBankDT2_active(self,sw):
        self.bank5scorecheck(1)
            
    def sw_fiveBankDT3_active(self,sw):
        self.bank5scorecheck(2)   
    
    def sw_fiveBankDT4_active(self,sw):
        self.bank5scorecheck(3)  
    
    def sw_fiveBankDT5_active(self,sw):
        self.bank5scorecheck(4)
        
    def sw_all5BankDown_active(self, sw):
        ejectvalue = self.game.utilities.get_player_stats('eject_hole')
        #### eject_hole values
        #### 1 = 5000 score
        #### 2 = 10000 score
        #### 3 = light extra ball
        #### actual light values are set when you hit the hole
        if ejectvalue < 3:
            self.game.utilities.set_player_stats('eject_hole', 1, 'add')
            
    def sw_ejectHole_active_for_100ms(self, sw):
        eject_hole = self.game.utilities.get_player_stats('eject_hole')
        eject_hole_made = self.game.utilities.get_player_stats('eject_hole_made')
        
           ### first see if we need to increment made both locally, and in player stats
        if eject_hole_made < eject_hole:
            eject_hole_made = eject_hole_made + 1
            self.game.utilities.set_player_stats('eject_hole_made', 1, 'add')
        
        ## now evaluate made
        if eject_hole_made == 1:
            self.game.utilities.score(5000)
        if eject_hole_made == 2:
            self.game.utilities.score(10000)
        if eject_hole_made == 3:
            self.game.utilities.set_player_stats('extra_balls', 1 , 'add')
            self.game.lamps.shoutAgainP.enable()
            ## now reset eject hole values
            self.game.utilities.set_player_stats('eject_hole', 1, 'set')
            self.game.utilities.set_player_stats('eject_hole_made', 0, 'set')

        ## now update the lights
        updateEjectHoleLights()
