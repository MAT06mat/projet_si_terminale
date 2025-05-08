from imports import bluetooth_socket as bs, analyser as a, solver as s
from time import time


CN = s.CubeNotation


class RubiksCubeMaster:
    solving = False
    mapping = {face: face for face in s.FACE_ORDER}
    cube_pos = s.FACE_ORDER

    def __init__(self, virtual=False, camera=True):
        self.virtual = virtual
        self.camera = camera
        self.in_test = False
        print("============ INIT RCM ============")
        print(f"Virtual : {virtual}")
        print(f"Camera : {camera}\n")
        if not virtual:
            from server.components.motors import Motors

            # Init motors
            print("-> Init motors")
            motors_getter = Motors()
            self.m1 = motors_getter.get_turn_motor(1)
            self.m2 = motors_getter.get_flip_motor(2)

            self.m2.led = True
            self.m2.led_color = self.m2.colors.green

            from server.components.camera import Camera

            # Init bluetooth
            print("-> Init bluetooth")
            self.server = bs.Server()

            if camera:
                # Init camera
                print("-> Init camera")
                self.camera = Camera()

        # Init cube solver
        print("-> Init cube")
        self.cube = s.Cube()

        # Init analyser
        print("-> Init analyser")
        self.anayser = a.FaceAnalyser(x=400, y=230, shape=120, squares=20)

        print("========= INIT COMPLETED =========")

    def run_server(self):
        # Define fucntions for start and stop the solver in the server
        self.server.public_vars[self.start_solver.__name__] = self.start_solver
        self.server.public_vars[self.stop_solver.__name__] = self.stop_solver

        def on_client_connect():
            self.m2.led_color = self.m2.colors.cyan

        def on_client_deconnect():
            self.m2.led_color = self.m2.colors.green

        self.server.on_client_connect = on_client_connect
        self.server.on_client_deconnect = on_client_deconnect

        try:
            # Start the server
            self.server.connect()
            print("Server main loop started, type 'exit' to stop it.")
            while self.server.is_server_connected:
                i = input("> ")
                if i == "exit":
                    self.m2.led = False
                    break
        finally:
            if not self.virtual:
                self.m2.led_color = self.m2.colors.red

    def test(self):
        self.in_test = True
        t = time()
        self.start_solver()
        print("End after", time() - t, "sec")
        print("Cube is solve :", self.cube.is_solve())
        self.in_test = False

    def continue_solving(self):
        if not self.solving:
            raise Exception("Solving is stopped")

    def start_solver(self, *args):
        self.solving = True
        self.m2.led_color = self.m2.colors.yellow
        try:
            self.solve()
        except Exception as e:
            print(e)
        self.solving = False
        self.m2.led_color = self.m2.colors.blue

    def solve(self):
        if not self.virtual:
            self.m2.init()
            self.continue_solving()
            self.m1.init()

        # Scan cube
        cube_string = self.scan_cube()

        # Cube resolution
        self.cube.from_string(cube_string)
        if self.cube.is_solve():
            return
        solution = self.cube.solve()

        if self.in_test:
            print("Solution find in", len(solution.split()), "moves")

        # Do mouvments
        for mouvment in solution.split():
            self.mouv(mouvment)

    def stop_solver(self, *args):
        self.solving = False

    def format_faces(self, faces: dict[list[str]]) -> dict[str]:
        # Create mapping
        faces_map = {}
        for relative_face, face in faces.items():
            faces_map[face[0]] = relative_face
        mapping = str.maketrans(faces_map)
        self.mapping = mapping

        # Use mapping
        for face in faces:
            faces[face] = faces[face][1].translate(mapping)

        return "".join((faces[face] for face in s.FACE_ORDER))

    def scan_cube(self):
        faces = {}
        for i in "FLBR":
            faces[i] = self.scan_face(i)
            self.turn_cube()
        self.flip_cube()
        faces["U"] = self.scan_face("U")
        self.flip_cube(2)
        faces["D"] = self.scan_face("D")

        return self.format_faces(faces)

    def scan_face(self, f) -> list[str]:
        """img = self.camera.get_image()
        face = self.anayser.analyse(img)"""
        face = {
            "F": ["L", "BFFRUDFL"],
            "L": ["U", "FBRDDRDL"],
            "B": ["R", "LFDULFDU"],
            "R": ["D", "ULBBBDRU"],
            "U": ["F", "LUUBLLUD"],
            "D": ["B", "RRFFRRBB"],
        }[f]
        return face

    def mouv(self, mouvment):
        mouv, num = mouvment[0], mouvment[-1]
        match num:
            case "'":
                num = 3
            case "2":
                num = 2
            case _:
                num = 1

        match self.cube_pos.index(mouv):
            case 0:
                self.flip_cube(2)
            case 1:
                self.turn_cube(3)
                self.flip_cube()
            case 2:
                self.flip_cube()
            case 4:
                self.turn_cube()
                self.flip_cube()
            case 5:
                self.turn_cube(2)
                self.flip_cube()

        self.turn_face(num)

    def flip_cube(self, num=1):
        self.continue_solving()
        num %= 4
        for i in range(num):
            self.cube_pos = "".join(self.cube_pos[i] for i in [5, 1, 0, 2, 4, 3])
            # Motors flip cube
            if not self.virtual:
                self.m2.pos = 0
                self.m2.pos = 135
                self.m2.pos = 0

    def turn_cube(self, num=1):
        self.continue_solving()
        num %= 4
        for i in range(num):
            self.cube_pos = "".join(self.cube_pos[i] for i in [0, 2, 4, 3, 5, 1])
        # Motors turn cube
        if not self.virtual:
            self.m2.pos = -65
            self.m1.turn(num)
            self.m2.pos = 25

    def turn_face(self, num=1):
        self.continue_solving()
        num %= 4
        for i in range(num):
            self.cube.turn(self.cube_pos[3])
        # Motors turn face
        if not self.virtual:
            self.m2.pos = 25
            self.m1.turn(num)


if __name__ == "__main__":
    RubiksCubeMaster(virtual=True).test()
