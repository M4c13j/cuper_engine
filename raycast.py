# coding=utf-8
import pygame
import math

pygame.init()

font_size = 22 # rozmiar czcionki

black = ( 0 , 0 , 0 )
white = ( 255 , 255 , 255 )
red = ( 255 , 0 , 0 )
blue = ( 0 , 0 , 255 )
grey = ( 128 , 128 , 128 )
green = ( 50 , 205 , 50 )
pink = (255,20,147)
yellow = (255,255,0)
brown = (210,105,30)

color = (red,blue,green,pink,yellow,brown)


#    ----  textury  ---- 8x8
'''
    [1,1,1,1,1,1,1,1],
    [0,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1],
    [0,1,0,0,0,1,0,0],
    [1,1,1,1,1,1,1,1],
    [0,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1],
    [0,1,0,0,0,1,0,0]'''

#    ----  elementy gry ----

class Engine:
    def __init__(self):
        self.delay = 0                              # opóźnienie w ms

        self.screenWidth = 900                     # szerokość
        self.screenHeight = 600                     # wysokość

        self.fov = 75                               # pole widzenia
        self.angle = 90                             # kąt obrotu
        self.rotAngle = 15                          # zmiana kąta przy obrocie
        self.step = 0.25                            # szybkość przemieszczania

        self.x = 1.5                                # pozycja x
        self.y = 1.5                                # pozycja y

        self.dAngle = self.fov / self.screenWidth   # przyrost kąta z każdą iteracją
        self.accuracy = 32                          # dokładność

        self.mapWidth = 24                          # szerokość mapy
        self.mapHeight = 24                         # wysokość mapy
        self.mapa = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,3,3,1,2,2,2,2,2,0,0,2,3,3,0,3,0,3,3,3,3,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,1,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
            [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,0,2,2,1,1,1,1,3,1,3,1,3,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,2,0,2,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,2,0,0,0,0,3,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,2,0,3,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,2,0,2,2,2,2,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,2,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
            

        self.screen = pygame.display.set_mode( (self.screenWidth , self.screenHeight) )  
        self.title = "Cuper Engine 0.5-beta"
        pygame.display.set_caption( self.title )
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible( 1 )
        self.font = pygame.font.SysFont( 'Arial', font_size )
        
    # czyści ekran i tyle
    def reset_ekranu( self ):
        #self.screen.fill( white )
        pygame.draw.rect( self.screen , black , ( 0 , 0 , self.screenWidth , self.screenHeight/2 ))
        pygame.draw.rect( self.screen , grey , (0 , self.screenHeight/2, self.screenWidth, self.screenHeight ))

    # stopnie do radianów
    def degToRad( self, angle ):
        return angle * math.pi / 180

    # rysuje mapę mapy
    def drawMap(self):
        a = 20 # bok kwadratu
        
        for i in range(self.mapHeight):
            x = (self.screenWidth/2 - a * self.mapWidth / 2)//1
            y = ( self.screenHeight/2 - a * self.mapHeight / 2)//1 + i*a
            for j in range(self.mapWidth):
                if self.mapa[i][j]!=0:
                    col = white
                else:
                    col = black
                pygame.draw.rect( self.screen , col , ( x , y , a , a))
                x+=a
        dx = self.screenWidth / self.mapWidth * self.x
        dy = self.screenHeight / self.mapHeight * self.y

        pygame.draw.circle( self.screen , red , (math.floor( self.screenWidth/2 - a * self.mapWidth / 2 + dx) , math.floor( self.screenHeight/2 - a * self.mapHeight / 2 +dy)), int(a/2))

    # rysuje tekstury
    def drawTexture(self , x , ray , wh , pos):
        th = 8
        tw = 8
        texture =  [
                    [[6,5,2,0,6,5,2,0],
                     [0,6,2,4,0,6,2,4],
                     [1,1,2,1,1,1,2,1],
                     [2,4,6,5,2,4,6,5],
                     [2,1,1,1,2,1,1,1],
                     [5,2,0,6,5,2,0,6],
                     [6,2,4,0,6,2,4,0],
                     [1,2,1,1,1,2,1,1]]
                    ,
                    [[1,1,1,1,1,1,1,1],
                     [1,0,0,0,0,0,0,1],
                     [1,0,1,0,0,1,0,1],
                     [1,0,0,0,0,0,0,1],
                     [1,0,0,0,0,0,0,1],
                     [1,0,1,0,0,1,0,1],
                     [1,0,0,0,0,0,0,1],
                     [1,1,1,1,1,1,1,1]]
                    ,
                    [[0,1,2,3,0,1,2,3],
                     [0,1,2,3,0,1,2,3],
                     [0,1,2,3,0,1,2,3],
                     [0,1,2,3,0,1,2,3],
                     [0,1,2,3,0,1,2,3],
                     [0,1,2,3,0,1,2,3],
                     [0,1,2,3,0,1,2,3],
                     [0,1,2,3,0,1,2,3]]
            ]
        c = [ 
                [ (110,62,44) , (109,96,90) , (130,117,111) , (108,95,89) , (78,44,34) , (126,70,50) , (125,60,50)] , 
                [ yellow,green ] , 
                [ red , yellow , green , (0,78,255)]
            ]
        12345
        dy = (wh * 2) / th
        y = self.screenHeight - wh
        for i in range(th):
            state = texture[pos-1][ i ][ int(tw * (ray[0]+ray[1]) % tw)]
            pygame.draw.line( self.screen , c[pos-1][state] , (x, int(self.screenHeight - wh)/2 +(i-1)*dy) , (x, int(self.screenHeight - wh)/2 +(i)*dy) , 1 )


    # rysuje kreskę w sumie
    def drawSection( self , wh , x , pos , ray):
        pygame.draw.line( self.screen , color[pos] , (x, (self.screenHeight - wh)/2 )//1 , (x,(self.screenHeight + wh)/2 )//1 , 1 )



    # tu się moi drodzy dzieje cała magia
    def raycasting(self):
        rayAngle = self.angle - self.fov/2

        for i in range( self.screenWidth ):

            ray = [ self.x, self.y ]

            rayCos = math.cos( rayAngle * math.pi / 180 )
            raySin = math.sin( rayAngle * math.pi / 180 )

            hit = False
            pos = 0

            ac = self.accuracy
            k = 0
            side = 0
            while hit!=True:
                if k%100==0:
                    ac = ac / 2
                ray[0] += rayCos / ac
                ray[1] += raySin / ac
                k+=1
                pos = self.mapa[int(ray[0])][int(ray[1])]
                hit = (pos != 0)
            
            dist = math.sqrt( math.pow(self.x - ray[0],2) + math.pow(self.y-ray[1],2) )
            dist = dist * math.cos( (rayAngle - self.angle) * math.pi / 180) # bye bye fisheye

            wh = int( self.screenHeight / (2 * dist))

            self.drawTexture(i,ray,wh, pos )

            rayAngle += self.dAngle


    # główna funkcja
    def play( self ):
        end = False
        i=0

        go = False
        back = False
        left = False
        right = False
        mapa = False
        shift = False
        while not end:
            i+=1
            #pygame.time.delay( self.delay )
            self.reset_ekranu()

            # obsługa kliknięć
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        back = True
                    if event.key == pygame.K_UP:
                        go = True
                    if event.key == pygame.K_RIGHT:
                        right = True
                    if event.key == pygame.K_LEFT:
                        left = True
                    if event.key == pygame.K_m:
                        mapa = True
                    if event.key == pygame.K_LSHIFT:
                        shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        back = False
                    if event.key == pygame.K_UP:
                        go = False
                    if event.key == pygame.K_RIGHT:
                        right = False
                    if event.key == pygame.K_LEFT:
                        left = False
                    if event.key == pygame.K_m:
                        mapa = False
                    if event.key == pygame.K_LSHIFT:
                        shift = False

            if go:
                self.x += math.cos( self.angle * math.pi / 180) * ( self.step * (1+shift) )
                self.y += math.sin( self.angle * math.pi / 180) * ( self.step * (1+shift) )
                self.x = round(self.x,3)
                self.y = round(self.y,3)
            if back:
                self.x -= math.cos( self.angle * math.pi / 180) * ( self.step * (1+shift) )
                self.y -= math.sin( self.angle * math.pi / 180) * ( self.step * (1+shift) )
                self.x = round(self.x,3)
                self.y = round(self.y,3)
            if left:
                self.angle -= self.rotAngle
                self.angle %= 360
            if right:
                self.angle += self.rotAngle
                self.angle %= 360

            self.raycasting()

            if mapa:
                self.drawMap()


            pygame.display.update()
            print( i,self.x,self.y, self.angle)


game = Engine()
game.play()

'''
https://lodev.org/cgtutor/raycasting.html
https://github.com/vinibiavatti1/RayCastingTutorial/wiki/RayCasting

'''