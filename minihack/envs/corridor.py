# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackNavigation
from minihack.envs import register
from nle import nethack

MOVE_ACTIONS = tuple(nethack.CompassDirection)
NAVIGATE_ACTIONS = MOVE_ACTIONS + (
    nethack.Command.OPEN,
    nethack.Command.KICK,
    nethack.Command.SEARCH,
)


class MiniHackCorridor(MiniHackNavigation):
    """Environment for "corridor" task.

    The agent has to navigate itself through randomely generated corridors that
    connect several rooms and find the goal.
    """

    def __init__(
        self,
        *args,
        des_file,
        max_episode_steps: int = 1000,
        actions: tuple[int] = NAVIGATE_ACTIONS,
        **other
    ):
        super().__init__(
            *args,
            des_file=des_file,
            max_episode_steps=max_episode_steps,
            actions=actions,
            **other
        )


class MiniHackCorridor2(MiniHackCorridor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="corridor2.des", **kwargs)


class MiniHackCorridor3(MiniHackCorridor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="corridor3.des", **kwargs)


class MiniHackCorridor5(MiniHackCorridor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="corridor5.des", **kwargs)


register(
    id="MiniHack-Corridor-R2-v0",
    entry_point="minihack.envs.corridor:MiniHackCorridor2",
)
register(
    id="MiniHack-Corridor-R3-v0",
    entry_point="minihack.envs.corridor:MiniHackCorridor3",
)
register(
    id="MiniHack-Corridor-R5-v0",
    entry_point="minihack.envs.corridor:MiniHackCorridor5",
)
