

import procgame
import pinproc
from procgame import *
import logging

class Sound(game.Mode):	
    """docstring for SoundMode"""

    soundCount = 1
    
    def __init__(self, game, priority):
        super(Sound, self).__init__(game, priority)
        self.log = logging.getLogger('flash.sound')
        self.log.info("attract mode initialized")

    def mode_started(self):
        pass
    
    ############################
    # Sound Test
    ############################
    #Sound test was written to try to determine what sounds exist at what address on the 
    # William type 1 sound board.  The whole purpose of this function is to cycle
    # throught the sounds (1 to 31) and play each one.
    def soundtest(self):
        self.log.info("sound test called, x is: " +str(self.soundCount))
        if self.soundCount < 32:
            self.playsound(self.soundCount)
            self.delay(name='soundtest', event_type=None, delay=2, handler=self.dosoundtest)
        else:
            self.soundCount = 1
    
    def dosoundtest(self):
        self.soundCount = self.soundCount +1
        self.soundtest()
        

#############################
#### sound definitions ######
#############################

    def playsound(self, x):

        #### this function is valid for intergers between 0 and 31
        if x > 0 and x <= 31:

            #### first we convert the input request to a binary number in the form of a string
            #### this call should give a string of 0s and 1s five digits long.  Special thanks
            #### to google for this solution

            inputString = bin(x)[2:].zfill(5)
            self.log.info("call for sound " +str(x))
            print("playing sound " +str(x))

            ### Now check for 1s, and schedule coils if it is present, note we are working
            ### from right to left, starting at index 4, there has to be a seperate if call
            ### for each digit so none get skipped

            if inputString[4] == '1':
                self.game.coils.soundC09.schedule(schedule=0xffff000, cycle_seconds=1, now=False)

            if inputString[3] == '1':
                self.game.coils.soundC10.schedule(schedule=0xffff000, cycle_seconds=1, now=False)
            
            if inputString[2] == '1':
                self.game.coils.soundC11.schedule(schedule=0xffff000, cycle_seconds=1, now=False)
            
            if inputString[1] == '1':
                self.game.coils.soundC12.schedule(schedule=0xffff000, cycle_seconds=1, now=False)

            if inputString[0] == '1':
                self.game.coils.soundC13.schedule(schedule=0xffff000, cycle_seconds=1, now=False)
        else:
            self.log.info('bad call to playsound ' +str(x)+ 'was sent')     
