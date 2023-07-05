
from typing import Optional, Union, List, NewType
from enum import Enum

class Element(Enum):
    QUANTUM = "Using Quantum attacks to inflict Weakness Break will deal Quantum DMG and cause Entanglement, delaying the enemy's action and dealing Additional Quantum DMG to the affected enemy at the start of the next turn. When the enemy is hit, this extra DMG will increase."
    PHYSICAL = "Using Physical attacks to trigger Weakness Break will deal Physical DMG and apply Bleed effect, dealing Physical DoT."
    FIRE = "Using Fire attacks to trigger Weakness Break will deal Fire DMG and apply the Burn effect, dealing Fire DoT."
    ICE = "Using Ice Aattacks to trigger Weakness Break will deal Ice DMG and Freeze the target, immobilizing the enmy and dealing Additional Ice DMG."
    LIGHTNING = "Using Lightning attacks to trigger Weakness Break will deal Lightning DMG and apply the Shock effect, dealing Lightning DoT."
    WIND = "Using Wind attacks to trigger Weakness Break will deal Wind DMG and apply the Wind Shear effect, dealing Wind DoT."
    IMAGINARY = "When using an Imaginary attack to inflict Weakness Break on target enemy, the attack will deal Imaginary DMG and additionaly inflicts Imprisonment. Imprisoned enemies suffer from delayed actions and SPD Reduction."

    def describe(self):
        return self.value

if __name__ == "__main__":
    elem = Element.WIND
    print(elem.describe())