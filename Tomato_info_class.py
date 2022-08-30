import requests

# HELPER FUNCTIONS

def dictComp(list): return {int(tank["id"]): tank for tank in list["recent1000"]["tankStats"]}

class TomatoGGInfo:

    def __init__(self, server, user_name):
        
        self.username = user_name
        self.playerServer = server.lower()
        
        # find account ID using WG's API
        if self.playerServer == "na":
            account_id = ((requests.get("https://api.worldoftanks.com/wot/account/list/?application_id=bd644ca5adf8dc631b1598528a4b7fc1&search=" + self.username)).json())\
            ["data"][0]["account_id"] # DICT value keys for userID
        else:
            account_id = ((requests.get("https://api.worldoftanks." + self.playerServer + "/wot/account/list/?application_id=bd644ca5adf8dc631b1598528a4b7fc1&search=" + self.username)).json())\
            ["data"][0]["account_id"]
        
        self.accountID = account_id

        # tomato.gg 
        if self.playerServer == "na":
            self.tomatoInfo = (requests.get(f"https://tomatobackend.herokuapp.com/api/player/com/{str(self.accountID)}")).json() #
        else:
            tomato_json = requests.get(f"https://tomatobackend.herokuapp.com/api/player/{self.playerServer}/{str(self.accountID)}")
            print(f"Status code is {tomato_json.status_code}")
            # if status code is not 200
            counter = 0
            while tomato_json.status_code != 200:
                counter += 1
                tomato_json = requests.get(f"https://tomatobackend.herokuapp.com/api/player/{self.playerServer}/{str(self.accountID)}")
                print(f"{counter} times pinging API, status code is {tomato_json.status_code}\n")
            self.tomatoInfo = tomato_json.json()
        
        print("QB recent stats initialized")
        self.recentStats = self.tomatoInfo["recents"]

        # Recent stats by battles *includes battles, overall wins, wn8, and has specific tank stats
        self.recent1000 = self.recentStats["recent1000"]
        self.recent1000Tanks = dictComp(self.recentStats) # tank_id from tomato backed is in str format
        self.recent100 = self.recentStats["recent100"]

        # Recent stats by days
        self.recent24hr = self.recentStats["recent24hr"]
        self.recent3days = self.recentStats["recent3days"]
        self.recent7days = self.recentStats["recent7days"]
        self.recent30days = self.recentStats["recent30days"]
        self.recent60days = self.recentStats["recent60days"]

    def WR(self, wins, battles):

        return str(round(((wins/battles) * 100), 2))

    # doesnt work
    def discordRecentsString(self):

        return (f"> **24 hr Recents:** {str(self.recent24hr['overallWN8'])} wn8 | {self.WR(self.recent24hr['wins'], self.recent24hr['battles'])} % WR\n"
        f"> **3 Day Recents:** {str(self.recent3days['overallWN8'])} wn8 | {self.WR(self.recent3days['wins'], self.recent3days['battles'])} % WR\n"
        f"> **7 Day Recents:** {str(self.recent7days['overallWN8'])} wn8 | {self.WR(self.recent7days['wins'], self.recent7days['battles'])} % WR\n"
        f"> **30 Day Recents:** {str(self.recent30days['overallWN8'])} wn8 | {self.WR(self.recent30days['wins'], self.recent30days['battles'])} % WR\n"
        f"> **60 Day Recents:** {str(self.recent60days['overallWN8'])} wn8 | {self.WR(self.recent60days['wins'], self.recent60days['battles'])} % WR\n")

#qb = TomatoGGInfo("eu", "Quickfingers")
#qbTankStats = qb.recent1000Tanks

#print(qb.recent1000Tanks[33])





