class QueryError:
    @staticmethod
    def leveldata_outofrange() -> str:
        return "Invalid input. Levels should be in range 20-80 in increments of 10."
