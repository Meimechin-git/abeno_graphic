import math
from abeno_graphic import world
from abeno_graphic import perspective

CUBE_POINTS = [[[0,0,0]],
    [[0,0.9,0]],
    [[0.9,0.9,0]],
    [[0.9,0,0]],
    [[0,0,1]],
    [[0,0.9,1]],
    [[0.9,0.9,1]],
    [[0.9,0,1]],
]

CUBE_SURFACES = [[[0,1,2,3]],
    [[4,5,6,7]],
    [[0,1,5,4]],
    [[1,2,6,5]],
    [[2,3,7,6]],
    [[3,0,4,7]]
]

class field():
    def __init__(self,width,height,list=[[]]):
        self.world1 = world()
        for y in range(height):
            for x in range(width):
                point_indexes = []
                for i in range(len(CUBE_POINTS)):
                    point_indexes.append(self.world1.add_point([CUBE_POINTS[i][0][0]+x,CUBE_POINTS[i][0][1]+y,CUBE_POINTS[i][0][2]]))
                for i in range(len(CUBE_SURFACES)):
                    self.world1.add_surface([point_indexes[p_i] for p_i in CUBE_SURFACES[i][0]],color=list[y][x])

field1 = field(3,3,[[[255,255,255],[255,255,255],[255,255,255]],
                    [[255,255,255],[255,255,255],[255,255,255]],
                    [[255,255,255],[255,255,255],[255,255,255]]])
perspective1 = perspective(field1.world1,[1,1,3],[math.radians(0),math.radians(180)],[1.50,1.00],[150,100],[False,False,True],[600,400],speed=3,aim_sensitivity=2,fps=60,brightness=10,contrast=0.8)
perspective1.start_user_interface()