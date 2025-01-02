import pygame
import math
import array

#行列と描画処理の一部を計算するクラス----------------------------------------------------------------------
class mtx_cal():
    #行列の足し算を行う静的メソッド
    def sum(col=None,val=None,ccv=None):
        if (val!=None):
            return [col[i]+val for i in range(len(col))]
        elif (ccv!=None):
            return [col[i]+ccv[i] for i in range(len(col))]
    #行列の引き算を行う静的メソッド
    def sub(col=None,val=None,ccv=None):
        if (val!=None):
            return [col[i]-val for i in range(len(col))]
        elif (ccv!=None):
            return [col[i]-ccv[i] for i in range(len(col))]
    #行列の掛け算(内積計算)を行う静的メソッド
    def mul(col=None,val=None,rcv=None,rscv=None):
        if (val!=None):
            return [col[i]*val for i in range(len(col))]
        elif (rcv!=None):
            return sum([col[i]*rcv[i] for i in range(len(col))])
        elif (rscv!=None):
            return [sum([col[i]*rcv[i] for i in range(len(rcv))]) for rcv in rscv]
    #行列の外積計算を行う静的メソッド
    def cross(col=None,ccv=None):
        return [col[1]*ccv[2]-col[2]*ccv[1],col[2]*ccv[0]-col[0]*ccv[2],col[0]*ccv[1]-col[1]*ccv[0]]
    #面と線の交点を求める静的メソッド
    def intersect_point(equition,p1,p2):
        numerator = -(mtx_cal.mul(col=p1,rcv=equition[:3])+equition[3])
        denominator = mtx_cal.mul(col=mtx_cal.sub(col=p2,ccv=p1),rcv=equition[:3])
        if denominator!=0:
            t = numerator / denominator
            return mtx_cal.sum(col=p1,ccv=mtx_cal.mul(col=mtx_cal.sub(col=p2,ccv=p1),val=t))

#３次元の世界を管理するクラス-----------------------------------------------------------------------------
class world():
    #コンストラクタ
    def __init__(self,points=[],sides=[],surfaces=[],default_color=[255,255,255]): #コンストラクタ：世界に存在する点のデータと面のデータを引数にとる
        self.world_points = [None for p in points]
        self.world_sides = [None for s in sides]
        self.world_surfaces = [None for s in surfaces]
        for i in range(len(points)):
            if len(points[i]) == 1:
                self.world_points[i] = world_point(i,points[i][0],color=default_color)
            elif len(points[i]) == 2:
                self.world_points[i] = world_point(i,points[i][1],color=points[i][0])
        for i in range(len(sides)):
            if len(sides[i])==1:
                self.world_sides[i] = world_side(i,sides[i][0][0],sides[i][0][1],self.world_points,color=default_color)
            elif len(sides[i])==2:
                self.world_sides[i] = world_side(i,sides[i][1][0],sides[i][1][1],self.world_points,color=sides[i][0])
        for i in range(len(surfaces)):
            if len(surfaces[i])==1:
                self.world_surfaces[i] = world_surface(i,surfaces[i][0],self.world_points,color=default_color)
            elif len(surfaces[i])==2:
                self.world_surfaces[i] = world_surface(i,surfaces[i][1],self.world_points,color=surfaces[i][0]) #世界に存在する面のデータであるworld_surfaceオブジェクトのリスト
    #点を追加する動的メソッド
    def add_point(self,coordinate,color=[255,255,255]):
        for world_point_index in range(len(self.world_points)):
            if self.world_points[world_point_index] == None:
                self.world_points[world_point_index] = world_point(world_point_index,coordinate,color)
                return world_point_index
        index = len(self.world_points)
        self.world_points.append(world_point(index,coordinate,color))
        return index
    #点を移動させる動的メソッド
    def move_point(self,index,coordinate,type='relative'):
        if type=='relative' or type=='absolute':
            self.world_points[index].move_point(coordinate,type)
    #点を削除する動的メソッド
    def delete_point(self,index):
        self.world_points[index] = None
    #線を追加する動的メソッド
    def add_side(self,side,color=[255,255,255]):
        for world_side_index in range(len(self.world_sides)):
            if self.world_sides[world_side_index] == None:
                self.world_sides[world_side_index] = world_side(world_side_index,side[0],side[1],self.world_points,color=color)
                return world_side_index
        index = len(self.world_sides)
        self.world_sides.append(world_side(index,side[0],side[1],self.world_points,color=color))
        return index
    #線を移動移動させる動的メソッド
    def parallel_move_side(self,index,point):
        self.world_sides[index].point1.move_point(point,'relative')
        self.world_sides[index].point2.move_point(point,'relative')
    #線を削除する動的メソッド
    def delete_side(self,index):
        self.world_sides[index] = None
    #面を追加する動的メソッド
    def add_surface(self,surface,color=[255,255,255]):
        for world_surface_index in range(len(self.world_surfaces)):
            if self.world_surfaces[world_surface_index] == None:
                self.world_surfaces[world_surface_index] = world_surface(world_surface_index,surface,self.world_points,color=color)
                return world_surface_index
        index = len(self.world_surfaces)
        self.world_surfaces.append(world_surface(index,surface,self.world_points,color=color))
        return index
    #面を平行移動させる動的メソッド
    def parallel_move_surface(self,index,point):
        for i in range(len(self.world_surfaces[index].points)):
            self.world_surfaces[index].points[i].move_point(point,'relative')
    #面を削除する動的メソッド
    def delete_surface(self,index):
        self.world_surfaces[index] = None

#３次元の世界の点を管理するクラス
class world_point():   
    #コンストラクタ
    def __init__(self,index,point,color=[255,255,255]):
        self.index = index
        self.point = point
        self.color = color
    #自身の点を移動させる動的メソッド
    def move_point(self,point,type='relative'):
        if type=='relative':
            self.point[0] += point[0]
            self.point[1] += point[1]
            self.point[2] += point[2]
        elif type=='absolute':
            self.point[0] = point[0]
            self.point[1] = point[1]
            self.point[2] = point[2]

class world_side():
    def __init__(self,index,first_point_index,second_point_index,world_points,color=[255,255,255]):
        self.index = index
        self.point1 = world_points[first_point_index]
        self.point2 = world_points[second_point_index]
        self.color = color

#３次元の世界の面のクラス：worldクラスとhas-aの関係で、world_surfacesフィールドにリストで管理されている
class world_surface():
    def __init__(self,index,point_indexes,world_points,color=[255,255,255]): #コンストラクタ：world_surfacesフィールドのリストのインデックスとRGBカラーリスト、面のデータ(面に属する点のworld_pointsフィールドのリストのインデックスのリスト)、自分が属するworldクラスのworld_pointsフィールドを引数にとる
        self.index = index #world_surfacesフィールドのリストのインデックス
        self.points = [world_points[p_i] for p_i in point_indexes] #自分に属する点のworld_pointオブジェクトのリスト(自分が属するworldオブジェクトのworld_pointsフィールドを参照)
        self.color = color #面のRGBカラーリスト

#３次元の世界の視点を管理するクラス------------------------------------------------------------------------------------------------------------------------------------------------------------------
class perspective():
    def __init__(self,world,position=[0,0,0],direction_facing=[0,0],viewport=[1.5,1.0],image_pixel=[150,100],drawing_mode=[True,True,True],window_size=[600,400],title="Abeno_Graphic",fps=60,speed=1,aim_sensitivity=1,brightness=1,contrast=0.5): #コンストラクタ：視点が存在する世界(worldクラス)と自分の座標、視点が向いている方向、ビューポート、ピクセル数、描画モード、描画するウィンドウのサイズを引数にとるworld引数以外は仮変数として初期値を入れてある
        self.world = world #視点が存在する世界(worldクラス)
        self.position = position #視点の座標
        self.direction_facing = direction_facing #視点が向いている方向
        self.viewport = viewport #ビューポート
        self.image_pixel = image_pixel #ピクセル数
        self.drawing_mode = drawing_mode
        self.window_size = window_size #ウィンドウサイズ
        self.title = title #ウィンドウタイトル
        self.fps = fps #fps
        self.speed = speed #移動速度
        self.aim_sensitivity = aim_sensitivity #視点移動速度
        self.brightness = brightness #光の強さ
        self.contrast = contrast #コントラスト
        self.load() #load関数を呼び出す

    def start_user_interface(self,external_function=None): #start_user_interface関数：pygameでGUIの処理を行う関数
        pygame.init() #初期化
        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1])) #ウィンドウサイズとタイトル設定
        pygame.display.set_caption(self.title) #ウィンドウタイトル
        self.running = True #ループを続けるか否かの真偽値
        while self.running: #ループ処理
            self.keys = pygame.key.get_pressed() #キー入力マップを受け取る
            self.user_interface_task()
            if external_function != None:
                external_function()
            self.load() #load関数を呼び出す
            self.screen.blit(pygame.transform.scale(pygame.transform.flip(pygame.transform.rotate(pygame.image.frombuffer(self.canvas.image,self.image_pixel, "RGB"),180),True,False),self.window_size), (0, 0))  #指定座標にcanvasフィールドのimageを元に描画
            pygame.display.flip() #画面更新
            pygame.time.Clock().tick(self.fps) #フレームレートを制御


    def user_interface_task(self):
        for event in pygame.event.get(): #イベントを一つずつ処理する
            if event.type == pygame.QUIT: #終了イベントが来たとき
                self.running = False #running変数をfalse
        distance = self.speed/self.fps #移動の速さとfpsから移動距離を算出
        rotation_matrix = [[math.cos(-self.direction_facing[0]),math.sin(-self.direction_facing[0]),0],[-math.sin(-self.direction_facing[0]),math.cos(-self.direction_facing[0]),0],[0, 0, 1]]
        angle = self.aim_sensitivity/self.fps*100 #視点移動速度とfpsから視点移動間隔を算出
        if self.keys[pygame.K_w]: #wキーが押されているとき前方向にdiscanceだけ進む
            self.position = mtx_cal.sub(col=self.position,ccv=mtx_cal.mul(col=[0,distance,0],rscv=rotation_matrix))
        if self.keys[pygame.K_a]: #aキーが押されているとき左方向にdiscanceだけ進む
            self.position = mtx_cal.sub(col=self.position,ccv=mtx_cal.mul(col=[distance,0,0],rscv=rotation_matrix))
        if self.keys[pygame.K_s]: #sキーが押されているとき後ろ方向にdiscanceだけ進む
            self.position = mtx_cal.sub(col=self.position,ccv=mtx_cal.mul(col=[0,-distance,0],rscv=rotation_matrix))
        if self.keys[pygame.K_d]: #dキーが押されているとき右方向にdiscanceだけ進む
            self.position = mtx_cal.sub(col=self.position,ccv=mtx_cal.mul(col=[-distance,0,0],rscv=rotation_matrix))
        if self.keys[pygame.K_SPACE]: #spaceキーが押されているとき上方向にdiscanceだけ進む
            self.position = mtx_cal.sum(col=self.position,ccv=[0,0,distance])
        if self.keys[pygame.K_LSHIFT]: #左shiftキーが押されているとき下方向にdiscanceだけ進む
            self.position = mtx_cal.sum(col=self.position,ccv=[0,0,-distance])
        if self.keys[pygame.K_UP]: #上十字キーが押されているとき視点方向を上向きにangleだけ変える
            self.direction_facing[1] -= math.radians(angle)
        if self.keys[pygame.K_DOWN]: #下十字キーが押されているとき視点方向を下向きにangleだけ変える
            self.direction_facing[1] += math.radians(angle)
        if self.keys[pygame.K_LEFT]: #左十字キーが押されているとき視点方向を左向きにangleだけ変える
            self.direction_facing[0] -= math.radians(angle)
        if self.keys[pygame.K_RIGHT]: #右十字キーが押されているとき視点方向を右向きにangleだけ変える
            self.direction_facing[0] += math.radians(angle)

    def load(self): #load関数：worldオブジェクトと自身のオブジェクトのフィールドを元に描画データ(canvasフィールドのimage)を作成
        self.graphic_points = [graphic_point(world_point.point,world_point.color).parallel_move(self.position).rotate(self.direction_facing[0],self.direction_facing[1]).make_2d_point() if world_point!=None else None for world_point in self.world.world_points] #world_pointsリストを描画できるように処理したgraphic_pointオブジェクトのリスト
        self.graphic_sides = [graphic_side(world_side,self.graphic_points,self.viewport) if world_side!=None else None for world_side in self.world.world_sides] #world_sidesリストを描画できるように処理したgraphic_sidesオブジェクトのリスト
        self.graphic_surfaces = [graphic_surface(world_surface,self.graphic_points) if world_surface!=None else None for world_surface in self.world.world_surfaces] #world_surfacesリストを描画できるように処理したgraphic_surfaceオブジェクトのリスト
        self.canvas = canvas(self) #描画を管理するcanvasオブジェクト

#点データを描画できるように加工するクラス(ビュー座標系への変換)：perspectiveクラスとhas-aの関係で、graphic_pointsフィールドにリストで管理されている
class graphic_point():
    def __init__(self,point,color=None): #コンストラクタ：３次元座標を引数にとる
        self._3d_point = point #点の３次元座標
        self.color = color

    def parallel_move(self,position): #parallel_move関数：３次元座標を引数にとり自身の点を平行移動させる関数
        self._3d_point = mtx_cal.sub(col=self._3d_point,ccv=position) #自身の点を引数の３次元座標から見た相対座標に変換する
        return self #34行でメソッドチェーンにできるように自身のオブジェクトを返す

    def rotate(self,z_axis_theata,x_axis_theata): #rotate関数：視点が向いている方向をz軸上向き方向をy軸横向き方向をx軸とする正規直交基底によって定義された座標(ビュー座標系)へ変換する
        z_axis_rotation = [                           #z軸の回転行列
            [math.cos(z_axis_theata),math.sin(z_axis_theata),0],
            [-math.sin(z_axis_theata),math.cos(z_axis_theata),0],
            [0, 0, 1]
        ]
        x_axis_rotation = [                           #x軸の回転行列
            [1,0,0],
            [0,math.cos(x_axis_theata), math.sin(x_axis_theata)],
            [0,-math.sin(x_axis_theata), math.cos(x_axis_theata)]
        ]
        self._3d_point = mtx_cal.mul(col=mtx_cal.mul(col=self._3d_point,rscv=z_axis_rotation),rscv=x_axis_rotation) #行列の積により変換
        return self #34行でメソッドチェーンにできるように自身のオブジェクトを返す
    
    def make_2d_point(self): #make_2d_point関数：３次元座標を描画用２次元座標にビューボート変換する関数
        self._2d_point = None if self._3d_point[2] <= 0 else [self._3d_point[0]/self._3d_point[2],self._3d_point[1]/self._3d_point[2]] #ビューボート変換
        return self #34行でメソッドチェーンにできるように自身のオブジェクトを返す

class graphic_side():
    def __init__(self,world_side,graphic_points,viewport):#-----------------------------------------------------------------------------------------------------------------------
        self.index = world_side.index
        self.color = world_side.color
        self.point1 = graphic_points[world_side.point1.index]
        self.point2 = graphic_points[world_side.point2.index]
        self.visible_range_adaptive_surgery()

    def visible_range_adaptive_surgery(self): #visible_range_adaptive_surgery関数：自身の線の目視可能範囲適合整形処理を行う------------------------------------------------------------------
        p3 = mtx_cal.intersect_point([0,0,1,-0.01],self.point1._3d_point,self.point2._3d_point)
        if self.point1._2d_point==None and self.point2._2d_point!=None:
            self.point1 = graphic_point(p3).make_2d_point()
        elif self.point1._2d_point!=None and self.point2._2d_point==None:
            self.point2 = graphic_point(p3).make_2d_point()
        
#面データを描画できるように加工するクラス：perspectiveクラスとhas-aの関係で、graphic_surfacesフィールドにリストで管理されている
class graphic_surface():
    def __init__(self,world_surface,graphic_points): #コンストラクタ：world_surfaceオブジェクトと自分が属するgraphic_pointsフィールドを引数にとる
        self.index = world_surface.index #graphic_surfacesフィールドのリストのインデックス
        self.color = world_surface.color #面のRGBカラーリスト
        self.points = [graphic_points[world_surface.points[i_s].index] for i_s in range(len(world_surface.points))] #自分に属する点のgraphic_pointオブジェクトのリスト(自分が属するperspectiveオブジェクトのgraphic_pointsフィールドを参照)
        self.make_equation(self.points[:3]) #make_equation関数を呼び出す
        self.make_center_of_gravity() #make_center_of_gravityを呼び出す
        self.visible_range_adaptive_surgery() #visible_range_adaptive_surgery関数を呼び出す

    def make_equation(self,points): #surface_from_points関数：３つの３次元座標の点のリストを引数にとり、自身の面の方程式([A,B,C,D]:Ax + By + Cz + D = 0)を求める
        v1 = mtx_cal.sub(col=points[1]._3d_point,ccv=points[0]._3d_point) #ベクトルを計算
        v2 = mtx_cal.sub(col=points[2]._3d_point,ccv=points[0]._3d_point)
        normal = mtx_cal.cross(col=v1,ccv=v2) #外積で法線ベクトルを求める
        A, B, C = normal
        D = -mtx_cal.mul(col=points[0]._3d_point,rcv=normal) #定数項 D を計算
        self.equation = [A, B, C, D] #新しいフィールドequitionに自身の面の方程式のリスト([A,B,C,D]:Ax + By + Cz + D = 0)を代入する

    def make_center_of_gravity(self):
        self.center_of_gravity = [sum([p._3d_point[0] for p in self.points])/len(self.points),sum([p._3d_point[1] for p in self.points])/len(self.points),sum([p._3d_point[2] for p in self.points])/len(self.points)]

    def visible_range_adaptive_surgery(self): #visible_range_adaptive_surgery関数：自身の面の目視可能範囲適合整形処理を行う
        new_points=[]
        for i_p in range(len(self.points)):
            p1 = self.points[i_p]
            p2 = self.points[0 if i_p+1==len(self.points) else i_p+1]
            if p1._2d_point != None and p1._3d_point[2] >= 0.01:
                new_points.append(p1)
                if p2._2d_point == None or p2._3d_point[2] < 0.01:
                    new_points.append(graphic_point(mtx_cal.intersect_point([0,0,1,-0.01],p1._3d_point,p2._3d_point)).make_2d_point())
            elif p2._2d_point != None and p2._3d_point[2] >= 0.01:
                new_points.append(graphic_point(mtx_cal.intersect_point([0,0,1,-0.01],p1._3d_point,p2._3d_point)).make_2d_point())
        self.points = new_points

    def y_drawing_range(self,search_range): #y_drawing_range関数：ビューポート座標系のy成分の多角形の描画範囲を返す
        max = -search_range;min = search_range
        for i in range(len(self.points)):
            max = max = self.points[i]._2d_point[1] if max<self.points[i]._2d_point[1] else max
            min = min = self.points[i]._2d_point[1] if min>self.points[i]._2d_point[1] else min
        if max > search_range and min <= search_range:
            max = search_range
        if min < -search_range and -search_range <= max:
            min = -search_range
        if -search_range <= min <= search_range and -search_range <= max <= search_range:
            return [min,max]
        return [0,0]
    
    def intersects_of_line_and_polygon(self,y,search_range): #intersects_of_line_and_polygon関数：ビューポート座標系のy座標を引数にとり、多角形との交点を返す
        intersects = []
        n = len(self.points)
        for i in range(n):
            x1, y1 = self.points[i]._2d_point
            x2, y2 = self.points[(i + 1) % n]._2d_point
            if min(y1, y2) <= y <= max(y1, y2) and y2 - y1!=0:
                intersect_x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                if y1 == y:
                    -search_range if -search_range > x1 else intersects.append(x1)
                    search_range if search_range < x2 else intersects.append(x2)
                elif -search_range > intersect_x:
                    intersects.append(-search_range)
                elif intersect_x > search_range:
                    intersects.append(search_range)
                else:
                    intersects.append(intersect_x)
        intersects.sort()
        return intersects
    
    def intersect_depth(self,point): #引数にビューポート座標系の座標をとり、3次元座標系の直線(視線)との交点の座標を求める
        return mtx_cal.intersect_point(self.equation,[0,0,0],[point[0],point[1],1])

#graphic_pointやgraphic_surfaceを元に描画データを作るクラス
class canvas():
    def __init__(self,perspective): #コンストラクタ：ピクセル座標、ビューポート座標、graphic_surfaceオブジェクトを
        self.perspective = perspective
        self.image = array.array('B', (0,) * (self.perspective.image_pixel[0] * self.perspective.image_pixel[1] * 3)) #描画データ
        self.layers = array.array('f', (-1,) * (self.perspective.image_pixel[0] * self.perspective.image_pixel[1])) #描画対象と奥行きを保存する
        if self.perspective.drawing_mode[0]:
            for graphic_point_index in range(len(self.perspective.graphic_points)):
                if self.perspective.graphic_points[graphic_point_index] != None:
                    self.drawing_point(graphic_point_index)
        if self.perspective.drawing_mode[1]:
            for graphic_side in self.perspective.graphic_sides:
                if graphic_side != None:
                    self.drawing_side(graphic_side)
        if self.perspective.drawing_mode[2]:
            for graphic_surface in self.perspective.graphic_surfaces:
                if graphic_surface != None:
                    self.drawing_surface(graphic_surface)


    def drawing_point(self,index): #drawing_point関数：点の描画データを作る関数
        graphic_point = self.perspective.graphic_points[index]
        if graphic_point._2d_point != None and graphic_point.color != None:
            point_radius = round(self.perspective.image_pixel[1]/self.perspective.window_size[1]*2)
            for y in range(round(self.coordinate_value_change(graphic_point._2d_point[1],'y:v_to_p'))-point_radius,round(self.coordinate_value_change(graphic_point._2d_point[1],'y:v_to_p'))+point_radius+1):
                for x in range(round(self.coordinate_value_change(graphic_point._2d_point[0],'x:v_to_p'))-point_radius,round(self.coordinate_value_change(graphic_point._2d_point[0],'x:v_to_p'))+point_radius+1):
                    depth = (graphic_point._3d_point[0]**2+graphic_point._3d_point[1]**2+graphic_point._3d_point[2]**2)**(1/2)
                    index = y*self.perspective.image_pixel[0]+x
                    if 0 <= x < self.perspective.image_pixel[0] and 0 <= y < self.perspective.image_pixel[1] and (self.layers[index]==-1 or self.layers[index] > depth):
                        self.layers[index] = depth
                        self.image[index*3] = round(graphic_point.color[0])
                        self.image[index*3+1] = round(graphic_point.color[1])
                        self.image[index*3+2] = round(graphic_point.color[2])

    def drawing_side(self,graphic_side): #drawing_side関数：線の描画データを作る関数
        if graphic_side.point1._2d_point != None and graphic_side.point2._2d_point != None:
            veiwport_p1 = graphic_side.point1._2d_point
            veiwport_p2 = graphic_side.point2._2d_point
            up_line = [veiwport_p1[1] <= self.perspective.viewport[1],veiwport_p2[1] <= self.perspective.viewport[1]]
            down_line = [veiwport_p1[1] >= -self.perspective.viewport[1],veiwport_p2[1] >= -self.perspective.viewport[1]]
            right_line = [veiwport_p1[0] <= self.perspective.viewport[0],veiwport_p2[0] <= self.perspective.viewport[0]]
            left_line = [veiwport_p1[0] >= -self.perspective.viewport[0],veiwport_p2[0] >= -self.perspective.viewport[0]]
            if ((up_line[0] and down_line[0]) or (up_line[1] and down_line[1])) and ((right_line[0] and left_line[0]) or (right_line[1] and left_line[1])):
                intersects_t = []
                for b_d in [[0,1,-self.perspective.viewport[1],1],[0,1,self.perspective.viewport[1],1],[1,0,-self.perspective.viewport[0],1],[1,0,self.perspective.viewport[0],1]]:
                    intersects_t.append(mtx_cal.intersect_point(b_d,veiwport_p1,veiwport_p2))
                if not up_line[0]:
                    veiwport_p1 = intersects_t[0]
                elif not up_line[1]:
                    veiwport_p2 = intersects_t[0]
                elif not down_line[0]:
                    veiwport_p1 = intersects_t[1]
                elif not down_line[1]:
                    veiwport_p2 = intersects_t[1]
                elif not right_line[0]:
                    veiwport_p1 = intersects_t[2]
                elif not right_line[1]:
                    veiwport_p2 = intersects_t[2]
                elif not left_line[0]:
                    veiwport_p1 = intersects_t[3]
                elif not left_line[1]:
                    veiwport_p2 = intersects_t[3]
                pixel_p1 = self.coordinate_system_change(veiwport_p1,'v_to_p')
                pixel_p2 = self.coordinate_system_change(veiwport_p2,'v_to_p')
                oblong = abs(pixel_p1[0]-pixel_p2[0])>abs(pixel_p1[1]-pixel_p2[1])
                point_range = round(abs(pixel_p1[0]-pixel_p2[0]) if oblong else abs(pixel_p1[1]-pixel_p2[1]))
                if point_range > 0:
                    for t in range(point_range+1):
                        t /= point_range
                        point = mtx_cal.sum(col=pixel_p1,ccv=mtx_cal.mul(col=mtx_cal.sub(col=pixel_p2,ccv=pixel_p1),val=t))
                        x = round(point[0]);y = round(point[1])
                        _3d_point= mtx_cal.sum(col=graphic_side.point1._3d_point,ccv=mtx_cal.mul(col=mtx_cal.sub(col=graphic_side.point2._3d_point,ccv=graphic_side.point1._3d_point),val=t))
                        depth = (_3d_point[0]**2+_3d_point[1]**2+_3d_point[2]**2)**(1/2)
                        side_radius = round(self.perspective.image_pixel[1]/self.perspective.window_size[1])
                        for line in range(-side_radius,side_radius+1):
                            x = x if oblong else x+side_radius
                            y = y+side_radius if oblong else y
                            index = y*self.perspective.image_pixel[0]+x
                            if 0 <= x < self.perspective.image_pixel[0] and 0 <= y < self.perspective.image_pixel[1] and (self.layers[index]==-1 or self.layers[index] > depth):
                                self.layers[index] = depth
                                self.image[index*3] = round(graphic_side.color[0])
                                self.image[index*3+1] = round(graphic_side.color[1])
                                self.image[index*3+2] = round(graphic_side.color[2])
    
    def drawing_surface(self,graphic_surface): #drawing_surface関数：面の描画データを作る関数
        y_range = graphic_surface.y_drawing_range(self.perspective.viewport[1])
        for y in range(math.ceil(self.coordinate_value_change(y_range[0],'y:v_to_p')),int(self.coordinate_value_change(y_range[1],'y:v_to_p')+1)):
            intersects = graphic_surface.intersects_of_line_and_polygon(self.coordinate_value_change(y,'y:p_to_v'),self.perspective.viewport[0])
            for i in range(int(len(intersects)/2)):
                for x in range(math.ceil(self.coordinate_value_change(intersects[i],'x:v_to_p')),0 if int(self.coordinate_value_change(intersects[i+1],'x:v_to_p'))==0 else int(self.coordinate_value_change(intersects[i+1],'x:v_to_p')+1)):
                    if 0 <= x < self.perspective.image_pixel[0] and 0 <= y < self.perspective.image_pixel[1]:
                        _3d_point = graphic_surface.intersect_depth(self.coordinate_system_change([x,y],'p_to_v'))
                        if _3d_point!=None:
                            depth = (_3d_point[0]**2+_3d_point[1]**2+_3d_point[2]**2)**(1/2)
                            index = y*self.perspective.image_pixel[0]+x
                            if self.layers[index]==-1 or self.layers[index] > depth:
                                self.layers[index] = depth
                                color_adjustment = (1/(depth**2)*self.perspective.brightness) * (abs(mtx_cal.mul(col=graphic_surface.equation[:3],rcv=_3d_point)/(((graphic_surface.equation[0]**2+graphic_surface.equation[1]**2+graphic_surface.equation[2]**2)**(1/2))*(depth)))*self.perspective.contrast+(1-self.perspective.contrast))
                                color_adjustment = 1 if depth==0 else min(color_adjustment,1)
                                self.image[index*3] = round(graphic_surface.color[0]*color_adjustment)
                                self.image[index*3+1] = round(graphic_surface.color[1]*color_adjustment)
                                self.image[index*3+2] = round(graphic_surface.color[2]*color_adjustment)
        
    def coordinate_system_change(self,point,type): #ビューポート座標系とピクセル座標系の座標変換を行う
        if (type=='v_to_p'):
            return [(point[0]/self.perspective.viewport[0]+1.0)*self.perspective.image_pixel[0]/2.0,(point[1]/self.perspective.viewport[1]+1.0)*self.perspective.image_pixel[1]/2.0]
        elif (type=='p_to_v'):
            return [(point[0]/self.perspective.image_pixel[0]*2.0-1.0)*self.perspective.viewport[0],(point[1]/self.perspective.image_pixel[1]*2.0-1.0)*self.perspective.viewport[1]]
        else:
            return None
        
    def coordinate_value_change(self,value,type): #ビューポート座標系とピクセル座標系の数値変換を行う
        if (type=='x:v_to_p'):
            return (value/self.perspective.viewport[0]+1.0)*self.perspective.image_pixel[0]/2.0
        elif (type=='x:p_to_v'):
            return (value/self.perspective.image_pixel[0]*2.0-1.0)*self.perspective.viewport[0]
        elif (type=='y:v_to_p'):
            return (value/self.perspective.viewport[1]+1.0)*self.perspective.image_pixel[1]/2.0
        elif (type=='y:p_to_v'):
            return (value/self.perspective.image_pixel[1]*2.0-1.0)*self.perspective.viewport[1]
        else:
            return None