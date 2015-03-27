########################
##Base game mode for FLASH
########################

import procgame.game 
from procgame import * 
import pinproc   
import time 
import sys 
import locale
from player import *
import bonus
import logging



class BaseGameMode(game.Mode): 
    def __init__(self, game, priority):  
        super(BaseGameMode, self).__init__(game, priority)

        #######set up logging#######
        self.log = logging.getLogger('flash.basegamemode')	
        self.log.info("Base Game initialized")


    def mode_started(self):
        logging.info("basegame mode started")

        

###########################################
#  MAIN GAME HANDLING FUNCTIONS
###########################################

    def sw_startButton_active_for_20ms(self, sw):
        self.log.info("startButton 20ms entered")

####Check to see if this is an active game or not
        if self.game.ball == 0:
            self.start_game()



    def start_game(self):
        self.log.info('Start Game')

        ##### Remove attract mode  #####
        self.game.modes.remove(self.game.attract_mode)
        ##Shut down all lamp shows
        self.game.lampctrl.stop_show()
        ####note, need to add display name to basic player stats
        #### for now, just add the player, start ball 1
        self.game.add_player()
        self.game.utilities.set_player_stats('display_name', 'P1')
        
        self.game.balls_per_game = 3 ###This needs to get moved to an user setting file
        self.log.info('Starting '+str(self.game.balls_per_game)+ ' ball game')
        self.start_ball()
        self.game.ball = self.game.ball + 1

    def start_ball(self):
        
        ####This should be where a ball save mode is added to the que
        #### for now it's empty 
        #### ball display needs to be updated here
        #### enable the flipper coils
        self.game.coils.flipperEnable.enable()

        ### enable bumpers and slings? ######

        #### reset drop targets#####
        self.resetdroptargets()
        self.game.jetbumper_mode.jetReset()

        ###after a delay, kick out ball
        self.delay( name = 'wait for ball', event_type = None, delay = 2, handler= self.kickBallOut)

        ###Change ball in play status from player####
        self.game.utilities.set_player_stats('ball_in_play',True)
         
        self.game.lamps.player1Up.enable()
        self.log.info('ball started: ' +str(self.game.ball))
        
        
    def kickBallOut(self):
        self.log.info('kickout pulsed')
        self.game.coils.ballRelease.pulse(30)

    def resetdroptargets(self):
        self.game.coils.bank3reset.pulse(50)
        self.game.coils.bank5reset1to3.future_pulse(50,45)
        self.game.coils.bank5reset4to5.future_pulse(50,80)

    def endBall(self):
        #### first thing we do is disable the fippers
        self.log.info('ball drained, in endball')
        self.game.coils.flipperEnable.disable()
        self.game.utilities.set_player_stats('ball_in_play',False)

        self.game.bonus.award_bonus()

        ### check to see if there are any extra balls available ####
        if (self.game.utilities.get_player_stats('extra_balls') > 0):
            self.log.info('extra ball available')
            eb = self.game.utilities.get_player_stats('extra_balls')
            self.game.utilities.set_player_stats('extra_balls', eb - 1)
            self.start_ball()
            if eb == 0:
                self.game.lamps.shootAgainP.disable()

        #### is this the last player?  ####
        elif self.game.current_player_index == len(self.game.players) -1:

        ### is this the last ball?
            if self.game.ball == self.game.balls_per_game:
                self.log.info('last ball drained')
                self.end_game()

        ### increment the player, and game ball
            else:
                self.game.current_player_index = 0
                self.game.ball += 1
                self.start_ball()

        ### not the last player drained
        else:
            self.log.info('not last player drained')
            self.game.current_player_index += 1
            self.start_ball

    def end_game(self):
        self.log.info('game ended')
        self.game.coils.flipperEnable.disable()
        self.game.reset()
        #self.game.modes.add(self.game.attract_mode)
        
    def reset():
        self.game.ball = 0
        self.game.old_players = []
        self.game.old_players = self.game.players[:]
        self.game.players = []
        self.game.current_player_index = 0
        
        
#########################################################
### Basic switch handling  ##############################
#########################################################

#### basic stand up switchs #############################

    def sw_topRstandup_active(self, sw):
        self.game.utilities.score(10)
        self.game.sound.playsound(1)

    def sw_rSStandup_active(self, sw):
        self.game.utilities.score(10)

    def sw_rsStandupCen_active(self, sw):
        self.game.utilities.score(10)

    def sw_rsStandupLower_active(self, sw):
        self.game.utilities.score(10)

#### basic Jet Bumper score handling #####################
        
    def leftKicker_active(self, sw):
        self.game.utilities.score(100)
    
    def rightKicker_active(self,sw):
        self.game.utilities.score(100)
        
#### eject hole handler ##################################
    def sw_ejectHole_active_for_100ms(self, sw):
        self.game.utilities.score(1000)
        self.game.coils.ejectHole.pulse(30)

#### outhole handler #####################################

    def sw_outHole_active_for_1s(self, sw):
        #### Check to see if this is a game ball #########
        if self.game.ball > 0:
            ###the following coils is needed to get VP going
            self.endBall()
        else:
            pass
        
       