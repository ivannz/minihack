# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackNavigation
from minihack.envs import register


class MiniHackHideAndSeekMapped(MiniHackNavigation):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 200,
        **other,
    ):
        super().__init__(
            *args,
            des_file="hidenseek_mapped.des",
            max_episode_steps=max_episode_steps,
            **other,
        )


class MiniHackHideAndSeek(MiniHackNavigation):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 200,
        **other,
    ):
        super().__init__(
            *args,
            des_file="hidenseek.des",
            max_episode_steps=max_episode_steps,
            **other,
        )


class MiniHackHideAndSeekLava(MiniHackNavigation):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 200,
        **other,
    ):
        super().__init__(
            *args,
            des_file="hidenseek_lava.des",
            max_episode_steps=max_episode_steps,
            **other,
        )


class MiniHackHideAndSeekBig(MiniHackNavigation):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 400,
        **other,
    ):
        super().__init__(
            *args,
            des_file="hidenseek_big.des",
            max_episode_steps=max_episode_steps,
            **other,
        )


register(
    id="MiniHack-HideNSeek-Mapped-v0",
    entry_point="minihack.envs.hidenseek:MiniHackHideAndSeekMapped",
)
register(
    id="MiniHack-HideNSeek-v0",
    entry_point="minihack.envs.hidenseek:MiniHackHideAndSeek",
)
register(
    id="MiniHack-HideNSeek-Lava-v0",
    entry_point="minihack.envs.hidenseek:MiniHackHideAndSeekLava",
)
register(
    id="MiniHack-HideNSeek-Big-v0",
    entry_point="minihack.envs.hidenseek:MiniHackHideAndSeekBig",
)
