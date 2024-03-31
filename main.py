from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Line, Ellipse, Rectangle, Triangle
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from math import cos, sin, pi, sqrt
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from random import choice
from copy import deepcopy
import numpy as np
import random
import time


# HomeScreen    [o]
# GameScreen    [o]
# Hexagon       [o]
# HexGrid       [o]
# MyApp         [o]






def pre_pascal(mat, team, side):
    mats = deepcopy(mat)
    if side == 'd':
        for i in range(len(mat)):
            if mat[i][0] == 0:
                mats[i][0] = 1
            elif mat[i][0] == team:
                mats[i][0] = 2
            else:
                mats[i][0] = 0
    else:
        for i in range(len(mat)):
            if mat[i][len(mat) - 1] == 0:
                mats[i][len(mat) - 1] = 1
            elif mat[i][len(mat) - 1] == team:
                mats[i][len(mat) - 1] = 2
            else:
                mats[i][len(mat) - 1] = 0
    return mats

def meilleur_coup(res, mat):
    flat = res.flatten()
    flat.sort()
    coup = np.where(mat != 0)
    libre = []
    occupe = []
    dic = {}
    for i in range(len(coup[0])):
        occupe.append((coup[0][i], coup[1][i]))
    n = 0
    while len(libre) == 0:
        n += 1
        li = np.where(res == flat[-n])
        libre = []
        for i in range(len(li[0])):
            libre.append((li[0][i], li[1][i]))
        for i in occupe:
            if i in libre:
                libre.remove(i)
        if len(occupe) == 0 and (int(len(mat) / 2), int(len(mat) / 2)) in libre:
            libre.remove((int(len(mat) / 2), int(len(mat) / 2)))
    for i in libre:
        sum_voisin = 0
        if i[0] + 1 <= len(res) - 1:
            sum_voisin += res[i[0] + 1][i[1]]
        if i[0] + 1 <= len(res) - 1 and i[1] - 1 >= 0:
            sum_voisin += res[i[0] + 1][i[1] - 1]
        if i[1] - 1 >= 0:
            sum_voisin += res[i[0]][i[1] - 1]
        if i[1] + 1 <= len(res) - 1:
            sum_voisin += res[i[0]][i[1] + 1]
        if i[0] - 1 >= 0 and i[1] + 1 <= len(res) - 1:
            sum_voisin += res[i[0] - 1][i[1] + 1]
        if i[0] - 1 >= 0:
            sum_voisin += res[i[0] - 1][i[1]]

        # doit etre un ratio entre la plus grosse valeur et ses voisins

        if sum_voisin not in dic:
            dic[sum_voisin] = [i]
        else:
            dic[sum_voisin].append(i)

    return choice(dic[max(dic.keys())])


def pascald(mat, slot, team):
    matx = deepcopy(mat)

    for i in range(1, len(matx) - (slot[1])):
        for j in range(slot[0] + 1):

            if matx[slot[0] - j][slot[1] + i] != team and matx[slot[0] - j][slot[1] + i] != 0:
                matx[slot[0] - j][slot[1] + i] = 0

            elif slot[0] - j + 1 < len(matx):
                if matx[slot[0] - j][slot[1] + i] == 0:
                    matx[slot[0] - j][slot[1] + i] = matx[slot[0] - j][slot[1] + i - 1] + matx[slot[0] - j + 1][
                        slot[1] + i - 1]
                elif matx[slot[0] - j][slot[1] + i] == team:
                    matx[slot[0] - j][slot[1] + i] = 2 * (
                                matx[slot[0] - j][slot[1] + i - 1] + matx[slot[0] - j + 1][slot[1] + i - 1])
            else:
                if matx[slot[0] - j][slot[1] + i] == 0:
                    matx[slot[0] - j][slot[1] + i] = matx[slot[0] - j][slot[1] + i - 1]
                elif matx[slot[0] - j][slot[1] + i] == team:
                    matx[slot[0] - j][slot[1] + i] = 2 * matx[slot[0] - j][slot[1] + i - 1]

    return matx


def pascalg(mat, slot, team):
    matx = deepcopy(mat)

    for i in range(1, (slot[1]) + 1):
        for j in range(len(matx) - slot[0]):

            if matx[slot[0] + j][slot[1] - i] != team and matx[slot[0] + j][slot[1] - i] != 0:
                matx[slot[0] + j][slot[1] - i] = 0

            elif slot[0] + j - 1 >= 0:
                if matx[slot[0] + j][slot[1] - i] == 0:
                    matx[slot[0] + j][slot[1] - i] = matx[slot[0] + j][slot[1] - i + 1] + matx[slot[0] + j - 1][
                        slot[1] - i + 1]
                elif matx[slot[0] + j][slot[1] - i] == team:
                    matx[slot[0] + j][slot[1] - i] = 2 * (
                                matx[slot[0] + j][slot[1] - i + 1] + matx[slot[0] + j - 1][slot[1] - i + 1])
            else:
                if matx[slot[0] + j][slot[1] - i] == 0:
                    matx[slot[0] + j][slot[1] - i] = matx[slot[0] + j][slot[1] - i + 1]
                elif matx[slot[0] + j][slot[1] - i] == team:
                    matx[slot[0] + j][slot[1] - i] = 2 * matx[slot[0] + j][slot[1] - i + 1]

    return matx




def ask_bot1(mat, team, assis):
    mat2 = deepcopy(np.transpose(mat))

    if team == 2:
        res = pascald(pre_pascal(mat, 2, "d"), (len(mat) - 1, 0), 2) * pascalg(pre_pascal(mat, 2, "g"), (0, len(mat) - 1), 2)
        res2 = np.transpose(pascald(pre_pascal(mat2, 1, "d"), (len(mat2) - 1, 0), 1) * pascalg(pre_pascal(mat2, 1, "g"), (0, len(mat2) - 1), 1))
    else:
        res = np.transpose(pascald(pre_pascal(mat2, 1, "d"), (len(mat2) - 1, 0), 1) * pascalg(pre_pascal(mat2, 1, "g"), (0, len(mat2) - 1), 1))
        res2 = pascald(pre_pascal(mat, 2, "d"), (len(mat) - 1, 0), 2) * pascalg(pre_pascal(mat, 2, "g"), (0, len(mat) - 1), 2)

    s = np.where(mat != 0)

    for i in range(len(s[0])):
        res[s[0][i]][s[1][i]] = 0
        res2[s[0][i]][s[1][i]] = 0

    coup = meilleur_coup(res + res2, mat)
    
    if assis==True:
        
        platposee = deepcopy (mat)
        poseeB = []
        for i in range (len (mat2)):        
            if platposee[:,i] [platposee [:,i] == team].size != 0:
                for y in range (platposee[:,i] [platposee [:,i] == team].size):
                    poseeB.append ((platposee [:,i].tolist().index(team), i))
                    platposee [platposee [:,i].tolist().index(team)][i] = 0
                    
        possibilites, pos = aide (mat, poseeB, team)
        if len (pos) != 0:
            coup = max(possibilites, key = possibilites.get)
        
    return (coup)

def calcul (search, distance, plat, pelement, team):
    elements = [pelement]
    zm = True
    search [pelement [0]][pelement [1]] = distance
    while len (elements) != 0:
        elements1 = deepcopy (elements)
        search1 = deepcopy (search)
        distance += 1
        
        for z in elements1:
            if pelement [1] == 0:
                if z [1] == len (plat) - 1:
                    zm = False
                    
            if pelement [1] == len (plat) - 1:
                if z [1] == 0:
                    zm = False
            
        up = []
        for slot in elements1:
            elements.remove (slot)
            if slot[0]+1 <= len(plat)-1:
                if plat [ slot[0]+1][ slot[1] ] == team and search1 [ slot[0]+1][ slot[1] ] == 0:
                    elements.append ((slot[0]+1, slot[1]))

                    search [slot[0]+1 ][ slot[1] ] = search [slot [0]][slot [1]]
                    up.append (((slot[0]+1, slot[1]), search [slot [0]][slot [1]]))
                    
                elif search1 [ slot[0]+1][ slot[1] ] == 0:
                    elements.append ((slot[0]+1, slot[1]))

                    search[ slot[0]+1 ][ slot[1] ] = search [slot [0]][slot [1]] + 1
                    up.append (((slot[0]+1, slot[1]), search [slot [0]][slot [1]] + 1))
            
            
            if slot[0]+1 <= len(plat)-1 and slot[1]-1 >= 0:
                if plat [ slot[0]+1][ slot[1]-1 ] == team and search1 [ slot[0]+1 ][ slot[1]-1 ] == 0:
                    elements.append ((slot[0]+1, slot[1]-1))

                    search[ slot[0]+1][ slot[1]-1] = search [slot [0]][slot [1]]
                    up.append (((slot[0]+1, slot[1]-1), search [slot [0]][slot [1]]))
                    
                elif search1 [ slot[0]+1 ][ slot[1]-1 ] == 0:
                    elements.append ((slot[0]+1, slot[1]-1))

                    search[ slot[0]+1 ][ slot[1]-1] = search [slot [0]][slot [1]] + 1
                    up.append (((slot[0]+1, slot[1]-1), search [slot [0]][slot [1]] + 1))
                
                
                
            if slot[1]-1 >= 0:
                if plat [ slot[0]][ slot[1]-1 ] == team and search1 [ slot[0] ][ slot[1]-1 ] == 0:
                    elements.append ((slot[0], slot[1]-1)) 
             
                    search[ slot[0] ][ slot[1]-1] = search [slot [0]][slot [1]]
                    up.append (((slot[0], slot[1]-1), search [slot [0]][slot [1]]))
                    
                elif search1 [ slot[0] ][ slot[1]-1 ] == 0:
                    elements.append ((slot[0], slot[1]-1))

                    search[ slot[0] ][ slot[1]-1] = search [slot [0]][slot [1]] + 1
                    up.append (((slot[0], slot[1]-1), search [slot [0]][slot [1]] + 1))
                
                
                
            if slot[1]+1 <= len(plat)-1:
                if plat [ slot[0]][ slot[1]+1 ] == team and search1 [ slot[0] ][ slot[1]+1 ] == 0:
                    elements.append ((slot[0], slot[1]+1))
 
                    search[ slot[0]][ slot[1]+1] = search [slot [0]][slot [1]]
                    up.append (((slot[0], slot[1]+1), search [slot [0]][slot [1]]))
                    
                elif search1 [ slot[0] ][ slot[1]+1 ] == 0:
                    elements.append ((slot[0], slot[1]+1))

                    search[ slot[0] ][ slot[1]+1 ] = search [slot [0]][slot [1]] + 1 
                    up.append (((slot[0], slot[1]+1), search [slot [0]][slot [1]] + 1))
                
                
                
            if slot[0]-1 >= 0 and slot[1]+1 <= len(plat)-1: 
                if plat [ slot[0]-1 ][ slot[1]+1 ] == team and search1 [ slot[0]-1 ][ slot[1]+1 ] == 0:
                    elements.append ((slot[0]-1, slot[1]+1))

                    search[ slot[0]-1 ][ slot[1]+1] = search [slot [0]][slot [1]]
                    up.append (((slot[0]-1, slot[1]+1), search [slot [0]][slot [1]]))
                    
                elif search1 [ slot[0]-1 ][ slot[1]+1 ] == 0:
                    elements.append ((slot[0]-1, slot[1]+1))

                    search[ slot[0]-1 ][ slot[1]+1] = search [slot [0]][slot [1]] + 1
                    up.append (((slot[0]-1, slot[1]+1), search [slot [0]][slot [1]] + 1))

                
            if slot[0]-1 >= 0:
                if plat [ slot[0]-1 ][ slot[1]] == team and search1 [ slot[0]-1 ][ slot[1] ] == 0:
                    elements.append ((slot[0]-1, slot[1]))
                
                    search[ slot[0]-1 ][ slot[1]] = search [slot [0]][slot [1]]
                    up.append (((slot[0]-1, slot[1]), search [slot [0]][slot [1]]))
                elif search1 [ slot[0]-1 ][ slot[1] ] == 0:
                    elements.append ((slot[0]-1, slot[1]))

                    search[ slot[0]-1 ][ slot[1] ] = search [slot [0]][slot [1]] + 1
                    up.append (((slot[0]-1, slot[1]), search [slot [0]][slot [1]] + 1))
        
        for i in up:
            if search [i [0][0]][i [0][1]] > i [1]:
                search [i [0][0]][i [0][1]] = i [1]
        
        
    return zm

def ask_bot2 (plat, team, assis):
    platposee = deepcopy (plat)
    if team == 2:
        autre = 1
        
    else:
        autre = 2
        plat = plat.transpose ()
    
    posee = []
    poseeB = []

    for i in range (len (plat)):        
        if platposee[:,i] [platposee [:,i] == team].size != 0:
            for y in range (platposee[:,i] [platposee [:,i] == team].size):
                poseeB.append ((platposee [:,i].tolist().index(team), i))
                platposee [platposee [:,i].tolist().index(team)][i] = 0
            
        if platposee[:,i] [platposee [:,i] == autre].size != 0:
            for y in range (platposee[:,i] [platposee [:,i] == autre].size):
                posee.append ((platposee [:,i].tolist().index(autre), i))
                platposee [platposee [:,i].tolist().index(autre)][i] = 0
    
    poss = [posee, poseeB]
    copy = deepcopy (plat)
    copy = np.where (copy == team, 0, copy)
    copy = np.where (copy == autre, 20, copy)

    posee = []
    for p in range (len (plat)):
        if plat [p][0] == autre:
            if p == 0:
                if plat [p+1][0] != autre:
                    posee.append ((p+1, 0))
            
            elif p == len (plat) - 1:
                if plat [p-1][0] != autre:
                    posee.append ((p-1, 0))
            else:
                if plat [p-1][0] != autre:
                    posee.append ((p-1, 0))
                if plat [p+1][0] != autre:
                    posee.append ((p+1, 0))
        else:
            posee.append ((p, 0))
        
        
        if plat [p][len (plat) - 1] == autre:
            if p == 0:
                if plat [p+1][len (plat) - 1] != autre:
                    posee.append ((p+1, len (plat) - 1))
            elif p == len (plat) - 1:
                if plat [p-1][len (plat) - 1] != 1:
                    posee.append ((p-1, len (plat) - 1))
            else:
                if plat [p-1][len (plat) - 1] != autre:
                    posee.append ((p-1, len (plat) - 1))
                if plat [p+1][len (plat) - 1] != autre:
                    posee.append ((p+1, len (plat) - 1))
        else:
            posee.append ((p, len (plat) - 1))
            
    zonem = []
    matriceprop = 0
    for slots in posee:
        zm = calcul (copy, 1, plat, slots, team)
        
        if zm == True:
            zonem.append (slots)
        
        matriceprop += copy
            
        copy = deepcopy (plat)
        copy = np.where (copy == team, 0, copy)
        copy = np.where (copy == autre, 20, copy)
        
    if team == 1:
        matriceprop = matriceprop.transpose () 
        platposee = platposee.transpose ()
        plat = plat.transpose ()

    for p in poss [0]:
        matriceprop [p [0]][p [1]] = 500
    
    for p2 in poss [1]:
        matriceprop [p2 [0]][p2 [1]] = 350
    
    for p3 in zonem:
        matriceprop [p3 [0]][p3 [1]] = 300
        

    possible = []
    for i in range (len (plat)):
        for y in range (len (plat)):
            if matriceprop [i][y] == np.min (matriceprop):
                possible.append ((i, y))  
    coup = random.choice (possible)
    
    
    if assis==True:

        possibilites, pos = aide (plat, poss [1], team)
        if len (pos) != 0:
            coup = max(possibilites, key = possibilites.get)
    
    return coup


def aide (plat, pos, team):
    if team == 2:
        autre = 1
    else:
        autre = 2
        
    possibilite = []
    for p in pos:
        y = p [0]
        x = p [1]
            
        v = False # y-2 et x+1
        if (y-2) > 0 and (x+1) < len (plat):
            if plat [y-2][x+1] == team:
                v = True
                
        if (y-2) == -1 and (x+1) <= len (plat) -1 and team == 1:
            v = True
                
        if v == True:
            n = 0
            if plat [y-1][x+1] == autre:
                n += 1
            elif plat [y-1][x] == autre:
                n -= 1
                    
            if n == -1:
                if plat [y-1][x+1] == 0:
                    possibilite.append ((y-1, x+1))
            
            elif n == 1:
                if plat [y-1][x] == 0:
                    possibilite.append ((y-1,x))
                    
        v = False #y-1 et x+2
        
        if (y-1) > 0 and (x+2) < len (plat):
            if plat [y-1][x+2] == team:
                v = True
                    
        if (x+2) == len (plat) and (y-1) >= 0 and team == 2:
            v = True
            
        if v == True:
            n = 0
            if plat [y-1][x+1] == autre:
                n += 1
            elif plat [y][x+1] == autre:
                n -= 1
                
            if n == -1:
                if plat [y-1][x+1] == 0:
                    possibilite.append ((y-1, x+1))
                
            elif n == 1:
                if plat [y][x+1] == 0:
                    possibilite.append ((y, x+1))
                    
            

        v = False #y-1 et x-1
        if (y-1) > 0 and (x-1) > 0:
            if plat [y-1][x-1] == team:
                v = True
            
        if v == True:
            n = 0
            if plat [y-1][x] == autre:
                n += 1
            elif plat [y][x-1] == autre:
                n -= 1
                    
            if n == -1:
                if plat [y-1][x] == 0:
                    possibilite.append ((y-1, x))
            
            elif n == 1:
                if plat [y][x-1] == 0:
                    possibilite.append ((y, x-1))
                    
            
            
        v = False #y+1 et x+1
        if (y+1) < len (plat) and (x+1) < len (plat):
            if plat [y+1][x+1] == team:
                v = True
                
        if v == True:
            n = 0
            if plat [y+1][x] == autre:
                n += 1
            elif plat [y][x+1] == autre:
                n -= 1
                
            if n == -1:
                if plat [y+1][x] == 0:
                    possibilite.append ((y+1, x))
            
            elif n == 1:
                if plat [y][x+1] == 0:
                    possibilite.append ((y, x+1))
                
            
        
            
        v = False #y+1 et x-2
        if ((y+1) < len (plat) and (x-2) > 0):
            if plat [y+1][x-2] == team:
                v = True
                
        if (y+1) <= len (plat) -1 and (x-2) == -1 and team == 2:
            v = True
            
        if v == True:
            n = 0
            if plat [y+1][x-1] == autre :
                n += 1
            elif plat [y][x-1] == autre:
                n -= 1
                
            if n == -1:
                if plat [y+1][x-1] == 0:
                    possibilite.append ((y+1, x-1))
            
            elif n == 1:
                if plat [y][x-1] == 0:
                    possibilite.append ((y, x-1))
        v = False #y+2 et x-1
        if (y+2) < len (plat) and (x-1) > 0:
            if plat [y+2][x-1] == team:
                v = True       
        if (y+2) == len (plat) and (x-1) >= 1 and team == 1:
           v = True      
        if v == True:
            n = 0
            if plat [y+1][x] == autre:
                n += 1
            elif plat [y+1][x-1] == autre:
                n -= 1       
            if n == -1:
                if plat [y+1][x] == 0:
                    possibilite.append ((y+1, x))   
            elif n == 1:
                if plat [y+1][x-1] == 0:
                    possibilite.append ((y+1, x-1))  
    possi = {}
    for i in possibilite:
        possi [i] = possibilite.count (i)   
    return possi, possibilite

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        Window.clearcolor = "#F0DBAF"
        #Window.fullscreen = 'auto'                    # FORCE FULLSCREEN

        self.window = GridLayout()
        self.window.rows = 5
        self.window.cols = 1

        self.player_box = GridLayout()
        self.player_box.rows = 1
        self.player_box.cols = 2

        self.player1 = GridLayout()
        self.player1.rows = 2
        self.player1.cols = 1

        self.player2 = GridLayout()
        self.player2.rows = 2
        self.player2.cols = 1

        self.player2_type = GridLayout()
        self.player2_type.rows = 1
        self.player2_type.cols = 2

        self.player1_type = GridLayout()
        self.player1_type.rows = 1
        self.player1_type.cols = 2

        self.play_box = GridLayout()
        self.play_box.rows = 1
        self.play_box.cols = 1

        self.exit_box = GridLayout()
        self.exit_box.rows = 1
        self.exit_box.cols = 1

        with self.window.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.rect = Rectangle(pos=self.window.pos, size=(self.window.size[0] + 20, self.window.size[1]))
        self.window.bind(pos=self.update_rect, size=self.update_rect)

        self.window.size_hint = (0.8, 0.8)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        self.window.spacing = 10
        self.player_box.spacing = 10

        self.titre = Label(text="Hex Game", font_size = 90)

        self.player1_entry = TextInput(text='enwatibateau',
                                       hint_text="Name player 1",
                                       multiline = False,
                                       size_hint=(0.75, 1.5))
        
        self.player1_type_check = CheckBox()
        self.player1_type_label = Label(text="bot ?")

        self.player2_entry = TextInput(text='shamiiow',
                                       hint_text="Name player 2",
                                       multiline = False,
                                       size_hint=(0.75, 1.5))
        
        self.player2_type_check = CheckBox()
        self.player2_type_label = Label(text="bot ?")
        

        self.len_grid = TextInput(text="7",
                                  hint_text = "len grid",)

        self.play_button = Button(text= "Play", font_size=40)
        self.exit_button = Button(text="Exit")

        self.play_button.bind(on_press=self.go_to_game)
        self.exit_button.bind(on_press=self.close_window)

        self.player1_type.add_widget(self.player1_type_check)
        self.player1_type.add_widget(self.player1_type_label)   

        self.player2_type.add_widget(self.player2_type_check)
        self.player2_type.add_widget(self.player2_type_label)

        self.play_box.add_widget(self.play_button)
        self.exit_box.add_widget(self.exit_button)

        self.player1.add_widget(self.player1_entry)
        self.player1.add_widget(self.player1_type)
        self.player2.add_widget(self.player2_entry)
        self.player2.add_widget(self.player2_type)

        self.player_box.add_widget(self.player1)
        self.player_box.add_widget(self.player2)

        self.window.add_widget(self.titre)
        self.window.add_widget(self.player_box)
        self.window.add_widget(self.len_grid)
        self.window.add_widget(self.play_box)
        self.window.add_widget(self.exit_box)

        self.add_widget(self.window)

    def update_rect(self, instance, value):
        value = 20
        self.rect.pos = (instance.pos[0] - value, instance.pos[1] - value)
        self.rect.size = (instance.size[0] + value*2, instance.size[1] + value*2)

    def go_to_game(self, instance):
        self.manager.get_screen('game').set_variables(self.player1_entry.text, self.player2_entry.text, self.p1_checkbox(), self.p2_checkbox(), int(self.len_grid.text))
        self.manager.get_screen('game').update()

        self.manager.current = 'game'

    def close_window(self, instance):
        App.get_running_app().stop() 
        Window.close()    

    def p1_checkbox(self):
        return self.player1_type_check.active

    def p2_checkbox(self):
        return self.player2_type_check.active
            
class GameScreen(Screen):
    def __init__(self, **kwargs):
        self.recap = []
        self.winner = 0
        self.widgets = []
        self.poss_pos = []
        self.hex_size = 25
        self.player = False
        self.turn_on = False
        self.longeur = 177013
        self.list_robot = ["dumb"]
        self.player1_name = 'shamiiow'
        self.player2_name = 'enwatibateau'
        self.type_robot = self.list_robot[0]
        self.couleur = ["white","blue", "red"]
        self.text_color = (176/255,97/255,97/255)

        # Creation du Grid

        super(GameScreen, self).__init__(**kwargs)
        self.GridGlobal = BoxLayout(orientation='vertical')

        # Creation des SousGrid

        self.header = GridLayout(rows=1, cols=3, size_hint_y=None, height=75)
        self.game_hex = Widget(size_hint_y=2)
        self.footer = GridLayout(rows=2, cols=2, size_hint_y=None, height=50*(Window.size[0]/Window.size[1]))

        # Creation des Widget

        self.player1_label = Label(text='Name player1', color = (176/255,97/255,97/255), font_size=30, bold = True)                                # Index 0
        self.turn_label = Label(text=self.player1_name+" commence !", color = (176/255,97/255,97/255), font_size=20, bold = True)                  # Index 1
        self.player2_label = Label(text='Name player2', color = (176/255,97/255,97/255), font_size=30, bold = True)                                # Index 2
        self.player1_last_play_label = Label(text='List of last play for player 1', color = (176/255,97/255,97/255), font_size=50)    # Index 3
        self.player2_last_play_label = Label(text='List of last play for player 2', color = (176/255,97/255,97/255), font_size=50)    # Index 4
        self.cancel_button = Button(text='Cancel last play', color = (0.9, 0.9, 0.9), font_size=40, background_color=(240/255, 219/255, 175/255), bold = True)                           # Index 5
        self.home_button = Button(text='Back home', color = (0.9, 0.9, 0.9), font_size=40, background_color=(240/255, 219/255, 175/255), bold = True)                                    # Index 6

        # Association des commande

        self.home_button.bind(on_press=self.go_to_home)
        self.cancel_button.bind(on_press=self.cancel_last_play)
        Window.bind(on_resize=self.on_window_resize)
        
        # Ajout des Widget aux SousGrid

        self.header.add_widget(self.player1_label)
        self.header.add_widget(self.turn_label)
        self.header.add_widget(self.player2_label)
        
        #self.footer.add_widget(self.player1_last_play_label)
        #self.footer.add_widget(self.player2_last_play_label)
        self.footer.add_widget(self.cancel_button)
        self.footer.add_widget(self.home_button)

        # Ajout des SousGrid au GridGlobal

        self.GridGlobal.add_widget(self.header)
        self.GridGlobal.add_widget(self.game_hex)
        self.GridGlobal.add_widget(self.footer)

        self.add_widget(self.GridGlobal)
        
        self.widgets.extend([self.player1_label, self.turn_label, self.player2_label, self.player1_last_play_label, self.player2_last_play_label, self.cancel_button, self.home_button])

    def on_window_resize(self, window, width, height):
        if self.turn_on:
            self.update()

    def on_touch_down(self, touch):
        poss_mouse = self.is_in_who(touch.pos)
        if (self.cancel_button.collide_point(*touch.pos)) or (self.home_button.collide_point(*touch.pos)) or (poss_mouse == None):
            self.update()
            return super(GameScreen, self).on_touch_down(touch)
        c = [poss_mouse[0]+1, poss_mouse[1]+1]
        if self.winner != 0 or self.grid_p[c[0]][c[1]] != 0:
            self.update()
            return

        self.play(c)
        
        if self.p2_type or self.p1_type: 
            clear_grid = [[self.grid_p[i][j] for j in range(1, len(self.grid_p[i])-1)] for i in range(1, len(self.grid_p)-1)]
            best_play = ask_bot1(np.array(clear_grid), 1, True)
            self.play([best_play[0]+1,best_play[1]+1])



        if self.player: self.turn_label.text= "Au tour de : "+ str(self.player2_name)
        else: self.turn_label.text= "Au tour de : "+ str(self.player1_name)

        self.update()

    def play(self, c):
        if self.winner != 0 or self.grid_p[c[0]][c[1]] != 0:
            return
        self.grid_w = [[0 for _ in range(self.longeur)] for _ in range(self.longeur)]
        self.grid_p[c[0]][c[1]] = 1 + int(self.player)
        self.recap.append(c)
        self.win()
        self.player = self.player ^ True

    def play_yummi(self):
        if self.winner != 0:
            self.update()
            return
        save_time = time.time()
        if self.type_robot == "dumb":
            self.poss_pos = []
            for i in range(1, self.longeur-1):
                for j in range(1, self.longeur-1):
                    if self.grid_p[i][j] == 0:
                        self.poss_pos.append((i, j))
            coord = random.choice(self.poss_pos)
        return coord
    
    def path(self, c, p):
        x, y = c[0], c[1]
        if self.grid_p[x][y] != p:
            return 
        self.grid_w[x][y] = 1
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if [i, j] != [0, 0] and [i, j] != [-1, -1]and [i, j] != [1, 1]:
                    if self.grid_p[x+i][y+j] == p and self.grid_w[x+i][y+j] == 0:
                        self.grid_w[x+i][y+j] = 1
                        self.path((x+i, y+j), p)               
        if (1 in self.grid_w[self.longeur-2] and p == 1) or (1 in [self.grid_w[i][self.longeur-2] for i in range(self.longeur)] and p == 2):
            self.winner = 1 + int(self.player)
            if self.winner == 1:
                self.turn_label.text= "Gagnant : "+ str(self.player1_name)
            if self.winner == 2:
                self.turn_label.text= "Gagnant : "+ str(self.player2_name)

    def win(self):
        self.grid_w = [[0 for _ in range(self.longeur)] for _ in range(self.longeur)]
        for i in range(1,self.longeur-1):
            if self.winner == 0:
                self.path((1 ,i), 1)
        self.grid_w = [[0 for _ in range(self.longeur)] for _ in range(self.longeur)]
        for i in range(1,self.longeur-1):
            if self.winner == 0:
                self.path((i, 1), 2)

    def is_in_who(self, moos_poss):
        for i in range(len(poss_hex)):
            for j in range(len(poss_hex[i])):
                distance = sqrt((moos_poss[0] - poss_hex[i][j][0])**2 + (moos_poss[1] - poss_hex[i][j][1])**2)
                if distance <= (self.hex_width)/2:
                    return [i,j]      
    
    def cancel_last_play(self, instance):
        if self.recap == []:
            return
        self.winner =0
        self.grid_p[self.recap[-1][0]][self.recap[-1][1]] = 0
        self.recap.pop()
        self.player = self.player ^ True
        if self.player: self.turn_label.text= "Au tour de : "+ str(self.player2_name)
        else: self.turn_label.text= "Au tour de : "+ str(self.player1_name)
        self.update()

    def update(self):
        self.game_hex.canvas.before.clear()
        if self.winner == 1:
            self.turn_label.text= "Gagnant : "+ str(self.player1_name)
        if self.winner == 2:
            self.turn_label.text= "Gagnant : "+ str(self.player2_name)

        facteur = 2.5

        self.hex_size = min((Window.size[0])/(facteur*(self.coll+self.coll//2)),((Window.size[1])/(facteur*self.coll)))

        self.hex_width = cos(pi/6) * 2 * self.hex_size
        self.hex_height = (cos(pi/3) * self.hex_size + self.hex_size * 0.5) * 2

        if self.longeur%2 != 0:
            self.center_x_grid = Window.size[0]*0.5 - (self.coll + self.coll//2 - 1)/2*self.hex_width
            self.center_y_grid = Window.size[1]*0.5 + (self.hex_height - cos(pi/3) * self.hex_size)*(self.coll//2) 
        if self.longeur%2 == 0:
            self.center_x_grid = Window.size[0]*0.5 - (0.75 + 1.5  * (self.coll/2 - 1))*self.hex_width
            self.center_y_grid = Window.size[1]*0.5 + ((cos(pi/3) + 1) * self.hex_size * 0.5) + (self.hex_height - cos(pi/3) * self.hex_size)*(self.coll/2 - 1)

        with self.game_hex.canvas.before:
            self.hex_grid = HexGrid(rows=self.coll, cols=self.coll, hex_size=self.hex_size, pos_x=self.center_x_grid, pos_y= self.center_y_grid, grid_p=self.grid_p, coll=self.coll) 

        self.footer.height=min((Window.size[1])/16, 1000000)
        #self.affiche() 

    def affiche(self):
        for i in range(1, self.longeur-1):
            print("  "*i+str(self.grid_p[i])+"   "*(self.longeur//2)+str(self.grid_w[i])+"   "*(self.longeur//2)+str(poss_hex[i-1]))
        print(self.winner)

    def set_variables(self, player1_name, player2_name, p1_checkbox, p2_checkbox, longUeur):
        global poss_hex
        
        self.turn_on = True
        self.longUeur = max(2, longUeur)
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.widgets[0].text = player1_name
        self.widgets[2].text = player2_name
        self.turn_label.text = self.player1_name+" commence !"
        self.p1_type = p1_checkbox
        self.p2_type = p2_checkbox
        self.longeur = self.longUeur +2
        self.coll = self.longeur-2
        self.height_total = self.hex_size*self.coll + (self.hex_size+1)*(0.15)

        self.hex_size = min((Window.size[0])/(2*(self.coll+self.coll//2)),((Window.size[1])/(2*self.coll)))

        self.hex_width = cos(pi/6) * 2 * self.hex_size
        self.hex_height = (cos(pi/3) * self.hex_size + self.hex_size * 0.5) * 2
        self.grid_p = [[0 for _ in range(self.longeur)] for _ in range(self.longeur)]
        self.grid_w = [[0 for _ in range(self.longeur)] for _ in range(self.longeur)]
        poss_hex = [[0 for _ in range(self.longeur-2)] for _ in range(self.longeur-2)]
        
        if self.longeur%2 != 0:
            self.center_x_grid = Window.size[0]*0.5 - (self.coll + self.coll//2 - 1)/2*self.hex_width
            self.center_y_grid = Window.size[1]*0.5 + (self.hex_height - cos(pi/3) * self.hex_size)*(self.coll//2) 
        if self.longeur%2 == 0:
            self.center_x_grid = Window.size[0]*0.5 - (0.75 + 1.5  * (self.coll/2 - 1))*self.hex_width
            self.center_y_grid = Window.size[1]*0.5 + ((cos(pi/3) + 1) * self.hex_size * 0.5) + (self.hex_height - cos(pi/3) * self.hex_size)*(self.coll/2 - 1)

        if self.p2_type and self.p1_type:
            while self.winner == 0: 
                self.play(self.play_yummi())   
                
        elif self.p1_type:
            self.play(self.play_yummi())
        
        for i in range(self.longeur):
            for j in range(self.longeur):
                if (i == 0) or (j == 0) or (i == self.longeur-1) or (j == self.longeur-1):
                    self.grid_p[i][j] = 9

        self.update()


        

    def go_to_home(self, instance):
        self.game_hex.canvas.before.clear()

        self.grid_p = [[0 for _ in range(self.longeur)] for _ in range(self.longeur)]
        self.recap == []
        self.player = False
        self.winner = 0
        self.manager.current = 'home'

class Hexagon(Widget):
    def __init__(self, center_x, center_y, hex_size, row, col, grid_p, coll, **kwargs):
        super(Hexagon, self).__init__(**kwargs)
        self.row = row
        self.col = col
        self.grid_p = grid_p
        self.hex_size = hex_size
        self.center_x = center_x
        self.center_y = center_y
        self.hex_width = cos(pi/6) * self.hex_size * 2
        self.coll = coll
        
        self.draw_hex()

    def draw_hex(self):
        with self.canvas:
            if self.grid_p[self.row+1][self.col+1] == 0:
                Color(.8,.8,.8)
            if self.grid_p[self.row+1][self.col+1] == 1:
                Color(126/255,215/255,193/255)
                #Color(0,0,0.5)
            
            points = []
            for i in range(6):
                angle = pi / 2 + 2 * pi * i / 6
                points.extend([self.center_x + self.hex_size * cos(angle), self.center_y + self.hex_size * sin(angle)])

            if self.grid_p[self.row+1][self.col+1] == 2:
                Color(220/255,134/255,134/255)
                #Color(0.5,0,0)


            Triangle(points=points[4:10])
            Triangle(points=points[-2:]+points[:5])
            Rectangle(pos=points[4:6], size=(self.hex_width, self.hex_size))


            Color(.2,.2,.2)
            
            # Dessiner les contours du triangle
            
            Line(points=points + points[:2], width = (35)/(self.coll))

            

class HexGrid(Widget):
    def __init__(self, rows, cols, hex_size, pos_x=0, pos_y=0, grid_p=0, coll=0, **kwargs):
        super(HexGrid, self).__init__(**kwargs)
        self.rows = rows
        self.cols = cols
        self.pos_x = pos_x 
        self.pos_y = pos_y 
        self.grid_p = grid_p
        self.hex_size = hex_size
        self.hex_width = cos(pi/6) * self.hex_size * 2
        self.height = (cos(pi/3) * self.hex_size + self.hex_size * 0.5) * 2
        self.coll = coll

        self.draw_grid()
        

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                center_x = self.pos_x + (col+(row/2)) * self.hex_width
                center_y = self.pos_y - row * (self.height - cos(pi/3) * self.hex_size)
                poss_hex[row][col] = (round(center_x), round(center_y))
        ratio = 1.25

        top_left = [(poss_hex[0][0][0]-self.hex_width*ratio), (poss_hex[0][0][1]+self.height*0.5*ratio)]
        bot_right = [(poss_hex[-1][-1][0]+self.hex_width*ratio), (poss_hex[-1][-1][-1]-self.height*0.5*ratio)]
        top_right = [(poss_hex[0][-1][0]+self.hex_width*0.5*ratio), (poss_hex[0][-1][1]+self.height*0.5*ratio)]
        bot_left = [(poss_hex[-1][0][0]-self.hex_width*0.5*ratio), (poss_hex[-1][0][1]-self.height*0.5*ratio)]
        middle = [Window.size[0]/2, Window.size[1]/2]

        Color(220/255,134/255,134/255)
        Triangle(points=top_left+bot_left+middle)
        Triangle(points=top_right+bot_right+middle)
        
        Color(126/255,215/255,193/255)
        Triangle(points=top_left+top_right+middle)
        Triangle(points=bot_left+bot_right+middle)
        

        for row in range(self.rows):
            for col in range(self.cols):
                center_x = self.pos_x + (col+(row/2)) * self.hex_width
                center_y = self.pos_y - row * (self.height - cos(pi/3) * self.hex_size)
                Hexagon(center_x, center_y, self.hex_size, row, col, self.grid_p, self.coll)    

class MyApp(App):
    def build(self):
        self.title = 'Hex Game'
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(GameScreen(name='game'))
        return sm
    
poss_hex = []

if __name__ == '__main__':
     MyApp().run()