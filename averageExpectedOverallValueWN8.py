import requests

raw_xvm_data = requests.get("https://static.modxvm.com/wn8-data-exp/json/wn8exp.json").json()["data"]
tank_to_expected = {tank["IDNum"]: tank for tank in raw_xvm_data}
# {1: {'IDNum': 1, 'expDef': 1.133, 'expFrag': 0.978, 'expSpot': 1.377, 'expDamage': 486.793, 'expWinRate': 54.914}, 
# 33: {'IDNum': 33, 'expDef': 1.194, 'expFrag': 1.24, 'expSpot': 1.559, 'expDamage': 614.322, 'expWinRate': 55.985}....

class AverageExpectedValuesSerializer:

    def __init__(self, overall_info):
        self.user_tanks = []
        for tank in overall_info:
            try:
                tank_id = tank["Tank ID"]
                tank_expected_values = tank_to_expected[tank_id].copy()
                tank_expected_values["Indv. Battles"] = tank["Battles"] #adds key indv. battles to dictionary tank_expected_values
                #print(tank_expected_values)
                self.user_tanks.append(tank_expected_values)
            except KeyError:
                pass

        total_exp_damage = total_exp_def = total_exp_frag = total_exp_spot = total_exp_wr = total_battles = 0
        
        for tank in self.user_tanks:
            total_exp_damage += (tank["expDamage"] * tank["Indv. Battles"])
            total_exp_def += (tank["expDef"] * tank["Indv. Battles"])
            total_exp_frag += (tank["expFrag"] * tank["Indv. Battles"])
            total_exp_spot += (tank["expSpot"] * tank["Indv. Battles"])
            total_exp_wr += (tank["expWinRate"] * tank["Indv. Battles"])
            total_battles += tank["Indv. Battles"]

        self.expected_damage = total_exp_damage 
        self.expected_defense_points = total_exp_def 
        self.expected_frags = total_exp_frag 
        self.expected_spots = total_exp_spot 
        self.expected_winrate = total_exp_wr 

    def print(self):
        print(self.expected_damage)
        print(self.expected_defense_points)
        print(self.expected_frags)
        print(self.expected_spots)
        print(self.expected_winrate)

# make parameter for overall_info able to accept more than one data type
def calculateOverallWn8(overall_info, avgDamage, avgDef, avgFrag, avgSpots, winrate):
    
    expected_values = AverageExpectedValuesSerializer(overall_info)

    rDAMAGE   = avgDamage / expected_values.expected_damage
    rSPOT     = avgSpots / expected_values.expected_spots
    rFRAG     = avgFrag / expected_values.expected_frags
    rDEF      = avgDef / expected_values.expected_defense_points
    rWIN      = winrate / expected_values.expected_winrate

    rWINc     = max(0, (rWIN - 0.71) / (1 - 0.71))
    rDAMAGEc  = max(0, (rDAMAGE - 0.22) / (1 - 0.22))
    rFRAGc    = max(0, min(rDAMAGEc + 0.2, (rFRAG - 0.12) / (1 - 0.12)))
    rSPOTc    = max(0, min(rDAMAGEc + 0.1, (rSPOT - 0.38) / (1 - 0.38)))
    rDEFc     = max(0, min(rDAMAGEc + 0.1, (rDEF - 0.1) / (1 - 0.1)))

    WN8 = \
        (980 * rDAMAGEc) +\
        (210 * rDAMAGEc * rFRAGc) +\
        (155 * rFRAGc * rSPOTc) +\
        (75 * rDEFc * rFRAGc) +\
        145 * min(1.8, rWINc)

    return WN8


#test_stats = [{"Tank ID": 57937, "Battles": 13}, {"Tank ID": 15953, "Battles": 10}, {"Tank ID": 15905, "Battles": 8}, {"Tank ID": 15697, "Battles": 3}, {"Tank ID": 13857, "Battles": 2},\
# {"Tank ID": 2433, "Battles": 1}]

#test = calculate_overall_wn8(test_stats, 4633, 0.11, 2.19, 1.57, 62.16)
#print(test)