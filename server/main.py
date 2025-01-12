from solver import Cube, test
from analyser import FaceAnalyser, Image

test(100)
c = Cube()

print()

img = Image.open("server/analyser/img.png")
anayser = FaceAnalyser(img, x=400, y=230, shape=120, squares=20)
print(anayser.analyse())
anayser.show()