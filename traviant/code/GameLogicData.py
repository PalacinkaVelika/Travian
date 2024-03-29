from datetime import datetime, timedelta
class GameLogicData:
    # Game rule logic and data
    def __init__(self):
        self.building_levels = {
            # Mines produce every minute regardles, but the value of how many you get changes
            "coal": {
                "base_production_speed": 1,
                "1": {
                    "cost_coal": 30,
                    "cost_ore": 10,
                    "cost_energy": 0, 
                    "wait_time": timedelta(hours=0, minutes=0, seconds=5),
                    "production_speed_bonus": 1
                },
                "2": {
                    "cost_coal": 50,
                    "cost_ore": 10,
                    "cost_energy": 0, 
                    "wait_time": timedelta(hours=0, minutes=0, seconds=10),
                    "production_speed_bonus": 2
                },
                "3": {
                    "cost_coal": 50,
                    "cost_ore": 10,
                    "cost_energy": 10, 
                    "wait_time": timedelta(hours=0, minutes=1, seconds=5),
                    "production_speed_bonus": 1
                },
                "4": {
                    "cost_coal": 30,
                    "cost_ore": 80,
                    "cost_energy": 10, 
                    "wait_time": timedelta(hours=0, minutes=10, seconds=5),
                    "production_speed_bonus": 1
                },
                "5": {
                    "cost_coal": 30,
                    "cost_ore": 80,
                    "cost_energy": 10, 
                    "wait_time": timedelta(hours=0, minutes=10, seconds=5),
                    "production_speed_bonus": 1
                }
            },
            "ore": {
                "base_production_speed": 1,
                "1": {
                    "cost_coal": 30,
                    "cost_ore": 80,
                    "cost_energy": 10, 
                    "wait_time": timedelta(hours=0, minutes=1, seconds=20),
                    "production_speed_bonus": 1
                },
                "2": {
                    "cost_coal": 30,
                    "cost_ore": 80,
                    "cost_energy": 10, 
                    "wait_time": timedelta(hours=0, minutes=2, seconds=50),
                    "production_speed_bonus": 2
                }
            },
            "energy": {
                "base_production_speed": 1,
                "1": {
                    "cost_coal": 30,
                    "cost_ore": 80,
                    "cost_energy": 0, 
                    "wait_time": timedelta(hours=0, minutes=1, seconds=20),
                    "production_speed_bonus": 1
                },
                "2": {
                    "cost_coal": 30,
                    "cost_ore": 80,
                    "cost_energy": 0, 
                    "wait_time": timedelta(hours=0, minutes=2, seconds=50),
                    "production_speed_bonus": 2
                }
            },
            "academy": {
                "base_time": 1,
                "1": {
                    "cost_coal": 30,
                    "cost_ore": 80,
                    "cost_energy": 10, 
                    "wait_time": timedelta(hours=0, minutes=1, seconds=20),
                    "production_speed_bonus": 1,
                    "stats_bonus": 1
                },
                "2": {
                    "cost_coal": 30,
                    "cost_ore": 80,
                    "cost_energy": 10, 
                    "wait_time": timedelta(hours=0, minutes=2, seconds=50),
                    "production_speed_bonus": 2,
                    "stats_bonus": 1
                }
            },
            "machinery": {
                "base_time": 1,
                "1": {
                    "cost_coal": 30,
                    "cost_ore": 80,
                    "cost_energy": 10, 
                    "wait_time": timedelta(hours=0, minutes=1, seconds=20),
                    "production_speed_bonus": 1,
                    "stats_bonus": 1
                },
                "2": {
                    "cost_coal": 30,
                    "cost_ore": 80,
                    "cost_energy": 10, 
                    "wait_time": timedelta(hours=0, minutes=2, seconds=50),
                    "production_speed_bonus": 2,
                    "stats_bonus": 1
                }
            },
            "specialists": {
                "base_time": 1,
                "1": {
                    "cost_coal": 30,
                    "cost_ore": 80,
                    "cost_energy": 10, 
                    "wait_time": timedelta(hours=0, minutes=1, seconds=20),
                    "production_speed_bonus": 1,
                    "stats_bonus": 1
                },
                "2": {
                    "cost_coal": 30,
                    "cost_ore": 80,
                    "cost_energy": 10, 
                    "wait_time": timedelta(hours=0, minutes=2, seconds=50),
                    "production_speed_bonus": 2,
                    "stats_bonus": 1
                }
            }
        }
        self.research_levels = {
            "soldier_damage": {
                "1": {
                    "bonus" : 1.5
                },
                "2": {
                    "bonus" : 2
                }
            },
            "tank_damage": {
                "1": {
                    "bonus" : 1.5
                },
                "2": {
                    "bonus" : 2
                }
            },
            "specialist_damage": {
                "1": {
                    "bonus" : 1.5
                },
                "2": {
                    "bonus" : 2
                }
            }
        }
        
    # attacking army vs defending army
    def battle(self):
        pass