# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackSkill
from minihack.envs import register


class MiniHackQuestEasy(MiniHackSkill):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 500,
        autopickup: bool = True,
        **other,
    ):
        super().__init__(
            *args,
            des_file="quest_easy.des",
            max_episode_steps=max_episode_steps,
            autopickup=autopickup,
            **other,
        )


class MiniHackQuestMedium(MiniHackSkill):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 1000,
        autopickup: bool = True,
        character: str = "kni-hum-law-fem",  # tested on human knight
        **other,
    ):
        super().__init__(
            *args,
            des_file="quest_medium.des",
            max_episode_steps=max_episode_steps,
            autopickup=autopickup,
            character=character,
            **other,
        )


class MiniHackQuestHard(MiniHackSkill):
    def __init__(self, *args, max_episode_steps: int = 1000, **other):
        super().__init__(
            *args,
            des_file="quest_hard.des",
            max_episode_steps=max_episode_steps,
            **other,
        )


register(
    id="MiniHack-Quest-Easy-v0",
    entry_point="minihack.envs.skills_quest:MiniHackQuestEasy",
)
register(
    id="MiniHack-Quest-Medium-v0",
    entry_point="minihack.envs.skills_quest:MiniHackQuestMedium",
)
register(
    id="MiniHack-Quest-Hard-v0",
    entry_point="minihack.envs.skills_quest:MiniHackQuestHard",
)
