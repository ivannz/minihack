# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackSkill, LevelGenerator, RewardManager
from minihack.envs import register


class MiniHackWoDEasy(MiniHackSkill):
    """Environment for "Wand of death" task."""

    def __init__(
        self,
        *args,
        autopickup: bool = True,
        max_episode_steps: int = 50,
        **other,
    ):
        map = """
|----------
|.........+
|----------
"""
        lvl_gen = LevelGenerator(map=map, lit=True)
        lvl_gen.set_start_pos((1, 1))

        lvl_gen.add_object(
            name="death",
            symbol="/",
            cursestate="blessed",
            place=(1, 1),
        )

        lvl_gen.add_monster(
            "minotaur",
            args=("asleep",),
            place=(9, 1),
        )

        rwrd_mngr = RewardManager()
        rwrd_mngr.add_kill_event("minotaur")

        super().__init__(
            *args,
            des_file=lvl_gen.get_des(),
            autopickup=autopickup,
            max_episode_steps=max_episode_steps,
            reward_manager=rwrd_mngr,
            **other,
        )


class MiniHackWoDMedium(MiniHackSkill):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 150,
        **other,
    ):
        map = """
|---------------------------|
|...........................|
|---------------------------|
"""
        lvl_gen = LevelGenerator(map=map, lit=True)

        lvl_gen.set_start_pos((1, 1))
        lvl_gen.add_goal_pos((27, 1))

        lvl_gen.add_object(
            name="death",
            symbol="/",
            cursestate="blessed",
            place=(2, 1),
        )

        lvl_gen.add_monster(
            "minotaur",
            args=("asleep",),
            place=(26, 1),
        )

        super().__init__(
            *args,
            des_file=lvl_gen.get_des(),
            max_episode_steps=max_episode_steps,
            **other,
        )


class MiniHackWoDHard(MiniHackSkill):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 400,
        **other,
    ):
        map = """
|---------------------------|
|...........................|
|.....|---------------------|
|.....|
|.....|
|-----|
"""
        lvl_gen = LevelGenerator(map=map, lit=True)

        lvl_gen.set_start_rect((1, 1), (5, 5))
        lvl_gen.add_goal_pos((27, 1))

        lvl_gen.set_area_variable(
            "$safe_room",
            "fillrect",
            1,
            1,
            5,
            5,
        )

        lvl_gen.add_object_area(
            "$safe_room",
            name="death",
            symbol="/",
            cursestate="blessed",
        )

        lvl_gen.add_monster(
            "minotaur",
            place=(26, 1),
        )

        super().__init__(
            *args,
            des_file=lvl_gen.get_des(),
            max_episode_steps=max_episode_steps,
            **other,
        )


class MiniHackWoDPro(MiniHackSkill):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 1000,
        **other,
    ):
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

        lvl_gen.add_monster(
            name="minotaur",
            place=(19, 9),
        )

        lvl_gen.add_object(
            name="death",
            symbol="/",
            cursestate="blessed",
        )

        super().__init__(
            *args,
            des_file=lvl_gen.get_des(),
            max_episode_steps=max_episode_steps,
            **other,
        )


register(
    id="MiniHack-WoD-Easy-v0",
    entry_point="minihack.envs.skills_wod:MiniHackWoDEasy",
)

register(
    id="MiniHack-WoD-Medium-v0",
    entry_point="minihack.envs.skills_wod:MiniHackWoDMedium",
)
register(
    id="MiniHack-WoD-Hard-v0",
    entry_point="minihack.envs.skills_wod:MiniHackWoDHard",
)
register(
    id="MiniHack-WoD-Pro-v0",
    entry_point="minihack.envs.skills_wod:MiniHackWoDPro",
)
