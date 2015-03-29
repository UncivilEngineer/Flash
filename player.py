#####################################################################################
## Player stats setup for FLASH
## A P-ROC Project by Uncivil Engineer
## Built on PyProcGame from Adam Preble, Gerry Stellenberg Mark Sunnucks
## Thanks to Scott Danesi for inspiration from his Earthshaker Aftershock, and Mark
## Sunnucks for his F14 second sortie code
#####################################################################################


#################################################################################
#
#     ___  __                    ______       __
#    / _ \/ /__ ___ _____ ____  / __/ /____ _/ /____
#   / ___/ / _ `/ // / -_) __/ _\ \/ __/ _ `/ __(_-<
#  /_/  /_/\_,_/\_, /\__/_/   /___/\__/\_,_/\__/___/
#              /___/
#################################################################################

import procgame.game

class Flashplayer(procgame.game.Player):

    def __init__(self, name):
        super(Flashplayer, self).__init__(name)
        self.name = name
### Create Player Stats Array ############################
        self.player_stats = {}

### General Stats ########################################
        self.player_stats['display_name'] = ' '
        self.player_stats['ball_in_play']=False
        self.player_stats['extra_balls']=0
        self.player_stats['extra_ball_lit']=False

### Ball Saver ###########################################
        self.player_stats['ballsave_active']=False
        self.player_stats['ballsave_timer_active']=False

### Bonus and Status #####################################
        self.player_stats['bonus_x']=1
        self.player_stats['bonus']=1000
        self.player_stats['eject_hole']=1
        
### Jackpot Stats ########################################
        self.player_stats['thunder']=False
        self.player_stats['lightning']=False
        self.player_stats['tempest']=False
        self.player_stats['super_flash']=False

### Skillshot ############################################
        self.player_stats['skillshot_active']=False
        self.player_stats['skillshot_x']=1

			

