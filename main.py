# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits

class Bot(GoslingAgent):
    # This function runs every in-game tick (every time the game updates anything)

    def run(self):
        if self.intent is not None:
            return
        d1 = abs(self.ball.location.y - self.foe_goal.location.y)
        d2 = abs(self.me.location.y - self.foe_goal.location.y)
        is_in_front_of_ball = d1 > d2
        if self.kickoff_flag:
        # set_intent tells the bot what it's trying to do
            self.set_intent(kickoff())
            return
        if is_in_front_of_ball:
            self.set_intent(goto(self.friend_goal.location))
            return 
        self.set_intent(short_shot(self.foe_goal.location))

        target = {
            'at_openent_goal': (self.foe_goal.left_post, self.foe_goal.left_post),
            'away_from_our_net': (self.friend_goal.right_post, self.friend_goal.left_post)
        }
        hits = find_hits(self, target)
        if len(hits['at_openent_goal']) > 0:
            self.set_intent(hits['at_openent_goal'][0])
            return
        if len(hits['away_from_our_net']) > 0:
            self.set_intent(hits['away_from_our_net'][0])
            return
        
        if self.me.boost > 99:
            self.set_intent(short_shot(self.foe_goal.location))
            return

        availableBoost = [boost for boost in self.boosts if boost.large and boost.active]
        closestBoost = None
        closestDistance = 10000
        for boost in availableBoost:
            distance = (self.me.location - boost.location).magnitude()
            if closestBoost is None or distance < closestDistance:
                closestBoost = boost
                closestDistance = distance

        if closestBoost is not None:
            self.set_intent(goto(closestBoost.location))
            return
        




