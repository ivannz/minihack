# Copyright (c) Facebook, Inc. and its affiliates.

from minihack import MiniHack
from minihack.base import MH_DEFAULT_OBS_KEYS
from minihack.envs import register


# make sure to include inv_* related fields
DEFAULT_OBS_KEYS = (
    *MH_DEFAULT_OBS_KEYS,
    "inv_strs",
    "inv_letters",
)


class MiniHackSkill(MiniHack):
    """The base class for MiniHack Skill Acquisition tasks.

    Navigation tasks have the following characteristics:

    - The full action space is used.
    - Yes/No questions are enabled, but the menu-selection actions are disabled
      by default.
    - The character is set to a neutral human male caveman.
    - Maximum episode limit defaults to 250 (can be overriden via the
      `max_episode_steps` argument)
    - The default goal is to reach the stair down. This can be changed using
      a reward manager.
    - Auto-pick is disabled by default.
    - Inventory strings and corresponding letter are also included as part of
      the agent observations.
    """

    def __init__(
        self,
        *args,
        des_file,
        # Autopickup off by defautlt
        autopickup: bool = False,
        # Allowing one-letter menu questions
        allow_all_yn_questions: bool = True,
        # Perform know steps
        allow_all_modes: bool = False,
        # Play with Caveman character by default
        character: str = "cav-hum-new-mal",
        # Default episode limit
        max_episode_steps: int = 250,
        # observations with inventory data
        observation_keys: tuple = DEFAULT_OBS_KEYS,
        # remaining kwargs (see `MiniHack`)
        **other,
    ):
        super().__init__(
            *args,
            des_file=des_file,
            autopickup=autopickup,
            allow_all_yn_questions=allow_all_yn_questions,
            allow_all_modes=allow_all_modes,
            character=character,
            max_episode_steps=max_episode_steps,
            observation_keys=observation_keys,
            **other,
        )


register(
    id="MiniHack-Skill-Custom-v0",
    entry_point="minihack.skills:MiniHackSkill",
)
