class ColorIcon:

    def __init__(self, player_wn8, player_wr = 0, player_wg_rating = 0, player_server = "na"):
        # initialized with set values

        self.wn8 = player_wn8
        self.server = player_server
        self.wr = player_wr
        self.wgRating = player_wg_rating
        
    def colorWN8(self):

        if self.wn8 >= 4000:
            return "🟪"
        elif (self.wn8 >= 3000) and (self.wn8 < 4000):
            return "🟣"
        elif (self.wn8 >= 2000) and (self.wn8 < 3000):
            return "🔵"
        elif (self.wn8 >= 1200) and (self.wn8 < 2000):
            return "🟢"
        elif (self.wn8 >= 750) and (self.wn8 < 1200):
            return "🟡"
        elif (self.wn8 >= 450) and (self.wn8 < 750):
            return "🟠"
        elif (self.wn8 < 450):
            return "🍅"
    
    def colorWR(self):
        
        if self.wr >= 65:
            return "🟪"
        elif (self.wr >= 58) and (self.wr < 65):
            return "🟣"
        elif (self.wr >= 55) and (self.wr < 58):
            return "🔵"
        elif (self.wr >= 51) and (self.wr < 55):
            return "🟢"
        elif (self.wr >= 48) and (self.wr < 51):
            return "🟡"
        elif (self.wr >= 46) and (self.wr < 48):
            return "🟠"
        elif (self.wr < 46):
            return "🍅"

    def colorWGRating(self):
        if self.wgRating >= 11000:
            return "🟪"
        elif (self.wgRating >= 9000) and (self.wgRating < 11000):
            return "🟣"
        elif (self.wgRating >= 7000) and (self.wgRating < 9000):
            return "🔵"
        elif (self.wgRating >= 5000) and (self.wgRating < 7000):
            return "🟢"
        elif (self.wgRating >= 3000) and (self.wgRating < 5000):
            return "🟡"
        elif (self.wgRating >= 2000) and (self.wgRating < 3000):
            return "🟠"
        elif (self.wgRating < 2000):
            return "🍅"
    
    def serverIcon(self):

        if self.server == "na":
            return ":flag_us:"
        if self.server == "eu":
            return ":flag_eu:"
        if self.server == "ru":
            return ":flag_ru:"
        if self.server == "asia":
            return ":flag_sg:"

#test = ColorIcon(1000)
#print(test.colorWN8())