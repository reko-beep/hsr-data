from enum import Enum

class Path(Enum):
    Harmony = "Applies buffs to allies to improve team's combat capabilities"
    Desctruction = "Deals outstanding amounts of damage and possesses great survivability. Suitable for various combat scenarios"
    Hunt = "Deals extraordinary amounts of single-target damage The main damage dealer against Elite Enemies"
    Erudion = "Deals remarkable amounts of multi-target damage. The main damage dealer against group of enemies"
    Nihility = "Applies debuffs to enemies to reduce their combat capabilities"
    Preservation = "Possesses powerful defensive abilities to protect allies in various ways"
    Abundance = "Heals allies and restores HP to them."

    def describe(self):
        return self.value

if __name__ == "__main__":
    path = Path.Harmony
    print(path.describe())