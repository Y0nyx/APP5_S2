###
###  Gabarit pour l'application de traitement des frequences de mots dans les oeuvres d'auteurs divers
###  Le traitement des arguments a ete inclus:
###     Tous les arguments requis sont presents et accessibles dans args
###     Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments
###
###  Frederic Mailhot, 26 fevrier 2018
###    Revise 16 avril 2018
###    Revise 7 janvier 2020

###  Parametres utilises, leur fonction et code a generer
###
###  -d   Deja traite dans le gabarit:  la variable rep_auth contiendra le chemin complet vers le repertoire d'auteurs
###       La liste d'auteurs est extraite de ce repertoire, et est comprise dans la variable authors
###
###  -P   Si utilise, indique au systeme d'utiliser la ponctuation.  Ce qui est considÃ©re comme un signe de ponctuation
###       est defini dans la liste PONC
###       Si -P EST utilise, cela indique qu'on dÃ©sire conserver la ponctuation (chaque signe est alors considere
###       comme un mot.  Par defaut, la ponctuation devrait etre retiree
###
###  -m   mode d'analyse:  -m 1 indique de faire les calculs avec des unigrammes, -m 2 avec des bigrammes.
###
###  -a   Auteur (unique a traiter).  Utile en combinaison avec -g, -G, pour la generation d'un texte aleatoire
###       avec les caracteristiques de l'auteur indique
###
###  -G   Indique qu'on veut generer un texte (voir -a ci-haut), le nombre de mots Ã  generer doit Ãªtre indique
###
###  -g   Indique qu'on veut generer un texte (voir -a ci-haut), le nom du fichier en sortie est indique
###
###  -F   Indique qu'on desire connaitre le rang d'un certain mot pour un certain auteur.  L'auteur doit etre
###       donnÃ© avec le parametre -a, et un mot doit suivre -F:   par exemple:   -a Verne -F Cyrus
###
###  -v   Deja traite dans le gabarit:  mode "verbose",  va imprimer les valeurs donnÃ©es en parametre
###
###
###  Le systeme doit toujours traiter l'ensemble des oeuvres de l'ensemble des auteurs.  Selon la presence et la valeur
###  des autres parametres, le systeme produira differentes sorties:
###
###  avec -a, -g, -G:  generation d'un texte aleatoire avec les caracteristiques de l'auteur identifie
###  avec -a, -F:  imprimer la frequence d'un mot d'un certain auteur.  Format de sortie:  "auteur:  mot  frequence"
###                la frequence doit Ãªtre un nombre reel entre 0 et 1, qui represente la probabilite de ce mot
###                pour cet auteur
###  avec -f:  indiquer l'auteur le plus probable du texte identifie par le nom de fichier qui suit -f
###            Format de sortie:  "nom du fichier: auteur"
###  avec ou sans -P:  indique que les calculs doivent etre faits avec ou sans ponctuation
###  avec -v:  mode verbose, imprimera l'ensemble des valeurs des paramÃ¨tres (fait deja partie du gabarit)
#-f TextesPourEtudiants -m 2 -v

import math
import argparse
import glob
import sys
import os
from pathlib import Path
from random import randint
from random import choice
import random
from pythonds3 import Vertex
from pythonds3.graphs import Graph

### Ajouter ici les signes de ponctuation Ã  retirer
PONC = ["!", '"', "'", ")", "(", ",", ".", ";", ":", "?", "-", "_"]

###  Vous devriez inclure vos classes et mÃ©thodes ici, qui seront appellÃ©es Ã  partir du main
class Author:
    def __init__(self, name):
        self.name = name
        self.textes = dict()
        self.frequence = dict()
        self.mFrequence = dict()

    def addTexte(self,texte):
        if texte not in self.textes:
            self.textes[texte] = dict()
        return texte

    def frequences(self):
        nbWord = 0
        self.frequence = dict()
        self.mFrequence = dict()
        for texte in self.textes.values():
            for wr in texte:
                nbWord += texte[wr]
                if wr in self.frequence:
                    self.frequence[wr] += texte[wr]
                else:
                    self.frequence[wr] = texte[wr]
### Calcul de la frequence
        for word in self.frequence:
            self.mFrequence[word] = self.frequence[word]/nbWord

def lectureFichier(nomFichier,author,texte, n):
    txt = open(nomFichier, encoding='utf-8').read()
    words = enleverPonc(txt.lower()).split()
    if n == 1:
        loopRange = len(words)
    else:
        loopRange = len(words) - (n-1)
    for x in range(loopRange):
        wr = words[x]
### enlever les determinants non representatif de la trace de l'auteur
        if len(wr) <= 2:
            pass
        else:
            if not n == 1:
### Creer un string de n gramme
                for y in range(1, n):
                    wr += " "
                    wr += words[x+y]
            wr_lo = wr.lower()
### met le n gramme dans le dictionnaire
            if wr_lo in author.textes[texte]:
                author.textes[texte][wr_lo] += 1
            else:
                author.textes[texte][wr_lo] = 1

def textToDictFreq(pathTextInconnu, n=1):
    txt = open(pathTextInconnu, encoding='utf-8').read()
    words = enleverPonc(txt.lower()).split()
    nbWord = 0
    wordsTextDict = dict()
    if n == 1:
        loopRange = len(words)
    else:
        loopRange = len(words) - (n-1)
    for x in range(loopRange):
        wr = words[x]
        if len(wr) <= 2:
            pass
        else:
            if not n == 1:
                for y in range(1,n):
                    wr += " "
                    wr += words[x + y]
            nbWord += 1
            wr_lo = wr.lower()
            if wr_lo in wordsTextDict:
                wordsTextDict[wr_lo] += 1
            else:
                wordsTextDict[wr_lo] = 1
    for word in wordsTextDict:
        wordsTextDict[word] = wordsTextDict[word] / nbWord

    return wordsTextDict

def textCompare(textToCompareDictFreq, author):
    coll = 0
    nbMot = 0
    for word in textToCompareDictFreq.keys():
        if word in author.mFrequence:
### comparer la frequence
            if textToCompareDictFreq[word]/author.mFrequence[word] > 0.75:
                coll += 1 * author.mFrequence[word]
                nbMot += 1 * author.mFrequence[word]
            else:
                nbMot += 1 * author.mFrequence[word]
    print('==========================================')
    print("Auteur: " + author.name + ", ressemblance: ","%.2f%%" % (coll/nbMot*100))
    return coll/nbMot

def buildMarkovDict(nomAuteur, rep_aut):
    authorDir = rep_aut + "\\" + nomAuteur
    textes = os.listdir(authorDir)
    dim1Dict = dict()
    dim2Dict = dict()
    # loop pour tous les textes de l'auteur
    for d in textes:
        textFile = authorDir + "\\" + d
        txt = open(textFile, encoding='utf-8').read()
        words = enleverPonc(txt.lower()).split()
        for x in range(len(words)-1):
            wr_current = words[x]
            wr_next = words[x+1]
            if wr_current in dim2Dict:
                dim1Dict[wr_current] += 1
                if wr_next in dim2Dict[wr_current]:
                    dim2Dict[wr_current][wr_next] += 1
                else:
                    dim2Dict[wr_current][wr_next] = 1
            else:
                dim1Dict[wr_current] = 1
                dim2Dict[wr_current] = {wr_next:1}
    return (dim1Dict,dim2Dict)

def buildPhrase(markovDict, length):
    dim1Dict = markovDict[0]
    dim2Dict = markovDict[1]
    mylist = list(dim1Dict.keys())
    myweights = list(dim1Dict.values())
    words = list()
    word = random.choices(mylist, weights=myweights, k=1)[0]
    for x in range(length - 1):
        word = dim2Dict[word]
        mylist = list(word.keys())
        myweights = list(word.values())
        word = random.choices(mylist, weights=myweights, k=1)[0]
        words.append(word)
    for word in words:
        print(word, end=" ")

def enleverPonc(word):
    for c in PONC:
        word = word.replace(c, " ")
    return word

def buildAuthorInfo(authors,rep_aut,n):
    authorsInfo = dict()
    for a in authors:
        authorsInfo[a] = Author(a)
        authorDir = rep_aut + "\\" + a
        textes = os.listdir(authorDir)
        # loop pour tous les textes de l'auteur
        for d in textes:
            textFile = authorDir + "\\" + d
            authorsInfo[a].addTexte(d)
            # buildGraph(textFile,args.m)
            lectureFichier(textFile, authorsInfo[a],d,n)
        authorsInfo[a].frequences()
    return authorsInfo

def auteurEtudier(auteur,fichier,n,F,rep_aut):
    objetAuteur = Author(auteur)
    authorDir = rep_aut + "\\" + auteur
    textes = os.listdir(authorDir)
    for d in textes:
        texteFile = authorDir + "\\" + d
        objetAuteur.addTexte(d)
        lectureFichier(texteFile, objetAuteur, d, n)
    objetAuteur.frequences()
    texteFreq = textToDictFreq(fichier,n)

    textCompare(texteFreq,objetAuteur)
    if F:
        meilleurFreq = dict()
        Fword = findFword(objetAuteur,F,meilleurFreq)
        print(F,"e mot le plus frequent :",Fword[0])

def ComparaisonAuteur(fichier,n,F,auteursInfo):
    texteFreq = textToDictFreq(fichier, n)
    for auteur in auteursInfo:
        textCompare(texteFreq, auteursInfo[auteur])
        if F:
            meilleurFreq = dict()
            Fword = findFword(auteursInfo[auteur], F, meilleurFreq)
            print(F, "e mot le plus frequent :", Fword[0])
    return 0

def findFword(objetAuteur,F,meilleurFreqDict,meilleurFreq=None):
    if F == 0:
        return meilleurFreq
    if None != meilleurFreq and meilleurFreq[0] in meilleurFreqDict:
        meilleurFreq = None
    for freq in objetAuteur.mFrequence:
        if meilleurFreq == None or objetAuteur.mFrequence[freq] > meilleurFreq[1]:
            if freq not in meilleurFreqDict:
                meilleurFreq = (freq,objetAuteur.mFrequence[freq])
    F -= 1
    meilleurFreqDict[meilleurFreq[0]] = meilleurFreq[1]
    return findFword(objetAuteur,F, meilleurFreqDict,meilleurFreq)

### Main: lecture des paramÃ¨tres et appel des mÃ©thodes appropriÃ©es
###
###       argparse permet de lire les paramÃ¨tres sur la ligne de commande
###             Certains paramÃ¨tres sont obligatoires ("required=True")
###             Ces paramÃ¨tres doivent Ãªtres fournis Ã  python lorsque l'application est exÃ©cutÃ©e
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='markov_cip1_cip2.py')
    parser.add_argument('-d', required=True, help='Repertoire contenant les sous-repertoires des auteurs')
    parser.add_argument('-a', help='Auteur a traiter')
    parser.add_argument('-f', help='Fichier inconnu a comparer')
    parser.add_argument('-m', required=True, type=int,
                        help='Mode (1 ou 2) - unigrammes ou digrammes')
    parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer')
    parser.add_argument('-G', type=int, help='Taille du texte a generer')
    parser.add_argument('-g', help='Nom de base du fichier de texte a generer')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    parser.add_argument('-P', action='store_true', help='Retirer la ponctuation')
    parser.add_argument('-A',action='store_true', help='Verifie touts les auteurs')
    args = parser.parse_args()

    ### Lecture du rÃ©pertoire des auteurs, obtenir la liste des auteurs
    ### Note:  args.d est obligatoire
    ### auteurs devrait comprendre la liste des rÃ©pertoires d'auteurs, peu importe le systÃ¨me d'exploitation
    cwd = os.getcwd()
    if os.path.isabs(args.d):
        rep_aut = args.d
    else:
        rep_aut = os.path.join(cwd, args.d)

    rep_aut = os.path.normpath(rep_aut)
    authors = os.listdir(rep_aut)

    ### Enlever les signes de ponctuation (ou non) - DÃ©finis dans la liste PONC
    if args.P:
        remove_ponc = True
    else:
        remove_ponc = False

    ### Si mode verbose, reflÃ©ter les valeurs des paramÃ¨tres passÃ©s sur la ligne de commande
    if args.v:
        print("Mode verbose:")
        print("Calcul avec les auteurs du repertoire: " + args.d)
        if args.f:
            print("Fichier inconnu a,"
                  " etudier: " + args.f)

        print("Calcul avec des " + str(args.m) + "-grammes")
        if args.F:
            print(str(args.F) + "e mot (ou digramme) le plus frequent sera calcule")

        if args.a:
            print("Auteur etudie: " + args.a)

        if args.P:
            print("Retirer les signes de ponctuation suivants: {0}".format(" ".join(str(i) for i in PONC)))

        if args.G:
            print("Generation d'un texte de " + str(args.G) + " mots")

        if args.g:
            print("Nom de base du fichier de texte genere: " + args.g)

        print("Repertoire des auteurs: " + rep_aut)
        print("Liste des auteurs: ")
        for a in authors:
            aut = a.split("/")
            print("    " + aut[-1])

### Ã€ partir d'ici, vous devriez inclure les appels Ã  votre code

    if args.a:
        auteurEtudier(args.a, args.f,args.m,args.F,rep_aut)
    if args.A:
        auteursInfo = buildAuthorInfo(authors,rep_aut,args.m)
        ComparaisonAuteur(args.f,args.m,args.F,auteursInfo)

    if args.G:
        print("markov chain")
        if args.a:
            markovDictAuteur = buildMarkovDict(args.a, rep_aut)
            print(f"Text selon l'auteur {args.a}:")
            buildPhrase(markovDictAuteur, args.G)
        elif args.A:
            for a in authors:
                markovDictAuteur = buildMarkovDict(a, rep_aut)
                print(f"{a} :: Début :", end="")
                buildPhrase(markovDictAuteur, args.G)
                print(f" :: Fin")


    print("done")
