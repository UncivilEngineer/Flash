import sys
sys.path.append(sys.path[0]+'/../..') 
# Set the path so we can find procgame.  We are assuming (stupidly?) that the first member is our directory.
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
from player import *
import logging
logging.basicConfig(level=logging.INFO, filename='flashLog.txt', format="%(asctime)s - %(name)s - %(levelname)s - %(message)s") 



#Path setups
curr_file_path = os.path.dirname(os.path.abspath( __file__ ))

#settings_path = curr_file_path + "\config\settings.yaml"
game_data_path = curr_file_path + "\config\game_data.yaml"
game_data_template_path = curr_file_path + "\config\game_data_template.yaml"
#settings_template_path = curr_file_path + "\config\settings_template.yaml"
game_machine_yaml = curr_file_path + "\config\Flash.yaml"
attractLampShow1 = curr_file_path + "\Assets\AttractLampShow1.lampshow"


###################################
# MODE IMPORTS
###################################
from Basemode import *
from utilities import *
from bonus import *
from sound import *
from jetbumpers import *
from droptargets  import *
from osc import *


###############################################
# GAME CLASS
################################################
class FLASH(game.BasicGame):
    def __init__(self):
        super(FLASH, self).__init__(pinproc.MachineTypeWPC)
        self.load_config(game_machine_yaml)
        self.log = logging.getLogger('game.config')
        self.logging_enabled = True
        ## Set loggin info ##
        #logging.basicConfig(filename='flashLog.txt',level=logging.INFO)
        logging.info('FLASH class initilized')

        #### Settings and Game Data #### 
        #self.load_settings(settings_template_path, settings_path)
        self.load_game_data(game_data_template_path, game_data_path)

        #### Setup Lamp Controller ####
        self.lampctrl = procgame.lamps.LampController(self)
        self.RegisterLampshows()
       
        

        self.reset()

    def RegisterLampshows(self):
        self.lampctrl.register_show('attractShow1', attractLampShow1)
        logging.info("lampshow1 registered from " + attractLampShow1)

    def reset(self):
        super(FLASH, self).reset()
        logging.info('reset called in class')
        self.game.old_players = []
        self.game.old_players = self.game.players[:]
        self.ball = 0
        self.players = []
        self.current_player_index = 0

        #### Mode Definitions #### 
        self.utilities = UtilitiesMode(self,99)
        self.sound = Sound(self,50)
        self.bonus = BonusGameMode(self, 6)
        self.base_mode = BaseGameMode(self,5) 
        self.attract_mode = Attract(self,3)
        self.jetbumper_mode = JetBumper(self,7)
        self.droptarget_mode = DropTargetMode(self,8)
        self.osc = modes.OSC_Mode(game = self, priority = 1, closed_switches = 'outHole')

        ###add modes to que
        self.modes.add(self.attract_mode)
        self.modes.add(self.bonus)
        self.modes.add(self.base_mode)
        self.modes.add(self.utilities)
        self.modes.add(self.sound)
        self.modes.add(self.jetbumper_mode)
        self.modes.add(self.droptarget_mode)
        self.modes.add(self.osc)
        ## update ball display
        self.game.utilities.updateDisplay('M1', self.game.ball)

        
    def create_player(self, name):
        return Flashplayer(name)	
        


##########################
### Attract mode
###  This need to get moved to its own file
##########################
class Attract(game.Mode):
    """docstring for AttractMode"""
    def __init__(self, game, prioirty):
        super(Attract, self).__init__(game, prioirty)
        self.log = logging.getLogger('flash.attractmode')
        self.log.info("attract mode initilized")

    def mode_started(self):
        self.game.lampctrl.play_show('attractShow1', repeat = True )
        self.game.utilities.allDisplaysOn()


    def mode_stopped(self): 
        self.log.info("Stop attract mode")
        self.game.lampctrl.stop_show()
        for lamp in self.game.lamps: 
            lamp.disable() 
    

def main():
    game = None
    log = logging.getLogger('FLASH.main')
   

    try:
        game = FLASH()
        game.run_loop()
    finally:
        del game

if __name__ == '__main__': main()



