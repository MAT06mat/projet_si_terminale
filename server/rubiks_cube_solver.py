from imports import bluetooth_socket as bs, analyser as a, solver as s
from camera import Camera
from motors import Motors


class RubiksCubeSolver:
    def __init__(self):
        print("============ INIT RCM ============")
        # Init motors
        print("-> Init motors")
        motors = Motors()
        self.m1 = motors.get_motor(1)
        self.m2 = motors.get_motor(2)

        self.m2.switch_led_on()
        self.m2.set_LED_color(self.m2.colors.green)

        # Init bluetooth
        print("-> Init bluetooth")
        self.server = bs.Server()

        # Init analyser
        print("-> Init analyser")
        self.anayser = a.FaceAnalyser(x=400, y=230, shape=120, squares=20)

        # Init cube solver
        print("-> Init cube")
        self.cube = s.Cube()

        # Init camera
        print("-> Init camera")
        self.camera = Camera()

        self.m2.switch_led_off()
        print("========= INIT COMPLETED =========")
