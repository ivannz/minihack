# Copyright (c) Facebook, Inc. and its affiliates.
from minihack.envs import register
from minihack import MiniHackNavigation
from minihack.envs.corridor import NAVIGATE_ACTIONS
from minihack.reward_manager import RewardManager
from nle.nethack import Command

EAT_ACTION = Command.EAT
ACTIONS = tuple(list(NAVIGATE_ACTIONS) + [EAT_ACTION])


def stairs_reward_function(env, previous_observation, action, observation):
    # Agent is on stairs down
    if observation[env._internal_index][4]:
        return 1
    return 0


class MiniHackExploreMaze(MiniHackNavigation):
    """Environment for a memory challenge."""

    def __init__(
        self,
        *args,
        des_file,
        max_episode_steps: int = 500,
        actions: tuple[int] = ACTIONS,
        autopickup: bool = False,
        allow_all_yn_questions: bool = True,
        **other
    ):
        reward_manager = RewardManager()
        reward_manager.add_eat_event(
            "apple",
            reward=0.5,
            repeatable=True,
            terminal_required=False,
            terminal_sufficient=False,
        )
        # Will never be achieved, but insures the environment keeps running
        reward_manager.add_message_event(
            ["Mission Complete."],
            terminal_required=True,
            terminal_sufficient=True,
        )
        reward_manager.add_custom_reward_fn(stairs_reward_function)
        super().__init__(
            *args,
            des_file=des_file,
            reward_manager=reward_manager,
            max_episode_steps=max_episode_steps,
            actions=actions,
            autopickup=autopickup,
            allow_all_yn_questions=allow_all_yn_questions,
            **other,
        )


class MiniHackExploreMazeEasy(MiniHackExploreMaze):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="exploremazeeasy.des", **kwargs)


class MiniHackExploreMazeHard(MiniHackExploreMaze):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="exploremazehard.des", **kwargs)


class MiniHackExploreMazeEasyMapped(MiniHackExploreMaze):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, des_file="exploremazeeasy_premapped.des", **kwargs
        )


class MiniHackExploreMazeHardMapped(MiniHackExploreMaze):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, des_file="exploremazehard_premapped.des", **kwargs
        )


register(
    id="MiniHack-ExploreMaze-Easy-v0",
    entry_point="minihack.envs.exploremaze:MiniHackExploreMazeEasy",
)
register(
    id="MiniHack-ExploreMaze-Hard-v0",
    entry_point="minihack.envs.exploremaze:MiniHackExploreMazeHard",
)
register(
    id="MiniHack-ExploreMaze-Easy-Mapped-v0",
    entry_point="minihack.envs.exploremaze:MiniHackExploreMazeEasyMapped",
)
register(
    id="MiniHack-ExploreMaze-Hard-Mapped-v0",
    entry_point="minihack.envs.exploremaze:MiniHackExploreMazeHardMapped",
)
