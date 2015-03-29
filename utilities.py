########################
##Utility game mode for FLASH
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
from player import *


class UtilitiesMode(game.Mode): 
    def __init__(self, game, priority):  
        super(UtilitiesMode, self).__init__(game, priority)

        #######set up logging#######
        self.log = logging.getLogger('flash.utilities')	
        self.log.info("Utilities initilized")


    def mode_started(self):
        logging.info("Utilities Mode started!")
        
    ##########################
    #### Player Functions ####
    ##########################
    
### Set the player stats###################################
    def set_player_stats(self,id,value,mode='set'):
        self.log.info('Player Stats - set '+id+' to '+str(value))
        if (self.game.ball <> 0):
            if mode == 'set':
                self.game.current_player().player_stats[id] = value
            if mode == 'add':
                self.game.current_player().player_stats[id] = self.game.current_player().player_stats[id] + value
            #return self.game.current_player().player_stats[id] <-- Why would this funciton return anything?
    
    
### Get the player stat#####################################
    def get_player_stats(self,id):
        if (self.game.ball <> 0):
            #self.log.info('Player Stats - get '+id+' is '+str(self.game.current_player().player_stats[id]))
            return self.game.current_player().player_stats[id]
        else:
            return False
    
    
### Adds points to the current players score ################
    def score(self, points):
        if (self.game.ball <> 0): #in case score() gets called when not in game
            self.p = self.game.current_player()
            #self.game.score(points) <-- Im not sure about this line
            self.p.score += points
            #self.log.info('player scored ' +str(points)+ ' points')
            #### This may be the place to call for a display update ####
    
                            
### gets current player score ################################
    def currentPlayerScore(self):
        if (self.game.ball <> 0): #in case score() gets called when not in game
            self.p = self.game.current_player()
            return self.p.score
        else:
            return 0