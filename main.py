import pyxel
import random

class ScrollGame:
    def __init__(self):
        # 1. 画面の初期化 (幅, 高さ, タイトル)
        pyxel.init(160, 120, title="Pyxel Scroll Game")
        
        # 2. ゲームの状態管理用変数
        self.player_x = 20
        self.player_y = 50
        self.player_speed = 2
        
        # 背景のスクロール位置
        self.bg_scroll = 0
        
        # 敵のデータ [x, y, スピード]
        self.enemies = []
        self.spawn_enemy()
        
        # ゲームオーバーフラグとスコア
        self.is_game_over = False
        self.score = 0

        # 3. ゲームループの開始 (更新関数, 描画関数)
        pyxel.run(self.update, self.draw)

    def spawn_enemy(self):
        """画面外（右側）に敵を生成する"""
        enemy_y = random.randint(10, 100)
        enemy_speed = random.randint(1, 3)
        self.enemies.append([160, enemy_y, enemy_speed])

    def update(self):
        """フレームごとのデータ更新処理（ロジック）"""
        if self.is_game_over:
            # ゲームオーバー時にRキーでリスタート
            if pyxel.btnp(pyxel.KEY_R):
                self.__init__()
            return

        # --- プレイヤーの移動処理 ---
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            self.player_y = max(0, self.player_y - self.player_speed)
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.player_y = min(112, self.player_y + self.player_speed)
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.player_x = max(0, self.player_x - self.player_speed)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.player_x = min(152, self.player_x + self.player_speed)

        # --- 背景のスクロール ---
        self.bg_scroll = (self.bg_scroll + 1) % 160

        # --- 敵の管理とスクロール ---
        # 一定確率で新しい敵を登場させる
        if pyxel.frame_count % 45 == 0:
            self.spawn_enemy()

        for enemy in self.enemies:
            enemy[0] -= enemy[1]  # 左へ進む (スピード分)

            # 当たり判定 (自機と敵の四角形が重なっているか)
            # 自機サイズ: 8x8, 敵サイズ: 8x8 と仮定
            if (self.player_x < enemy[0] + 8 and
                enemy[0] < self.player_x + 8 and
                self.player_y < enemy[1] + 8 and
                enemy[1] < self.player_y + 8):
                self.is_game_over = True

        # 画面外に出た敵を削除し、スコア加算
        old_count = len(self.enemies)
        self.enemies = [e for e in self.enemies if e[0] > -8]
        self.score += (old_count - len(self.enemies))

    def draw(self):
        """フレームごとの描画処理（画面への表示）"""
        # 画面をクリア (0は黒)
        pyxel.cls(0)

        if self.is_game_over:
            # ゲームオーバー画面
            pyxel.text(50, 50, "GAME OVER", 8)  # 8は赤色
            pyxel.text(40, 70, f"YOUR SCORE: {self.score}", 7)
            pyxel.text(35, 90, "Press 'R' to Restart", 6)
            return

        # --- 背景（星屑）の描画 ---
        # スクロール座標を利用して、左に流れるドットを描画
        for i in range(10):
            x = (i * 32 - self.bg_scroll) % 160
            y = (i * 13) % 120
            pyxel.pset(x, y, 5) # 5は暗いグレー

        # --- プレイヤー（自機）の描画 ---
        # とりあえず四角形 (x, y, 幅, 高さ, 色番)
        # 11は緑色 / 9はオレンジ色など
        pyxel.rect(self.player_x, self.player_y, 8, 8, 11)

        # --- 敵の描画 ---
        for enemy in self.enemies:
            pyxel.rect(enemy[0], enemy[1], 8, 8, 8) # 8は赤色

        # --- スコア表示 ---
        pyxel.text(5, 5, f"SCORE: {self.score}", 7) # 7は白色

# ゲームの実行
ScrollGame()