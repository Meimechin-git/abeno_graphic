import math
from abeno_graphic import world
from abeno_graphic import perspective

world1 = world(points=[[[0,0,-1]],
    [[1,0,0]],
    [[1/2**(1/2),1/2**(1/2),0]],
    [[0,1,0]],
    [[-1/2**(1/2),1/2**(1/2),0]],
    [[-1,0,0]],
    [[-1/2**(1/2),-1/2**(1/2),0]],
    [[0,-1,0]],
    [[1/2**(1/2),-1/2**(1/2),0]],
    [[0,0,1]]
],sides=[]
,surfaces=[[[0,1,2]],
    [[0,2,3]],
    [[0,3,4]],
    [[0,4,5]],
    [[0,5,6]],
    [[0,6,7]],
    [[0,7,8]],
    [[0,8,1]],
    [[9,1,2]],
    [[9,2,3]],
    [[9,3,4]],
    [[9,4,5]],
    [[9,5,6]],
    [[9,6,7]],
    [[9,7,8]],
    [[9,8,1]],
],default_color=[255,255,255])
perspective1 = perspective(world1,[0,0,3],[0,0],[1.5,1.0],[150,100],[False,False,True],[600,400],speed=3,aim_sensitivity=2,fps=60,brightness=3,contrast=0.8)
perspective1.start_user_interface()