""" File containing the code for the cats that are in Calico"""


class Cat:
    def __init__(self, name, score, num_of_tiles):
        self.name = name
        self.score = score
        self.num_of_tiles = num_of_tiles
        self.pattern_1 = None
        self.pattern_2 = None
        self.num_of_cats = 0

    def get_patterns(self):
        """
        Function that gets the patterns that the cat was assigned and returns
        them in a list, to simplify the code
        :return:
        """
        return [self.pattern_1, self.pattern_2]
