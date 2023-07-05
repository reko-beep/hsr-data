from enum import Enum

class Path(Enum):
    HARMONY = "Applies buffs to allies to improve team's combat capabilities"
    DESTRUCTION = "Deals outstanding amounts of damage and possesses great survivability. Suitable for various combat scenarios"
    HUNT = "Deals extraordinary amounts of single-target damage The main damage dealer against Elite Enemies"
    ERUDITION = "Deals remarkable amounts of multi-target damage. The main damage dealer against group of enemies"
    NIHILITY = "Applies debuffs to enemies to reduce their combat capabilities"
    PRESERVATION = "Possesses powerful defensive abilities to protect allies in various ways"
    ABUNDANCE = "Heals allies and restores HP to them."

    def describe(self):
        return self.value

if __name__ == "__main__":
    path = Path.HARMONY
    print(path.describe())