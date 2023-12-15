import pygame
import random
from typing import List
from time import sleep

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)

class Morpion:
    def __init__(self):
        """
        Initialise une nouvelle partie de Morpion.

        Initialise la grille de jeu en tant que matrice 3x3 et définit le gagnant à 0 (pas de gagnant).
        """
        self.grille = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.gagnant = 0

    def verifier_gagnant(self) -> int:
        """
        Vérifie s'il y a un gagnant dans la partie de Morpion.

        Retourne :
            int: Le gagnant (1 pour le joueur, -1 pour le bot, 0 pour aucun gagnant).
        """
        self.gagnant = (
            self.verifier_lignes()
            or self.verifier_colonnes()
            or self.verifier_diagonales()
            or self.verifier_egalite()
        )
        return self.gagnant

    def verifier_lignes(self) -> int:
        """
        Vérifie s'il y a un gagnant dans les lignes de la grille de jeu.

        Retourne :
            int: Le gagnant dans les lignes (1 pour le joueur, -1 pour le bot, 0 pour aucun gagnant).
        """
        for ligne in self.grille:
            if all(valeur == ligne[0] and valeur != 0 for valeur in ligne):
                return ligne[0]
        return 0

    def verifier_colonnes(self) -> int:
        """
        Vérifie s'il y a un gagnant dans les colonnes de la grille de jeu.

        Retourne :
            int: Le gagnant dans les colonnes (1 pour le joueur, -1 pour le bot, 0 pour aucun gagnant).
        """
        for col in range(3):
            if all(
                ligne[col] == self.grille[0][col] and ligne[col] != 0 for ligne in self.grille
            ):
                return self.grille[0][col]
        return 0

    def verifier_diagonales(self) -> int:
        """
        Vérifie s'il y a un gagnant dans les diagonales de la grille de jeu.

        Retourne :
            int: Le gagnant dans les diagonales (1 pour le joueur, -1 pour le bot, 0 pour aucun gagnant).
        """
        if all(
            self.grille[i][i] == self.grille[0][0] and self.grille[i][i] != 0
            for i in range(3)
        ):
            return self.grille[0][0]
        if all(
            self.grille[i][2 - i] == self.grille[0][2] and self.grille[i][2 - i] != 0
            for i in range(3)
        ):
            return self.grille[0][2]
        return 0

    def verifier_egalite(self) -> int:
        """
        Vérifie si la partie s'est terminée par une égalité.

        Retourne :
            int: 200 si la partie est une égalité, 0 sinon.
        """
        return 200 if all(cellule != 0 for ligne in self.grille for cellule in ligne) else 0

    def coup_joueur(self, i: int, j: int) -> bool:
        """
        Effectue le coup d'un joueur dans la partie.

        Args:
            i (int): Indice de la ligne.
            j (int): Indice de la colonne.

        Retourne :
            bool: Vrai si le coup est valide, Faux sinon.
        """
        if self.grille[i][j] == 0:
            self.grille[i][j] = 1
            return True
        return False

    def coup_bot(self) -> bool:
        """
        Effectue le coup d'un bot dans la partie.

        Retourne :
            bool: Vrai si le coup est valide, Faux sinon.
        """
        coords_valides = [
            (i, j) for i in range(3) for j in range(3) if self.grille[i][j] == 0
        ]
        if coords_valides:
            coord = random.choice(coords_valides)
            self.grille[coord[0]][coord[1]] = -1
            return True
        return False

class InterfaceUtilisateur:
    def __init__(self, grille: List[List[int]], largeur: int, hauteur: int):
        """
        Initialise l'InterfaceUtilisateur pour le jeu de Morpion.

        Args:
            grille (List[List[int]]): La grille de jeu.
            largeur (int): Largeur de la fenêtre de jeu.
            hauteur (int): Hauteur de la fenêtre de jeu.
        """
        self.grille = grille
        self.largeur = largeur
        self.hauteur = hauteur

        pygame.init()
        self.police = pygame.font.SysFont("Segoe UI", 35, True)
        self.fenetre = pygame.display.set_mode((self.largeur, self.hauteur))

    def dessiner_jeu(self):
        """Dessine l'état actuel du jeu de Morpion sur l'écran."""
        self.dessiner_grille()
        for i in range(len(self.grille)):
            for j in range(len(self.grille[0])):
                if self.grille[i][j] == 1:
                    self.dessiner_croix(i, j)
                elif self.grille[i][j] == -1:
                    self.dessiner_cercle(i, j)

    def dessiner_grille(self):
        """Dessine la grille de jeu sur l'écran."""
        epaisseur_ligne = 2

        lignes = pygame.Rect(
            self.largeur // 3,
            -epaisseur_ligne,
            self.largeur // 3,
            self.hauteur + epaisseur_ligne * 2,
        )

        colonnes = pygame.Rect(
            -epaisseur_ligne,
            self.hauteur // 3,
            self.largeur + epaisseur_ligne * 2,
            self.hauteur // 3,
        )

        pygame.draw.rect(self.fenetre, BLANC, lignes, epaisseur_ligne)
        pygame.draw.rect(self.fenetre, BLANC, colonnes, epaisseur_ligne)

    def dessiner_croix(self, i: int, j: int):
        """
        Dessine un symbole 'X' (croix) dans la cellule de grille spécifiée.

        Args:
            i (int): Indice de la ligne.
            j (int): Indice de la colonne.
        """
        coord_ligne_1 = [
            [
                j * self.largeur // 3 + self.largeur // 9, # x1
                i * self.hauteur // 3 + self.hauteur // 9 # y1
            ],
            [
                j * self.largeur // 3 + 2 * self.largeur // 9, # x2
                i * self.hauteur // 3 + 2 * self.hauteur // 9 # y2
            ]
        ]
        coord_ligne_2 = [
            [
                j * self.largeur // 3 + 2 * self.largeur // 9, # x1
                i * self.hauteur // 3 + self.hauteur // 9 # y1
            ],
            [
                j * self.largeur // 3 + self.largeur // 9, # x2
                i * self.hauteur // 3 + 2 * self.hauteur // 9 # y2
            ]
        ]
        pygame.draw.line(self.fenetre, ROUGE, coord_ligne_1[0], coord_ligne_1[1], 10)
        pygame.draw.line(self.fenetre, ROUGE, coord_ligne_2[0], coord_ligne_2[1], 10)

    def dessiner_cercle(self, i: int, j: int):
        """
        Dessine un symbole 'O' (cercle) dans la cellule de grille spécifiée.

        Args:
            i (int): Indice de la ligne.
            j (int): Indice de la colonne.
        """
        rayon = max(self.largeur // 15, self.hauteur // 15)
        pygame.draw.circle(
            self.fenetre, BLEU, (j * self.largeur // 3 + self.largeur // 6, i * self.hauteur // 3 + self.hauteur // 6), rayon, 10
        )

    def afficher_message_victoire(self, gagnant: int):
        """
        Affiche un message de victoire ou d'égalité sur l'écran.

        Args:
            gagnant (int): Le gagnant (1 pour le joueur, -1 pour le bot, 0 pour une égalité).
        """
        if gagnant == 1:
            message_victoire = self.police.render("VOUS AVEZ GAGNÉ", False, VERT)
        elif gagnant == -1:
            message_victoire = self.police.render("VOUS AVEZ PERDU", False, ROUGE)
        else:
            message_victoire = self.police.render("ÉGALITÉ", False, BLANC)

        rect_texte = message_victoire.get_rect(center=(self.largeur / 2, self.hauteur / 2))
        self.fenetre.fill(NOIR, rect_texte)
        self.fenetre.blit(message_victoire, rect_texte)

class GestionnaireJeu:
    def __init__(self, largeur: int, hauteur: int):
        """
        Initialise le ControleurJeu pour le jeu de Morpion.

        Args:
            largeur (int): Largeur de la fenêtre de jeu.
            hauteur (int): Hauteur de la fenêtre de jeu.
        """
        self.jeu = Morpion()
        self.largeur = largeur
        self.hauteur = hauteur
        self.ui = InterfaceUtilisateur(self.jeu.grille, self.largeur, self.hauteur)
        self.enCours = True

    def executer(self):
        """Démarre et exécute la boucle de jeu du Morpion."""
        while self.enCours:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    self.enCours = False
                elif evenement.type == pygame.MOUSEBUTTONDOWN:
                    self.gerer_clic_souris(evenement)

            self.jeu.verifier_gagnant()
            self.mettre_a_jour_iu()
            pygame.display.update()

    def gerer_clic_souris(self, evenement: pygame.event.Event):
        """
        Gère les clics de souris pendant le jeu.

        Args:
            evenement (pygame.event.Event): Événement de clic de souris.
        """
        x, y = evenement.pos
        i, j = y // (self.hauteur // 3), x // (self.largeur // 3)

        if self.jeu.coup_joueur(i, j):
            self.jeu.coup_bot()

    def mettre_a_jour_iu(self):
        """Met à jour l'interface utilisateur du jeu."""
        self.ui.fenetre.fill((0, 0, 0))
        self.ui.dessiner_jeu()
        gagnant = self.jeu.verifier_gagnant()
        if gagnant:
            self.ui.afficher_message_victoire(gagnant)
            pygame.display.update()
            sleep(2)
            self.enCours = False

if __name__ == "__main__":
    controleur = GestionnaireJeu(largeur=600, hauteur=600)
    controleur.executer()
