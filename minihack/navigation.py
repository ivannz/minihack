# Copyright (c) Facebook, Inc. and its affiliates.

from minihack import MiniHack
from minihack.envs import register
from nle import nethack


MOVE_ACTIONS = tuple(nethack.CompassDirection)


class MiniHackNavigation(MiniHack):
    """The base class for MiniHack Navigation tasks.

    Navigation tasks have the following characteristics:

    - Restricted action space: By default, the agent can only move towards
      eight compass directions.
    - Yes/No questions, as well as menu-selection actions are disabled by
      default.
    - The character is set to chaotic human male rogue.
    - Auto-pick is enabled by default.
    - Maximum episode limit defaults to 100 (can be overriden via the
      `max_episode_steps` argument)
    - The default goal is to reach the stair down. This can be changed using
      a reward manager.
    """

    def __init__(
        self,
        *args,
        des_file: str = None,
        # Actions space - move only by default
        actions: tuple[int] = MOVE_ACTIONS,
        # Disallowing one-letter menu questions
        allow_all_yn_questions: bool = False,
        # Perform known steps
        allow_all_modes: bool = False,
        # Play with Rogue character by default
        character: str = "rog-hum-cha-mal",
        # Default episode limit
        max_episode_steps: int = 100,
        # remaining kwargs (see `base.MiniHack`)
        **other,
    ):
        super().__init__(
            *args,
            des_file=des_file,
            actions=actions,
            allow_all_yn_questions=allow_all_yn_questions,
            allow_all_modes=allow_all_modes,
            character=character,
            max_episode_steps=max_episode_steps,
            **other,
        )


register(
    id="MiniHack-Navigation-Custom-v0",
    entry_point="minihack.navigation:MiniHackNavigation",
)
