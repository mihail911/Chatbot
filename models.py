"""
Some really basic system agent files
"""

import random


class Agent(object):
    def __init__(self):
        """Do any preprocessing setup for agent such as model loading, etc."""
        pass
    
    def respond(self, user_txt):
        raise NotImplementedError


class EchoAgent(Agent):
    def __init__(self):
        pass
 
    def respond(self, user_txt):
        return user_txt


class RandomAgent(Agent):
    def __init__(self):
         self.corpus = ["I like you", "You're pretty cool", "I like cats", "I am a fan of deep learning", 
                   "I like lollipops", "I think dialogue is an interesting research direction", "I think dropout actually isn't that cool"]

    
    def respond(self, user_txt):
         return random.choice(self.corpus) 
