def extraire_valeur_fraction(file="game_screen"):
    with open("config/config.txt", "r") as f:
        for i in f:
            ligne = i.strip()
            ligne = ligne.replace(" ", "").split("=")
            if ligne[0] == file:
                return eval(ligne[1])

        
print(extraire_valeur_fraction("waiting_screen"))

