from tkinter import *
import time
from math import*



########################################################## Classes #####################################################################


class Niveau:
        """Classe permettant de créer un niveau"""
        def __init__(self,fichier):
                self.liste = 0
                self.fichier = fichier
        
        def generer(self):
                """Méthode permettant de générer le niveau en fonction du fichier.
                On crée une liste générale, contenant une liste par ligne à afficher""" 
                #On ouvre le fichier
                with open(self.fichier, "r") as fichier:
                        structure_niveau = []
                        #On parcourt les lignes du filter                                                                                       
                        for ligne in fichier:
                                ligne_niveau = []
                                #On parcourt les sprites (lettres) contenus dans le fichier
                                for sprite in ligne:
                                        #On ignore les "\n" de fin de ligne
                                        if sprite != '\n':
                                                #On ajoute le sprite à la liste de la ligne
                                                ligne_niveau.append(sprite)
                                #On ajoute la ligne à la liste du niveau
                                structure_niveau.append(ligne_niveau)
                        #On sauvegarde cette structure
                        self.liste = structure_niveau
                        
        def afficher(self):
                """Méthode permettant d'afficher le niveau en fonction 
                de la liste de structure renvoyée par generer()"""
                self.fond=PhotoImage(file="images/fond.gif")
                canvas.create_image(0,0, anchor = NW, image=self.fond)
                self.fond_menu=PhotoImage(file="images/fond_menu_jeu.gif")
                canvas.create_image(0,780,anchor = NW, image=self.fond_menu)

                self.mur = PhotoImage(file="images/mur.gif")
                self.depart = PhotoImage(file="images/depart.gif")
                self.arrivee = PhotoImage(file="images/arrivee.gif")
                
                
                #On parcourt la liste du niveau
                num_ligne = 0
                for ligne in self.liste:
                        #On parcourt les listes de lignes
                        num_case = 0
                        for sprite in ligne:
                                #On calcule la position réelle en pixels
                                x = num_case * taille_sprite
                                y = num_ligne * taille_sprite
                                if sprite == 'm':                  #m = Mur
                                       canvas.create_image(x, y,anchor = NW,image=self.mur)
                                elif sprite == 'd':                #d = Départ
                                        canvas.create_image(x, y,anchor = NW,image=self.depart)
                                        
                                elif sprite == 'a':               #a = Arrivée
                                        canvas.create_image(x, y,anchor = NW,image=self.arrivee)
                                num_case += 1
                        num_ligne += 1

                self.tour1_menu_image= PhotoImage(file="images/tour1_menu.gif")
                self.tour1_menu=canvas.create_image(140,800,anchor=NW,image=self.tour1_menu_image)
                self.mine_menu_image=PhotoImage(file="images/mine_menu.gif")
                self.tour1_menu=canvas.create_image(375,800,anchor=NW,image=self.mine_menu_image)
                self.b_vie=canvas.create_image(1150,825,anchor=NW,image=img_vie)
                self.b_argent=canvas.create_image(1150,875,anchor=NW,image=img_argent)



#Classe permettant de créer un ennemi, le faire se déplacer et lui infliger des dégats  
class Mechant:
        def __init__(self,niveau,vitesse,vie,vitesse_tir):
                #Niveau dans lequel l'ennemi se trouve
                self.niveau=niveau
                #Positionnement de l'ennemi en cases et pixels
                self.case_x=0                   
                self.case_y=0
                self.x = 60
                self.y = 0
                #Vitesse et vie de l'ennemi
                self.vitesse=vitesse
                self.vie_monstre=vie
                self.vie_monstre_ref=vie
                #Variable barre de vie de l'ennemi
                self.color='green'
                self.xBV=60
                self.xmaxBV=60
                self.yBV=0
                self.jaune=False
                self.rouge=False
                #Vitesse des dégats subit par l'ennemi
                self.vitesse_tir=vitesse_tir

                


        #Méthode permettant de créer l'ennemi 
        def creation(self):
                #Chargement des images
                self.img_monstre=PhotoImage(file="images/monstre.gif")
                self.monstre=canvas.create_image(self.case_x,self.case_y,image=self.img_monstre,anchor=NW,tag="monstre1")
                #Creation barre de vie
                self.barre_vie=canvas.create_rectangle(self.xBV+10,self.yBV+45,self.xmaxBV+50,self.yBV+48,fill=self.color)
                #Ajout de l'ennemi dans "liste_ennemi"
                liste_ennemi.append(self.monstre)

                self.detection()


        #Méthode permettant de déplacer l'ennemi 
        def deplacement(self):

                global vie_joueur,argent
                #Variable pour le deplacement de l'ennemi 
                droite=0
                bas=0
                self.indication()
                #Actualisation de la barre de vie de l'ennemi
                canvas.itemconfigure(self.barre_vie,fill=self.color)

                
                if len(canvas.find_withtag("monstre1"))>0:
                        #Destruction de l'ennemi si sa vie est inférieur à 0
                        if self.vie_monstre<=0:
                                if self.monstre in liste_ennemi:
                                        liste_ennemi.remove(self.monstre)
                                self.case_x=0
                                self.case_y=0
                                self.vie_monstre=10000000
                                
                                canvas.delete(self.monstre)
                                canvas.delete(self.barre_vie)
                                #Ajout et actualisation de l'argent 
                                argent+=20
                                compteur_argent.configure(text=argent)
                                
                                             
                        #Destruction de l'ennemi si il atteint la ligne d'arrivé
                        if self.case_x < spriteX_max:
                                if niveau.liste[self.case_y][self.case_x+1] == 'a':           
                                        self.case_x=0
                                        self.case_y=0
                                        if self.monstre in liste_ennemi:
                                                liste_ennemi.remove(self.monstre)
                                        canvas.delete(self.monstre)
                                        canvas.delete(self.barre_vie)
                                        #On enleve 1 de vie au joueur
                                        vie_joueur-=1
                                        compteur_vie.configure(text=vie_joueur)
                                        #Si la vie du joueur est inférieur a 0 il perd la parti 
                                        if vie_joueur<=0:
                                                fin()
                        #On vérifie si l'ennemi peut avancer vers le bas 
                        if self.case_y < spriteY_max:
                                if niveau.liste[self.case_y+1][self.case_x] != 'm':
                                        bas=1
                        #On vérifie si l'ennemi peut avancer vers la droite
                        if self.case_x < spriteX_max-1:
                                if niveau.liste[self.case_y][self.case_x+1] != 'm':
                                        droite=1
                        #Déplacement vers le bas
                        if bas==1:
                                self.case_y += 1
                                self.y = self.case_y * taille_sprite
                                self.yBV=self.case_y * taille_sprite
                                self.xmaxBV=self.case_x * taille_sprite
                                if self.jaune==True:
                                        self.xmaxBV-=20
                                if self.rouge==True:
                                        self.xmaxBV-=35
                                canvas.coords(self.monstre,self.x,self.y)
                                canvas.coords(self.barre_vie,self.xBV+10,self.yBV+45,self.xmaxBV+50,self.yBV+48)
                        #Déplacement vers la droite        
                        if droite==1:
                                self.case_x += 1
                                self.x = self.case_x * taille_sprite
                                self.xBV=self.case_x * taille_sprite
                                self.xmaxBV=self.case_x * taille_sprite
                                if self.jaune==True:
                                        self.xmaxBV-=20
                                if self.rouge==True:
                                        self.xmaxBV-=35
                                canvas.coords(self.monstre,self.x,self.y)
                                canvas.coords(self.barre_vie,self.xBV+10,self.yBV+45,self.xmaxBV+50,self.yBV+48)
                        #Vitesse de déplacement de l'ennemi    
                        canvas.after(self.vitesse,self.deplacement)
                
                
        #Méthode permettant l'actualisation de la barre de vie de l'ennemi 
        def indication (self):
                if ((100*self.vie_monstre)/self.vie_monstre_ref)<=55:
                        self.color='yellow'
                        self.jaune=True
                        if ((100*self.vie_monstre)/self.vie_monstre_ref)<=20:
                                self.jaune=False
                                self.color='red'
                                self.rouge=True

        #Méthode permmetant d'infliger des dégats au premier ennemi sur le terrain       
        def vie(self):
                if liste_ennemi[0]==self.monstre:
                        self.vie_monstre-=1 

        #Méthode permettant de verifier si l'ennemi est à porter d'attque des tours                 
        def detection(self):
                if len(canvas.find_withtag("zoneT1"))>0:#On test si il y a des hitbox sur le terrain pour ne pas lancer toute la fonction en boucle
                                bbox=canvas.bbox(self.monstre)
                                if bbox is not None: 
                                        xminM,yminM,xmaxM,ymaxM=canvas.bbox(self.monstre) #Coordonnées de l'ennemi
                                        hitbox=canvas.find_overlapping(xminM,yminM,xmaxM,ymaxM) #On regarde quand les coordonnées de l'ennemi entre en collision avec un objet
                                        
                                        for i in hitbox:                                                      
                                                tag=canvas.gettags(i)
                                                #On chercher le tag de notre hitbox('zoneT1')
                                                if len(tag)>0:
                                                        if tag ==('zoneT1',) or tag==('zoneT1', 'current') : #Si il est present on lance la fonction vie
                                                                self.vie()
                

                canvas.after(self.vitesse_tir,self.detection)
                       

#Classe permetant de créer une tour infligeant de dégats aux ennmis        
class Tour:
        def __init__(self,niveau,xdepart,ydepart):
                #Coordonnées de départ de la tour 
                self.xdepart=xdepart
                self.ydepart=ydepart
                #Niveau dans lequel se trouve la tour 
                self.niveau=niveau
                
        #Méthode permettant la création de la tour        
        def creation(self):
                #Chargement et affichage des images
                self.tour1_menu_image= PhotoImage(file="images/tour1_menu.gif")
                self.tour1_image=PhotoImage(file="images/tour1.gif")
                self.tour1_menu=canvas.create_image(self.xdepart,self.ydepart,anchor=NW,image=self.tour1_menu_image)

        #Méthode permettant de detecter si le joueur sélectionne la tour 
        def clic(self,event):
                """ Gestion de l'événement Clic gauche """
                global DETECTION_CLIC_SUR_TOUR
                
                # position du pointeur de la souris
                X = event.x
                Y = event.y
                # coordonnées de l'objet
                [xmin,ymin,xmax,ymax] = canvas.bbox(self.tour1_menu)

                #On vérifie que le pointeur de la souris est sur l'image de la tour
                if xmin<=X<=xmax and ymin<=Y<=ymax:
                        DETECTION_CLIC_SUR_TOUR = True
                        self.cercleT1=canvas.create_oval(X-centre_cercle,Y-centre_cercle,X+centre_cercle,Y+centre_cercle)
                        self.tour1=canvas.create_image(X-centreTour,Y-centreTour,anchor=NW,image=self.tour1_image)

                else:
                        DETECTION_CLIC_SUR_TOUR = False

                
        #Méthode permettant de déplacer la tour en fonction de la position du pointeur du joueur
        def drag(self,event):
                """ Gestion de l'événement bouton gauche enfoncé """
                X = event.x
                Y = event.y
                
                if DETECTION_CLIC_SUR_TOUR == True:
                        # limite de l'objet dans la zone graphique
                        if X<centreTour:X=centreTour
                        if X>largeur-centreTour: X=largeur-centreTour
                        if Y<centreTour: Y=centreTour
                        if Y>hauteur-centreTour: Y=hauteur-centreTour
                        # mise à jour de la position de l'objet (drag)
                        canvas.coords(self.tour1,X-centreTour,Y-centreTour)
                        canvas.coords(self.cercleT1,X-centre_cercle,Y-centre_cercle,X+centre_cercle,Y+centre_cercle)

        #Méthode permettant de calculer la case ou poser la tour
        def case(self,event):
                if DETECTION_CLIC_SUR_TOUR == True:
                        #Coordonnées du pointeur de la souris
                        X=event.x
                        Y=event.y
                        #Case ou se trouve la tour
                        self.caseX= X/taille_sprite
                        self.caseY= Y/taille_sprite

                        self.caseX_Arrondi=floor(self.caseX)# arrondi en dessous
                        self.caseY_Arrondi=floor(self.caseY)# arrondi en dessous

                        #Condition pour ne pas que le joueur puisse dépasser l'écran avec la tour 
                        if self.caseX_Arrondi>spriteX_max:
                                self.caseX_Arrondi=spriteX_max 
                        if self.caseX_Arrondi<0:
                                self.caseX_Arrondi=0
                        if self.caseY_Arrondi>spriteY_max:
                                self.caseY_Arrondi=spriteY_max 

        #Méthode permettant de verifier le positionnement valide de la tour et de la poser       
        def positionnement(self,event):
                global argent
                if DETECTION_CLIC_SUR_TOUR == True:
                        X=event.x
                        Y=event.y

                        #Supprime la tour en dessous d'une certaine hauteur 
                        if  Y>=(spriteY_max*taille_sprite):
                                canvas.delete(self.tour1) 
                                canvas.delete(self.cercleT1)

                        if Y<(spriteY_max*taille_sprite):       
                                #Supprime la tour elle est sur case non autorisé
                                if niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="0" or niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="d" or niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="a":
                                        canvas.delete(self.tour1) 
                                        canvas.delete(self.cercleT1)
                                        
                                
                                if niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="m":
                                        #Place la tour et créer une hitbox si son emplacement est valide et l'argent suffisant
                                        if [self.caseX_Arrondi,self.caseY_Arrondi] not in liste_tour and argent>=100:
                                                #Retrait de l'argent pour l'achat de la tour 
                                                argent-=100
                                                compteur_argent.configure(text=argent)
                                                #Placement de la tour 
                                                canvas.coords(self.tour1,self.caseX_Arrondi*taille_sprite,self.caseY_Arrondi*taille_sprite)
                                                canvas.delete(self.cercleT1)
                                                
                                                #Coordonnées de la zone d'attaque
                                                self.xminHitboxT1=((self.caseX_Arrondi*taille_sprite)+centreTour)-centre_cercle
                                                self.yminHitboxT1=((self.caseY_Arrondi*taille_sprite)+centreTour)-centre_cercle
                                                self.xmaxHitboxT1=((self.caseX_Arrondi*taille_sprite)+centreTour)+centre_cercle
                                                self.ymaxHitboxT1=((self.caseY_Arrondi*taille_sprite)+centreTour)+centre_cercle

                                                #Création de la zone d'attaque
                                                hitboxT1=canvas.create_oval(self.xminHitboxT1,self.yminHitboxT1,self.xmaxHitboxT1,self.ymaxHitboxT1,width=0,fill='',tags="zoneT1")#Creation de la hitbox
                                                self.liste()
                                        else:
                                                canvas.delete(self.tour1) 
                                                canvas.delete(self.cercleT1)
                        
                                else:
                                        canvas.delete(self.tour1) 
                                        canvas.delete(self.cercleT1)


        #Méthode permettant d'ajouter les coordonées de la tour dans une liste
        def liste(self):
                global liste_tour
                self.list_case=[self.caseX_Arrondi,self.caseY_Arrondi]
                liste_tour.append(self.list_case)
                
#Classe permetant de créer une tour qui produit de l'argent        
class Tour_Argent:
        def __init__(self,niveau,xdepart,ydepart):
                #Coordonnées de départ de la tour
                self.xdepart=xdepart
                self.ydepart=ydepart
                #Niveau dans lequel se trouve la tour
                self.niveau=niveau
                
        #Méthode permettant la création de la tour      
        def creation(self):
                #Chargement et affichage des images
                self.mine_menu_image=PhotoImage(file="images/mine_menu.gif")
                self.mine_menu=canvas.create_image(self.xdepart,self.ydepart,anchor=NW,image=self.mine_menu_image)
                self.mine_image=PhotoImage(file="images/mine.gif")

        #Méthode permettant de detecter si le joueur sélectionne la tour 
        def clic(self,event):
                """ Gestion de l'événement Clic gauche """
                global DETECTION_CLIC_SUR_MINE
                
                # position du pointeur de la souris
                X = event.x
                Y = event.y
                # coordonnées de l'objet
                [xmin,ymin,xmax,ymax] = canvas.bbox(self.mine_menu)
                #On vérifie que le pointeur de la souris est sur l'image de la tour
                if xmin<=X<=xmax and ymin<=Y<=ymax:
                        DETECTION_CLIC_SUR_MINE = True
                        self.mine=canvas.create_image(X-centreTour,Y-centreTour,anchor=NW,image=self.mine_image)

                else:
                        DETECTION_CLIC_SUR_MINE = False

                
        #Méthode permettant de déplacer la tour en fonction de la position du pointeur du joueur
        def drag(self,event):
                """ Gestion de l'événement bouton gauche enfoncé """
                X = event.x
                Y = event.y
                
                if DETECTION_CLIC_SUR_MINE == True:
                        # limite de l'objet dans la zone graphique
                        if X<centreTour:X=centreTour
                        if X>largeur-centreTour: X=largeur-centreTour
                        if Y<centreTour: Y=centreTour
                        if Y>hauteur-centreTour: Y=hauteur-centreTour
                        # mise à jour de la position de l'objet (drag)
                        canvas.coords(self.mine,X-centreTour,Y-centreTour)
                        
        #Méthode permettant de calculer la case ou poser la tour
        def case(self,event):
                #Coordonnées du pointeur de la souris
                X=event.x
                Y=event.y
                #Case ou se trouve la tour
                self.caseX= X/taille_sprite
                self.caseY= Y/taille_sprite

                self.caseX_Arrondi=floor(self.caseX)# arrondi en dessous
                self.caseY_Arrondi=floor(self.caseY)# arrondi en dessous

                #Condition pour ne pas que le joueur puisse dépasser l'écran avec la tour
                if self.caseX_Arrondi>spriteX_max:
                        self.caseX_Arrondi=spriteX_max 
                if self.caseX_Arrondi<0:
                        self.caseX_Arrondi=0
                if self.caseY_Arrondi>spriteY_max:
                        self.caseY_Arrondi=spriteY_max 
                
        #Méthode permettant de verifier le positionnement valide de la tour et de la poser        
        def positionnement(self,event):
                global argent
                X=event.x
                Y=event.y
                
                if DETECTION_CLIC_SUR_MINE == True:
                        #Supprime la tour en dessous d'une certaine hauteur
                        if  Y>=(spriteY_max*taille_sprite):
                                canvas.delete(self.mine) 
                                
                        if Y<(spriteY_max*taille_sprite):       
                                #Supprime la tour elle est sur case non autorisé
                                if niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="0" or niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="d" or niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="a":
                                        canvas.delete(self.mine) 
                                if niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="m":      
                                        #Place la tour si son emplacement est valide et l'argent suffisant
                                        if [self.caseX_Arrondi,self.caseY_Arrondi] not in liste_tour and argent>=150:
                                                #Retrait de l'argent pour l'achat de la tour
                                                argent-=150
                                                compteur_argent.configure(text=argent)
                                                #Placement de la tour
                                                canvas.coords(self.mine,self.caseX_Arrondi*taille_sprite,self.caseY_Arrondi*taille_sprite)
                                                self.liste()
                                                self.prod_argent()
                                        else:
                                                canvas.delete(self.mine)
                                else:
                                    canvas.delete(self.mine)    
        #Méthode permettant d'ajouter les coordonées de la tour dans une liste               
        def liste(self):
                global liste_tour
                self.list_case=[self.caseX_Arrondi,self.caseY_Arrondi]
                liste_tour.append(self.list_case)                

        #Méthode permettant d'ajouter de l'argent au joueur lorsque la vague est lancé
        def prod_argent(self):
                global argent
                if menu_check==False:
                        if Vague==True:
                                argent+=5
                                compteur_argent.configure(text=argent)
                                
                        canvas.after(1000,self.prod_argent)
                








#Fonction lorsque l'on lance la fonction en active d'autres
def b_lancer():
        start()
        vague()
        test_win()



#Fonction pour les vagues d'ennemis
def vague():
        global Nb_ennemis,Nb_ennemis_voulus,Vague,liste_ennemi,win,compt_vague
        #si pas dans le menu
        if menu_check==False:
            #si bouton lancer_vague est activé
                if scenario==1:
                    #si nombre d'ennemis créés < à nombre d'ennemis voulus
                        if Nb_ennemis<Nb_ennemis_voulus:
                                #appel des fonctions de la classe Mechant
                                mechant=Mechant(niveau,vitesse_ennemi,vie_ennemi,75)
                                mechant.creation()
                                mechant.deplacement()              
                                Vague=True
                                Nb_ennemis+=1
                        
                        #si nombre d'ennemis créés = nombre d'ennemis voulus
                        #ET si nombre d'ennemis dans le canvas = 0
                        if Nb_ennemis==Nb_ennemis_voulus and len(canvas.find_withtag("monstre1"))==0:
                                liste_ennemi=[]
                                Vague=False
                                win+=1
                                compt_vague+=1
                                #mettre à jour l'étiquette du numéro de vague
                                compteur_vague.configure(text="Vagues : "+str(compt_vague)+"/5")
                                start()
                                Nb_ennemis_voulus+=2
                                Nb_ennemis=0
                        #attendre 1s puis rappeler la fonction vague()
                        canvas.after(1000,vague)                
        
#Verifcation de la victoire
def test_win():
        if menu_check==False:
                if win==5:
                        gagner()
        canvas.after(10,test_win)

#Fonction de régulation du jeu 
def start():
        global scenario
        scenario=1
        b_lancer.config(state='disabled')
        if Nb_ennemis==Nb_ennemis_voulus and len(canvas.find_withtag("monstre1"))==0:
                scenario=0
                b_lancer.config(state='normal')

        
                



#Fonction lier au clic gauche
def clic_gauche(event):
        if menu_check==False:
                tour.clic(event)
                tour_argent.clic(event)

                def drag(event):
                        tour.drag(event)
                        tour.case(event)
                        tour_argent.drag(event)
                        tour_argent.case(event)                               

                def relacher(event):
                        tour.positionnement(event)
                        tour_argent.positionnement(event)

                canvas.bind('<B1-Motion>',drag) # événement bouton gauche enfoncé (hold down)
                canvas.bind('<ButtonRelease-1>',relacher)



#Si l'on perd la partie              
def fin():
        global menu_check
        menu_check=True
        canvas.delete(ALL)
        b_lancer.pack_forget()
        b_menu.pack_forget()
        b_lancer.place_forget()
        b_menu.place_forget()

        canvas.create_image(0,0,image=img_fin, anchor=NW)
        bouton_rejouer.place(x=590,y=600)
        
#Si l'on gagne la partie 
def gagner():
        global menu_check
        menu_check=True
        canvas.delete(ALL)
        b_lancer.pack_forget()
        b_menu.pack_forget()
        b_lancer.place_forget()
        b_menu.place_forget()

        canvas.create_image(0,0,image=img_win, anchor=NW)
        bouton_win.place(x=590,y=500)



#Retour au menu
def menu():
        global menu_check,liste_tour,Nb_ennemis,scenario,argent,Vague,Nb_ennemis_voulus,liste_ennemi,argent,vie_joueur,win,compt_vague
        
        #Réinitialisation des variables 
        menu_check=True
        liste_tour=[]
        liste_ennemi=[]
        Nb_ennemis=0
        scenario=0
        argent=100
        Vague=False
        Nb_ennemis_voulus=3
        argent=200
        vie_joueur=5
        win=0
        compt_vague=0
        



        compteur_argent.configure(text=argent)
        compteur_vie.configure(text=vie_joueur)
        compteur_vague.configure(text="Vagues : " +str(compt_vague)+"/5")

        b_lancer.config(state='normal')

        
        
        bouton_rejouer.place_forget()
        bouton_win.place_forget()
        b_lancer.place_forget()
        b_menu.place_forget()

        canvas.delete(ALL)

        canvas.create_image(0,0,image=fond, anchor=NW)
        canvas.create_image(840,438, image=titre)

        bouton_jouer.place(x=168,y=600)
        bouton_quitter.place(x=924,y=600)




        


#Lancement du jeu       
def jeu():
        global  menu_check,Vague
        #Réinitialisation
        menu_check=False
        Vague=False
        bouton_jouer.place_forget()
        bouton_quitter.place_forget()
        canvas.delete(ALL)

        #Fenetre dans le canvas pour fixer précisément les étiquettes
        canvas.create_window(1330,850,window=compteur_vie)
        canvas.create_window(1310,900,window=compteur_argent)
        canvas.create_window(315,850,window=texte_mine)
        canvas.create_window(80,850,window=texte_tour)
        canvas.create_window(735,920,window=compteur_vague)


        b_lancer.place(x=590,y=815)       
        b_menu.place(x=920,y=840)

        niveau.generer()
        niveau.afficher()
        
        
       

        tour.creation()
        tour_argent.creation()
        
        canvas.bind('<Button-1>',clic_gauche)

        



        
        
       

################################################ Variables #########################################################


#Paramètres matrice et terrain
choix = 'niveaux1'
taille_sprite=60
spriteX_max=24
spriteY_max=13

#Paramètres Tours
centreTour=30
centre_cercle=150
liste_tour=[]

#Paramètres ennemis
vie_ennemi = 27
vitesse_ennemi = 500 # ms/case
Nb_ennemis_voulus = 3
liste_ennemi = []

#Paramètres vagues
Nb_ennemis=0
scenario=0
win=0
compt_vague=0

#Taille canvas
largeur=1680
hauteur=1050

#Detection si le joueur clic sur une tour
DETECTION_CLIC_SUR_TOUR = False
#Detection si le joueur clic sur une mine
DETECTION_CLIC_SUR_MINE= False

#Verification du menu
menu_check=True
#Verifaction de l'activation de la vague d'ennemis
Vague=False

#Paramètres du joueur
argent=200
vie_joueur=5



######## Fenêtre Menu Initialisation ################################################################################
fenetre = Tk()
fenetre.attributes("-fullscreen",1)

canvas = Canvas(fenetre, width=largeur, height=hauteur,background="tan")
canvas.pack(fill="both",expand=1) 
                       
#Définition des images
fond = PhotoImage(file="images/fond_menu2.gif")
img_b_jouer = PhotoImage(file = "images/bouton_jouer.gif")
img_b_quitter = PhotoImage(file = "images/bouton_quitter.gif")
titre = PhotoImage(file = "images/titre.gif")
img_fin = PhotoImage(file="images/fin2.gif")
img_b_rejouer = PhotoImage(file="images/bouton_rejouer.gif")
img_win = PhotoImage(file="images/win2.gif")
img_b_win = PhotoImage(file="images/bouton_win.gif")
img_b_lancer = PhotoImage(file="images/bouton_lancer.gif")
img_b_menu = PhotoImage(file="images/bouton_menu.gif")
img_vie = PhotoImage(file="images/image_vie.gif")
img_argent = PhotoImage(file="images/image_argent.gif")

#Interface de menu
##Images
canvas.create_image(0,0,image=fond, anchor=NW)
canvas.create_image(840,438, image=titre)

##Boutons menu
bouton_jouer = Button(canvas,image=img_b_jouer,command=jeu)
bouton_jouer.place(x=168,y=600)

bouton_quitter = Button(canvas,image=img_b_quitter,command=fenetre.destroy)
bouton_quitter.place(x=924,y=600)                        

##Boutons échec/victoire
bouton_rejouer = Button(canvas,image=img_b_rejouer,command=menu)
bouton_win = Button(canvas,image=img_b_win,command=menu)

#Interface de jeu
##Étiquettes de texte
compteur_vague = Label (canvas, text="Vagues : " +str(compt_vague)+"/5",font="bold",bg="grey76")
compteur_vie = Label (canvas, text=vie_joueur, font="bold", fg="red", bg="grey76")
compteur_argent = Label (canvas, text=argent, font="bold", fg="yellow", bg="grey76")
texte_mine = Label (canvas, text="Mine d'or : 150$", font="bold",fg='black', bg="grey")
texte_tour = Label (canvas, text="Tour : 100$", font="bold",fg='black', bg="grey")


##Boutons lancer vague/retour menu
b_lancer = Button(canvas,image=img_b_lancer,command=b_lancer)      
b_menu = Button(canvas,image=img_b_menu , command=menu)

#Appel des classes
niveau = Niveau(choix)
tour = Tour(niveau,140,800)      
tour_argent = Tour_Argent(niveau,375,800)


fenetre.mainloop()

                                                                                                                                                                                                                                                        
