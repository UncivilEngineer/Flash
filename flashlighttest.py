####Flash 2.0
####  This is a modified game file for testing
#### the Proc-system 11 board setup
#### it will run light only

import sys
sys.path.append(sys.path[0]+'/../..') # Set the path so we can find procgame.  We are assuming (stupidly?) that the first member is our directory.
import procgame
import pinproc
from procgame import *
from random import *
import string
import time
import locale
import math
import copy
import yaml
import os
import logging
#Path setups
curr_file_path = os.path.dirname(os.path.abspath( __file__ ))
#settings_path = curr_file_path + "/config/settings.yaml"
#game_data_path = curr_file_path + "/config/game_data.yaml"
#game_data_template_path = curr_file_path + "/config/game_data_template.yaml"
#settings_template_path = curr_file_path + "/config/settings_template.yaml"
game_machine_yaml = curr_file_path + "\config\Flash.yaml"
attractLampShow1 = curr_file_path + "\Assets\AttractLampShow1.lampshow"

#################################### MODE IMPORTS####################################

from sound import *
from utilities import *

################################################ GAME CLASS################################################
class FLASH(game.BasicGame):
    def __init__(self):
        super(FLASH, self).__init__(pinproc.MachineTypeWPC)
        self.load_config(game_machine_yaml)
	self.log = logging.getLogger('flashLog.txt')
        self.logging_enabled = True

        ## Set loggin info ##
        logging.basicConfig(filename='flashLog.txt',level=logging.INFO)	
        self.log.info('FLASH class initilized')

	#### Settings and Game Data ####
        #self.load_settings(settings_template_path, settings_path)
        #self.load_game_data(game_data_template_path, game_data_path)

        #### Setup Lamp Controller ####	
        #self.lampctrl = procgame.lamps.LampController(self)
        #self.RegisterLampshows()
        self.reset()

#    def RegisterLampshows(self):
#        self.lampctrl.register_show('attractShow1', attractLampShow1)
#	logging.info("lampshow1 registered from " + attractLampShow1)

    
    def reset(self):        
        super(FLASH, self).reset()
        logging.info('reset called in class')
        self.ball = 0
        self.players = []        
        self.current_player_index = 0

        #### Mode Definitions #### 
        self.utilities = UtilitiesMode(self,99) 
       #self.base_mode = BaseGameMode(self,3) 
        self.attract_mode = Attract(self,5)
	self.sound_mode = Sound(self,10)

        ###add modes to que
	self.modes.add(self.utilities)
        self.modes.add(self.attract_mode)
	self.modes.add(self.sound_mode)

        self.utilities.allDisplaysOn()
	self.utilities.updateDisplay('P1', '0075')
#    def create_player(self, name):
#        return Player(name)


#########################
### test base mode  ---> move to own file!
#########################
#class BaseGameMode(game.Mode): 
#    def __init__(self, game, priority): 
#        super(BaseGameMode, self).__init__(game, priority) 
#        self.log = logging.getLogger('flash.basegamemode')
#	self.log.info("Base Game initialized")#	#	
#
#    def mode_started(self):
#	logging.info("basegame mode started")
#	






############################# Attract mode##########################
class Attract(game.Mode):	
    """docstring for AttractMode"""

    def __init__(self, game, prioirty):
        super(Attract, self).__init__(game, prioirty)
        self.log = logging.getLogger('flash.attractmode')
        self.log.info("attract mode initilized")

    def mode_started(self):
	self.game.utilities.allDisplaysOn()
        # This is a simple light show, works well.	    
        i = 0	    
        self.log.info("Start basic attract show")
        for lamp in self.game.lamps:
            if i % 8 == 7:
                lamp.schedule(schedule=0xf00000ff, cycle_seconds=0, now=False)
            elif i % 8 == 6:
                lamp.schedule(schedule=0xff00000f, cycle_seconds=0, now=False)
            elif i % 8 == 5:
                lamp.schedule(schedule=0xfff00000, cycle_seconds=0, now=False)
            elif i % 8 == 4:
                lamp.schedule(schedule=0x0fff0000, cycle_seconds=0, now=False)
            elif i % 8 == 3:
                lamp.schedule(schedule=0x00fff000, cycle_seconds=0, now=False)
            elif i % 8 == 2:	    
                lamp.schedule(schedule=0x000fff00, cycle_seconds=0, now=False)
            elif i % 8 == 1:
                lamp.schedule(schedule=0x0000fff0, cycle_seconds=0, now=False)
            elif i % 8 == 0:
                lamp.schedule(schedule=0x00000fff, cycle_seconds=0, now=False)
            i = i + 1
        #self.game.lampctrl.play_show('attractShow1', repeat = True )
	self.game.sound_mode.playsound(16)
	self.delay('sound1', delay = 2, handler = self.soundbackup)
    
    def soundbackup(self):
	self.game.sound_mode.playsound(18)
	self.delay('sound2', delay = .1, handler = self.soundbackup2)
    
    def soundbackup2(self):
	self.game.sound_mode.playsound(18)
	self.delay('sound2', delay = .1, handler = self.soundbackup3)
	
    def soundbackup3(self):
	self.game.sound_mode.playsound(18)
	self.delay('sound3', delay = 2, handler = self.soundbackup4)
    
    def soundbackup4(self):
	self.game.sound_mode.playsound(19)
	
    def sw_startButton_active_for_20ms(self, sw):
	self.log.info("start button pressed")
	for lamp in self.game.lamps:
	    lamp.disable()
	    
	self.game.coils.flashStrobe.pulse(30)
	#self.game.enable_bumpers(enable = True)
	
	#self.game.coils.ballRelease.pulse(25)
	self.game.sound_mode.soundtest()
	
	    


	

########################################################
##main run loop
########################################################
def main():	
    game = None
    log = logging.getLogger('FLASH.main')
    log.setLevel(logging.INFO)
    fh = logging.FileHandler('flash.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    log.addHandler(fh)
    
    log.setLevel(logging.DEBUG)
    dh = logging.FileHandler('flashdebug.log')
    dh.setLevel(logging.DEBUG)
    dh.setFormatter(formatter)
    log.addHandler(dh)

	
    try:	 	
        game = FLASH()
        game.run_loop()
    finally:
	del game
if __name__ == '__main__': main()