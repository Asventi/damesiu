def moves(plateau, joueur):
    liste_coup =[]
    for ligne in range(10):
        for colonne in range(10):
            if (ligne+colonne) % 2 == 1 and plateau[ligne][colonne] == joueur:
                #remplacer la notation du joueur et mettre une nouvelle notation pour la reine
                #deplacement pion
                if joueur == "O" or plateau[ligne][colonne] == "R":
                    #pour déplacer vers de haut gauche puis droite
                    if ligne > 0 and colonne > 0 and plateau[ligne - 1][colonne - 1] == " ":
                        try :
                            liste_coup.append(((ligne, colonne), (ligne -1, colonne -1)))
                        except :
                            liste_coup.append(((ligne, colonne), (ligne -2, colonne -2)))
                    if ligne > 0 and colonne < 9 and plateau[ligne - 1][colonne + 1] == " ":
                        try :
                            liste_coup.append(((ligne, colonne), (ligne - 1, colonne + 1)))
                        except :
                            liste_coup.append(((ligne, colonne), (ligne -2, colonne + 2)))
                #remplacer la notation pour la reine
                #deplacement reine
                if plateau[ligne][colonne] == "R":
                    if ligne < 9 and colonne > 0 and plateau[ligne - 1][colonne - 1] ==" ":
                        liste_coup.append(((ligne, colonne), (ligne -1, colonne -1)))
                    if ligne < 9 and colonne < 9 and plateau[ligne + 1][colonne + 1] == " ":
                        liste_coup.append(((ligne, colonne), (ligne + 1, colonne + 1)))
    return liste_coup