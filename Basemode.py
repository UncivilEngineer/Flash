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
        ### add players if game is already started
        elif self.game.ball == 1 and len(self.game.players) < 4:
            self.game.add_player()
            if (len(self.game.players) == 2):
                self.game.players[1].player_stats['display_name'] = 'P2'
                ### this is where the Player two display would turn on
                self.game.lamps.canPlay2.enable()
            elif(len(self.game.players) == 3):
                self.game.players[2].player_stats['display_name'] = 'P3'
                ### this is where player three display would turn on
                self.game.lamps.canPlay3.enable()
            elif(len(self.game.players) == 4):
                self.game.players[3].player_stats['display_name'] = 'P4'
                ### this is where player four display would turn on
                self.game.lamps.canPlay4.enable()


    def start_game(self):
        self.log.info('Start Game')

        ##### Remove attract mode  #####
        self.game.modes.remove(self.game.attract_mode)
        ##Shut down all lamp shows
        self.game.lampctrl.stop_show()
        ### adds player for player 1 game
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

        #### reset drop targets#####
        self.game.droptarget_mode.dropTargetsReset()
        self.game.jetbumper_mode.jetReset()
        self.game.droptarget_mode.updateEjectHoleLights()
        self.game.bonus.update_bonus_lights_basic()

        ###after a delay, kick out ball
        self.delay( name = 'wait for ball', event_type = None, delay = 1, handler= self.kickBallOut)

        ###Change ball in play status from player####
        self.game.utilities.set_player_stats('ball_in_play',True)
        self.log.info('ball started: ' +str(self.game.ball))
        
        
    def kickBallOut(self):
        self.log.info('kickout pulsed')
        self.game.coils.ballRelease.pulse(30)

    #def resetdroptargets(self):
    #    self.game.coils.bank3reset.pulse(50)
    #    self.game.coils.bank5reset1to3.future_pulse(50,45)
    #    self.game.coils.bank5reset4to5.future_pulse(50,80)

    def endBall(self):
        #### first thing we do is disable the fippers
        self.log.info('ball drained, in endball')
        self.game.coils.flipperEnable.disable()
        self.game.utilities.set_player_stats('ball_in_play',False)

        self.game.bonus.award_bonus()
    ### in order to make sure the bonus gets added in before we start a new ball
    ### it was necessary to split this function up.  award_bonus calls endBallCont()
    
    def endBallCont(self):

        ### check to see if there are any extra balls available ####
        if (self.game.utilities.get_player_stats('extra_balls') > 0):
            self.log.info('extra ball available')
            eb = self.game.utilities.get_player_stats('extra_balls')
            self.game.utilities.set_player_stats('extra_balls', eb - 1)
            
            if eb == 0:
                self.game.lamps.shootAgainP.disable()
            
            self.start_ball()

        #### is this the last player?  ####
        elif self.game.current_player_index == len(self.game.players) -1:

        ### is this the last ball?
            if self.game.ball == self.game.balls_per_game:
                self.log.info('last ball drained')
                self.end_game()

        ### Go back to first player, increment the game ball
            else:
                self.game.current_player_index = 0
                self.game.ball += 1
                self.start_ball()

        ### not the last player drained
        else:
            self.log.info('not last player drained, going to next player')
            ### move to next player
            self.game.current_player_index += 1
            self.start_ball

    def end_game(self):
        self.log.info('game ended')
        self.game.coils.flipperEnable.disable()
        self.game.reset()
        
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
        self.game.sound.playsound(1)

    def sw_rsStandupCen_active(self, sw):
        self.game.utilities.score(10)
        self.game.sound.playsound(1)

    def sw_rsStandupLower_active(self, sw):
        self.game.utilities.score(10)
        self.game.sound.playsound(1)

#### basic Kicker score handling #####################
        
    def sw_leftKicker_active(self, sw):
        self.game.utilities.score(100)
        self.game.sound.playsound(3)
    
    def sw_rightKicker_active(self,sw):
        self.game.utilities.score(100)
        self.game.sound.playsound(3)
        
#### basic star score handling #######################
    
    def sw_uRStar_active_for_10ms(self,sw):
        self.game.utilities.score(100)
        self.game.sound.playsound(2)
        
    def sw_lRStar_active_for_10ms(self,sw):
        self.game.utilities.score(100)
        self.game.sound.playsound(2)        
        

#### outhole handler #####################################

    def sw_outHole_active_for_1s(self, sw):
        #### Check to see if this is a game ball #########
        if self.game.ball > 0:
            ###the following coils is needed to get VP going
            self.endBall()
        else:
            pass
        
       
