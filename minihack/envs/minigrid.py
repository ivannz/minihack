# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackNavigation, LevelGenerator
from nle.nethack import Command, CompassDirection
from minihack.envs import register
import gym
from nle import nethack


MOVE_ACTIONS = tuple(nethack.CompassDirection)
MOVE_AND_KICK_ACTIONS = MOVE_ACTIONS + tuple(
    [nethack.Command.OPEN, nethack.Command.KICK]
)


class MiniGridHack(MiniHackNavigation):
    def __init__(
        self,
        *args,
        env_name,
        num_mon: int = 0,
        num_trap: int = 0,
        door_state: str = "closed",
        lava_walls: bool = False,
        **other
    ):
        # Only ask users to install gym-minigrid if they actually need it
        try:
            import gym_minigrid  # noqa: F401
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "To use MiniGrid-based environments, please install"
                " gym-minigrid: pip3 install gym-minigrid"
            ) from None

        self.minigrid_env = gym.make(env_name)
        self.num_mon = num_mon
        self.num_trap = num_trap
        self.door_state = (
            door_state  # "nodoor", "locked", "closed", "open", "random"
        )

        # if actions are not specified, use the default set depending on the door
        if "actions" not in other:
            if self.door_state == "locked":
                other["actions"] = MOVE_AND_KICK_ACTIONS

            else:
                other["actions"] = MOVE_ACTIONS  # from MiniHackNavigation

        if lava_walls:
            self.wall = "L"
        else:
            self.wall = "|"

        des_file = self.get_env_desc()
        super().__init__(*args, des_file=des_file, **other)

    def get_env_map(self, env):
        door_pos = []
        goal_pos = None
        empty_strs = 0
        empty_str = True
        env_map = []

        for j in range(env.grid.height):
            str = ""
            for i in range(env.width):
                c = env.grid.get(i, j)
                if c is None:
                    str += "."
                    continue
                empty_str = False
                if c.type == "wall":
                    str += self.wall
                elif c.type == "door":
                    str += "+"
                    door_pos.append((i, j - empty_strs))
                elif c.type == "floor":
                    str += "."
                elif c.type == "lava":
                    str += "L"
                elif c.type == "goal":
                    goal_pos = (i, j - empty_strs)
                    str += "."
                elif c.type == "player":
                    str += "."
            if not empty_str and j < env.grid.height - 1:
                if set(str) != {"."}:
                    str = str.replace(".", " ", str.index(self.wall))
                    inv = str[::-1]
                    str = inv.replace(".", " ", inv.index(self.wall))[::-1]
                    env_map.append(str)
            elif empty_str:
                empty_strs += 1

        start_pos = (int(env.agent_pos[0]), int(env.agent_pos[1]) - empty_strs)
        env_map = "\n".join(env_map)

        return env_map, start_pos, goal_pos, door_pos

    def get_env_desc(self):
        self.minigrid_env.reset()
        env = self.minigrid_env

        map, start_pos, goal_pos, door_pos = self.get_env_map(env)

        lev_gen = LevelGenerator(map=map)

        lev_gen.add_goal_pos(goal_pos)
        lev_gen.set_start_pos(start_pos)

        for d in door_pos:
            lev_gen.add_door(self.door_state, d)

        lev_gen.wallify()

        for _ in range(self.num_mon):
            lev_gen.add_monster()

        for _ in range(self.num_trap):
            lev_gen.add_trap()

        return lev_gen.get_des()

    def seed(self, core=None, disp=None, reseed=False):
        """The signature of this method corresponds to that of NLE base class.
        For more information see
        https://github.com/facebookresearch/nle/blob/main/nle/env/base.py.

        Sets the state of the NetHack RNGs after the next reset.

        Arguments:
            core [int or None]: Seed for the core RNG. If None, chose a random
                value.
            disp [int or None]: Seed for the disp (anti-TAS) RNG. If None, chose
                a random value.
            reseed [boolean]: As an Anti-TAS (automation) measure,
                NetHack 3.6 reseeds with true randomness every now and then. This
                flag enables or disables this behavior. If set to True,
                trajectories won't be reproducible.

        Returns:
            [tuple] The seeds supplied, in the form (core, disp, reseed).
        """
        self.minigrid_env.seed(core)
        return super().seed(core, disp, reseed)

    def reset(self, wizkit_items=None):
        des_file = self.get_env_desc()
        self.update(des_file)
        return super().reset(wizkit_items=wizkit_items)


class MiniHackMultiRoomN2(MiniGridHack):
    def __init__(self, *args, max_episode_steps: int = 40, **other):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N2-S4-v0",
            max_episode_steps=max_episode_steps,
            **other
        )


class MiniHackMultiRoomN4(MiniGridHack):
    def __init__(self, *args, max_episode_steps: int = 120, **other):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N4-S5-v0",
            max_episode_steps=max_episode_steps,
            **other
        )


class MiniHackMultiRoomN6(MiniGridHack):
    def __init__(self, *args, max_episode_steps: int = 240, **other):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N6-v0",
            max_episode_steps=max_episode_steps,
            **other
        )


register(
    id="MiniHack-MultiRoom-N2-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN2",
)
register(
    id="MiniHack-MultiRoom-N4-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN4",
)
register(
    id="MiniHack-MultiRoom-N6-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN6",
)


# MiniGrid: LockedMultiRoom
class MiniHackMultiRoomN2Locked(MiniGridHack):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 40,
        door_state: str = "locked",
        **other
    ):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N2-S4-v0",
            max_episode_steps=max_episode_steps,
            door_state=door_state,
            **other
        )


class MiniHackMultiRoomN4Locked(MiniGridHack):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 120,
        door_state: str = "locked",
        **other
    ):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N4-S5-v0",
            max_episode_steps=max_episode_steps,
            door_state=door_state,
            **other
        )


class MiniHackMultiRoomN6Locked(MiniGridHack):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 240,
        door_state: str = "locked",
        **other
    ):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N6-v0",
            max_episode_steps=max_episode_steps,
            door_state=door_state,
            **other
        )


register(
    id="MiniHack-MultiRoom-N2-Locked-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN2Locked",
)
register(
    id="MiniHack-MultiRoom-N4-Locked-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN4Locked",
)
register(
    id="MiniHack-MultiRoom-N6-Locked-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN6Locked",
)


# MiniGrid: LavaMultiRoom
class MiniHackMultiRoomN2Lava(MiniGridHack):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 40,
        lava_walls: bool = True,
        **other
    ):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N2-S4-v0",
            max_episode_steps=max_episode_steps,
            lava_walls=lava_walls,
            **other
        )


class MiniHackMultiRoomN4Lava(MiniGridHack):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 120,
        lava_walls: bool = True,
        **other
    ):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N4-S5-v0",
            max_episode_steps=max_episode_steps,
            lava_walls=lava_walls,
            **other
        )


class MiniHackMultiRoomN6Lava(MiniGridHack):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 240,
        lava_walls: bool = True,
        **other
    ):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N6-v0",
            max_episode_steps=max_episode_steps,
            lava_walls=lava_walls,
            **other
        )


register(
    id="MiniHack-MultiRoom-N2-Lava-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN2Lava",
)
register(
    id="MiniHack-MultiRoom-N4-Lava-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN4Lava",
)
register(
    id="MiniHack-MultiRoom-N6-Lava-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN6Lava",
)


# MiniGrid: MonsterpedMultiRoom
class MiniHackMultiRoomN2Monster(MiniGridHack):
    def __init__(
        self, *args, max_episode_steps: int = 40, num_mon: int = 3, **other
    ):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N2-S4-v0",
            max_episode_steps=max_episode_steps,
            num_mon=num_mon,
            **other
        )


class MiniHackMultiRoomN4Monster(MiniGridHack):
    def __init__(
        self, *args, max_episode_steps: int = 120, num_mon: int = 6, **other
    ):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N4-S5-v0",
            max_episode_steps=max_episode_steps,
            num_mon=num_mon,
            **other
        )


class MiniHackMultiRoomN6Monster(MiniGridHack):
    def __init__(
        self, *args, max_episode_steps: int = 240, num_mon: int = 9, **other
    ):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N6-v0",
            max_episode_steps=max_episode_steps,
            num_mon=num_mon,
            **other
        )


# MiniGrid: MonsterMultiRoom
register(
    id="MiniHack-MultiRoom-N2-Monster-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN2Monster",
)
register(
    id="MiniHack-MultiRoom-N4-Monster-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN4Monster",
)
register(
    id="MiniHack-MultiRoom-N6-Monster-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN6Monster",
)


# MiniGrid: ExtremeMultiRoom
class MiniHackMultiRoomN2Extreme(MiniGridHack):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 40,
        num_mon: int = 3,
        lava_walls: bool = True,
        door_state: str = "locked",
        **other
    ):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N2-S4-v0",
            max_episode_steps=max_episode_steps,
            num_mon=num_mon,
            lava_walls=lava_walls,
            door_state=door_state,
            **other
        )


class MiniHackMultiRoomN4Extreme(MiniGridHack):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 120,
        num_mon: int = 6,
        lava_walls: bool = True,
        door_state: str = "locked",
        **other
    ):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N4-S5-v0",
            max_episode_steps=max_episode_steps,
            num_mon=num_mon,
            lava_walls=lava_walls,
            door_state=door_state,
            **other
        )


class MiniHackMultiRoomN6Extreme(MiniGridHack):
    def __init__(
        self,
        *args,
        max_episode_steps: int = 240,
        num_mon: int = 9,
        lava_walls: bool = True,
        door_state: str = "locked",
        **other
    ):
        super().__init__(
            *args,
            env_name="MiniGrid-MultiRoom-N6-v0",
            max_episode_steps=max_episode_steps,
            num_mon=num_mon,
            lava_walls=lava_walls,
            door_state=door_state,
            **other
        )


register(
    id="MiniHack-MultiRoom-N2-Extreme-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN2Extreme",
)
register(
    id="MiniHack-MultiRoom-N4-Extreme-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN4Extreme",
)
register(
    id="MiniHack-MultiRoom-N6-Extreme-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN6Extreme",
)

# MiniGrid: LavaCrossing
register(
    id="MiniHack-LavaCrossingS9N1-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-LavaCrossingS9N1-v0"},
)
register(
    id="MiniHack-LavaCrossingS9N2-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-LavaCrossingS9N2-v0"},
)
register(
    id="MiniHack-LavaCrossingS9N3-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-LavaCrossingS9N3-v0"},
)
register(
    id="MiniHack-LavaCrossingS11N5-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-LavaCrossingS11N5-v0"},
)

# MiniGrid: Simple Crossing
register(
    id="MiniHack-SimpleCrossingS9N1-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-SimpleCrossingS9N1-v0"},
)
register(
    id="MiniHack-SimpleCrossingS9N2-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-SimpleCrossingS9N2-v0"},
)
register(
    id="MiniHack-SimpleCrossingS9N3-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-SimpleCrossingS9N3-v0"},
)
register(
    id="MiniHack-SimpleCrossingS11N5-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-SimpleCrossingS11N5-v0"},
)
