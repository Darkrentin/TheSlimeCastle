import pyxel
import random

class Monstre3:
    def __init__(self,x,y,lvl,id):
        self.px=x+mres
        self.y=y+mres
        self.sens=True
        self.an=0
        self.an2=0
        self.start=0
        self.phase=0
        self.lvl=lvl
        self.lim=0
        self.lim2=0
        self.id=id
    def update(self,jeu):
        if self.phase==0:
            self.lim=self.px-jeu.perso.x
            self.lim2=self.lim
            if pyxel.frame_count%3==0:
                if pyxel.frame_count-self.start>200:
                    self.start=pyxel.frame_count
                    self.phase=1

                if self.sens:
                    test=pyxel.tilemap(0).pget((self.px-mres-2)//8,(self.y+(w*jeu.lvl)+mres+2)//8)
                    test2=pyxel.tilemap(0).pget((self.px-mres-2)//8,(self.y+(w*jeu.lvl))//8)
                else:
                    test=pyxel.tilemap(0).pget((self.px+mres+1)//8,(self.y+(w*jeu.lvl)+mres+1)//8)
                    test2=pyxel.tilemap(0).pget((self.px+mres+1)//8,(self.y+(w*jeu.lvl))//8)
                if test2 in switchON:
                    self.sens= not self.sens
                    print("ok")
                    for x in range(32*16):
                        for y in range((w*self.lvl)//8,(w*self.lvl)//8+32):
                            t=pyxel.tilemap(0).pget(x,y)
                            if t == MurO[0]:
                                jeu.mur(x*8,y*8,voidO)
                            if t == voidO[0]:
                                jeu.mur(x*8,y*8,MurO)
                            if t== switchON[0]:
                                jeu.mur(x*8,y*8,switchOFF)
                elif test2 in switchOFF:
                    self.sens= not self.sens
                    print("ok2")
                    for x in range(32*16):
                        for y in range((w*self.lvl)//8,(w*self.lvl)//8+32):
                            t=pyxel.tilemap(0).pget(x,y)
                            if t == MurO[0]:
                                jeu.mur(x*8,y*8,voidO)
                            if t == voidO[0]:
                                jeu.mur(x*8,y*8,MurO)
                            if t== switchOFF[0]:
                                jeu.mur(x*8,y*8,switchON)
                elif test in mur and test2 not in mur:
                    if self.sens==True:
                        self.px+=-2
                    else:
                        self.px+=2

                else:
                    self.sens=not self.sens
        elif self.phase==1:
            if pyxel.frame_count-self.start>60:
                self.phase=0
                self.an2=0
            if self.sens:
                for i in range(self.px,self.px-w,-1):
                    if pyxel.tilemap(0).pget(i//8,self.y//8) in mur:
                        self.lim=i-1
                        break
                self.lim=i
            elif not self.sens:
                for i in range(self.px,self.px+w):
                    if pyxel.tilemap(0).pget(i//8,self.y//8) in mur:
                        self.lim=i+1
                        break
                self.lim=i
            if pyxel.frame_count%3==0 and self.an2<=3:
                self.an2+=1

    def draw(self,persox):
        if self.sens:
            W=-res
        else:
            W=res
        if self.phase==0:
            if pyxel.frame_count%3==0:
                self.an+=1
            pyxel.blt(self.px-mres-persox,self.y-mres,1,16*(self.an%11),80,W,res,8)
        if self.phase==1:
            if self.an2==3:
                if self.lim2<self.lim-9:
                    self.lim2+=8
                elif self.lim2>self.lim+9:
                    self.lim2-=8
                else:
                    self.lim2=self.lim
                for i in range(self.px,self.lim2,8):
                    pyxel.blt(i-persox,self.y-mres,1,0,96,8,res,8)


            pyxel.blt(self.px-mres-persox,self.y-mres,1,16*(11+self.an2),80,W,res,8)

    def mort(self,perso):
        if perso.an==2:
            X=perso.x+perso.px
            if perso.sens:
                if X+4<self.px<X+22 and (perso.y%w)-mres<self.y<(perso.y%w)+mres:
                    return True
            else:
                if X-5>self.px>X-21 and (perso.y%w)-mres<self.y<(perso.y%w)+mres:
                    return True
        return False

class Monstre2:
    def __init__(self,x,y,lvl,id):
        self.px=x+mres
        self.y=y+mres
        self.x=0
        self.lvl=lvl
        self.tir=[]
        self.mor=[]
        self.start=pyxel.frame_count-100
        self.start2=self.start
        self.an=0
        self.play=False
        self.id=id
    def update(self,jeu):
        if pyxel.frame_count%5==0:
            self.an=(self.an+1)%4
        x,y=jeu.perso.x+jeu.perso.px,jeu.perso.y-w*jeu.lvl
        self.x=jeu.perso.px
        dist=((self.px-x)**2 + (self.y-y)**2)**0.5
        print(self.lvl,dist)
        vx=(x-self.px)/dist
        vy=(y-self.y)/dist
        if dist<w//2 and pyxel.frame_count-self.start>150 and len(self.tir)<2:
            self.start=pyxel.frame_count
            self.play=True
        if self.play and pyxel.frame_count-self.start>15:
            self.play=False
        if self.play and pyxel.frame_count-self.start>5 and pyxel.frame_count-self.start2>150 and len(self.tir)<2:
            self.tir.append([self.px,self.y+3,vx,vy,vx,vy])
            self.start2=pyxel.frame_count
        for t in self.tir:
            px,py=jeu.perso.x+jeu.perso.px,jeu.perso.y-w*jeu.lvl
            x,y,Vx,Vy,Ix,Iy=t
            dist=round(((px-x)**2 + (py-y)**2)**0.5,2)
            Vx=round((px-x)/dist,2)
            Vy=round((py-y)/dist,2)
            if Ix<Vx:
                Ix+=0.01
            elif Ix>Vx:
                Ix-=0.01
            if Iy<Vy:
                Iy+=0.01
            elif Iy>Vy:
                Iy-=0.01
            t[0]+=Ix
            t[1]+=Iy
            t[2]=Vx
            t[3]=Vy
            t[4]=Ix
            t[5]=Iy
            if pyxel.tilemap(0).pget((t[0]+t[4]*2)//8,(t[1]+w*jeu.lvl+t[5]*2)//8) in Mur or jeu.perso.x-mres+jeu.perso.px<t[0]<jeu.perso.x+mres+jeu.perso.px and py-mres<t[1]<py+mres:
                self.mor.append([t,0])
                self.tir.remove(t)
            if jeu.perso.x-mres+jeu.perso.px<t[0]<jeu.perso.x+mres+jeu.perso.px and py-mres<t[1]<py+mres:
                del jeu.perso
                jeu.perso=Perso(jeu.Rx,jeu.pRx,jeu.Ry)
        for m in self.mor:
            t,r=m
            if r>=2:
                self.mor.remove(m)
            else:
                m[1]+=1
    def draw(self,persox):
        if persox+self.x<self.px:
            W=-res
        else:
            W=res
        if self.play:
            pyxel.blt(self.px-mres-persox,self.y-mres,1,res*4,64,W,res,11)
        else:
            pyxel.blt(self.px-mres-persox,self.y-mres,1,res*self.an,64,W,res,11)
        for t in self.tir:
            x,y,Vx,Vy,Ix,Iy=t
            pyxel.blt(x-persox-mres,y-mres,1,res*5,64,res,res,11)
        for m in self.mor:
            t,r=m
            pyxel.blt(t[0]-persox-mres,t[1]-mres,1,res*5+res*r,64,res,res,11)

    def mort(self,perso):
        if perso.an==2:
            X=perso.x+perso.px
            if perso.sens:
                if X+4<self.px<X+22 and (perso.y%w)-mres<self.y<(perso.y%w)+mres:
                    return True
            else:
                if X-5>self.px>X-21 and (perso.y%w)-mres<self.y<(perso.y%w)+mres:
                    return True
        return False

class Monstre:
    def __init__(self,x,y,lvl,id):
        self.px=x+mres
        self.y=y+mres
        self.sens=True
        self.an=0
        self.lvl=lvl
        self.id=id
    def update(self,jeu):
        if pyxel.frame_count%5==0:
            if self.sens:
                test=pyxel.tilemap(0).pget((self.px-mres-2)//8,(self.y+(w*jeu.lvl)+mres+2)//8)
                test2=pyxel.tilemap(0).pget((self.px-mres-2)//8,(self.y+(w*jeu.lvl))//8)
            else:
                test=pyxel.tilemap(0).pget((self.px+mres+1)//8,(self.y+(w*jeu.lvl)+mres+1)//8)
                test2=pyxel.tilemap(0).pget((self.px+mres+1)//8,(self.y+(w*jeu.lvl))//8)
            if test2 in switchON:
                self.sens= not self.sens
                print("ok")
                for x in range(32*16):
                    for y in range((w*self.lvl)//8,(w*self.lvl)//8+32):
                        t=pyxel.tilemap(0).pget(x,y)
                        if t == MurO[0]:
                            jeu.mur(x*8,y*8,voidO)
                        if t == voidO[0]:
                            jeu.mur(x*8,y*8,MurO)
                        if t== switchON[0]:
                            jeu.mur(x*8,y*8,switchOFF)
            elif test2 in switchOFF:
                self.sens= not self.sens
                print("ok2")
                for x in range(32*16):
                    for y in range((w*self.lvl)//8,(w*self.lvl)//8+32):
                        t=pyxel.tilemap(0).pget(x,y)
                        if t == MurO[0]:
                            jeu.mur(x*8,y*8,voidO)
                        if t == voidO[0]:
                            jeu.mur(x*8,y*8,MurO)
                        if t== switchOFF[0]:
                            jeu.mur(x*8,y*8,switchON)
            elif test in mur and test2 not in mur:
                if self.sens==True:
                    #if dist>res and (vx>0 or vx==0) and (Y==self.y):
                        self.px+=-2
                else:
                    #if dist>res and (vx<0 or vx==0) and (Y==self.y):
                        self.px+=2

            else:
                self.sens=not self.sens

    def draw(self,persox):
        if self.sens:
            W=-res
        else:
            W=res
        if pyxel.frame_count%3==0:
            self.an+=1
        pyxel.blt(self.px-mres-persox,self.y-mres,1,16*(self.an%11),48,W,res,8)

    def mort(self,perso):
        if perso.an==2:
            X=perso.x+perso.px
            if perso.sens:
                if X+4<self.px<X+22 and (perso.y%w)-mres<self.y<(perso.y%w)+mres:
                    return True
            else:
                if X-5>self.px>X-21 and (perso.y%w)-mres<self.y<(perso.y%w)+mres:
                    return True
        return False


class Perso:
    def __init__(self,x,px,y):
        self.x=x
        self.px=px
        self.y=y
        self.vy=0
        self.g=0.8*(mres//4)
        self.sens=True
        self.o=0

        self.an=0
        self.A=[(0,16,4,16),(15,16,10,16),(4,16,11,16)]
        self.play=False

        self.jump_speed=-mres*1.8

        p1=[-mres//2.5,0]
        p2=[mres//2.5,0]

        self.hit=[p1,p2]

    def update(self,soll,lvl,input):
        i,u,r,l,d=input
        x,y=self.x,self.y
        px=self.px
        self.vy+=self.g
        if self.vy>res:
            self.vy=res-1
        if self.inn(r):
            if pyxel.tilemap(0).pget((self.x+self.px+mres+1)//8,y//8) not in mur and pyxel.tilemap(0).pget((self.x+self.px+mres+1)//8,(y-mres+1)//8) not in mur  and pyxel.tilemap(0).pget((self.x+self.px+mres+1)//8,(y+mres-1)//8) not in mur :
                if px<(w//2):
                    px+=mres//2
                elif self.x+w+mres//2<=mapx:
                    x+=mres//2
                elif px+2<=w-mres:
                    px+=mres//2
            self.sens=True
        if self.inn(l):
            if pyxel.tilemap(0).pget((self.x+self.px-mres-2)//8,y//8) not in mur  and pyxel.tilemap(0).pget((self.x+self.px-mres-2)//8,(y-mres+1)//8) not in mur  and pyxel.tilemap(0).pget((self.x+self.px-mres-2)//8,(y+mres-1)//8) not in mur :
                if px>(w//2):
                    px-=mres//2
                elif self.x-mres//2>=0:
                    x-=mres//2
                elif px-mres//2>=mres:
                    px-=mres//2
            self.sens=False
        while (pyxel.tilemap(0).pget((x+px)//8,(y+self.vy-mres+1)//8) in mur or (pyxel.tilemap(0).pget((x+px)//8,(y+self.vy-mres+1)//8)) in pick or pyxel.tilemap(0).pget((x+px+mres-2)//8,(y+self.vy-mres+1)//8) in mur or pyxel.tilemap(0).pget((x+px+mres-2)//8,(y+self.vy-mres+1)//8) in pick or pyxel.tilemap(0).pget((x+px-mres)//8,(y+self.vy-mres+1)//8) in mur or pyxel.tilemap(0).pget((x+px-mres)//8,(y+self.vy-mres+1)//8) in pick) and (self.vy<=0):
            print(self.vy)
            self.vy+=1

        y+=self.vy
        if y>=soll-mres:
            self.vy=0
            y=soll-mres
            if self.o==1:
                self.o=0
        if self.inn(u) and y+mres==soll:
            self.vy=self.jump_speed
            self.o=1

        prevx=self.x
        prevy=y
        if pyxel.tilemap(0).pget((x+px)//8,y//8) not in mur :
            self.x=x
            self.y=round(y,2)
            self.px=px

        if self.inn(i):
            self.play=True
        if self.play and pyxel.frame_count%3==0:
            self.an+=1
            if self.an==3:
                self.an=0
                self.play=False

    def draw(self):
        if self.sens:
            W=res
        else:
            W=-res
        H=res
        pyxel.blt(self.px-mres,(self.y%w)-mres,1,0,0,W,H,8)

        x,y,WW,h=self.A[self.an]
        if self.sens==False:
            WW=-WW
            pyxel.blt(self.px-4+WW,(self.y%w)-mres,1,x,y,WW,h,8)
        else:
            pyxel.blt(self.px+4,(self.y%w)-mres,1,x,y,WW,h,8)

    def inn(self,b):
        test=INPUT[b]
        if pyxel.btn(test):
            return True
        else:
            return False

class Jeu:
    def __init__(self):
        global res,mres,w,mapx,mapy,mur,Mur,MurO,voidO,pick,exit,switchON,switchOFF,void,checkON,checkOFF,Rx,Ry, KEYS, INPUT
        Mur=[(0,0),(1,0),(1,1),(0,1)]
        MurO=[(6,2),(7,2),(7,3),(6,3)]
        mur=Mur+MurO
        pick=[(2,0),(3,0),(3,1),(2,1)]
        void=[(0,2),(1,2),(1,3),(0,3)]
        voidO=[(4,2),(5,2),(5,3),(4,3)]
        exit=[(4,0),(5,0),(5,1),(4,1)]
        checkON=[(8,0),(9,0),(9,1),(8,1)]
        checkOFF=[(6,0),(7,0),(6,1),(7,1)]
        switchON=[(10,0),(11,0),(11,1),(10,1)]
        switchOFF=[(12,0),(13,0),(13,1),(12,1)]

        res=16
        mres=res//2
        w=res*16
        mapx,mapy=w*8,w
        Rx=0
        Ry=(w//4)*3
        KEYS = tuple(k for k in dir(pyxel) if sum(map(lambda s: s in k, ('KEY', 'MOUSE', 'GAMEPAD'))))
        INPUT={"GAMEPAD1_AXIS_LEFTX":pyxel.GAMEPAD1_AXIS_LEFTX,"GAMEPAD1_AXIS_LEFTY":pyxel.GAMEPAD1_AXIS_LEFTY,"GAMEPAD1_AXIS_RIGHTX":pyxel.GAMEPAD1_AXIS_RIGHTX,"GAMEPAD1_AXIS_RIGHTY":pyxel.GAMEPAD1_AXIS_RIGHTY,"GAMEPAD1_AXIS_TRIGGERLEFT":pyxel.GAMEPAD1_AXIS_TRIGGERLEFT,"GAMEPAD1_AXIS_TRIGGERRIGHT":pyxel.GAMEPAD1_AXIS_TRIGGERRIGHT,"GAMEPAD1_BUTTON_A":pyxel.GAMEPAD1_BUTTON_A,"GAMEPAD1_BUTTON_B":pyxel.GAMEPAD1_BUTTON_B,"GAMEPAD1_BUTTON_BACK":pyxel.GAMEPAD1_BUTTON_BACK,"GAMEPAD1_BUTTON_DPAD_DOWN":pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,"GAMEPAD1_BUTTON_DPAD_LEFT":pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,"GAMEPAD1_BUTTON_DPAD_RIGHT":pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,"GAMEPAD1_BUTTON_DPAD_UP":pyxel.GAMEPAD1_BUTTON_DPAD_UP,"GAMEPAD1_BUTTON_GUIDE":pyxel.GAMEPAD1_BUTTON_GUIDE,"GAMEPAD1_BUTTON_LEFTSHOULDER":pyxel.GAMEPAD1_BUTTON_LEFTSHOULDER,"GAMEPAD1_BUTTON_LEFTSTICK":pyxel.GAMEPAD1_BUTTON_LEFTSTICK,"GAMEPAD1_BUTTON_RIGHTSHOULDER":pyxel.GAMEPAD1_BUTTON_RIGHTSHOULDER,"GAMEPAD1_BUTTON_RIGHTSTICK":pyxel.GAMEPAD1_BUTTON_RIGHTSTICK,"GAMEPAD1_BUTTON_START":pyxel.GAMEPAD1_BUTTON_START,"GAMEPAD1_BUTTON_X":pyxel.GAMEPAD1_BUTTON_X,"GAMEPAD1_BUTTON_Y":pyxel.GAMEPAD1_BUTTON_Y,"GAMEPAD2_AXIS_LEFTX":pyxel.GAMEPAD2_AXIS_LEFTX,"GAMEPAD2_AXIS_LEFTY":pyxel.GAMEPAD2_AXIS_LEFTY,"GAMEPAD2_AXIS_RIGHTX":pyxel.GAMEPAD2_AXIS_RIGHTX,"GAMEPAD2_AXIS_RIGHTY":pyxel.GAMEPAD2_AXIS_RIGHTY,"GAMEPAD2_AXIS_TRIGGERLEFT":pyxel.GAMEPAD2_AXIS_TRIGGERLEFT,"GAMEPAD2_AXIS_TRIGGERRIGHT":pyxel.GAMEPAD2_AXIS_TRIGGERRIGHT,"GAMEPAD2_BUTTON_A":pyxel.GAMEPAD2_BUTTON_A,"GAMEPAD2_BUTTON_B":pyxel.GAMEPAD2_BUTTON_B,"GAMEPAD2_BUTTON_BACK":pyxel.GAMEPAD2_BUTTON_BACK,"GAMEPAD2_BUTTON_DPAD_DOWN":pyxel.GAMEPAD2_BUTTON_DPAD_DOWN,"GAMEPAD2_BUTTON_DPAD_LEFT":pyxel.GAMEPAD2_BUTTON_DPAD_LEFT,"GAMEPAD2_BUTTON_DPAD_RIGHT":pyxel.GAMEPAD2_BUTTON_DPAD_RIGHT,"GAMEPAD2_BUTTON_DPAD_UP":pyxel.GAMEPAD2_BUTTON_DPAD_UP,"GAMEPAD2_BUTTON_GUIDE":pyxel.GAMEPAD2_BUTTON_GUIDE,"GAMEPAD2_BUTTON_LEFTSHOULDER":pyxel.GAMEPAD2_BUTTON_LEFTSHOULDER,"GAMEPAD2_BUTTON_LEFTSTICK":pyxel.GAMEPAD2_BUTTON_LEFTSTICK,"GAMEPAD2_BUTTON_RIGHTSHOULDER":pyxel.GAMEPAD2_BUTTON_RIGHTSHOULDER,"GAMEPAD2_BUTTON_RIGHTSTICK":pyxel.GAMEPAD2_BUTTON_RIGHTSTICK,"GAMEPAD2_BUTTON_START":pyxel.GAMEPAD2_BUTTON_START,"GAMEPAD2_BUTTON_X":pyxel.GAMEPAD2_BUTTON_X,"GAMEPAD2_BUTTON_Y":pyxel.GAMEPAD2_BUTTON_Y,"KEY_0":pyxel.KEY_0,"KEY_1":pyxel.KEY_1,"KEY_2":pyxel.KEY_2,"KEY_3":pyxel.KEY_3,"KEY_4":pyxel.KEY_4,"KEY_5":pyxel.KEY_5,"KEY_6":pyxel.KEY_6,"KEY_7":pyxel.KEY_7,"KEY_8":pyxel.KEY_8,"KEY_9":pyxel.KEY_9,"KEY_A":pyxel.KEY_A,"KEY_AC_BACK":pyxel.KEY_AC_BACK,"KEY_AC_BOOKMARKS":pyxel.KEY_AC_BOOKMARKS,"KEY_AC_FORWARD":pyxel.KEY_AC_FORWARD,"KEY_AC_HOME":pyxel.KEY_AC_HOME,"KEY_AC_REFRESH":pyxel.KEY_AC_REFRESH,"KEY_AC_SEARCH":pyxel.KEY_AC_SEARCH,"KEY_AC_STOP":pyxel.KEY_AC_STOP,"KEY_AGAIN":pyxel.KEY_AGAIN,"KEY_ALT":pyxel.KEY_ALT,"KEY_ALTERASE":pyxel.KEY_ALTERASE,"KEY_AMPERSAND":pyxel.KEY_AMPERSAND,"KEY_APPLICATION":pyxel.KEY_APPLICATION,"KEY_ASTERISK":pyxel.KEY_ASTERISK,"KEY_AT":pyxel.KEY_AT,"KEY_AUDIOMUTE":pyxel.KEY_AUDIOMUTE,"KEY_AUDIONEXT":pyxel.KEY_AUDIONEXT,"KEY_AUDIOPLAY":pyxel.KEY_AUDIOPLAY,"KEY_AUDIOPREV":pyxel.KEY_AUDIOPREV,"KEY_AUDIOSTOP":pyxel.KEY_AUDIOSTOP,"KEY_B":pyxel.KEY_B,"KEY_BACKQUOTE":pyxel.KEY_BACKQUOTE,"KEY_BACKSLASH":pyxel.KEY_BACKSLASH,"KEY_BACKSPACE":pyxel.KEY_BACKSPACE,"KEY_BRIGHTNESSDOWN":pyxel.KEY_BRIGHTNESSDOWN,"KEY_BRIGHTNESSUP":pyxel.KEY_BRIGHTNESSUP,"KEY_C":pyxel.KEY_C,"KEY_CALCULATOR":pyxel.KEY_CALCULATOR,"KEY_CANCEL":pyxel.KEY_CANCEL,"KEY_CAPSLOCK":pyxel.KEY_CAPSLOCK,"KEY_CARET":pyxel.KEY_CARET,"KEY_CLEAR":pyxel.KEY_CLEAR,"KEY_CLEARAGAIN":pyxel.KEY_CLEARAGAIN,"KEY_COLON":pyxel.KEY_COLON,"KEY_COMMA":pyxel.KEY_COMMA,"KEY_COMPUTER":pyxel.KEY_COMPUTER,"KEY_COPY":pyxel.KEY_COPY,"KEY_CRSEL":pyxel.KEY_CRSEL,"KEY_CTRL":pyxel.KEY_CTRL,"KEY_CURRENCYSUBUNIT":pyxel.KEY_CURRENCYSUBUNIT,"KEY_CURRENCYUNIT":pyxel.KEY_CURRENCYUNIT,"KEY_CUT":pyxel.KEY_CUT,"KEY_D":pyxel.KEY_D,"KEY_DECIMALSEPARATOR":pyxel.KEY_DECIMALSEPARATOR,"KEY_DELETE":pyxel.KEY_DELETE,"KEY_DISPLAYSWITCH":pyxel.KEY_DISPLAYSWITCH,"KEY_DOLLAR":pyxel.KEY_DOLLAR,"KEY_DOWN":pyxel.KEY_DOWN,"KEY_E":pyxel.KEY_E,"KEY_EJECT":pyxel.KEY_EJECT,"KEY_END":pyxel.KEY_END,"KEY_EQUALS":pyxel.KEY_EQUALS,"KEY_ESCAPE":pyxel.KEY_ESCAPE,"KEY_EXCLAIM":pyxel.KEY_EXCLAIM,"KEY_EXECUTE":pyxel.KEY_EXECUTE,"KEY_EXSEL":pyxel.KEY_EXSEL,"KEY_F":pyxel.KEY_F,"KEY_F1":pyxel.KEY_F1,"KEY_F10":pyxel.KEY_F10,"KEY_F11":pyxel.KEY_F11,"KEY_F12":pyxel.KEY_F12,"KEY_F13":pyxel.KEY_F13,"KEY_F14":pyxel.KEY_F14,"KEY_F15":pyxel.KEY_F15,"KEY_F16":pyxel.KEY_F16,"KEY_F17":pyxel.KEY_F17,"KEY_F18":pyxel.KEY_F18,"KEY_F19":pyxel.KEY_F19,"KEY_F2":pyxel.KEY_F2,"KEY_F20":pyxel.KEY_F20,"KEY_F21":pyxel.KEY_F21,"KEY_F22":pyxel.KEY_F22,"KEY_F23":pyxel.KEY_F23,"KEY_F24":pyxel.KEY_F24,"KEY_F3":pyxel.KEY_F3,"KEY_F4":pyxel.KEY_F4,"KEY_F5":pyxel.KEY_F5,"KEY_F6":pyxel.KEY_F6,"KEY_F7":pyxel.KEY_F7,"KEY_F8":pyxel.KEY_F8,"KEY_F9":pyxel.KEY_F9,"KEY_FIND":pyxel.KEY_FIND,"KEY_G":pyxel.KEY_G,"KEY_GREATER":pyxel.KEY_GREATER,"KEY_GUI":pyxel.KEY_GUI,"KEY_H":pyxel.KEY_H,"KEY_HASH":pyxel.KEY_HASH,"KEY_HELP":pyxel.KEY_HELP,"KEY_HOME":pyxel.KEY_HOME,"KEY_I":pyxel.KEY_I,"KEY_INSERT":pyxel.KEY_INSERT,"KEY_J":pyxel.KEY_J,"KEY_K":pyxel.KEY_K,"KEY_KBDILLUMDOWN":pyxel.KEY_KBDILLUMDOWN,"KEY_KBDILLUMTOGGLE":pyxel.KEY_KBDILLUMTOGGLE,"KEY_KBDILLUMUP":pyxel.KEY_KBDILLUMUP,"KEY_KP_0":pyxel.KEY_KP_0,"KEY_KP_00":pyxel.KEY_KP_00,"KEY_KP_000":pyxel.KEY_KP_000,"KEY_KP_1":pyxel.KEY_KP_1,"KEY_KP_2":pyxel.KEY_KP_2,"KEY_KP_3":pyxel.KEY_KP_3,"KEY_KP_4":pyxel.KEY_KP_4,"KEY_KP_5":pyxel.KEY_KP_5,"KEY_KP_6":pyxel.KEY_KP_6,"KEY_KP_7":pyxel.KEY_KP_7,"KEY_KP_8":pyxel.KEY_KP_8,"KEY_KP_9":pyxel.KEY_KP_9,"KEY_KP_A":pyxel.KEY_KP_A,"KEY_KP_AMPERSAND":pyxel.KEY_KP_AMPERSAND,"KEY_KP_AT":pyxel.KEY_KP_AT,"KEY_KP_B":pyxel.KEY_KP_B,"KEY_KP_BACKSPACE":pyxel.KEY_KP_BACKSPACE,"KEY_KP_BINARY":pyxel.KEY_KP_BINARY,"KEY_KP_C":pyxel.KEY_KP_C,"KEY_KP_CLEAR":pyxel.KEY_KP_CLEAR,"KEY_KP_CLEARENTRY":pyxel.KEY_KP_CLEARENTRY,"KEY_KP_COLON":pyxel.KEY_KP_COLON,"KEY_KP_COMMA":pyxel.KEY_KP_COMMA,"KEY_KP_D":pyxel.KEY_KP_D,"KEY_KP_DBLAMPERSAND":pyxel.KEY_KP_DBLAMPERSAND,"KEY_KP_DBLVERTICALBAR":pyxel.KEY_KP_DBLVERTICALBAR,"KEY_KP_DECIMAL":pyxel.KEY_KP_DECIMAL,"KEY_KP_DIVIDE":pyxel.KEY_KP_DIVIDE,"KEY_KP_E":pyxel.KEY_KP_E,"KEY_KP_ENTER":pyxel.KEY_KP_ENTER,"KEY_KP_EQUALS":pyxel.KEY_KP_EQUALS,"KEY_KP_EQUALSAS400":pyxel.KEY_KP_EQUALSAS400,"KEY_KP_EXCLAM":pyxel.KEY_KP_EXCLAM,"KEY_KP_F":pyxel.KEY_KP_F,"KEY_KP_GREATER":pyxel.KEY_KP_GREATER,"KEY_KP_HASH":pyxel.KEY_KP_HASH,"KEY_KP_HEXADECIMAL":pyxel.KEY_KP_HEXADECIMAL,"KEY_KP_LEFTBRACE":pyxel.KEY_KP_LEFTBRACE,"KEY_KP_LEFTPAREN":pyxel.KEY_KP_LEFTPAREN,"KEY_KP_LESS":pyxel.KEY_KP_LESS,"KEY_KP_MEMADD":pyxel.KEY_KP_MEMADD,"KEY_KP_MEMCLEAR":pyxel.KEY_KP_MEMCLEAR,"KEY_KP_MEMDIVIDE":pyxel.KEY_KP_MEMDIVIDE,"KEY_KP_MEMMULTIPLY":pyxel.KEY_KP_MEMMULTIPLY,"KEY_KP_MEMRECALL":pyxel.KEY_KP_MEMRECALL,"KEY_KP_MEMSTORE":pyxel.KEY_KP_MEMSTORE,"KEY_KP_MEMSUBTRACT":pyxel.KEY_KP_MEMSUBTRACT,"KEY_KP_MINUS":pyxel.KEY_KP_MINUS,"KEY_KP_MULTIPLY":pyxel.KEY_KP_MULTIPLY,"KEY_KP_OCTAL":pyxel.KEY_KP_OCTAL,"KEY_KP_PERCENT":pyxel.KEY_KP_PERCENT,"KEY_KP_PERIOD":pyxel.KEY_KP_PERIOD,"KEY_KP_PLUS":pyxel.KEY_KP_PLUS,"KEY_KP_PLUSMINUS":pyxel.KEY_KP_PLUSMINUS,"KEY_KP_POWER":pyxel.KEY_KP_POWER,"KEY_KP_RIGHTBRACE":pyxel.KEY_KP_RIGHTBRACE,"KEY_KP_RIGHTPAREN":pyxel.KEY_KP_RIGHTPAREN,"KEY_KP_SPACE":pyxel.KEY_KP_SPACE,"KEY_KP_TAB":pyxel.KEY_KP_TAB,"KEY_KP_VERTICALBAR":pyxel.KEY_KP_VERTICALBAR,"KEY_KP_XOR":pyxel.KEY_KP_XOR,"KEY_L":pyxel.KEY_L,"KEY_LALT":pyxel.KEY_LALT,"KEY_LCTRL":pyxel.KEY_LCTRL,"KEY_LEFT":pyxel.KEY_LEFT,"KEY_LEFTBRACKET":pyxel.KEY_LEFTBRACKET,"KEY_LEFTPAREN":pyxel.KEY_LEFTPAREN,"KEY_LESS":pyxel.KEY_LESS,"KEY_LGUI":pyxel.KEY_LGUI,"KEY_LSHIFT":pyxel.KEY_LSHIFT,"KEY_M":pyxel.KEY_M,"KEY_MAIL":pyxel.KEY_MAIL,"KEY_MEDIASELECT":pyxel.KEY_MEDIASELECT,"KEY_MENU":pyxel.KEY_MENU,"KEY_MINUS":pyxel.KEY_MINUS,"KEY_MODE":pyxel.KEY_MODE,"KEY_MUTE":pyxel.KEY_MUTE,"KEY_N":pyxel.KEY_N,"KEY_NONE":pyxel.KEY_NONE,"KEY_NUMLOCKCLEAR":pyxel.KEY_NUMLOCKCLEAR,"KEY_O":pyxel.KEY_O,"KEY_OPER":pyxel.KEY_OPER,"KEY_OUT":pyxel.KEY_OUT,"KEY_P":pyxel.KEY_P,"KEY_PAGEDOWN":pyxel.KEY_PAGEDOWN,"KEY_PAGEUP":pyxel.KEY_PAGEUP,"KEY_PASTE":pyxel.KEY_PASTE,"KEY_PAUSE":pyxel.KEY_PAUSE,"KEY_PERCENT":pyxel.KEY_PERCENT,"KEY_PERIOD":pyxel.KEY_PERIOD,"KEY_PLUS":pyxel.KEY_PLUS,"KEY_POWER":pyxel.KEY_POWER,"KEY_PRINTSCREEN":pyxel.KEY_PRINTSCREEN,"KEY_PRIOR":pyxel.KEY_PRIOR,"KEY_Q":pyxel.KEY_Q,"KEY_QUESTION":pyxel.KEY_QUESTION,"KEY_QUOTE":pyxel.KEY_QUOTE,"KEY_QUOTEDBL":pyxel.KEY_QUOTEDBL,"KEY_R":pyxel.KEY_R,"KEY_RALT":pyxel.KEY_RALT,"KEY_RCTRL":pyxel.KEY_RCTRL,"KEY_RETURN":pyxel.KEY_RETURN,"KEY_RETURN2":pyxel.KEY_RETURN2,"KEY_RGUI":pyxel.KEY_RGUI,"KEY_RIGHT":pyxel.KEY_RIGHT,"KEY_RIGHTBRACKET":pyxel.KEY_RIGHTBRACKET,"KEY_RIGHTPAREN":pyxel.KEY_RIGHTPAREN,"KEY_RSHIFT":pyxel.KEY_RSHIFT,"KEY_S":pyxel.KEY_S,"KEY_SCROLLLOCK":pyxel.KEY_SCROLLLOCK,"KEY_SELECT":pyxel.KEY_SELECT,"KEY_SEMICOLON":pyxel.KEY_SEMICOLON,"KEY_SEPARATOR":pyxel.KEY_SEPARATOR,"KEY_SHIFT":pyxel.KEY_SHIFT,"KEY_SLASH":pyxel.KEY_SLASH,"KEY_SLEEP":pyxel.KEY_SLEEP,"KEY_SPACE":pyxel.KEY_SPACE,"KEY_STOP":pyxel.KEY_STOP,"KEY_SYSREQ":pyxel.KEY_SYSREQ,"KEY_T":pyxel.KEY_T,"KEY_TAB":pyxel.KEY_TAB,"KEY_THOUSANDSSEPARATOR":pyxel.KEY_THOUSANDSSEPARATOR,"KEY_U":pyxel.KEY_U,"KEY_UNDERSCORE":pyxel.KEY_UNDERSCORE,"KEY_UNDO":pyxel.KEY_UNDO,"KEY_UP":pyxel.KEY_UP,"KEY_V":pyxel.KEY_V,"KEY_VOLUMEDOWN":pyxel.KEY_VOLUMEDOWN,"KEY_VOLUMEUP":pyxel.KEY_VOLUMEUP,"KEY_W":pyxel.KEY_W,"KEY_WWW":pyxel.KEY_WWW,"KEY_X":pyxel.KEY_X,"KEY_Y":pyxel.KEY_Y,"KEY_Z":pyxel.KEY_Z,"MOUSE_BUTTON_LEFT":pyxel.MOUSE_BUTTON_LEFT,"MOUSE_BUTTON_MIDDLE":pyxel.MOUSE_BUTTON_MIDDLE,"MOUSE_BUTTON_RIGHT":pyxel.MOUSE_BUTTON_RIGHT,"MOUSE_BUTTON_UNKNOWN":pyxel.MOUSE_BUTTON_UNKNOWN,"MOUSE_BUTTON_X1":pyxel.MOUSE_BUTTON_X1,"MOUSE_BUTTON_X2":pyxel.MOUSE_BUTTON_X2,"MOUSE_POS_X":pyxel.MOUSE_POS_X,"MOUSE_POS_Y":pyxel.MOUSE_POS_Y,"MOUSE_WHEEL_X":pyxel.MOUSE_WHEEL_X,"MOUSE_WHEEL_Y":pyxel.MOUSE_WHEEL_Y}
        pyxel.init(w,w,display_scale=3)
        pyxel.load("sc.pyxres")
        pyxel.mouse(True)
        self.perso=Perso(Rx,w//4,Ry)
        self.monstre=[]
        self.dispo=[]
        self.start=0
        self.sol=w
        self.lvl=0
        self.phase=0
        self.b=0
        self.an=0
        self.option=[">START<","OPTION"]
        self.o=0
        self.choice=0
        self.mapy=mapy
        self.Ry=Ry
        self.Rx=Rx
        self.pRx=(w//2)
        self.time=0
        self.mode=0
        self.cl=7
        self.cy=w//4
        self.by=0
        self.input=["KEY_E","KEY_UP","KEY_RIGHT","KEY_LEFT","KEY_DOWN"]
        self.tx=["attack","jump","right","left","interaction"]
        pyxel.run(self.update,self.draw)

    def update(self):
        for m in self.monstre:
            if m.lvl!=self.lvl:
                self.monstre.remove(m)
                del m

        if self.phase==0:
            if pyxel.btn(pyxel.KEY_RETURN) and self.choice==0:
                self.an+=1
                self.start=pyxel.frame_count
            if pyxel.btn(pyxel.KEY_RETURN) and self.choice==1  and pyxel.frame_count-self.start>5:
                self.phase=2
                self.start=pyxel.frame_count
            if self.an!=0 and pyxel.frame_count-self.start>0.8:
                if self.an==10:
                    self.an=0
                    self.start=0
                    self.phase+=1
                else:
                    self.start=pyxel.frame_count
                    self.an+=1
            if pyxel.btn(pyxel.KEY_UP) and pyxel.frame_count-self.start>5:
                self.start=pyxel.frame_count
                self.o=(self.o+1)%2
            if pyxel.btn(pyxel.KEY_DOWN) and pyxel.frame_count-self.start>5:
                self.start=pyxel.frame_count
                self.o=(self.o+1)%2
            if self.o==0:
                self.option=[">START<","OPTION"]
                self.choice=0
            if self.o==1:
                self.option=["START",">OPTION<"]
                self.choice=1
        elif self.phase==1:
            # edit
            if self.lvl==3:
                self.phase=3
                self.start=pyxel.frame_count
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.frame_count-self.start>3:
                self.start=pyxel.frame_count
                self.mur(pyxel.mouse_x+self.perso.x,pyxel.mouse_y+w*self.lvl,mur)
            if pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT) and pyxel.frame_count-self.start>3:
                self.start=pyxel.frame_count
                self.mur(pyxel.mouse_x+self.perso.x,pyxel.mouse_y+w*self.lvl,pick)
            if pyxel.btn(pyxel.MOUSE_BUTTON_MIDDLE) and pyxel.frame_count-self.start>3:
                self.start=pyxel.frame_count
                self.mur(pyxel.mouse_x+self.perso.x,pyxel.mouse_y+w*self.lvl,void)

            self.sol=w*(self.lvl+1)
            for i in range(int(self.perso.y),self.mapy):
                a=pyxel.tilemap(0).pget((self.perso.px+self.perso.x)//8,i//8)
                b=pyxel.tilemap(0).pget((self.perso.px+self.perso.x-mres+1)//8,i//8)
                c=pyxel.tilemap(0).pget((self.perso.px+self.perso.x+mres-2)//8,i//8)
                if a in mur or b in mur or c in mur:
                    self.sol=i
                    if i>=self.perso.y+mres-1:
                        break
                    else:
                        self.perso.y-=1

            self.perso.update(self.sol,self.lvl,self.input)
            for monstre in self.monstre:
                if 1==1:
                    monstre.update(self)
                if monstre.y-mres<self.perso.y%w<monstre.y+mres and (monstre.px-mres<self.perso.x+self.perso.px<monstre.px+mres or monstre.px-mres<self.perso.x+self.perso.px-mres+3<monstre.px+mres or monstre.px-mres<self.perso.x+self.perso.px+mres-4<monstre.px+mres):
                    del self.perso
                    self.perso=Perso(self.Rx,self.pRx,self.Ry)


                if monstre.mort(self.perso):
                    self.monstre.remove(monstre)
                    del monstre

            lave=pyxel.tilemap(0).pget((self.perso.x+self.perso.px)//8,self.perso.y//8)
            d=self.input[-1]
            if self.perso.inn(d) and pyxel.frame_count-self.start>3 and lave in exit:
                self.start=pyxel.frame_count
                self.an+=1
            if self.perso.inn(d) and pyxel.frame_count-self.start>5 and lave in switchON:
                self.start=pyxel.frame_count
                #self.mur(self.perso.x+self.perso.px,self.perso.y,switchOFF)
                for x in range(32*16):
                    for y in range((w*self.lvl)//8,(w*self.lvl)//8+32):
                        t=pyxel.tilemap(0).pget(x,y)
                        if t == MurO[0]:
                            self.mur(x*8,y*8,voidO)
                        if t == voidO[0]:
                            self.mur(x*8,y*8,MurO)
                        if t== switchON[0]:
                            self.mur(x*8,y*8,switchOFF)
            if self.perso.inn(d) and pyxel.frame_count-self.start>5 and lave in switchOFF:
                self.start=pyxel.frame_count
                #self.mur((self.perso.x+self.perso.px),self.perso.y,switchON)
                for x in range(32*16):
                    for y in range((w*self.lvl)//8,(w*self.lvl)//8+32):
                        t=pyxel.tilemap(0).pget(x,y)
                        if t == MurO[0]:
                            self.mur(x*8,y*8,voidO)
                        if t == voidO[0]:
                            self.mur(x*8,y*8,MurO)
                        if t== switchOFF[0]:
                            self.mur(x*8,y*8,switchON)
            if self.an!=0 and pyxel.frame_count-self.start>0.8:
                if self.an==10:
                    a=False
                    for x in range(32*16):
                        for y in range((w*self.lvl)//8,(w*self.lvl)//8+32):
                            t=pyxel.tilemap(0).pget(x,y)
                            if t== switchON[0]:
                                a=True
                                self.mur(x*8,y*8,switchOFF)
                    if a:
                        for x in range(32*16):
                            for y in range((w*self.lvl)//8,(w*self.lvl)//8+32):
                                t=pyxel.tilemap(0).pget(x,y)
                                if t == MurO[0]:
                                    self.mur(x*8,y*8,voidO)
                                if t == voidO[0]:
                                    self.mur(x*8,y*8,MurO)
                    self.an=0
                    self.start=0
                    self.lvl+=1
                    del self.perso
                    self.Ry+=w
                    self.mapy+=w
                    self.Rx=0
                    self.pRx=(w//3)
                    self.perso=Perso(self.Rx,self.pRx,self.Ry)
                else:
                    self.start=pyxel.frame_count
                    self.an+=1

            if lave in checkOFF:
                print("ok")
                self.Rx=self.perso.x
                self.pRx=self.perso.px
                self.Ry=self.perso.y
                self.mur(self.perso.x+self.perso.px,self.perso.y,checkON)
            """
            if lave in pick:
                del self.perso
                self.perso=Perso(self.Rx,self.pRx,self.Ry)
            """
            mort=False
            for p in self.perso.hit:
                x,y=self.perso.x+self.perso.px+p[0],self.perso.y+p[1]
                l=pyxel.tilemap(0).pget(x//8,y//8)
                if l in pick:
                    mort=True
            if mort:
                del self.perso
                self.perso=Perso(self.Rx,self.pRx,self.Ry)

            for x in range(0,32):
                for y in range(0,32):
                    t=pyxel.tilemap(0).pget(((self.perso.x//8)+x),y+(w*self.lvl)//8)
                    if t==(0,7):
                        test=Monstre(self.perso.x+x*8,y*8,self.lvl,1)
                        if ((self.perso.x//8)+x,y+(w*self.lvl)//8) not in self.dispo:
                            self.monstre.append(test)
                            self.dispo.append(((self.perso.x//8)+x,y+(w*self.lvl)//8))
                            self.mur(self.perso.x+x*8,(w*self.lvl)+y*8,void)
                    if t==(2,7):
                        test=Monstre2(self.perso.x+x*8,y*8,self.lvl,2)
                        if ((self.perso.x//8)+x,y+(w*self.lvl)//8) not in self.dispo:
                            self.monstre.append(test)
                            self.dispo.append(((self.perso.x//8)+x,y+(w*self.lvl)//8))
                            self.mur(self.perso.x+x*8,(w*self.lvl)+y*8,void)
                    if t==(4,7):
                        test=Monstre3(self.perso.x+x*8,y*8,self.lvl,3)
                        if ((self.perso.x//8)+x,y+(w*self.lvl)//8) not in self.dispo:
                            self.monstre.append(test)
                            self.dispo.append(((self.perso.x//8)+x,y+(w*self.lvl)//8))
                            self.mur(self.perso.x+x*8,(w*self.lvl)+y*8,void)
            for m in self.monstre:
                if m.lvl!=self.lvl:
                    self.monstre.remove(m)
                    del m


        elif self.phase==2:
            if pyxel.btn(pyxel.KEY_RETURN) and pyxel.frame_count-self.start>5 and self.mode==5:
                self.phase=0
                self.start=pyxel.frame_count
            if pyxel.btn(pyxel.KEY_RETURN) and pyxel.frame_count-self.start>5 and self.mode!=5:
                self.start=pyxel.frame_count
                self.cl=11
            if self.cl==11:
                test=""
                for k in KEYS:
                    if pyxel.btn(eval(f'pyxel.{k}')):
                        test=k
                if test!="" and test!="KEY_RETURN":
                    self.cl=7
                    self.input[self.mode]=test
            if pyxel.btn(pyxel.KEY_UP) and pyxel.frame_count-self.start>5:
                self.start=pyxel.frame_count
                self.mode-=1
                self.mode=self.mode%5
            if pyxel.btn(pyxel.KEY_DOWN) and pyxel.frame_count-self.start>5:
                self.start=pyxel.frame_count
                self.mode+=1
                self.mode=self.mode%6
        elif self.phase==3:
            if pyxel.frame_count-self.start>120:
                if pyxel.frame_count%2==0 and self.by<900:
                    self.cy-=1
                    self.by+=1

    def draw(self):
        pyxel.cls(0)
        self.b+=1
        if self.phase==0:
            pyxel.bltm(0,0,1,(pyxel.frame_count%(32*8)),0,w,w)
            x=(w//2)
            y=w//4
            s,o=self.option
            self.txt(x-self.len_txt("THE SLIME CASTLE")/2,y,"THE SLIME CASTLE")
            pyxel.blt(x-self.len_txt("THE SLIME CASTLE")/2,y+res+2,2,193,16,2,5,8)
            for i in range(1,self.len_txt("THE SLIME CASTLE")):
                pyxel.blt((x-self.len_txt("THE SLIME CASTLE")/2)+i,y+res+2,2,195,16,1,5,8)
            pyxel.blt(x+self.len_txt("THE SLIME CASTLE")/2,y+res+2,2,193,16,-2,5,8)
            self.txt(x-self.len_txt(s)/2,y*2,s)
            self.txt(x-self.len_txt(o)/2,y*3,o)
            if self.an!=0:
                for i in range(0,w,10):
                    pyxel.rect(0,i,w,self.an,0)
        elif self.phase==1:
            pyxel.cls(0)
            pyxel.bltm(0,0,1,(self.perso.x/4)%(32*8),0,w,w)
            #pyxel.bltm(0,0,2,(self.perso.x/2)%(32*8),w*self.lvl,w,w,0)
            pyxel.bltm(0,0,0,self.perso.x,w*self.lvl,w,w,11)
            if self.lvl==0:
                self.txt((w//4)*3-self.perso.x,w//2,"Jump")
                self.txt((w*2.6)-self.perso.x,w//2,"ATTACK")
                self.txt(w*6-self.perso.x+3,(w//2)-res,"CHECKPOINT")
                self.txt(w*7-self.perso.x,mres,"TELEPORT")
                self.txt(w*1.5-self.perso.x-res,w//2,"TOGGLE")

            for monstre in self.monstre:
                monstre.draw(self.perso.x)
            self.perso.draw()

            if self.an!=0:
                for i in range(0,w,10):
                    pyxel.rect(0,i,w,self.an,0)
            self.time=pyxel.frame_count//30
            a=self.time
            pyxel.text(1,1,"{}:{}".format("0"*(2-len(str(a//60)))+str(a//60),"0"*(2-len(str(a%60)))+str(a%60)),7)
        elif self.phase==2:
            a=res*2
            for i in self.tx:
                self.txt((w//3)+res*2,a,i)
                a+=res*2.5
            a=mres+res*2
            for i in self.input:
                pyxel.text(w//5,a,i,7)
                a+=res*2.5
            pyxel.text(w//5,a,"back",7)
            pyxel.rectb(res*2,2.2*res+(res*2.5*self.mode),w//4,res,self.cl)

        elif self.phase==3:

            pyxel.bltm(0,0,2,0,self.by%w,w,w)
            self.txt((w//2)-self.len_txt("CONGRATULATIONS")//2,self.cy,"CONGRATULATIONS")
            pyxel.blt(w//2-mres-4,self.cy+res*2,1,32,0,res*2,res*2,8)
            pyxel.text(w//2-((len("Lead Developer")*4-1)//2),self.cy+w,"Lead Developer",7)
            self.txt((w//2)-self.len_txt("DARKRENTIN")//2,self.cy+w+res,"DARKRENTIN")
            pyxel.text(w//2-((len("Game Designer")*4-1)//2),self.cy+w+w//4,"Game Designer",7)
            self.txt((w//2)-self.len_txt("TENEBRIX")//2,self.cy+w+w//4+res,"TENEBRIX")
            pyxel.text(w//2-((len("Lead Artist")*4-1)//2),self.cy+w+(w//4)*2,"Lead Artist",7)
            self.txt((w//2)-self.len_txt("DARKRENTIN")//2,self.cy+w+(w//4)*2+res,"DARKRENTIN")
            pyxel.text(w//2-((len("Sound Designer")*4-1)//2),self.cy+w+(w//4)*3,"Sound Designer",7)
            self.txt((w//2)-self.len_txt("NONE")//2,self.cy+w+(w//4)*3+res,"NONE")
            pyxel.text(w//2-((len("Producer")*4-1)//2),self.cy+w+(w//4)*4,"Producer",7)
            self.txt((w//2)-self.len_txt("DARKRENTIN")//2,self.cy+w+(w//4)*4+res,"DARKRENTIN")
            pyxel.text(w//2-((len("Gameplay Consultant")*4-1)//2),self.cy+w+(w//4)*5,"Gameplay Consultant",7)
            self.txt((w//2)-self.len_txt("TENEBRIX")//2,self.cy+w+(w//4)*5+res,"TENEBRIX")
            pyxel.text(w//2-((len("Special Effects Specialist")*4-1)//2),self.cy+w+(w//4)*6,"Special Effects Specialist",7)
            self.txt((w//2)-self.len_txt("DARKRENTIN")//2,self.cy+w+(w//4)*6+res,"DARKRENTIN")
            pyxel.text(w//2-((len("Community Manager")*4-1)//2),self.cy+w+(w//4)*7,"Community Manager",7)
            self.txt((w//2)-self.len_txt("TENEBRIX")//2,self.cy+w+(w//4)*7+res,"TENEBRIX")
            pyxel.text(w//2-((len("Some textures")*4-1)//2),self.cy+w+(w//4)*8,"some textures",7)
            self.txt((w//2)-self.len_txt("RANDOM GUYS")//2,self.cy+w+(w//4)*8+res,"RANDOM GUYS")
            self.txt((w//2)-self.len_txt("ON INTERNET")//2,self.cy+w+(w//4)*8+res*2.5,"ON INTERNET")

            self.txt((w//2)-self.len_txt("THANK YOU")//2,self.cy+w+(w//4)*10+res,"THANK YOU")
            self.txt((w//2)-self.len_txt("FOR PLAYING")//2,self.cy+w+(w//4)*10+res*2.5,"FOR PLAYING")


    def mur(self,x,y,tile):
        x=x//16
        y=y//16
        pos=[(0,0),(1,0),(1,1),(0,1)]
        for i in range(len(pos)):
            p=pos[i]
            t=tile[i]
            vx,vy=p
            pyxel.tilemap(0).pset(x*2+vx,y*2+vy,t)

    def txt(self,x,y,msg):
        A1="ABCDEFGHIJKLMNOP"
        B1=[13,12,13,13,13,13,13,13,7,13,13,11,13,13,13,13]
        A2="QRSTUVWXYZ><"
        B2=[13,13,13,13,13,13,16,13,13,13,12,12]
        a=0
        for lettre in msg:
            if lettre.upper() in A1:
                pyxel.blt(x+a,y,2,A1.index(lettre.upper())*16,0,16,16,8)
                a+=B1[A1.index(lettre.upper())]
            elif lettre.upper() in A2:
                pyxel.blt(x+a,y,2,A2.index(lettre.upper())*16,16,res,res,8)
                a+=B2[A2.index(lettre.upper())]
            else:
                a+=13
    def len_txt(self,msg):
        A1="ABCDEFGHIJKLMNOP"
        B1=[13,12,13,13,13,13,13,13,7,13,13,11,13,13,13,13]
        A2="QRSTUVWXYZ><_"
        B2=[13,13,13,13,13,13,16,13,13,13,12,12]
        a=0
        for i in msg:
            if i in A1:
                a+=B1[A1.index(i)]
            elif i in A2:
                a+=B2[A2.index(i)]
            else:
                a+=13
        return a


Jeu()