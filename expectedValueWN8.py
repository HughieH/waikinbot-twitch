import requests

raw_xvm_data = requests.get("https://static.modxvm.com/wn8-data-exp/json/wn8exp.json").json()["data"]
tank_to_expected = {tank["IDNum"]: tank for tank in raw_xvm_data}
# {1: {'IDNum': 1, 'expDef': 1.133, 'expFrag': 0.978, 'expSpot': 1.377, 'expDamage': 486.793, 'expWinRate': 54.914}, 
# 33: {'IDNum': 33, 'expDef': 1.194, 'expFrag': 1.24, 'expSpot': 1.559, 'expDamage': 614.322, 'expWinRate': 55.985}....

# wn8 calculator

class ExpectedValueSerializer:

    def __init__(self, tank_ID):
        
        try:
            self.expDamage = tank_to_expected[tank_ID]["expDamage"]
            self.expDef = tank_to_expected[tank_ID]["expDef"]
            self.expFrag = tank_to_expected[tank_ID]["expFrag"]
            self.expSpot = tank_to_expected[tank_ID]["expSpot"]
            self.expWinRate = tank_to_expected[tank_ID]["expWinRate"]
        except KeyError:
            pass

    def print(self):
        print(self.expDamage)
        print(self.expDef)
        print(self.expFrag)
        print(self.expSpot)
        print(self.expWinRate)

def calculateWn8 (id, avgDamage, avgDef, avgFrag, avgSpots, winrate):
    
    expValues = ExpectedValueSerializer(id)

    rDAMAGE   = avgDamage / expValues.expDamage
    rSPOT     = avgSpots / expValues.expSpot
    rFRAG     = avgFrag / expValues.expFrag
    rDEF      = avgDef / expValues.expDef
    rWIN      = winrate / expValues.expWinRate

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


#test_chieftian = calculateWn8 (57937, (3366719/691), (514/691), (1477/691), (1183/691), ((458/691) * 100))
#print(test_chieftian)