# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackNavigation, LevelGenerator
from minihack.envs import register


class MiniHackFightCorridor(MiniHackNavigation):
    def __init__(
        self,
        *args,
        lit: bool = True,
        # Play with human knight character by default
        character: str = "kni-hum-law-fem",
        # Default episode limit
        max_episode_steps: int = 350,
        # remaining kwargs (see `MiniHackNavigation`)
        **other,
    ):
        map = """
-----       ----------------------
|...|       |....................|
|....#######.....................|
|...|       |....................|
-----       ----------------------
"""
        lvl_gen = LevelGenerator(map=map, lit=lit)
        lvl_gen.set_start_rect((1, 1), (3, 3))
        lvl_gen.add_monster(name="giant rat", place=(30, 1))
        lvl_gen.add_monster(name="giant rat", place=(30, 2))
        lvl_gen.add_monster(name="giant rat", place=(30, 3))
        lvl_gen.add_monster(name="giant rat", place=(31, 1))
        lvl_gen.add_monster(name="giant rat", place=(31, 2))
        lvl_gen.add_monster(name="giant rat", place=(31, 3))
        lvl_gen.add_goal_pos((32, 2))

        super().__init__(
            *args,
            des_file=lvl_gen.get_des(),
            character=character,
            max_episode_steps=max_episode_steps,
            **other,
        )


class MiniHackFightCorridorDark(MiniHackFightCorridor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, lit=False, **kwargs)


register(
    id="MiniHack-CorridorBattle-v0",
    entry_point="minihack.envs.fightcorridor:MiniHackFightCorridor",
)

register(
    id="MiniHack-CorridorBattle-Dark-v0",
    entry_point="minihack.envs.fightcorridor:MiniHackFightCorridorDark",
)
