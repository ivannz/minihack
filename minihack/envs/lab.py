# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackNavigation, LevelGenerator
from minihack.envs import register


class MiniHackLabyrinth(MiniHackNavigation):
    def __init__(self, *args, max_episode_steps: int = 1000, **other):
        lvl_gen = LevelGenerator(
            map="""
-------------------------------------
|.................|.|...............|
|.|-------------|.|.|.------------|.|
|.|.............|.|.|.............|.|
|.|.|----------.|.|.|------------.|.|
|.|.|...........|.|.............|.|.|
|.|.|.|----------.|-----------|.|.|.|
|.|.|.|...........|.......|...|.|.|.|
|.|.|.|.|----------------.|.|.|.|.|.|
|.|.|.|.|.................|.|.|.|.|.|
|.|.|.|.|.-----------------.|.|.|.|.|
|.|.|.|.|...................|.|.|.|.|
|.|.|.|.|--------------------.|.|.|.|
|.|.|.|.......................|.|.|.|
|.|.|.|-----------------------|.|.|.|
|.|.|...........................|.|.|
|.|.|---------------------------|.|.|
|.|...............................|.|
|.|-------------------------------|.|
|...................................|
-------------------------------------
""",
            lit=True,
        )
        lvl_gen.set_start_pos((19, 1))
        lvl_gen.add_goal_pos((19, 7))

        des_file = lvl_gen.get_des()

        super().__init__(
            *args,
            des_file=des_file,
            max_episode_steps=max_episode_steps,
            **other,
        )


class MiniHackLabyrinthSmall(MiniHackNavigation):
    def __init__(self, *args, max_episode_steps: int = 400, **other):
        lvl_gen = LevelGenerator(
            map="""
--------------------
|.......|.|........|
|.-----.|.|.-----|.|
|.|...|.|.|......|.|
|.|.|.|.|.|-----.|.|
|.|.|...|....|.|.|.|
|.|.--------.|.|.|.|
|.|..........|...|.|
|.|--------------|.|
|..................|
--------------------
""",
            lit=True,
        )
        lvl_gen.set_start_pos((9, 1))
        lvl_gen.add_goal_pos((14, 5))

        des_file = lvl_gen.get_des()

        super().__init__(
            *args,
            des_file=des_file,
            max_episode_steps=max_episode_steps,
            **other,
        )


register(
    id="MiniHack-Labyrinth-Big-v0",
    entry_point="minihack.envs.lab:MiniHackLabyrinth",
)

register(
    id="MiniHack-Labyrinth-Small-v0",
    entry_point="minihack.envs.lab:MiniHackLabyrinthSmall",
)
