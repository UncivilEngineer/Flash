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
    bank5Reset = True
    bank5Made = 0
    fiveBankDT1down = False
    fiveBankDT2down = False
    fiveBankDT3down = False
    fiveBankDT4down = False
    fiveBankDT5down = False
    
    bank3index = 0
    bank3lights=[]
    bank3hold = False
    bank3Reset = False
    threeBankDTLdown = False
    threeBankDTCdown = False
    ThreeBankDTRdown = False
    specialEnable = False
    
    
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
            
            ## set up the light list for bank 3
            
            self.bank3lights.append(self.game.lamps.threeBankRArrow)
            self.bank3lights.append(self.game.lamps.threeBankCArrow)
            self.bank3lights.append(self.game.lamps.threeBankLArrow)
    
    def mode_started(self):
        logging.info("Drop Target mode started")
        #self.dropTargetsReset()
        
    def dropTargetsReset(self):
        self.bank3DTreset()
        self.bank5DTreset()
        self.bank5Made = 0
        self.bank5index = 0
        self.bank5hold = False
        self.cancel_delayed('5bankdelay')
        self.cancel_delayed('3bankdelay')
        self.updateEjectHoleLights()
        self.bank5blink()
        self.bank3blink()
        
        #reset special lights
        self.game.lamps.rightSpecial.disable()
        self.game.lamps.leftSpecial.disable()
        self.specialEnable = False
        
        #reset upper arrows
        self.game.lamps.upperLeftArrows.disable()
        self.game.lamps.spinnerAndRollover.disable()
        self.game.lamps.centerRightAndLowerStars.disable()        
        
    def bank5DTreset(self):
        ## to keep from scoring going up, we need to change the reset flag
        self.bank5Reset = True 
        self.log.info("bank 5 reset called")
        ## then fire the reset coils, and add a delay so the switches don't get called
        self.delay('5bankresetdelay', delay = .75 , handler = self.bank5resetdelay)
        self.game.coils.bank5reset1to3.pulse(50)
        self.game.coils.bank5reset4to5.future_pulse(50,30)        
    
    def bank3DTreset(self):
        self.bank3Reset = True
        self.log.info("bank 3 reset called")
        self.delay('3bankresetdelay', delay = .90, handler = self.bank3ResetDelay)
        ### im trying to stagger the pulses to the reset coils, so the don't go off all at once
        self.game.coils.bank3reset.future_pulse(60, 80)
        
    def bank5resetdelay(self):
        ### turn off the reset flag so the DTs will score when they go down
        ### reset the down flags
        self.fiveBankDT1down = False
        self.fiveBankDT2down = False
        self.fiveBankDT3down = False
        self.fiveBankDT4down = False
        self.fiveBankDT5down = False
        self.bank5Reset = False
        
    def bank3ResetDelay(self):
        self.threeBankDTLdown = False
        self.threeBankDTCdown = False
        self.threeBankDTRdown = False
        self.bank3Reset = False
        
        
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
        
    def bank3blink(self):
        ###First check if we are in hold mode
        if self.bank3hold == False:
            ### first thing to do is turn off the old lights
            for lamps in self.bank3lights:
                    lamps.disable()        
            
                ### then turn on the next lamp, based on the index value
            if self.bank3index <= 1:
                self.bank3index = self.bank3index +1
                self.bank3lights[self.bank3index].enable()
                ## call to the delay for next lamp
                self.delay('3bankdelay', delay = 1, handler = self.bank3blinkdelay)
            else:
                ### gets called if index is greater than 2
                ### reset the index back to 0, then enable the light
                self.bank3index = 0
                self.bank3lights[self.bank3index].enable()
                ## call to the delay for next lamp
                self.delay('3bankdelay', delay = 1, handler = self.bank3blinkdelay)
        else:
            pass
        
    def bank3blinkdelay(self):
        if self.bank5hold == False:
            ### this method is basically a copy of bank3blink
            ### both methods are used in sequense to create
            ### a moving target effect
            ### first thing to do is turn off the old lights
            for lamps in self.bank3lights:
                lamps.disable()
                ### then turn on the next lamp, based on the index value
            if self.bank3index <= 1:
                self.bank3index = self.bank3index +1
                self.bank3lights[self.bank3index].enable()
                ## call to the delay for next lamp
                self.delay('3bankdelay', delay = 1, handler = self.bank3blink)
            else:
                ### gets called if index is greater than 4
                ### reset the index back to 0
                self.bank3index = 0
                self.bank3lights[self.bank3index].enable()
                ## call to the delay for next lamp
                self.delay('3bankdelay', delay = 1, handler = self.bank3blink)        
        else:
            pass        

    
    def bank5scorecheck(self, index):
        self.game.utilities.set_player_stats('bonus', 1000, 'add')
        self.game.bonus.update_bonus_lights_basic()
        #check to see if we are in hold, happens after 4 drops
        if self.bank5hold == False:
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
        else:
            # if bank5Hold is enabled, socre 5000
            self.game.utilities.score(5000)
            
        
        ### the All Bank Down switch are notoriously for not closing when the bank is down, so I added a second check here
        if self.fiveBankDT1down == True and self.fiveBankDT2down == True and self.fiveBankDT3down == True and self.fiveBankDT4down == True and self.fiveBankDT5down == True:
            
            ### if all the bank flags are down, it calls the all 5 down
            self.bank5AllDown()
            
    def bank5resume(self):
        self.bank5hold = False
        ### after this pause, it resumes the target lights
        self.bank5blink()

    def bank5AllDown(self):
        self.bank5Made = self.bank5Made + 1
        if self.bank5Made >= 1:
            self.rollOverArrowCheck()
            
        self.updateEjectHoleLights()
        self.bank5DTreset()
    
    def rollOverArrowCheck(self):
        ## used to light up roll over star lamps
        self.game.lamps.upperLeftArrows.enable()
        self.game.lamps.spinnerAndRollover.enable()
        self.game.lamps.centerRightAndLowerStars.enable()
    
    def updateEjectHoleLights(self):
        #### shut down all eject hole lights
        self.game.lamps.ejectHole5000.disable()
        self.game.lamps.ejectHole10000.disable()
        self.game.lamps.extraBallEjectHole.disable()
        self.game.lamps.leftSpecial.disable()
        self.game.lamps.rightSpecial.disable()
        
        # Im not sure we are going to use this any more
        #eject_hole = self.game.utilities.get_player_stats('eject_hole')
        #eject_hole_made = self.game.utilities.get_player_stats('eject_hole_made')
        
        if self.bank5Made == 0:
            self.game.lamps.ejectHole5000.enable()
        elif self.bank5Made == 1:
            self.game.lamps.ejectHole5000.disable()
            self.game.lamps.ejectHole10000.enable()
        elif self.bank5Made == 2:
            self.game.lamps.ejectHole10000.disable()
            self.game.lamps.extraBallEjectHole.enable()
        elif self.bank5Made == 3:
            self.specialEnable = True
            self.game.lamps.rightSpecial.enable()
            self.game.lamps.leftSpecial.enable() 
        elif self.bank5Made == 4:
            self.game.lamps.fiveBank1Arrow.enable()
            self.game.lamps.fiveBank2Arrow.enable()
            self.game.lamps.fiveBank3Arrow.enable()
            self.game.lamps.fiveBank4Arrow.enable()
            self.game.lamps.fiveBank5Arrow.enable()
            self.bank5hold = True 
       
        
    def bank3scorecheck(self, index):
        self.game.utilities.set_player_stats('bonus', 1000, 'add')
        self.game.bonus.update_bonus_lights_basic()
        if self.bank3index == index:
            ###pause the target lights
            ### and cancel the delay chain
            self.bank3hold == True
            self.cancel_delayed('3bankdelay')
            ### do a short blink ###
            self.bank3lights[self.bank3index].schedule(schedule = 0xff00ff00, cycle_seconds = 2, now = False)
            self.game.utilities.score(3000)
            #### pause for 1.5 seconds before restarting the target lights
            self.delay('bank3hold', delay = 1.5, handler =self.bank3resume)
        else:
            self.game.utilities.score(1000)  
            
    def bank3resume(self):
        self.cancel_delayed('3bankdelay')
        self.bank3hold = False
        ### after this pause, it resumes the target lights
        self.bank3blink()
        
    def bank3AllDown(self):
        ### load award status
        thunder = self.game.utilities.get_player_stats('thunder')
        lightning = self.game.utilities.get_player_stats('lightning')
        tempest = self.game.utilities.get_player_stats('tempest')
        super_flash = self.game.utilities.get_player_stats('super_flash')
        
        if thunder == False:
            self.game.utilities.score(5000)
            self.game.sound.playsound(6)
            self.game.utilities.set_player_stats('thunder', True, 'set')
            self.reset3BankScoreLights()
            
        elif lightning == False:
            self.game.utilities.score(10000)
            self.game.sound.playsound(6)
            self.game.utilities.set_player_stats('lightning', True, 'set')
            self.reset3BankScoreLights()
            
        elif tempest == False:
            self.game.utilities.score(20000)
            self.game.sound.playsound(6)
            self.game.utilities.set_player_stats('tempest', True, 'set')
            self.reset3BankScoreLights()
            
        elif super_flash == False:
            self.game.utilities.score(50000)
            self.game.sound.playsound(6)
            self.game.utilities.set_player_stats('super_flash', True, 'set')
            self.reset3BankScoreLights()
            self.delay('super_flash_reset', delay = 2, handler = self.super_flash_reset)
        else:
            pass
        
        ## reset the drop targets
        self.bank3DTreset()

    def super_flash_reset(self):
        self.game.utilities.set_player_stats('thunder', False, 'set')
        self.game.utilities.set_player_stats('lightning', False, 'set')
        self.game.utilities.set_player_stats('tempest', False, 'set')
        self.game.utilities.set_player_stats('super_flash', False, 'set')
        self.reset3BankScoreLights()
    
    def reset3BankScoreLights(self):
        ### load award status
        thunder = self.game.utilities.get_player_stats('thunder')
        lightning = self.game.utilities.get_player_stats('lightning')
        tempest = self.game.utilities.get_player_stats('tempest')
        super_flash = self.game.utilities.get_player_stats('super_flash')
        
        self.game.lamps.thunder.disable()
        self.game.lamps.lightning.disable()
        self.game.lamps.tempest.disable()
        self.game.lamps.superFLASH.disable()
       
        if thunder == False:
            self.game.lamps.thunder.schedule(schedule = 0xff00ff00, cycle_seconds = 0, now = False)
        
        if thunder == True:
            self.game.lamps.thunder.enable()
            self.game.lamps.lightning.schedule(schedule = 0xff00ff00, cycle_seconds = 0, now = False)
        
        if lightning == True:
            self.game.lamps.lightning.enable()
            self.game.lamps.tempest.schedule(schedule = 0xff00ff00, cycle_seconds = 0, now = False)
            
        if tempest == True:
            self.game.lamps.tempest.enable()
            self.game.lamps.superFLASH.schedule(schedule = 0xff00ff00, cycle_seconds = 0, now = False)
        
        if super_flash == True:
            self.game.lamps.superFLASH.enable()
        
########################################
####  drop target switch handlers ######
########################################
        
    def sw_fiveBankDT1_closed_for_10ms(self,sw):
        ## check if we are in reset mode first (happens when DTs are reset so they don't score going up)
        if self.bank5Reset == False:
            ## Set down flag
            self.fiveBankDT1down = True
            self.log.info("five bank DT 1 dropped")
            ## check scoring
            self.bank5scorecheck(0)
            
    def sw_fiveBankDT2_closed_for_10ms(self,sw):
        if self.bank5Reset == False:
            self.fiveBankDT2down = True
            self.log.info("five bank DT 2 dropped")
            self.bank5scorecheck(1)
            
            
    def sw_fiveBankDT3_closed_for_10ms(self,sw):
        if self.bank5Reset == False:
            self.fiveBankDT3down = True
            self.log.info("five bank DT 3 dropped")
            self.bank5scorecheck(2)   
    
    def sw_fiveBankDT4_closed_for_10ms(self,sw):
        if self.bank5Reset == False:
            self.fiveBankDT4down = True
            self.log.info("five bank DT 4 dropped")
            self.bank5scorecheck(3)  
    
    def sw_fiveBankDT5_closed_for_10ms(self,sw):
        if self.bank5Reset == False:
            self.fiveBankDT5down = True
            self.log.info("five bank DT 5 dropped")
            self.bank5scorecheck(4)
        
    def sw_all5BankDown_active(self, sw):
        if self.bank5Reset == False:
            self.log.info("five bank all down")
            self.bank5AllDown()
            
    def sw_rDropTarget3B_closed_for_10ms(self, sw):
        if self.bank3Reset == False:
            self.threeBankDTLdown = True
            self.log.info("three bank DT Left dropped")
            self.bank3scorecheck(0)
            
    def sw_cDropTarget3B_closed_for_10ms(self, sw):
        if self.bank3Reset == False:
            self.threeBankDTLdown = True
            self.log.info("three bank DT center dropped")
            self.bank3scorecheck(1)
            
    def sw_lDropTarget3B_closed_for_10ms(self, sw):
        if self.bank3Reset == False:
            self.threeBankDTLdown = True
            self.log.info("three bank DT Right dropped")
            self.bank3scorecheck(2)
            
    def sw_all3BankDown_closed_for_10ms(self,sw):
        if self.bank3Reset == False:
            self.log.info("three bank all down")
            self.bank3AllDown()

            
    def sw_ejectHole_active_for_100ms(self, sw):
         
        ## check the scoreing
        if self.bank5Made == 0:
            self.game.utilities.score(5000)
            self.game.lamps.ejectHole5000.schedule(schedule = 0xff00ff00, cycle_seconds = 2, now = False)
        elif self.bank5Made == 1:
            self.game.utilities.score(10000)
            self.game.lamps.ejectHole10000.schedule(schedule = 0xff00ff00, cycle_seconds = 2, now = False)
        elif self.bank5Made == 2:
            if self.game.utilities.get_player_stats('extra_balls') == 0:
                self.game.lamps.extraBallEjectHole.schedule(schedule = 0xff00ff00, cycle_seconds = 2, now = False)
                self.game.utilities.set_player_stats('extra_balls', 1 , 'add')
                self.game.lamps.shootAgainP.enable()
            else:
                ## extra ball has already been awarded
                self.game.utilities.score(20000)
            ## now reset eject hole values
        elif self.bank5Made > 2:
            self.game.utilities.score(20000)

        self.delay('ejectHoleDelay', delay = 1.5, handler = self.doEjectHole)
        
    def doEjectHole(self):
        self.updateEjectHoleLights()
        self.game.coils.ejectHole.pulse(30)
    
    def sw_rightSpecial_closed_for_10ms(self, sw):
        ## get eject hole made value to check if the value is 4
        
        
        if self.specialEnable == True:
            self.game.utilities.set_player_stats('extra_balls', 1 , 'add')
            self.game.lamps.shootAgainP.enable()
            #self.game.utilities.set_player_stats('eject_hole_made', 0, 'set')
            self.game.lamps.rightSpecial.disable()
            self.game.lamps.leftSpecial.disable()
            self.specialEnable = False
        else:
            self.game.utilities.score(2000)
            self.game.utilities.set_player_stats('bonus', 2000, 'add')
            self.game.sound.playsound(4)
            
    def sw_leftSpecial_closed_for_10ms(self, sw):
        
        if self.specialEnable == True:
            self.game.utilities.set_player_stats('extra_balls', 1 , 'add')
            self.game.lamps.shootAgainP.enable()
            self.game.utilities.set_player_stats('eject_hole_made', 0, 'set')
            self.game.lamps.rightSpecial.disable()
            self.game.lamps.leftSpecial.disable()
            self.special.Enable = False
        else:
            self.game.utilities.score(2000)
            self.game.utilities.set_player_stats('bonus', 2000, 'add')
            self.game.sound.playsound(4)
    
    def sw_outerULStar_closed_for_10ms(self, sw):
        if self.bank5Made >= 1:
            self.game.utilities.score(3000)
        else:
            self.game.utilities.score(1000)
    
    def sw_innerULStar_closed_for_10ms(self, sw):
        if self.bank5Made >=1:
            self.game.utilities.score(3000)
        else:
            self.game.utilities.score(1000)
    
    def sw_spinner_active(self, sw):
        if self.bank5Made >= 1:
            self.game.utilities.score(1000)
        else:
            self.game.utilities.score(100)
        