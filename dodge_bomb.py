import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {pg.K_UP : (0, -5), 
         pg.K_DOWN : (0, 5), 
         pg.K_LEFT : (-5, 0),
         pg.K_RIGHT : (5, 0),
         }



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    #コウカトン初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    #爆弾初期化
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    vx = 5
    vy = 5
    #応用課題1こうかとん
    kk_img2 = pg.image.load("fig/8.png")

    def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
        """ 
        引数：こうかとん Rectまたは爆弾Rect
        戻り値：判定結果タプル（横, 縦）
        画面内ならTrue, 画面外ならFalse
        """
        yoko, tate = True, True
        #横方向判定
        if rct.left < 0 or WIDTH < rct.right:
            yoko = False
        #縦方向判定
        if rct.top < 0 or HEIGHT < rct.bottom:
            tate = False
        return (yoko, tate)
    
    #応用課題1
    def gameover(screen: pg.Surface) -> None:
        img = pg.Surface((WIDTH, HEIGHT))
        pg.draw.rect(img, (0,0,0), pg.Rect(0, 0, WIDTH, HEIGHT))
        img.set_alpha(100)
        screen.blit(img, [0,0])
        screen.blit(kk_img2, [350, 280]) 
        screen.blit(kk_img2, [710, 280]) 
        fonto = pg.font.Font(None, 80)
        txt = fonto.render("Game Over", True, (255, 255, 255))
        screen.blit(txt, [400, 300])
        pg.display.update()
        time.sleep(5)
    
    # 応用課題2
    def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
        bb_accs = [a for a in range(1, 11)]
        bb_imgs = []
        for r in range(1, 11):
            bb_img = pg.Surface((20*r, 20*r))
            pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
            bb_img.set_colorkey((0, 0, 0))
            bb_imgs += [bb_img]
        return bb_accs, bb_imgs


    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]



        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        # 応用課題2
        bb_accs, bb_imgs = init_bb_imgs()
        avx = vx * bb_accs[min(tmr//500, 9)]
        avy = vy * bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)
        yoko, tate =  check_bound(bb_rct)
        if not yoko:  # 左右どちらかにはみ出ていたら
            vx *= -1
        if not tate:  # 上下どちらかにはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
