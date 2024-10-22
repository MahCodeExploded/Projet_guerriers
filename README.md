# Projet_guerriers

Fonctionnement du programme :

- Il s'agit d'un tournoi d'avatars. 
- Il prend une liste d'avatars de différentes classes (Voleur, Mage et Guerrier), la randomise et les fait s'affronter chacun à leur tour en un contre un jusqu'à ce qu'il n'en reste qu'un seul en vie.
- L'utilisateur peut utiliser une liste préfaite ou créer chacun des avatars composant ladite liste.
- Chaque round est précédé d'une scène où les deux avatars qui vont combattre peuvent parler à des PNJs présents dans l'arène et leur acheter des potions avec leur or si ces derniers sont des marchands.
- Les combats sont au tour par tour : chaque avatar attaque l'autre à tour de rôle. Le combat prend fin lorsque l'un des deux n'a plus de points de vie  (il meurt). Le gagnant prend l'or du perdant.

Spécificités :

- Si un avatar a ses points de vie trop bas, il peut tenter de boire une potion (s'il n'en a pas sur lui, il attaque à la place). Pareil avec les points de magie("mana") si le personnage est un mage.
- A chaque round, il y a une chance de 1% pour que les dieux accordent un artefact (une arme très puissante) à l'un des avatars. Cet avatar conservera l'arme jusqu'à sa mort ou à sa victoire dans le dernier combat du programme.
- Si un avatar détenteur d'artefact remporte son premier combat, l'artefact gagne un "spell", une capacité spéciale très puissante qui est alors utilisée à la place de l'attaque de l'avatar.

Spécificités de classes :

- Un voleur vole de l'or à l'avatar ou au PNJ qu'il salue.
- Un voleur a une  attaque très faible, mais il a 33% de chance de voir son attaque devenir un coup critique qui fait 3000% de dégâts.
- Un mage consomme du mana en attaquant à coups de boules de feu. S'il n'a plus de mana et qu'il est à court de potions de mana, il attaquera en donnant un coup de bâton (moins puissant mais ne consomme pas de mana)
- Un PNJ peut soit être un marchand qui propose de vendre des potions lors de ses interactions avec les avatars, soit être un spectateurs qui se contente de discuter avec eux.

Points de la consigne accomplis :

► Chaque avatar a les attributs :
- nom ("name")
- puissance ("power")
- vie ("health")
- magie ("mana")
- gold ("gold")
- (d'autres attributs non-demandés dans la consigne sont présents)

► Chaque avatar peut (entre autres choses):
- saluer via la méthode salute() (la classe voleur vole de l'or en même temps)
- attaquer via la méthode attack()
- boire une potion via la méthode drink_potion()

► Relations :
- Classe abstraite : la classe Avatar
- Interface : la classe Greater_Item dont hérite la classe Artefact
- Association : la méthode attack prend un autre avatar en argument
- Composition : chaque instance de la classe Artefact a un objet de classe Charm qui la compose
- Agrégation : chaque instance de la classe Artefact peut potentiellement se voir agréger un objet de la classe Spell

NOTE : 
- Les tests unitaires se démarrent en lançant le fichier "unit_test.py"
- Le programme en lui-même (sans les tests) se démarre en lançant le fichier "projet_avatar.py"
