import pygame as pg
from random import *
import time
import math
from os import path
vek = pg.math.Vector2

TITLE = "Hüppaja"
laius = 800
kõrgus = 600
kell = 60
fonti_nimi = "arial"
Fail = "Suurim_Skoor.txt"

#mängia settingud

mängija_kiirendus = 0.5
mängija_takistus_teg = -0.12
mängija_gravitatsioon = 0.5
hüppe_kõrgus = 15
sheet = "spritesheet_jumper.png"
Raha = 10
mitu_esinemist = 4
Arv = 0
LEVEL = 0

#platvormid

platvormide_list1 = [(0, kõrgus-40),(125, kõrgus-300),(650,200),(500,300)]
platvormide_list2 = [(750, 550), (125, laius - 350), (350, 200), (175, 100)]
platvormide_list3 = [(550, 450), (650, 250), (450, 150), (100, 150)]
platvormide_list4 = [(100, 400), (100, 150), (400, 250), (650, 150)]
platvormide_list5 = [(100, 250), (400, 100), (650, 550), (700, 250)]
platvormide_list6 = [(50, 550), (50, 350), (150, 50), (450, 150), (700, 250)]
platvormide_list7 = [(100, 300), (50, 100), (370, 100), (600, 200), (550, 350)]
platvormide_list8 = [(50, 250), (355, 130), (650, 350)]

algplat = [(laius/2 - 50, kõrgus*3/4)]

# värvid ja pildid
ekraanide_vahevärv = (0, 0, 0)
valge = (255, 255, 255)
must = (0, 0, 0)
punane = (255, 0, 0)
roheline = (0, 255, 0)
sinine = (0, 0, 255)
kollane = (255, 255, 0)
helesinine = (0, 155, 155)
pallImg = pg.image.load("pall.png")
teradimg = pg.image.load("terad.png")



class Spritesheet:
    #kujundus
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        pilt = pg.Surface((width, height))
        pilt.blit(self.spritesheet, (0, 0), (x, y, width, height))
        pilt = pg.transform.scale(pilt, (width // 2, height // 2))
        return pilt



class Player(pg.sprite.Sprite):

    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pallImg
        self.rect = self.image.get_rect()
        self.rect.center = (laius/2 , kõrgus/2)
        self.pos = vek(laius/2 -15, kõrgus/2)
        self.kiirus = vek(0, 0)
        self.kiirendus = vek(0,0)

    def hüppa(self):
        self.rect.x += 1
        puude = pg.sprite.spritecollide(self, self.game.platvormid, False)
        self.rect.x -= 1
        if puude:
            self.game.hüppamis_sound.play()
            self.kiirus.y = -hüppe_kõrgus

    def update(self):
        self.kiirendus = vek(0, mängija_gravitatsioon)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.kiirendus.x = -mängija_kiirendus

        if keys[pg.K_RIGHT]:
            self.kiirendus.x = mängija_kiirendus

        self.kiirendus.x += self.kiirus.x * mängija_takistus_teg
        self.kiirus += self.kiirendus
        self.pos += self.kiirus + 0.5 * self.kiirendus
        if self.pos.x > laius:
            self.pos.x = 0
        if self. pos.x < 0:
            self.pos.x = laius

        self.rect.midbottom = self.pos


class AlgPlatvorm(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.platvormid
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(382, 408, 200, 100)
        self.image.set_colorkey(must)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Platvorm(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.platvormid
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(213, 1662, 201, 100)
        self.image.set_colorkey(must)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        Mün(self.game, self)



class Mün(pg.sprite.Sprite):
    def __init__(self, game, plat):
        global Arv
        self.grupid = game.all_sprites, game.mündid
        pg.sprite.Sprite.__init__(self, self.grupid)
        self.game = game
        self.hetk_raam = 0
        self.viimane_uuendus = 0

        self.plat = plat
        a = randint(1, 2)
        if a == 2:
            self.type = "Surm"
            self.image = teradimg
            self.rect = self.image.get_rect()
            self.rect.centerx = self.plat.rect.centerx
            self.rect.bottom = self.plat.rect.top
        else:
            self.type = "Kuld"
            self.image = self.game.spritesheet.get_image(698, 1931, 84, 84)
            self.image.set_colorkey(must)
            self.rect = self.image.get_rect()
            self.rect.centerx = self.plat.rect.centerx
            self.rect.bottom = self.plat.rect.top - 5
            Arv += 1



class Game:
    def __init__(self):
        global LEVEL
        # aknad ja stuff
        self.koguskoor = 0
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((laius, kõrgus))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.jookseb = True
        self.elus = True
        self.font_name = pg.font.match_font(fonti_nimi)
        self.load_data()


    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, Fail), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        self.dir = path.dirname(__file__)
        pildid_dir = path.join(self.dir, "pildid")
        self.spritesheet = Spritesheet(path.join(pildid_dir, sheet))
        self.heli_dir = path.join(self.dir, 'heli')
        self.hüppamis_sound = pg.mixer.Sound(path.join(self.heli_dir, 'Jump33.wav'))

    def new(self):
        # alusta uut mängu
        global LEVEL
        global Arv
        Arv = 0
        self.skoor = 0
        self.all_sprites = pg.sprite.Group()
        self.platvormid = pg.sprite.Group()
        self.algusPlat = pg.sprite.Group()
        self.mündid = pg.sprite.Group()
        self.mängija = Player(self)
        self.all_sprites.add(self.mängija)
        if LEVEL == 0:
            a = platvormide_list1
        if LEVEL == 1:
            a = platvormide_list2
        if LEVEL == 2:
            a = platvormide_list3
        if LEVEL == 3:
            a = platvormide_list4
        if LEVEL == 4:
            a = platvormide_list5
        if LEVEL == 5:
            a = platvormide_list6
        if LEVEL == 6:
            a = platvormide_list7
        if LEVEL == 7:
            a = platvormide_list8
        for plat in a:
            Platvorm(self, *plat)
        for alg in algplat:
            AlgPlatvorm(self, *alg)
        pg.mixer.music.load(path.join(self.heli_dir, 'Mängumuusika.ogg'))
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.fadeout(100)

        self.run()

    def run(self):
        # loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        self.level_com = False
        while self.playing:
            self.clock.tick(kell)
            self.events()
            self.update()
            self.draw()






    def update(self):
        # uuendused mängija ja objektide vahel
        global Arv
        global LEVEL
        self.aeg = round(time.perf_counter(), 1)
        self.all_sprites.update()
        if self.mängija.kiirus.y > 0:
            kokkupuude = pg.sprite.spritecollide(self.mängija, self.platvormid, False)
            if kokkupuude:
                self.mängija.pos.y = kokkupuude[0].rect.top + 1
                self.mängija.kiirus.y = 0

        if self.mängija.rect.bottom > kõrgus:
            if self.mängija.rect.bottom < 0:
                self.mängija.kill()
            self.playing = False
            LEVEL = 0

        objekt_kokkupõrge = pg.sprite.spritecollide(self.mängija, self.mündid, True)
        for münt in objekt_kokkupõrge:
            if münt.type == "Kuld":
                self.skoor += Raha
            if münt.type == "Surm":
                self.mängija.kill()
                self.playing = False
                LEVEL = 0

        if Arv*Raha == self.skoor:
            self.mängija.kill()
            self.koguskoor += self.skoor
            LEVEL += 1
            if LEVEL == 8:
                self.level_com = True
                self.playing = False
                LEVEL = 0
            else:
                self.level_com = True
                self.playing = False




    def events(self):
        # eventid mängijalt
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.jookseb = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.mängija.hüppa()

    def draw(self):
        # asjad platsile
        self.screen.fill(helesinine)
        self.all_sprites.draw(self.screen)
        self.kuva_tekst("Skoor: " + str(self.skoor), 22, valge, 100, 15)
        self.kuva_tekst("Koguskoor: " + str(self.koguskoor), 22, valge, laius -100, 15)
        #ekraan tagurpidi x ja y jaoks, mugavus tapab
        pg.display.flip()

    def mäng_algus_ekraan(self):
        self.screen.fill(ekraanide_vahevärv)
        self.kuva_tekst("Hüppaja", 48, valge, laius/2, kõrgus/4)
        self.kuva_tekst("Hüppad ja liigud suunaklahvidega", 22, valge, laius/2, kõrgus/2)
        self.kuva_tekst("Leveli läbimiseks kogu raha", 22, valge, laius / 2, kõrgus / 1.7)
        self.kuva_tekst("NB! Kui hüppad ekraanist välja liigub pall teisele poole ekraani", 22, valge, laius / 2, kõrgus/1.5 )
        self.kuva_tekst("Vajuta suvalist nuppu, et mängida", 22, valge, laius/2, kõrgus * 3/4)
        pg.display.flip()
        self.oota_vajutust_alg_ekraan()

    def levelite_vahel(self):
        if not self.playing:
            return
        self.screen.fill(ekraanide_vahevärv)
        self.kuva_tekst("Level läbitud!", 48, valge, laius / 2, kõrgus / 4)
        self.kuva_tekst("Skoor: " + str(self.skoor), 22, valge, laius / 2, kõrgus / 2)
        self.kuva_tekst("Vajuta suvalist nuppu, et uut levelit alustada", 22, valge, laius / 2, kõrgus * 3 / 4)
        pg.display.flip()
        self.oota_vajutust_alg_ekraan()

    def mäng_läbi_ekraan(self):
        #Mäng läbi ja uuesti
        if not self.jookseb:
            return
        self.screen.fill(ekraanide_vahevärv)
        self.kuva_tekst("Mäng Läbi", 48, punane, laius / 2, kõrgus / 4)
        self.kuva_tekst("Skoor: " + str(self.koguskoor), 22, valge, laius / 2, kõrgus / 2)
        self.aeg = time
        self.kuva_tekst("Vajuta suvalist nuppu, et uuesti mängida", 22, valge, laius / 2, kõrgus* 3/4)
        if self.koguskoor > self.highscore:
            self.highscore = self.koguskoor
            self.kuva_tekst("UUS PARIM SKOOR!", 22, helesinine, laius / 2, kõrgus / 2 + 40)
            with open(path.join(self.dir, Fail), 'w') as f:
                f.write(str(self.koguskoor))
        else:
            self.kuva_tekst("Parim Skoor: " + str(self.highscore), 22, kollane, laius / 2, kõrgus / 2 + 40)
        pg.display.flip()
        self.oota_vajutust_alg_ekraan()
        self.koguskoor = 0
        pg.mixer.music.fadeout(100)

    def oota_vajutust_alg_ekraan(self):
        magamine = True
        while magamine:
            self.clock.tick(1)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    magamine = False
                    self.jookseb = False
                if event.type == pg.KEYUP:
                    magamine = False



    def kuva_tekst(self, tekst, suurus, värv, x, y):
        font = pg.font.Font(self.font_name, suurus)
        tekst_pinnal = font.render(tekst, True, värv)
        text_rect = tekst_pinnal.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(tekst_pinnal, text_rect)


g = Game()
g.mäng_algus_ekraan()
while g.jookseb:
    g.new()
    if g.level_com == False:
        g.mäng_läbi_ekraan()
    else:
        g.levelite_vahel()

pg.quit()
quit()