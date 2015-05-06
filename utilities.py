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
import serial

display_board = serial.Serial('COM4', 9600, timeout = .1)

class UtilitiesMode(game.Mode): 
    def __init__(self, game, priority):  
        super(UtilitiesMode, self).__init__(game, priority)

        #######set up logging#######
        self.log = logging.getLogger('flash.utilities')	
        self.log.info("Utilities initilized")
        self.allDisplaysOn()


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
            self.log.info('Player Stats - get '+id+' is '+str(self.game.current_player().player_stats[id]))
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
            self.updateScoreDisplay()
            #### This may be the place to call for a display update ####
    
                            
### gets current player score ################################
    def currentPlayerScore(self):
        if (self.game.ball <> 0): #in case score() gets called when not in game
            self.p = self.game.current_player()
            return self.p.score
        else:
            return 0
        
### display drivers #########################################

#### This function turns all displays on, needed to initialize the displays
    def allDisplaysOn(self):
        display_board.write("<G>")
        self.log.info("all displays on")
        
#### This function turns all displays off
    def allDisplaysOff(self):
        display_board.write("<B>")
        self.log.info("all displays off")

#### this function blanks out a display
    def displayOff(self, displayName):
        if displayName == 'P1':
            self.log.info("display 1 off called")
            display_board.write("<P1BBBBBB>")
        elif displayName == 'P2':
            self.log.info("display 2 off called")
            display_board.write("<P2BBBBBB>")
        elif displayName == 'P3':
            self.log.info("display 3 off called")
            display_board.write("<P3BBBBBB>")
        elif displayName == 'P4':
            self.log.info("display 4 off called")
            display_board.write("<P4BBBBBB>")
        elif displayName == 'M1':
            display_board.write("<M1BB>")
        elif displayName == 'M2':
            display_board.write("<M2BB>")
        else:
            self.log.info("Bad displayoff call")
            
#### this function clears all of the score displays
    def clearAllScoreDisplays(self):
        display_board.write("<P1BBBBBB>")
        display_board.write("<P2BBBBBB>")
        display_board.write("<P3BBBBBB>")
        display_board.write("<P4BBBBBB>")
        
            
    ### function for sending raw data to a display
    ## this function was written after updateScoreDisplay, so much of code is recycled
    def updateDisplay(self, displayName, displayValue):
        
        ## pre defined display templates
        if displayName == 'P1':
            output_template = '<P1BBBBBB>'
            template_len = 9
        elif displayName == 'P2':
            output_template = '<P2BBBBBB>'
            template_len = 9
        elif displayName == 'P3':
            output_template = '<P3BBBBBB>'
            template_len = 9
        elif displayName == 'P4':
            output_template = '<P4BBBBBB>'
            template_len = 9
        elif displayName == 'M1':
            output_template = '<M1BB>'
            template_len = 5
        elif displayName == 'M2':
            output_template = '<M2BB>'
            template_len = 5
        else:
            print "Bad display write call"
            badstring = "Name value is: " + displayName
            print badstring
            return            
        
        #First you have to convert the templante,
        #and the score value to a list
        template_list = list(output_template)
        display_string = str(displayValue) 
        display_list = list(display_string)
        
        #now you have to do the list item swaps
        #it starts with getting the lenght of the display string
        display_len = len(display_string)
        #Y is needed to set through the display list
        y = 0
        #set through the numbers to replace, and swap them out
        for x in range(template_len - display_len , template_len):
            template_list[x] = display_list[y]
            y = y + 1
            
        #write results to an output string
        output_string = "".join(template_list)
        ##print "output_string is:", output_string
        #send to display board
        display_board.write(output_string)        

##### This is the big one, this one updates the display given a string, used for
##### updating scores only
            
    def updateScoreDisplay(self):
        name = self.game.current_player().name
        
        ## pre defined templates for each display
        
        if name == 'Player 1':
            output_template = '<P1BBBBBB>'
            template_len = 9
        elif name == 'Player 2':
            output_template = '<P2BBBBBB>'
            template_len = 9
        elif name == 'Player 3':
            output_template = '<P3BBBBBB>'
            template_len = 9
        elif name == 'Player 4':
            output_template = '<P4BBBBBB>'
            template_len = 9
        else:
            print "Bad score name value"
            badstring = "Name value is: " + name
            print badstring
            return
            
        #First you have to convert the templante,
        #and the score value to a list
        template_list = list(output_template)
        score_string = str(self.currentPlayerScore()) 
        score_list = list(score_string)
        
        #now you have to do the list item swaps
        #it starts with getting the lenght of the score string
        score_len = len(score_string)
        #Y is needed to set through the score list
        y = 0
        #set through the numbers to replace, and swap them out
        for x in range(template_len - score_len , template_len):
            template_list[x] = score_list[y]
            y = y + 1
            
        #write results to an output string
        output_string = "".join(template_list)
        ##print "output_string is:", output_string
        #send to display board
        display_board.write(output_string)
