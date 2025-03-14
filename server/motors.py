from pypot.dynamixel import Dxl320IO

# Doc : https://poppy-project.github.io/pypot/pypot.dynamixel.html


class Dxl320:
    def __init__(self, dxl_io, id, available_pos=[-135, -45, 45, 135], default_pos=45):
        self._dxl_io: Motors = dxl_io
        self.id = id
        self.available_pos = available_pos
        self._pos = default_pos

    def init(self, _pos: int = None):
        if _pos in self.available_pos:
            self._pos = _pos
        self._dxl_io.set_joint_mode([self.id])
        self._dxl_io.set_goal_position({self.id: self._pos})

    def turn(self, number: int = 1):
        if self._pos in self.available_pos:
            i = self.available_pos.index(self._pos)
            i += number
            i %= len(self.available_pos)
            self._pos = self.available_pos[i]
        self._dxl_io.set_goal_position({self.id: self._pos})


class Motors(Dxl320IO):
    def __init__(
        self,
        port="/dev/serial0",
        baudrate=1000000,
        timeout=0.05,
        use_sync_read=False,
        error_handler_cls=None,
        convert=True,
    ):
        super().__init__(
            port, baudrate, timeout, use_sync_read, error_handler_cls, convert
        )

    def set_wheel_mode(self, ids: list[int]):
        self.disable_torque(ids)
        super().set_wheel_mode(ids)
        self.enable_torque(ids)

    def set_joint_mode(self, ids: list[int]):
        self.disable_torque(ids)
        super().set_joint_mode(ids)
        self.enable_torque(ids)

    def get_motor(self, id: int, **kwargs):
        return Dxl320(self, id, **kwargs)

    def set_pos(self, id: int, pos: int):
        self.set_goal_position({id: pos})

    def get_pos(self, ids: list) -> list[int]:
        return self.get_present_position(ids)
