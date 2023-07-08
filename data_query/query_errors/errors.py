class LevelOutOfRangeError(Exception):
    msg = (
        "defaultvalue: 80\nLevelOutOfRange: "
        "level must be int and in range 20-80 with increments of 10."
    )

    def __init__(self, message=msg):
        self.message = message
        super().__init__(self.message)


class LightConeSkillLevelOutOfRange(Exception):
    msg = (
        "defaultvalue: 5\nLightconeSkillLevelError: "
        "level must be int and in range 1-5 with increments of 1."
    )

    def __init__(self, message=msg):
        self.message = message
        super().__init__(self.message)

class SkillLevelOutOfrange(Exception):
    msg = "Input level out of range.\n" \
          "Basic ATK: 1-9\n" \
          "Skill, Ultimate, Talent: 1-15\n" \
          "Technique: 1"
    def __init__(self, message=msg):
        self.message = message
        super().__init__(self.message)