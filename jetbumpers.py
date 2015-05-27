##########################Jet Bumper game mode for FLASH########################import procgame.game from procgame import * import pinproc  import random import time import sys import localefrom player import *from utilities import *import loggingclass JetBumper(game.Mode):    targetHits = 0    flipperLaneHits = 0     def __init__(self, game, priority):          super(JetBumper, self).__init__(game, priority)        #######set up logging#######        self.log = logging.getLogger('flash.JetBumper')	        self.log.info("JetBumper initialized")    def mode_started(self):        logging.info("JetBumper Mode started!")        self.jetReset()        def jetReset(self):        self.log.info("jet reset called")        self.flipperLaneHits = 0        self.targetHits = 0        self.game.lamps.leftJetBumper.disable()        self.game.lamps.rightJetBumper.disable()        self.game.lamps.lowerJetBumper.disable()        self.game.lamps.right3BonusAdv.disable()        self.game.lamps.left3BonusAdv.disable()        #### Jet Bumper Target handling #####################    def sw_leftTarget_closed_for_10ms(self,sw):        self.targetHits = self.targetHits + 1        self.game.utilities.set_player_stats('bonus', 1000, 'add')        self.game.utilities.score(1000)        ###  Check the jet bumper lights        if self.targetHits == 1:            self.game.lamps.leftJetBumper.enable()        elif self.targetHits == 2:            self.game.lamps.leftJetBumper.enable()            self.game.lamps.rightJetBumper.enable()        elif self.targetHits == 3:            self.game.lamps.leftJetBumper.enable()            self.game.lamps.rightJetBumper.enable()            self.game.lamps.lowerJetBumper.enable()        elif self.targetHits == 4:            self.game.lamps.leftJetBumper.schedule(schedule = 0xff00ff00ff, cycle_seconds = 0, now = False)            self.game.lamps.rightJetBumper.enable()            self.game.lamps.lowerJetBumper.enable()        elif self.targetHits == 5:            self.game.lamps.leftJetBumper.schedule(schedule = 0xff00ff00ff, cycle_seconds = 0, now = False)            self.game.lamps.rightJetBumper.schedule(schedule = 0xff00ff00ff, cycle_seconds = 0, now = False)            self.game.lamps.lowerJetBumper.enable()        elif self.targetHits == 6:            self.game.lamps.leftJetBumper.schedule(schedule = 0xff00ff00ff, cycle_seconds = 0, now = False)            self.game.lamps.rightJetBumper.schedule(schedule = 0xff00ff00ff, cycle_seconds = 0, now = False)            self.game.lamps.lowerJetBumper.schedule(schedule = 0xff00ff00ff, cycle_seconds = 0, now = False)################################################ Jet Bumper switch Handlers#############################################    def sw_leftJetBumper_closed(self, sw):        self.game.sound.playsound(7)        if self.targetHits == 0:            self.game.utilities.score(100)        elif self.targetHits >=1 and self.targetHits < 4:            self.game.utilities.score(1000)        elif self.targetHits >= 4:            self.game.utilities.score(2000)    def sw_rightJetBumper_closed_for_10ms(self, sw):        self.game.sound.playsound(7)        if self.targetHits >= 0 and self.targetHits < 2:            self.game.utilities.score(100)        elif self.targetHits >=2 and self.targetHits < 5:            self.game.utilities.score(1000)        elif self.targetHits >= 5:            self.game.utilities.score(2000)    def sw_lowerJetBumper_closed_for_10ms(self,sw):        self.game.sound.playsound(7)        if self.targetHits >= 0 and self.targetHits < 3:            self.game.utilities.score(100)        elif self.targetHits >=3 and self.targetHits < 6:            self.game.utilities.score(1000)        elif self.targetHits >= 6:            self.game.utilities.score(2000)###################################################### flipper return lane target hit ################################################################                def sw_rightTarget_closed_for_10ms(self,sw):        self.game.utilities.score(1000)        if self.flipperLaneHits == 0:            self.game.lamps.right3BonusAdv.enable()            self.flipperLaneHits = 1        elif self.flipperLaneHits == 1:            self.game.lamps.left3BonusAdv.enable()            self.flipperLaneHits = 2        elif self.flipperLaneHits == 2:            self.game.lamps.right3BonusAdv.schedule(schedule = 0x00ff00ff00, cycle_seconds = 0, now = True)            self.flipperLaneHits = 3        elif self.flipperLaneHits ==3:            self.game.lamps.left3BonusAdv.schedule(schedule = 0x00ff00ff00, cycle_seconds = 0, now = True)            self.flipperLaneHits = 4        else:            self.game.utilities.score(5000)            def sw_rightFRLane_active_for_10ms(self, sw):                if self.flipperLaneHits == 0:            self.game.utilities.score(1000)            self.game.utilities.set_player_stats('bonus', 1000, 'add')        elif self.flipperLaneHits == 1 or self.flipperLaneHits == 2:            self.game.utilities.score(3000)            self.game.utilities.set_player_stats('bonus', 3000, 'add')        elif self.flipperLaneHits == 3 or self.flipperLaneHits == 4:            self.game.utilities.score(6000)            self.game.utilities.set_player_stats('bonus', 6000, 'add')        else:            pass                self.game.bonus.update_bonus_lights_basic()        def sw_leftFRLane_active_for_10ms(self, sw):                if self.flipperLaneHits == 0 or self.flipperLaneHits == 1:            self.game.utilities.score(1000)            self.game.utilities.set_player_stats('bonus', 1000, 'add')        elif self.flipperLaneHits == 2 or self.flipperLaneHits == 3:            self.game.utilities.score(3000)            self.game.utilities.set_player_stats('bonus', 3000, 'add')        elif self.flipperLaneHits == 4:            self.game.utilities.score(6000)            self.game.utilities.set_player_stats('bonus', 6000, 'add')        else:            pass                self.game.bonus.update_bonus_lights_basic()