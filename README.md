# Abeno Graphic

## 概要
Pythonで3次元の描画を行うライブラリです。

sample1.pyイメージ
![Image](https://github.com/user-attachments/assets/501bbb58-cd40-4b33-9d93-1da257fe08fb)

sample2.pyイメージ
![Image](https://github.com/user-attachments/assets/09136165-fad6-4043-82c1-b84bab992f19)

## 特徴
- PyPyに最適化
- 面、線、点などの情報を指定して描画
- カプセル化などは行っておらず、柔軟性重視の設計
- 処理速度は、描画ピクセル数と強い関係

## 詳細
- **モジュール名**：abeno_graphic
- **言語**：(Python 3.7以上)
- **ライブラリやツール**：(PyPy(CPython) pip pygame)

## データの扱い方について
- **3次元座標**：\[x座標,y座標,z座標\] (float)
- **色情報**：\[red,green,blue\] (unit8)
- **点情報**：\[色情報,3次元座標\] ※色情報は省略可
- **点配列**：\[点情報1,点情報2,...\]
- **線情報**：\[色情報,\[線の始点の点情報,線の終点の点情報\]\] ※点情報は点配列のインデックスを指定
                                                       ※また、色情報は省略可
- **線配列**：\[線情報1,線情報2,...\]
- **面情報**：\[色情報,\[面に属する点情報1,面に属する点情報2,...\]\] ※点情報は点配列のインデックスを指定
                                                             ※また、色情報は省略可
- **面配列**：\[面情報1,面情報2,...\]

## 外部用に設計されたクラス
- **world**：3次元の世界を管理するクラス
- **perspective**：3次元の世界の視点を管理するクラス
- **クラス同士の関係** 上記2クラスは、world has-a perspectiveの関係

### 各クラスの説明

#### worldクラスについて
- **主要属性**
  - world_points：3次元世界の点配列
  - world_sides：3次元世界の線配列
  - world_surfaces：3次元世界の面配列
- **外部用メソッド**
  - \_\_init\_\_(self,points=\[\],sides=\[\],surfaces=\[\],default_color=\[255,255,255\]): コンストラクタ
    - points：点配列を受け取る仮引数 world_points属性に代入
    - sides：線配列を受け取る仮引数 world_sides属性に代入
    - surfaces：面配列を受け取る仮引数 world_surfaces属性に代入
    - default_color：初期の色情報を受け取る仮引数 ※色情報を省略した点、線、面はこの色になる

  - add_point(self,coordinate,color=\[255,255,255\]): 点を追加するメソッド
    - coordinate：3次元座標を受け取る引数
    - color：色情報を受け取る仮引数
    - return index：点が追加されたworld_points属性のインデックスを戻り値とする

  - move_point(self,index,coordinate,type='relative'): 点を動かすメソッド
    - index：world_points属性のインデックスを受け取る引数
    - coordinate：3次元座標を受け取る引数
    - type：相対座標(relative)か絶対座標(absolute)かを指定する仮引数

  - delete_point(self,index): 点を削除するメソッド
    - index：削除するworld_points属性のインデックスを受け取る引数

  - add_side(self,side,color=\[255,255,255\]): 線を追加するメソッド
    - side：\[線の始点のworld_points属性のインデックス,線の終点のworld_pointsのインデックス\]を受け取る引数
    - color：色情報を受け取る仮引数
    - return index：線が追加されたworld_sides属性のインデックスを戻り値とする

  - parallel_move_side(self,index,coordinate): 線を相対移動させるメソッド
    - index：world_sides属性のインデックスを受け取る引数
    - coordinate：3次元相対座標を受け取る引数

  - delete_side(self,index): 線を削除するメソッド
    - index：削除するworld_sides属性のインデックスを受け取る引数

  - add_surface(self,surface,color=\[255,255,255\]): 線を追加するメソッド
    - surface：\[world_points属性のインデックス1,world_points属性のインデックス2,...\]を受け取る引数
    - color：色情報を受け取る仮引数
    - return index：線が追加されたworld_surfaces属性のインデックスを戻り値とする

  - parallel_move_surface(self,index,coordinate): 線を相対移動させるメソッド
    - index：world_surfaces属性のインデックスを受け取る引数
    - coordinate：3次元相対座標を受け取る引数

  - delete_side(self,index): 線を削除するメソッド
    - index：削除するworld_surfaces属性のインデックスを受け取る引数

#### perspectiveクラスについて
- **主要属性**
  - self.world：視点が存在する3次元世界 (world)
  - self.position：視点の3次元座標
  - self.direction_facing：視点が向いている方向 \[z軸回転成分,x軸回転成分\] (radian)
  - self.viewport：ビューポート \[横幅,縦幅\] (float)
  - self.image_pixel：演算ピクセル数のリスト \[横幅,縦幅\] (int)
  - self.drawing_mode：描画モード \[点描画判定,線描画判定,面描画判定\] (bool)
  - self.window_size：ウィンドウサイズ \[横幅,縦幅\] (int)
  - self.title：ウィンドウタイトル (str)
  - self.fps：fps (int)
  - self.speed：移動速度 (foat)
  - self.aim_sensitivity：視点移動速度 (float)
  - self.brightness：光の強さ (foat)
  - self.contrast：コントラスト (float)
- **外部用メソッド**
  - \_\_init\_\_(self,world,position=\[0,0,0\],direction_facing=\[0,0\],viewport=\[1.5,1.0\],image_pixel=\[150,100\],drawing_mode=\[True,True,True\],window_size=\[600,400\],title="Abeno_Graphic",fps=60,speed=1,aim_sensitivity=1,brightness=1,contrast=0.5): コンストラクタ
    - world：worldクラスを受け取る引数 world属性に代入
    - position：3次元座標を受け取る仮引数 position属性に代入
    - direction_facing：視点が向いている方向 \[z軸回転成分,x軸回転成分\] (float,radian) direction_facing属性に代入
                        ※視点が向いている方向をz軸上向き方向をy軸横向き方向をx軸とする正規直交基底によって定義された座標系を元に回転する。また、回転の順序はリスト順です。
    - viewport：ビューポート座標系の領域設定 \[横幅の半領域,縦幅の半領域\] (float) viewport属性に代入
                ※viewport = \[Vw,Vh\] と視野角の横幅 Aw と視野角の縦幅 Ah は次のような関係に当たります。
                Vw = tan(Aw)/2 Vh = tan(Ah)/2
    - image_pixel：演算ピクセル数のリストを受け取る仮引数 \[横幅,縦幅\] (int) image_pixel属性に代入
    - drawing_mode：描画モードのリストを受け取る仮引数 \[点描画判定,線描画判定,面描画判定\] (bool) drawing_mode属性に代入
    - window_size：ウィンドウサイズを受け取る仮引数 \[横幅,縦幅\] (int) window_size属性に代入
    - title：ウィンドウタイトルを受け取る仮引数 (str) title属性に代入
    - fps：fpsを受け取る仮引数 (int) fps属性に代入
    - speed：移動速度を受け取る仮引数 (foat) speed属性に代入
    - aim_sensitivity：視点移動速度を受け取る仮引数 (float) aim_sensitivity属性に代入
    - brightness：光の強さ (foat) brightness属性に代入
    - contrast：コントラスト (float,c:0<=c<=1) contrast属性に代入

  - start_user_interface(self,external_function=None): GUIを起動させるメソッド
    - external_function：ループ内で呼び出される外部関数 (function) 

## 視点の操作方法について
- w：前移動
- a：左移動
- s：後移動
- d：右移動
- ↑：上方視点移動
- ←：左方視点移動
- ↓：下方視点移動
- →：右方視点移動

## 処理速度について
1. PyPyを利用することで処理速度が一段と早くなります ※PyPyを利用するとnumpyなどのC言語系のライブラリが著しく遅くなります
2. 演算ピクセル解像度(image_pixel\[0\]×image_pixel\[1\])が50000を超えると処理が重くなりやすくなります
3. 処理速度はビューポート内の面のピクセル数に依存するため、近くで面を見ると処理速度が遅くなる場合があります。