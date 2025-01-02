import math
from abeno_graphic import world
from abeno_graphic import perspective

world1 = world(points=[[[0,0,0]],
    [[0,1,0]],
    [[1,1,0]],
    [[1,0,0]],
    [[0,0,1]],
    [[0,1,1]],
    [[1,1,1]],
    [[1,0,1]],
],sides=[[[100,100,100],[0,1]],[[100,100,100],[1,2]],[[100,100,100],[2,3]],[[100,100,100],[3,0]]
],surfaces=[[[0,1,2,3]],
    [[4,5,6,7]],
    [[0,1,5,4]],
    [[1,2,6,5]],
    [[2,3,7,6]],
    [[3,0,4,7]]
],default_color=[255,255,255])
perspective1 = perspective(world1,[-1,-0.2,0.7],[math.radians(60),math.radians(90)],[1.5,1.0],[150,100],[False,False,True],[600,400],speed=3,aim_sensitivity=2,fps=60,brightness=1,contrast=0.8)
def pop():
    for i in range(8):
        world1.move_point(i,[0,0,0.01],'relative')
perspective1.start_user_interface(pop)

