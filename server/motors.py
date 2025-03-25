from pypot.dynamixel import Dxl320IO as MotorsController

# Doc : https://poppy-project.github.io/pypot/pypot.dynamixel.html


class LedColors:
    red = "red"
    green = "green"
    yellow = "yellow"
    blue = "blue"
    pink = "pink"
    cyan = "cyan"
    white = "white"


class Motor:
    colors = LedColors
    _led_color = None
    _control_mode = None
    available_pos = []
    default_pos = None

    def __init__(self, dxl_io, id):
        self._dxl_io: Motors = dxl_io
        self.id = id
        self._pos = self.default_pos
        self.led = False
        self.led_color = self.colors.white
        self.control_mode = "joint"

    def init(self, _pos: int = None):
        if _pos in self.available_pos:
            self._pos = _pos
        self.led = False
        self.control_mode = "joint"
        self._dxl_io.set_pos(self.id, self._pos)

    def turn(self, number: int = 1):
        if self._pos in self.available_pos:
            i = self.available_pos.index(self._pos)
            i += number
            i %= len(self.available_pos)
            self.pos = self.available_pos[i]

    @property
    def pos(self) -> int:
        return self._pos

    @pos.setter
    def pos(self, value):
        if self._pos == value:
            return
        if value in self.available_pos:
            self._pos = value
            self._dxl_io.set_pos(self.id, self._pos)
            while self._dxl_io.is_moving([self.id]) != [False]:
                continue

    @property
    def compliant(self) -> bool:
        """If compliant, the torque is disable"""
        return not self._dxl_io.is_torque_enabled([self.id])[0]

    @compliant.setter
    def compliant(self, value):
        if self.compliant == value:
            return
        if value:
            self._dxl_io.disable_torque([self.id])
        else:
            self._dxl_io.enable_torque([self.id])

    @property
    def led(self) -> bool:
        """If the led is on"""
        return self.is_led_on([self.id])[0]

    @led.setter
    def led(self, value):
        if self.led == value:
            return
        if value:
            self._dxl_io.switch_led_on([self.id])
        else:
            self._dxl_io.switch_led_off([self.id])

    @property
    def led_color(self) -> str:
        """The color of the led"""
        return self._led_color

    @led_color.setter
    def led_color(self, value) -> str:
        if value == self._led_color or value not in self.colors:
            return
        self._led_color = value
        self._dxl_io.set_LED_color({self.id: value})

    @property
    def control_mode(self) -> str:
        """Joint or wheel"""
        return self._control_mode

    @control_mode.setter
    def control_mode(self, value) -> str:
        if value == self._control_mode or value in ("joint", "wheel"):
            return
        if self.compliant:
            if value == "joint":
                self._dxl_io.set_wheel_mode([self.id])
            else:
                self._dxl_io.set_joint_mode([self.id])
        else:
            self.compliant = True
            if value == "joint":
                self._dxl_io.set_wheel_mode([self.id])
            else:
                self._dxl_io.set_joint_mode([self.id])
            self.compliant = False
        self._control_mode = value


class FlipMotor(Motor):
    available_pos = [-125, -65, 25, 105]
    default_pos = -125


class TurnMotor(Motor):
    available_pos = [-135, -45, 45, 135]
    default_pos = 45


class Motors(MotorsController):
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

    def get_turn_motor(self, id: int) -> TurnMotor:
        return TurnMotor(self, id)

    def get_flip_motor(self, id: int) -> FlipMotor:
        return FlipMotor(self, id)

    def set_pos(self, id: int, pos: int):
        self.set_goal_position({id: pos})

    def get_pos(self, ids: list) -> list[int]:
        return self.get_present_position(ids)
