def stat_data_max(self) -> Generator[Tuple[str, float], None, None]:
    """
    Returns a generator object containing the base stat data of a
    character at max level.

    stat_data_max = Character("character_name").stat_data_max()
    for data in stat_data_max():
        print(data)
    """
    stat_dict = self.content["levelData"][-1]
    for data, value in stat_dict.items():
        if isinstance(value, list) and len(value) == 0:
            pass
        else:
            yield data, value


def stat_at_max(self) -> dict:
    """
    Returns character's base stat at max level

    stat_data_max = Character("character_name").stat_data_max()
    for data in stat_data_max():
        print(data)
    """
    max_stats: Dict = defaultdict(float)
    for stat, value in self.stat_data_max():
        max_stats[stat] = float(value)
    return dict(max_stats)
