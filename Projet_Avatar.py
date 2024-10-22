from abc import ABC, abstractmethod
import random


class Avatar(ABC) : #la classe abstraite Avatar 
    def __init__(self, name:str) :
        self.name = name
        self.power = 5 
        self.health = 100
        self.mana = 20 
        self.gold = 100
        self.greet = "Salut."
        self.inventory = [] #potions dans le sac de l'avatar
        self.wielded = [] #artefact brandis par l'avatar

    @abstractmethod
    def salute(self, target):
        print(self.name, " dit : ",target.name, " ! ", self.greet)
        greet_quirk = 0 #pour le vol d'or du voleur
        return greet_quirk
    
    def drink_potion(self, potion): #boire une potion
        #checke si potion dans inventaire. Si oui, la supprime de l'inventaire et en applique les effets.
        print(self.name, " cherche une ", potion, "dans son sac") 
        if potion in self.inventory :
            self.inventory.remove(potion)
            if potion == "potion de vie" :
                print("Potion de santée bue !")
                self.health += 30
                print(f"Santée de {self.name} remontée à {self.health} PV !")
            elif potion == "potion de mana" :
                print("Potion de mana bue !")
                self.mana += 30
                print(f"Mana de {self.name} remonté à {self.mana} MP !")
            return True
        else :
            print("Pas de potion requise dans l'inventaire !")
            return False

    @abstractmethod
    def attack(self, target): 
        #Attaque via l'attaque de classe si la santée est suffisemment elevée. Sinon, boit une potion de santé.
        print("Au tour de ", self.name, " d'attaquer !")
        if self.health <= 20 and self.drink_potion("potion de vie") == True:
            return 0
        
        elif self.wielded : #checke s'il y a au moins un objet dans la liste d'artefacts possédés
            chosen_artifact = self.wielded[random.randint(0, len(self.wielded) -1)] #choisit un artefact de la liste au pif
            if chosen_artifact.spell :   
                return self.attack_artifact(chosen_artifact, target)
            else :
                return self.attack_class(target)
        else :
            return self.attack_class(target)
      
    def attack_artifact(self, selected_artifact, target) :
        print(f"{self.name} invoque le sort lié à {selected_artifact.name} !")
        damage_output = selected_artifact.use_spell()
        target.set_health(damage_output)

    @abstractmethod
    #Attaque de classe. Change pour chaque classe de héros.
    def attack_class(self, target):
        pass

    @abstractmethod
    def buy(self, target):
        #constitue un stock de potions si la vie ou le mana sont bas juste avant le début d'un combat.
        #...et si l'or possédé est suffisant. 
        merchant_stock = target.inventory
        if len(self.inventory) < 3 : #la taille de l'inventaire est limitée à 3 objets  
            #checke la santé en priorité.
            if self.health <= 75 and "potion de vie" in merchant_stock :
                if self.gold >= merchant_stock["potion de vie"] :
                    self.set_gold(-merchant_stock["potion de vie"])
                    target.set_gold(merchant_stock["potion de vie"])
                    self.inventory.append("potion de vie")
                    print (self.name, " achète une potion de vie !")
                else : #trop pauvre
                    print ( self.name, " est à court d'argent et ne peut plus acheter !")
                    return None
            else : 
                print ( self.name, "n'achète rien !")
                return None    
        else :
            print(f"Inventaire de  {self.name} plein, achats terminés !")
            return None
        self.buy(target)
   
    def get_gold(self) : #getter pour l'or
        return self.gold
    
    def set_gold(self, value): #setter pour gold
        if self.get_gold() + value <= 0 :
            transfered_gold = self.get_gold()
            self.gold = 0
            return transfered_gold 
        else :
            self.gold += value
            transfered_gold = value
            return -transfered_gold

    def set_health(self, value): #setter pour santé        
        if self.health - value <= 0 :
            self.health = 0
        else : 
            self.health -= value

class Rogue (Avatar) : #la classe Voleur
    def __init__(self, name):
        super().__init__(name)
        self.power = 1
        self.gold = 150.0 #le voleur commence avec un peu plus d'or
        self.greet= "Bonjour, que vous me semblez beau aujourd'hui !"

    def salute(self, target) :
        print(f"{self.name} dit : {target.name} !  {self.greet}")
        greet_quirk = 25 #quantité d'or que le voleur tente de voler vole à chaque salut.
        print(self.name, "lui vole discrètement des pièces d'or !")
        self.steal_gold(target, greet_quirk)
        print(f"Or de {target.name} : {target.gold}. Or de {self.name} : {self.gold}")

    def steal_gold(self, target, value): 
        self.set_gold(target.set_gold(-value))
       

    def attack(self, target):
        return super().attack(target)
    
    def attack_class(self, target):
        print("Tentative de coup dans le dos !")
        success_chance = random.randint(0, 100)
        if success_chance >= 66 :
            print("poignardage réussi !")
            damage_output = self.power * 30
            target.set_health(damage_output) 
        else :
            print("poignardage raté !")
            damage_output = self.power
            target.set_health(damage_output)
        print(f"{self.name} inflige {damage_output} dégâts!")
    
    def drink_potion(self, potion):
        return super().drink_potion(potion)
    
    def buy(self, target):
        return super().buy(target)
            
class Warrior(Avatar) :# la classe Guerrier
    def __init__(self, name) :
        super().__init__(name)
        self.health = 110 #le guerrier a un peu plus de santé
        self.power = 9 #le guerrier a un bonus de dégâts un peu plus élevé
        self.greet = "Argh."

    def attack(self,target):
        return super().attack(target)

    def attack_class(self,target):
        print("Hache dans ta face !")
        damage_bonus = random.randint(2,5)
        damage_output = self.power + damage_bonus
        target.set_health(damage_output)
        print(f"{self.name} inflige {damage_output} dégâts!")
    
    def drink_potion(self, potion):
        return super().drink_potion(potion)
    
    def salute(self, target):
        return super().salute(target)
    
    def buy(self, target):
        return super().buy(target)

class Mage(Avatar) :#la classe Mage
    def __init__(self, name) :
        super().__init__(name)
        self.power = 5
        self.health = 90 #le mage a un peu moins de santé
        self.mana = 100 #le mage a beaucoup plus de mana
        self.greet = "Hello sir."

    def attack(self, target):
        return super().attack(target)

    def attack_class(self, target):
        if self.mana >= 20 :    
            print("Boule de feu !")
            self.mana -= 15
            damage_output = random.randint(13,20) + self.power
            target.set_health(damage_output)
        else :
            print("pas assez de mana !")
            if self.drink_potion("potion de mana") == True :
                damage_output = 0
            else :
                print("Coup de bâton !")
                damage_output = self.power
                target.set_health(damage_output)
        print(f"{self.name} inflige {damage_output} dégâts!")
    
    def drink_potion(self, potion):
        return super().drink_potion(potion)
    
    def salute(self, target):
        return super().salute(target)
    
    def buy(self, target):
        merchant_stock = target.inventory
        if len(self.inventory) < 4 : #le mage peut transporter jusqu'à 4 objets parce que sa grande robe de mage a plein de poches
            
            #checke la santé en priorité.
            if self.health <= 75 and "potion de vie" in merchant_stock :
                if self.gold >= merchant_stock["potion de vie"] :
                    self.set_gold(-merchant_stock["potion de vie"])
                    target.set_gold(merchant_stock["potion de vie"])
                    self.inventory.append("potion de vie")
                    print (self.name, " achète une potion de vie !")
                else : #trop pauvre
                    print ( self.name, " est à court d'argent et ne peut plus acheter !")
                    return None
            else : 
                None    
            #si le personnage est un mage,il vérifie ensuite s'il a besoin d'une potion de mana (la potion de vie est achetée en priorité) :
            if self.mana <= 75 and "potion de mana" in merchant_stock and len(self.inventory) < 4: 
                if self.gold >= merchant_stock["potion de mana"] :
                    self.set_gold(-merchant_stock["potion de mana"])
                    target.set_gold(merchant_stock["potion de mana"])
                    self.inventory.append("potion de mana")
                    print(self.name, " achète une potion de mana !")
                else: #trop pauvre ou inventaire plein
                    print ("achats de", self.name, " terminés !")
                    return None
            if (self.health > 75 or "potion de vie" not in merchant_stock) and (self.mana > 75 or "potion de mana" not in merchant_stock) or len(self.inventory) >= 4 :
                print(f"achats de {self.name} terminés !")
                return None
        else :
            print(f"Inventaire de  {self.name} plein, achats terminés !")
            return None
        self.buy(target)

class NPC(Avatar) :#la classe NPC
    def __init__(self, name:str, job:str):
        self.name = name
        self.job = job
        self.gold = 100.0
        self.inventory = {}
        self.dialogues = ["On veut du combat !", "Des gens qui se battent pour de l'argent ? Je payerais pour voir ça !", "Quelqu'un sait où est le stand de frites ?" ]
        self.become_merchant()

    def salute(self):
        print(self.name, " dit : Bonjour, mon nom est ", self.name, " et je suis ", self.job)
        if self.job == "merchant":
            print(self.name, " dit : Voici ce que j'ai en stock :")
            for merchandise in self.inventory :
                print(merchandise)

    #remplit l'inventaire du NPC s'il est un marchand
    def become_merchant(self):
        if self.job == "merchant" :
            self.inventory["potion de vie"] = 50
            self.inventory["potion de mana"] = 50
   
    #fait un vague commentaire 
    def comment_fight(self) :
        dialogue_choice = random.randint(0,2)
        print(self.name, " dit : ", self.dialogues[dialogue_choice])
    
    def attack(self, target):
        print(f"{self.name} dit : 'Je ne peux pas me battre !'")
        self.attack_class(target)

    def attack_class(self, target):
        return 0
    
    def drink_potion(self, potion):
        print(f"{self.name} dit : 'Comment on ouvre une {potion} ?'")

    def buy(self, target):
        print(f"{self.name} dit : 'je n'achète rien !'")

class Greater_Item: #l'interface des items spéciaux dont dépend les artefacts
    def __init__(self, name:str, charm_name:str, charm_power:int, spell_list:list):
        self.name = name
        self.charm = Charm(charm_name, charm_power)
        self.spell = None
        self.spell_list = spell_list

    @abstractmethod
    def appear(self, target) :
        pass
    @abstractmethod
    def charm_effect (self, target) :
        pass
    @abstractmethod
    def add_spell(self) :
        pass
    @abstractmethod
    def use_spell(self):
        pass

class Artefact(Greater_Item):#la classe artefact, des items puissants pour les héros
    def __init__(self, name, charm_name, charm_power, spell_list):
        self.name = name
        self.charm = Charm(charm_name, charm_power)
        self.spell = None
        self.spell_list = spell_list

    def appear(self, target) :
        print(f"Les dieux favorisent {target.name} ! L'artefact {self.name} apparaît dans son inventaire !") 
        target.wielded.append(self) #NOTE : ça mettra obj#IDblabla dans son inventaire.
        self.charm_effect(target)
    
    def charm_effect (self, target) :
        print(f"Effet de cet artefact : {self.charm.name} ! {self.charm.power} dégâts ajoutés à sa puissance d'attaque!")
        target.power += self.charm.power
    
    def add_spell(self) :
        if self.spell == None :
            self.spell = Spell(self.spell_list[random.randint(1, len(self.spell_list))]) #de 0 à 2 so far
            print(f"Cette victoire permet de donner à l'artefact {self.name} sa véritable puissance ! Il peut maintenant déclencher {self.spell.name} !")
        else :
            None

    def use_spell(self):
        if self.spell :
            damage_output = self.spell.spell_effect()
            return damage_output
        else : 
            print ("Aucun pouvoir lié !")

class Charm: #la classe charm, une propriété des Artefacts accordant un bonus d'attaque aux héros
    def __init__(self, name:str, power:int):
        self.name = name
        self.power = power

class Spell : #la classe spell, qui ajoute à l'artefact un sort puissant qui remplace l'attaque de son possesseur
    def __init__(self, ID:dict):
        self.name = ID["name"] 
        self.description = ID["description"]
        self.damage_range = ID["damage_range"]

    def spell_effect(self):
        print(f"{self.name} !")
        damage_output = random.randint(self.damage_range[0], self.damage_range[1])
        print(f"{self.description} {damage_output} points de dégâts !")
        return damage_output      

def start_menu(premade_hero_roster:list, premade_npc_roster:list, an_artifact_list):#affichage de l'intro du menu
    welcome = """
    *******************************************
    * Bienvenue dans le tournoi des avatars ! *
    *******************************************
    """
    print(welcome)
    main_menu(premade_hero_roster, premade_npc_roster, an_artifact_list)

def main_menu (premade_hero_roster:list, premade_npc_roster:list, an_artifact_list):#menu principal
    intro_text = """
    Options du tournoi :
    [L]iste de participants préfaite
    [C]réer une liste de combattants personnalisée 
    [Q]uitter
    """
    try :
        
        choice = (input(intro_text)).lower()
    except :
        print("Entrez un choix correct !")
        main_menu(premade_hero_roster, premade_npc_roster, an_artifact_list) 
    
    if choice == "l" :
        tournament(premade_hero_roster, premade_npc_roster, an_artifact_list)
    elif choice == "c" :
        heroes_list = []
        NPCs_list = []
        heroes_number = characters_number(2,4,8, "héros") #choix du nombre de héros dans le tournoi 
        NPCs_number = characters_number(1,2,3, "NPCs") #choix du nombre de NPC entre les combats
        for i in range(heroes_number):
            print("Héros ", i+1, " : ")
            heroes_list.append(create_hero())
        for j in range(NPCs_number) :
            print("NPC ", j+1, " : ")
            NPCs_list.append(create_NPC())
        tournament(heroes_list, NPCs_list, an_artifact_list)
    elif choice == "t":
        print("Lancement des tests unitaires...")
    elif choice == "q" :
        print("Fin du programme...")
        exit()  
    else :
        print("Entrez un choix correct !")
        main_menu(premade_hero_roster, premade_npc_roster, an_artifact_list)

def characters_number (a:int, b:int, c:int, character_type:str) : #demande le nombre de personnages à l'utilisateur
    print(f"Nombre de {character_type} ?")
    number_of_characters = input ( f"[{a}] / [{b}] / [{c}] : ")
    try :
        number_of_characters = int(number_of_characters)
    except:
        print("Entrez une valeur correcte !")
        return characters_number(a, b, c, character_type)
    else :
        if number_of_characters != a and number_of_characters !=b and number_of_characters != c :
            print("Entrez une valeur correcte !")
            return characters_number(a,b,c, character_type)
        else :
            return number_of_characters

def create_hero():#création de héros, l'user rentre un nom et choisit une classe
    hero_name = str(input("Nom de ce héros ? "))
    if hero_name.isalpha() == False :
        print("Entrez un nom correct, séparez les noms composés par des tirets.")
        return create_hero()
    else :
        hero_class = input("Classe de ce héros ? [G]uerrier / [M]age / [V]oleur ")
        if hero_class == "G" or hero_class == "g" :
            new_hero = Warrior(hero_name)
            return new_hero
        elif hero_class == "M" or hero_class == "m" :
            new_hero = Mage(hero_name)
            return new_hero
        elif hero_class == "V" or hero_class == "v" :
            new_hero = Rogue(hero_name)
            return new_hero
        else :
            print("Valeur incorrecte, entrez à nouveau le héros !")
            return create_hero()

def create_NPC (): #création de NPC, l'user rentre un nom et choisit un job
    NPC_name = str(input("Nom de ce NPC ? "))
    if NPC_name.isalpha() == False :
        print("Entrez un nom correct, séparez les noms composés par des tirets.")
        return create_NPC()
    else :
        NPC_class = input("Classe de ce NPC ? [M]archand / [S]pectateur ")
        if NPC_class == "M" or NPC_class == "m" :
            new_NPC = NPC(NPC_name, "merchant")
            return new_NPC
        elif NPC_class == "S" or NPC_class == "s" :
            new_NPC = NPC(NPC_name, "spectator")
            return new_NPC
        else :
            print("Valeur incorrecte, entrez à nouveau les paramètres du NPC !")
            return create_NPC()

#Tournoi de x**2 participants :
def tournament(heroes:list, NPCs:list, an_artifact_list):
    fight_list = heroes
    random.shuffle(fight_list)
    list_display = """
    ******************************************************
    * Liste des combattants en vie à ce stade du tournoi *
    ******************************************************
    """
    print (list_display)
    for fighter in fight_list :
        fighter_class = type(fighter).__name__
        if fighter_class == "Rogue" :
            displayed_class = "Voleur"
        elif fighter_class == "Warrior" :
            displayed_class = "Guerrier"
        else : 
            displayed_class = "Magicien"
        print(f"{fighter.name} le {displayed_class}")

    next_stage_list = []

    if len(fight_list) >= 2:
        for i in range(0, len(fight_list), 2) :
            pre_combat(fight_list[i], fight_list[i+1], NPCs)
            next_stage_list.append(combat(fight_list[i], fight_list[i+1], an_artifact_list))   
        tournament(next_stage_list, NPCs, an_artifact_list)
    else:
        final_text = f"""
        ********************************
        * Vainqueur FINAL :  {fight_list[0].name} ! *
        ********************************
        """
        print(final_text)
    
def pre_combat(character1, character2, NPCs:list) : #avant le combat, les héros interagissent avec les npc
    intro =f"""
    
    ******************************************************************
    * {character1.name} et {character2.name} préparent leur combat ! 
    * Nos héros sont dans les stands de l'arène et parlent aux NPCs. *
    ******************************************************************

    """

    print(intro)
    for a_NPC in NPCs :
        a_NPC.salute()
        character1.salute(a_NPC)
        character2.salute(a_NPC)
        if a_NPC.job == "merchant" :
            character1.buy(a_NPC)
            character2.buy(a_NPC)
        else :
            a_NPC.comment_fight()
    return character1, character2

def combat(character1, character2, an_artifact_list) : #lance un combat entre deux avatars
    """Définit le premier à attaquer"""
    first_character_to_play = random.randint(0,1) #ca génère 1 aussi
    if first_character_to_play == 0 :
        player_1 = character1
        player_2 = character2
    else :
        player_1 = character2
        player_2 = character1
    
    """combat jusqu'à la mort"""
    intro = """

    ***********************************************************
    * Le combat va commencer ! Les combatants se font face... *
    ***********************************************************
    
    """
    print(intro)

    artifact_distributed = False #indique si un artefact a déjà été distribué au cours du combat

    player_1.salute(player_2)
    player_2.salute(player_1)
    while player_1.health > 0 and player_2.health > 0 :
        artifact_appearance_chance = random.random()
        if artifact_appearance_chance <= 0.01 and not artifact_distributed :
            artifact_distributed = artifact_distribution(an_artifact_list, player_1, player_2) 
        player_1.attack(player_2)
        print ("santé de ", player_2.name, " : ", player_2.health, "pv !")
        if player_2.health <= 0 :
            print(player_2.name, "est mort !")
            winner = player_1
            loser = player_2
            break
        player_2.attack(player_1)
        print ("santé de ", player_1.name, " : ", player_1.health, "pv !")
        if player_1.health <= 0 :
            print(player_1.name, "est mort !")
            winner = player_2
            loser = player_1
            break
    print ("Vainqueur : ", winner.name, "! Il prend les ", loser.gold, " d'or de ", loser.name, " !")
    winner.set_gold(loser.get_gold())
    loser.set_gold(loser.get_gold())
    spell_distribution(winner) #si le gagnant possède un artefact, lui distribue un spell
    return winner

def artifact_distribution(artifact_list, target1, target2): #distribue un artefact à l'une des deux cibles
    if artifact_list : #s'il reste des artefacts dans la liste de distribution
        selected_artifact = artifact_list[random.randint(0, len(artifact_list) -1)]
        distribution_pool = (target1, target2)
        sorted_winner = random.randint(0,1)
        lucky_one = distribution_pool[sorted_winner]
        selected_artifact.appear(lucky_one)
        artifact_list.remove(selected_artifact)
        return True
    else:
        return False
    
def spell_distribution(target): #distribue une capacité à un artefact possédé
    if target.wielded : #si le personnage ciblé possède au moins un artefact
        for possessed_artifact in target.wielded :
            if not possessed_artifact.spell :
                possessed_artifact.add_spell()
                return None
            else :
                None
    else :
        return None

#lance le programe normalement s'il est lancé tout seul, 
#ou en mode test s'il est lancé depuis le programme de test unitaires: 
def launcher_mode(): 
    if __name__ == "__main__": #si le programme est lancé tout seul
        start_menu(default_premade_hero_list, default_premade_NPC_list, base_artifact_list)
    else: #si le programme est lancé depuis un programme de test
        None
    
"""Héros préfaits pour la liste préfaite :"""
magus = Mage("Magus")
abracadabrus = Mage("Abracadabrus")
shazamus = Mage("Shazamus")

brutos = Warrior("Brutos")
musclos = Warrior("Musclos")
lourdos = Warrior("Lourdos")

traitrus = Rogue("Traitrus")
fourbus = Rogue("Fourbus")
perfidus = Rogue("Perfidus")

default_premade_hero_list = [traitrus, magus, brutos, fourbus, lourdos, musclos, abracadabrus, perfidus]

"""NPC préfaits: """
armand = NPC("Armand le Marchand", "merchant")
bernard = NPC("Bernard le Passant", "spectator")

default_premade_NPC_list = [armand, bernard]

"""Spells préfaits :"""
base_spell_list = {
1 : {"name" : "Brasier Infernal", "description" : "Des flammes écarlates jaillissent autour de son adversaire !", "damage_range" : (25, 25)},
2 : {"name" : "Pluie de Lames", "description" : "Des lames acérées pleuvent du ciel et s'écrasent sur son adversaire !", "damage_range" : (20, 30)},     
3 : {"name" : "Vent d'Outre-Tombe", "description" : "Des esprits d'outre-tombe sont invoqués et partent dans tous les sens !", "damage_range" : (1, 50)}
}

"""Artefacts préfaits :"""
excalibur = Artefact("Excalibur", "Bénédiction de tranchage", 5, base_spell_list)
reaper_cloak = Artefact("Manteau de la Faucheuse", "Toucher Mortel", 2, base_spell_list)
archmage_staff = Artefact("Bâton de l'Archimage", "Aura Archimagique", 3, base_spell_list)

base_artifact_list = [excalibur, reaper_cloak, archmage_staff]



"""Lancement du programme :"""

launcher_mode()

