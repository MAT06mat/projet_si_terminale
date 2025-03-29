from imports import bluetooth_socket as bs, analyser as a, solver as s


CN = s.CubeNotation


class RubiksCubeSolver:
    solving = False
    mapping = {face: face for face in s.FACE_ORDER}
    cube_pos = s.FACE_ORDER

    def __init__(self, virtual=False):
        self.virtual = virtual
        print("============ INIT RCM ============")
        if not virtual:
            from camera import Camera
            from motors import Motors

            # Init motors
            print("-> Init motors")
            motors = Motors()
            self.m1 = motors.get_turn_motor(1)
            self.m2 = motors.get_flip_motor(2)
            self.m1.compliant = True
            self.m2.compliant = True

            # Init bluetooth
            print("-> Init bluetooth")
            self.server = bs.Server()

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
        self.server.public_vars[self.start_solver.__name__] = self.start_solver
        self.server.public_vars[self.stop_solver.__name__] = self.stop_solver
        self.server.connect()

    def continue_solving(self):
        if not self.solving:
            raise Exception("Solving is stopped")

    def start_solver(self, *args):
        self.solving = True
        try:
            self.solve()
        except Exception as e:
            print(e)

    def solve(self):
        if not self.virtual:
            self.m1.compliant = False
            self.m2.compliant = False

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

        # Do mouvments
        for mouvment in solution.split():
            self.mouv(mouvment)

        if not self.virtual:
            self.m1.compliant = True
            self.m2.compliant = True

    def stop_solver(self, *args):
        self.solving = False

    def scan_cube(self):
        faces = {}
        for i in "FLBR":
            faces[i] = self.scan_face(i)
            self.turn_cube()
        self.flip_cube()
        faces["U"] = self.scan_face("U")
        self.flip_cube(2)
        faces["D"] = self.scan_face("D")

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

    def scan_face(self, f) -> dict[str:str]:
        """img = self.camera.get_image()
        face = self.anayser.analyse(img)"""
        face = {
            "F": ["F", "DLLBBFFF"],
            "L": ["L", "FFFLLLUU"],
            "B": ["B", "RRUBBBBB"],
            "R": ["R", "FFBDDRRR"],
            "U": ["U", "RDDUUURR"],
            "D": ["D", "DDUULLLD"],
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
            self.m2.pos = 25
            self.m2.pos = 105
            self.m2.pos = 25
            self.m2.pos = -65

    def turn_cube(self, num=1):
        self.continue_solving()
        num %= 4
        for i in range(num):
            self.cube_pos = "".join(self.cube_pos[i] for i in [0, 2, 4, 3, 5, 1])
        # Motors turn cube
        if not self.virtual:
            self.m2.pos = -65
            self.m1.turn(num)

    def turn_face(self, num=1):
        self.continue_solving()
        num %= 4
        for i in range(num):
            self.cube.turn(self.cube_pos[3])
        # Motors turn face
        if not self.virtual:
            self.m2.pos = 25
            self.m1.turn(num)
            self.m2.pos = -65


if __name__ == "__main__":
    rcm = RubiksCubeSolver(virtual=True)
    rcm.start_solver()
    print(rcm.cube.is_solve())
