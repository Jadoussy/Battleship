'''
Module principal. Permet de lancer l’application : LE jeu de la BATAILLE NAVALE
Version 1.0 du 14/11/26

Codé et testé sur l'IDE Spyder par Jadoussy
'''
import time # pour les time.sleep() -> console moins brutale

# Déclaration des constantes (variable qui ne change pas)
N_ROWS = 10
N_COLS = 10

# Symbole indiquant statut de la case et sont utilisés dans la grille personnelle
EMPTY_SYMBOL = '.'
SHIP_SYMBOL = 'N'
HIT_SYMBOL = 'X'
MISS_SYMBOL = 'O'


def create_grid() -> list[list[str]]:
    """ 
    Permet de générer et retourner une grille de 10 lignes et 10 colonnes, initialisée avec le symbole '.'
    """
    grid = []
    for i in range(10) :  # lignes
        line = []
        for j in range(10) :   # colones
            line.append(EMPTY_SYMBOL)
        grid.append(line)
    return grid


def create_grid_short() -> list[list[str]]:
    """ VERSION COURTE
    Permet de générer et retourner une grille de 10 lignes et 10 colonnes, initialisée avec le symbole '.'
    """
    return [[EMPTY_SYMBOL for j in range(10)]
            for i in range(10)]


def display_grid(grid: list[list[str]]) -> None:
    """
    Permet d'afficher le contenu de la grille : le numéro des lignes et colones et les symboles des cases.
    Ne s'exécute pas et indique si une erreur de typage ou définition de la grille est présente.
    """
    # CAS D'ERREUR : 
    if grid is None:
        print("ERREUR : Grille non initialisée")
    
    elif type(grid) != list :
        print(f'ERREUR : Type de la grille pas respecté : {type(grid)} ≠ list')
        
    else :
        for i, row in enumerate(grid):
            
            # Affiche des n° des lignes
            num_row = i + 1
            
            if num_row == 10 :
                print('',num_row, end=' | ')
            else : 
                print(' ',num_row, end=' | ')
                
            # Affichage des cases (symbole)
            for case in row:
                print(case, end=' ')
            print()

        # Affichage des n° de colonnes
        print('      ', end='')
        for j in range(10):
            print(j+1, end=' ')
        
        print("\n")
    
    
# "Logique" de placement pour (ligne,col) : 
# Horizontal, ajout à droite de l'emplacement indiqué par l'utilisateur | H : x -> 
# Vertical, ajout en bas de l'emplacement indiqué par l'utilisateur     | V : vers bas 
def is_valid_placement(grid: list[list[str]],
                       row: int,
                       col: int,
                       size: int, # orientation H ou V
                       orientation: str) -> bool:
    """
    Vérifie si un navire peut être placé à partir de la position indiquée.
    Renvoie True si le placement est valide, sinon False.
    """
    # ORIENTATION : l'orientation n'est ni "H" ou "V"
    if orientation not in ("H","V") :
        return False
    
    # HORS PERIMETRE : col ou row en dehors de 10 et en dessous de 1
    if not (1 <= row <= 10 and 1 <= col <= 10) :
        return False
    
    # Adaptation de -1 pour éviter décalage : passer les indices de 0 à 9
    r = row -1
    c = col -1
    
    # Pour l'horizontal
    if orientation == "H" :
        # LIMITES GRILLE : Si dépassement de la grille (vers la droite)
        if c + size > len(grid[0]) :
            return False
        
        # CASES LIBRES : si pas de symbole '.'
        for i in range(size):
            if grid[r][c+i] != EMPTY_SYMBOL :
                return False
            
    # Pour vertical
    if orientation == "V" :
        # LIMITES GRILLE : Si dépassement de la grille (en bas)
        if r + size > len(grid[0]) :
            return False
        
        # CASES LIBRES : si pas de symbole '.'
        for i in range(size):
            if grid[r+i][c] != EMPTY_SYMBOL :
                return False
        
    # Placement valide
    return True


def place_ship(grid: list[list[str]],
               row: int,
               col: int,
               size: int,
               orientation: str) -> bool:
    """ 
    Positionne un navire (symbole N) sur la grille. 
    Retourne True si le navire a été placé (placement valide), sinon False.
    Fonction appelée : is_valid_placement
    """
    # Si le placement est valide
    if is_valid_placement(grid, row, col, size, orientation):

        if orientation =="H" :
            for i in range(size) : 
                # -1 pour éviter le décalage 0 -> 10 alors que 1 à 10
                grid[row-1][col+i-1] = SHIP_SYMBOL
                
        if orientation =="V" :
            for i in range(size) :
                grid[row+i-1][col-1] = SHIP_SYMBOL
        return True
    
    # Sinon (le placement est invalide) donc le navire n'a pas été placé
    else : 
        return False


def place_fleet(grid: list[list[str]]) -> None:
    """
    Demande à l'utilisateur de rentrer les coordonnées de chaque nav afin de tous les positionner.
    Appel de la fonction place_ship()
    [!] Appel de la fonction display_grid() si l'utilisateur rentre "show grid" ou "hint" ou "my".
    """
    
    # Constantes
    SHIP_NAME_LIST = ("Porte-avions","Croiseur","Contre-torpilleur","Sous-marin","Torpilleur")
    SHIP_SIZE_LIST = (5,4,3,3,2)
    
    # Déclaration de la variable du compteur de navires placés
    placed_ships = 0
    
    # Tant que les 5 navires ne sont pas placés :
    while placed_ships != 5 : 
        print(f'\n[{placed_ships+1}/5] Placement du {SHIP_NAME_LIST[placed_ships]} ({SHIP_SIZE_LIST[placed_ships]})')
        
        input_row = input("   N° de ligne : ")      
        # ERREURS DE SAISIE : mauvais type ou hors périmètre
        while input_row not in(10,9,8,7,6,5,4,3,2,1) : # Tant qu'on a pas une valeur valide :
            # Cas où python récupère l'int sous forme de string
            if input_row in('10','9','8','7','6','5','4','3','2','1') : 
                input_row = int(input_row) # Convertit le type en int
                break
            
            # Mots clé pour l'aide : afficher la grille de l'utilisateur
            if input_row in ("my","hint","show grid") :
                display_grid(grid)
                input_row = input("   N° de ligne : ")  
                pass   # on repart au début d'un tour de boucle
            
            # Toujours pas valide :
            else :    
                input_row = input("   Incorrect, réessayez : ")
        
        # COLONNE
        input_col = input("   N° de colonne : ")
        while input_col not in(10,9,8,7,6,5,4,3,2,1) : 

            if input_col in('10','9','8','7','6','5','4','3','2','1') : 
                input_col = int(input_col)
                break
            
            # Mots clé pour l'aide : afficher la grille de l'utilisateur
            if input_col in ("my","hint","show grid") :
                display_grid(grid)
                input_col = input("   N° de colonne : ")
                pass # Jump direct à un nouveau tour de boucle
            
            # Toujours pas valide :
            else : 
                input_col = input("   Incorrect, réessayez : ")

        
        input_o = input("   Orientation (H ou V) : ")
        # ERREURS DE SAISIE : hors "h" et "v"
        while input_o not in("H","V") : # Tant qu'on a pas une valeur valide :
            input_o = input("   Incorrect, réessayez : ")
            
            # Mots clé pour l'aide : afficher la grille de l'utilisateur
            if input_o in ("my","hint","show grid") :
                display_grid(grid)
                input_o = input("   Orientation (H ou V) : ")
                pass
        
        
        if place_ship(grid,input_row,input_col,SHIP_SIZE_LIST[placed_ships],input_o) :
            print(f"[OK] Navire placé en ({input_row},{input_col})")
            placed_ships += 1   # +1 navire placé
        
        # Si données rentrées invalides, on n'actualise pas le compteur des navires placés
        else :
            print("Erreur de saisie ou case non libre/valide, merci de réessayer...")


def is_valid_shot(grid: list[list[str]],
                  row: int,
                  col: int) -> bool:
    """
    Renvoie True si un tir est possible, sinon False.
    Conditions de validité d'un tir :
        - Coordonnées comprises dans les limites de la grille
        - La case n'a pas déjà été touchée ou visée
    """
    # CAS où coordonnées hors du périmètre de la grille (10x10)
    if not (1 <= row <= 10 and 1 <= col <= 10) :
        return False
    
    # CAS où la case a déjà été touché ou visée
    elif grid[row-1][col-1] == HIT_SYMBOL or grid[row-1][col-1] == MISS_SYMBOL:
        return False
    
    # Sinon c'est VALIDE
    else :
        return True
    
    
def shoot(grid: list[list[str]],
          row: int,
          col: int) -> str:
    """
    Réalise un tir sur la grille adverse. 
    Retourne le symbole lié à l'action du tir.
    Appel de la fonction is_valid_shot afin de vérifier la validité du tir.
    """
    # Vérification : si le tir n'est pas valide, aucune modif
    if not is_valid_shot(grid, row, col) :
        return "" # rien
    
    # La casé visée est celle d'un navire(N) -> cette case devient X (tir réussi)
    elif grid[row-1][col-1] == SHIP_SYMBOL :
        return HIT_SYMBOL
    
    # La casé visée est vide(.) -> cette case devient 0 (tir raté)
    elif grid[row-1][col-1] == EMPTY_SYMBOL :
        return MISS_SYMBOL
    
    
def is_ship_sunk(grid: list[list[str]]) -> bool:
    """
    Renvoi True si au moins un navire présent sur la grille a été entièrement détruit, False sinon.
    """
    # Déclaration de la constante : taille des navires
    SHIP_SIZE_LIST = (5,4,3,3,2)
    
    # Pour les lignes
    for r in range(10):
        x_next = 0 # Compteur de symbole touché consécutif (x)
        for c in range(10):
            if grid[r][c] == HIT_SYMBOL: # Si un symbole X est trouvé +1 au compteur
                x_next += 1
            else :
                if x_next in SHIP_SIZE_LIST : # Compare le nombre de X consécutifs au tailles de nav
                    return True
                x_next = 0 # On a trouvé un navire coulé, remise à 0 du compteur
        # Vérification fin de ligne
        if x_next in SHIP_SIZE_LIST :
            return True
    
    # Idem pour les colonnes   
    for c in range(10):
        x_next = 0
        for r in range(10):
            if grid[r][c] == HIT_SYMBOL:
                x_next += 1
            else :
                if x_next in SHIP_SIZE_LIST :
                    return True
                x_next = 0
            
        if x_next in SHIP_SIZE_LIST :
            return True
        
    # Sinon, aucun navire coulé
    return False

def is_fleet_destroyed(grid: list[list[str]]) -> bool:
    """
    Retourne True si la flotte de la grille est entièrement détruite, False sinon.
    """
    N_counter = 0   # Nombre de navire restant
    P_counter = 0   # Nombre de case vide (.)
    
    # Parcourt la grille
    for r in range(10):
        for c in range(10):
            
            # Compteur de navire
            if grid[r][c] == ("N") :
                N_counter += 1
                
            # Compteur de case vide
            elif grid[r][c] == (".") :
                P_counter += 1

    # CAS D'ERREUR où la grille serait vide (= 100 cases de '.')
    if P_counter >= 100 :
        pass
        
    # Si pas de navire trouvé -> return False
    elif N_counter == 0 :
        return True
        
    # Si un navire est trouvé (= N_counter pas à 0) -> return False
    else :
        return False
    

def play_game() -> None:
    """
    Assure le déroulement complet de la partie.
    Et affiche le joueur gagnant.
    
    Déroulement de la partie :
    1. Initialiser des grilles des 2 joueurs.
    2. Permettre à chaque joueur de positionner sa flotte
    3. Organiser alternativement les tours de jeu
    4. Demander au joueur courant les coordonnées de son tir.
    5. Vérifier la validité du tir.
    6. Exécuter le tir sur la grille adverse.
    7. Afficher le résultat du tir.
    8. Signaler lorsqu'un navire est coulé.
    9. Vérifier si la flotte adverse est entièrement détruite.
    10. Passer au joueur suivant si la partie continue.
    
    MECANISMES
    Veiller à ce que le joueur adverse ne puisse pas consulter autre grille
    -> print("\033[H\033[J", end="")
    -> clear la console, comme un clear dans le cmd par exemple
    
    FIN : le programme annoncer le joueur gagnant.
    """

    print("====================")
    print("   BATAILLE NAVALE  ")
    print("====================\n") 
    
    time.sleep(1)
    
    ##### 1. Initialisation des grilles des Joueurs
    print("1. [O.K] Création des grilles des 2 Joueurs \n")
    GRID_J1 = create_grid_short()
    GRID_J2 = create_grid_short()    
    
    time.sleep(1)
    
    ##### 2. Permet à chaque joueur de positionner sa flotte
    print("2. Les joueurs vont définir leur flotte :")
    
    # Déclaration des variables
    PLAYERS_GRID = [GRID_J1,GRID_J2]  # Utilisé pour parcourir les 2 J afin d'éviter lignes supp
    """ Info TEST : Début commentaire pour sauter la partie placement des flottes """
    i = 0   # index du numéro de joueur : 0 = J1 et 1 = J2
    
    # Tant qu'on a pas fait les 2 joueurs
    while i < 2 :
        print("\n#### Joueur",i+1,"####")
        
        time.sleep(1)
        
        place_fleet(PLAYERS_GRID[i])
        display_grid(PLAYERS_GRID[i]) # affichage final après définition de la flotte par le J
            
        # Demande de confirmation avant de valider la config de la grille du joueur
        ask_player_to_confirm = str(input("Tu es sur de la configuration ? n pour recommencer (y/n)"))
        
        # Si le J ne rentre pas N ou n alors on passe au joueur suivant :
        if ask_player_to_confirm.lower() != 'n' :
            i +=1         
            
        print("\033[H\033[J", end="")  # clear du terminal
    """ Info TEST : Fin du commentaire pour skip cette partie """
    
    
    time.sleep(1)
    
    
    """ Début TEST ZONE : complétion manuellement pour gagner temps^
    #J1
    place_ship(GRID_J1,1,1,5,"V")
    place_ship(GRID_J1,2,2,4,"V")
    place_ship(GRID_J1,3,3,3,"V")
    place_ship(GRID_J1,4,4,3,"V")
    place_ship(GRID_J1,5,5,2,"V")
    
    #J2
    place_ship(GRID_J2,1,1,5,"V")
    place_ship(GRID_J2,2,2,4,"V")
    place_ship(GRID_J2,3,3,3,"V")
    place_ship(GRID_J2,4,4,3,"V")
    place_ship(GRID_J2,5,5,2,"V")
    
    #J2 - test flotte vaincu du joueur 2
    GRID_J2[1][1] = "X"
    
    #print("J1")
    #display_grid(GRID_J1)
    
    #print("\n J2")
    #display_grid(GRID_J2)
    
    #Fin TEST ZONE 
    """ 
    
    ##### 3. Organiser alternativement les tours de jeu
    # Définition des variables
    t = 0       # numéro de tour. Tour paire = J1, tour impair = J2
    index_p = 1 # index des joueurs : J1 = 1 et J2 = 2
    
    ##### 9. Vérifier si la flotte adverse est entièrement détruite
    # Tant qu'aucune des 2 flottes n'est détruite
    while not (is_fleet_destroyed(GRID_J1) or is_fleet_destroyed(GRID_J2) ) :
        print(f"Tour n°{t+1} ===> Joueur {index_p} <===")
        
        # Determine la grille énemie
        if index_p == 1:
            target_grid = GRID_J2
        else : 
            target_grid = GRID_J1
        
        # Affichage de la grille du joueur actuel
        display_grid(PLAYERS_GRID[index_p-1])
        
        print(f"t{t+1}-[J{index_p}] Moment du TIR -----")
       
        #### 4. Demander au joueur courant les coordonnées de son tir.
        # Préparation du tir : INPUTS ligne et col
        input_shoot_r = input("   N° de ligne : ")  
        
        #### 5. Vérifier la validité du tir
        # Tant que l'entrée n'est pas entre 1 et 10 (1 et 10 inclus)
        while input_shoot_r not in(10,9,8,7,6,5,4,3,2,1) :
               
            # Si python enregistre la valeur sous forme (type) de string
            if input_shoot_r in('10','9','8','7','6','5','4','3','2','1') : 
               input_shoot_r = int(input_shoot_r) # Convertit le type en int
               break # jump au début de la boucle
           
            # Toujours pas valide :
            else :    
               input_shoot_r = input("   Incorrect, réessayez : ")
           
        input_shoot_c = input("   N° de colonne : ")
        while input_shoot_c not in(10,9,8,7,6,5,4,3,2,1) :
            
            if input_shoot_c in ('10','9','8','7','6','5','4','3','2','1') : 
               input_shoot_c = int(input_shoot_c) # Convertit le type en int
               break # jump au début de la boucle
                
            else :    
               input_shoot_c = input("   Incorrect, réessayez : ")
                
        
        # Récupère le résultat du tir dans la var res_short
        res_shot = shoot(target_grid, input_shoot_r, input_shoot_c)
        #### 6. Exécuter le tir sur la grille adverse : applique le résultat du tir
        target_grid[input_shoot_r-1][input_shoot_c-1] = res_shot
        
        
        #### 7. Afficher le résultat du tir au Joueur
        if res_shot == HIT_SYMBOL :
            print(f"Navire Touché en ({input_shoot_r},{input_shoot_c})")
        else :
            print(f"Raté, aucun navire présent en ({input_shoot_r},{input_shoot_c})")
        
        #### 8. Signaler lorsqu'un navire est coulé.
        if is_ship_sunk(target_grid) :
            print("[!] Navire coulé ")
            time.sleep(1)
        
        
        #### 10. Passer au joueur suivant si la partie continue
        # Gestion de l'alternance des joueurs et le tir sur la grille adverse
        if index_p == 1 :         
            index_p = 2 # J1, passe l'index au J2s
        else :   
            index_p = 1 # J2, passe l'index au J1
                
            
        # Fin du tour : compteur de tour + 1 et gestion alternance
        t += 1
        time.sleep(1)
        print("\033[H\033[J", end="")
    
    
    # Sortie de la boucle : une des 2 flottes est détruite 
    # Détermine laquelle et annonce le gagnant
    if is_fleet_destroyed(GRID_J1) :
        print(f"\nBravo, le joueur 2 a gagné en {t} tours")
    else : 
        print(f"\nBravo, le joueur 1 a gagné en {t} tours")


if __name__ == '__main__' :  
    #pass # Pour éviter l'erreur expected an indented block after 'if' statement on line 502
    
    """ Tests des CREATE_GRID et DISPLAY_GRID """
    

if __name__ == '__main__' :
    
    """ Tests de DISPLAY_GRID """
    GRID_J1 = create_grid_short()
    #display_grid(GRID_J1)
    
    #GRID_Jx = None
    #GRID_Jstr = "test" 
    
    #display_grid(GRID_Jx)
    #display_grid(GRID_Jstr)
    
    
    """ Tests de IS_VALIDE_PLACEMENT """
    #print(f'TEST pour CAS valide : {is_valid_placement(GRID_J1, 1,1,2, "H")}')
    #print(f'TEST pour CAS hors grille : {is_valid_placement(GRID_J1, 9,9,4, "V")}')
    
    
    """ Tests de PLACE_SHIP """
    #print(f'Pour (1,1) t2 VRAI -> placement: {place_ship(GRID_J1, 1,1,2, "H")}')
    #print(f'Pour (5,5) t5 VRAI -> placement: {place_ship(GRID_J1, 5,5,5, "V")}')
    #print(f'Pour (5,3) t3 FAUX -> placement: {place_ship(GRID_J1, 5,3,3, "H")}')
    

    """ Tests de PLACE_FLEET """
    #place_fleet(GRID_J1)
    #display_grid(GRID_J1)
    
    """ Tests de IS_VALID_SHOT """
    #GRID_J1[0][0] = MISS_SYMBOL 
    #GRID_J1[1][1] = HIT_SYMBOL
    
    #display_grid(GRID_J1)
    
    #print(f'(1,1) Tir valide? (O) : {is_valid_shot(GRID_J1,1,1)}') 
    #print(f'(2,2) Tir valide? (X) : {is_valid_shot(GRID_J1,2,2)}') 
    #print(f'(3,3) Tir valide? (oui) : {is_valid_shot(GRID_J1,3,3)}') 
    #print(f'(11,11) Tir valide? (hors perim) : {is_valid_shot(GRID_J1,11,11)}')  
    
    
    """ Tests de SHOT """
    #GRID_J1[1][1], GRID_J1[2][3] = SHIP_SYMBOL, SHIP_SYMBOL
    #display_grid(GRID_J1)
    
    #print(f'(2,2) Touché : {shoot(GRID_J1, 2, 2)}') 
    #print(f'(3,3) Raté : {shoot(GRID_J1, 3, 3)}') 
    #print(f'(11,11) En dehors grille : {shoot(GRID_J1, 11, 11)}') 
    
    
    """ Tests de IS_SHIP_SUNK """
    #GRID_J1[1][1], GRID_J1[1][2] = SHIP_SYMBOL, SHIP_SYMBOL
    #print("Coulé ? (non : N,N) :", is_ship_sunk(GRID_J1))
    
    #GRID_J1[1][1] = HIT_SYMBOL
    #print("Coulé ? (non : X,N) :", is_ship_sunk(GRID_J1))
    
    #GRID_J1[1][2] = HIT_SYMBOL
    #print("Coulé ? (oui : X,X): ", is_ship_sunk(GRID_J1))
    
    
    """ Tests de IS_FLEET_DESTROYED """
    #print("Flotte détruite ? (Grille VIDE) :",is_fleet_destroyed(GRID_J1))
    
    #GRID_J1[0][0] = SHIP_SYMBOL
    #print("Flotte détruite ? (N en 1,1) :",is_fleet_destroyed(GRID_J1))
    
    #GRID_J1[0][0] = HIT_SYMBOL
    #print("Flotte détruite ? (H en 1,1) :",is_fleet_destroyed(GRID_J1))
    
    
    """ Test de PLAY_GAME """
    play_game()     # + de lignes de test commentées (désactivées) sont présentes dans la fonction
    
    