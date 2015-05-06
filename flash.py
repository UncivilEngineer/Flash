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
        self.old_players = []
        self.old_players = self.players[:]
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
        ### make sure all light from the game are off:
        for lamp in self.game.lamps:
            lamp.disable()
        ## start lamps show
        self.game.lampctrl.play_show('attractShow1', repeat = True )
        ## turn the displays on
        self.game.utilities.allDisplaysOn()
        
        ##start the game over lamps
        self.game.lamps.gameOver.schedule(schedule = 0xff00ff00, cycle_seconds = 0, now = True)
        self.game.lamps.canPlay1.schedule(schedule = 0xff00ff00, cycle_seconds = 0, now = True)
        self.game.lamps.canPlay2.schedule(schedule = 0xff00ff00, cycle_seconds = 0, now = True)
        self.game.lamps.canPlay3.schedule(schedule = 0xff00ff00, cycle_seconds = 0, now = True)
        self.game.lamps.canPlay4.schedule(schedule = 0xff00ff00, cycle_seconds = 0, now = True)
        
        ### starts looping the high scores through the displays
        self.highScoreDisplay()
        
    def highScoreDisplay(self):
        self.game.lamps.highScore.enable()
        
        self.game.utilities.updateDisplay('P1', self.game.game_data['highScore0'])
        self.game.utilities.updateDisplay('P2', self.game.game_data['highScore1'])
        self.game.utilities.updateDisplay('P3', self.game.game_data['highScore2'])
        self.game.utilities.updateDisplay('P4', self.game.game_data['highScore3'])
        
        ### now schedule the last players score to display
        self.delay('display loop', delay = 2, handler = self.lastScoreDisplay)
        
    def lastScoreDisplay(self):
        ## first clear all displays
        self.game.utilities.clearAllScoreDisplays()
        
        ## turn off the high score lamp
        self.game.lamps.highScore.disable()
        
        numberOfOldPlayers = len(self.game.old_players)
        self.log.info("old player len is: " +str(len(self.game.old_players)))
        ## when the game first starts, there will be no value in old players (len == 0)
        ## so you have to fake the values for the attract mode
        if numberOfOldPlayers == 0:
            self.game.utilities.updateDisplay('P1', 0)
            self.game.utilities.updateDisplay('P2', 0)
            self.game.utilities.updateDisplay('P3', 0)
            self.game.utilities.updateDisplay('P4', 0)            
        elif numberOfOldPlayers == 1:
            self.game.utilities.updateDisplay('P1', self.game.old_players[0].score)
        elif numberOfOldPlayers == 2:
            self.game.utilities.updateDisplay('P1', self.game.old_players[0].score)            
            self.game.utilities.updateDisplay('P2', self.game.old_players[1].score)
        elif numberOfOldPlayers == 3:
            self.game.utilities.updateDisplay('P1', self.game.old_players[0].score)            
            self.game.utilities.updateDisplay('P2', self.game.old_players[1].score)            
            self.game.utilities.updateDisplay('P3', self.game.old_players[2].score)
        elif numberOfOldPlayers == 4:
            self.game.utilities.updateDisplay('P1', self.game.old_players[0].score)            
            self.game.utilities.updateDisplay('P2', self.game.old_players[1].score)            
            self.game.utilities.updateDisplay('P3', self.game.old_players[2].score)
            self.game.utilities.updateDisplay('P4', self.game.old_players[3].score)
            
        #### after displaying, return to highscoredisplay
        self.delay('display loop', delay = 2, handler = self.highScoreDisplay)
        

    def mode_stopped(self): 
        self.log.info("Stop attract mode")
        self.game.lampctrl.stop_show()
        for lamp in self.game.lamps: 
            lamp.disable() 
        
        ## stop the display loop
        self.cancel_delayed('display loop')
        ## clear the score displays
        self.game.utilities.clearAllScoreDisplays()
    
##### main game loop
        


def main():
    game = None
    log = logging.getLogger('FLASH.main')
   

    try:
        game = FLASH()
        game.run_loop()
    finally:
        del game

if __name__ == '__main__': main()



