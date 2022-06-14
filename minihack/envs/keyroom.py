# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackNavigation
from minihack.level_generator import PATH_DAT_DIR
from minihack.envs import register
from nle.nethack import Command
from nle import nethack
import os

MOVE_ACTIONS = tuple(nethack.CompassDirection)
APPLY_ACTIONS = tuple(list(MOVE_ACTIONS) + [Command.PICKUP, Command.APPLY])


class KeyRoomGenerator:
    def __init__(self, room_size, subroom_size, lit):
        des_path = os.path.join(PATH_DAT_DIR, "key_and_door_tmp.des")
        with open(des_path) as f:
            df = f.read()

        df = df.replace("RS", str(room_size))
        df = df.replace("SS", str(subroom_size))
        if not lit:
            df = df.replace("lit", str("unlit"))

        self.des_file = df

    def get_des(self):
        return self.des_file


class MiniHackKeyDoor(MiniHackNavigation):
    """Environment for "key and door" task."""

    def __init__(
        self,
        *args,
        des_file,
        charachter: str = "rog-hum-cha-mal",
        max_episode_steps: int = 200,
        actions: tuple[int] = APPLY_ACTIONS,
        autopickup: bool = False,
        **other
    ):
        super().__init__(
            *args,
            des_file=des_file,
            charachter=charachter,
            max_episode_steps=max_episode_steps,
            actions=actions,
            autopickup=autopickup,
            **other
        )

    def step(self, action: int):
        # If apply action is chosen
        if self._actions[action] == Command.APPLY:
            key_key = self.key_in_inventory("key")
            # if key is in the inventory
            if key_key is not None:
                # Check if there is a closed door nearby
                dir_key = self.get_object_direction("closed door")
                if dir_key is not None:
                    # Perform the following NetHack steps
                    self.env.step(Command.APPLY)  # press apply
                    self.env.step(ord(key_key))  # choose key from the inv
                    self.env.step(dir_key)  # select the door's direction
                    obs, done = self.env.step(ord("y"))  # press y
                    obs, done = self._perform_known_steps(
                        obs, done, exceptions=True
                    )
                    # Make sure the door is open
                    while True:
                        obs, done = self.env.step(dir_key)
                        obs, done = self._perform_known_steps(
                            obs, done, exceptions=True
                        )
                        if (
                            self.get_object_direction("closed door", obs)
                            is None
                        ):
                            break

        obs, reward, done, info = super().step(action)
        return obs, reward, done, info


class MiniHackKeyRoom(MiniHackKeyDoor):
    def __init__(self, *args, room_size, subroom_size, lit, **other):
        lev_gen = KeyRoomGenerator(room_size, subroom_size, lit)
        des_file = lev_gen.get_des()
        super().__init__(*args, des_file=des_file, **other)


class MiniHackKeyRoom5x5Fixed(MiniHackKeyDoor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="key_and_door.des", **kwargs)


class MiniHackKeyRoom5x5(MiniHackKeyRoom):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, room_size=5, subroom_size=2, lit=True, **kwargs
        )


class MiniHackKeyRoom5x5Dark(MiniHackKeyRoom):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, room_size=5, subroom_size=2, lit=False, **kwargs
        )


class MiniHackKeyRoom15x15(MiniHackKeyRoom):
    def __init__(self, *args, max_episode_steps: int = 400, **other):
        super().__init__(
            *args,
            room_size=15,
            subroom_size=5,
            lit=True,
            max_episode_steps=max_episode_steps,
            **other
        )


class MiniHackKeyRoom15x15Dark(MiniHackKeyRoom):
    def __init__(self, *args, max_episode_steps: int = 400, **other):
        super().__init__(
            *args,
            room_size=15,
            subroom_size=5,
            lit=False,
            max_episode_steps=max_episode_steps,
            **other
        )


register(
    id="MiniHack-KeyRoom-Fixed-S5-v0",
    entry_point="minihack.envs.keyroom:MiniHackKeyRoom5x5Fixed",
)
register(
    id="MiniHack-KeyRoom-S5-v0",
    entry_point="minihack.envs.keyroom:MiniHackKeyRoom5x5",
)
register(
    id="MiniHack-KeyRoom-S15-v0",
    entry_point="minihack.envs.keyroom:MiniHackKeyRoom15x15",
)
register(
    id="MiniHack-KeyRoom-Dark-S5-v0",
    entry_point="minihack.envs.keyroom:MiniHackKeyRoom5x5Dark",
)
register(
    id="MiniHack-KeyRoom-Dark-S15-v0",
    entry_point="minihack.envs.keyroom:MiniHackKeyRoom15x15Dark",
)
