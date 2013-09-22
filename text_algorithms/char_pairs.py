# Determine Character Pairs of a String and Return the Pairs in a List
# ex: United = ['un','ni', 'it', 'te', 'ed']
class CharPairs:
    def __init__(self, string):
        self.string = string.lower()
        # 1.) Create a dictionary of characters.
        self.create_char_list()
        # 2.) Turn the dictionary into character pairs.
        self.create_char_pairs()
        
    def create_char_list(self):
        self.strChars = {}
        for (counter, char) in enumerate(self.string):
            self.strChars[counter] = char
    
    def create_char_pairs(self):
        stringLength = self.string.__len__()
        self.charPairs = []
        for (counter, (key, char)) in enumerate(self.strChars.iteritems()):
            if counter < (stringLength - 1):
                nxt = counter + 1
                pair = char + self.strChars[nxt]
                self.charPairs.append(pair)
    
    def getCharPairs(self):
        return self.charPairs
        
    def getCharPairCount(self):
        return self.charPairs.__len__()    