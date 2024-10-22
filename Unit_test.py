import unittest
import Projet_Avatar

#NOTE :  

class complete_test_1 (unittest.TestCase):
    
    def setUp(self):
        self.test_warrior = Projet_Avatar.Warrior("test_warrior_name")
        self.test_warrior2 = Projet_Avatar.Warrior("test_warrior_name2")
        self.test_mage = Projet_Avatar.Mage("test_mage_name")
        self.test_rogue = Projet_Avatar.Rogue("test_rogue_name")
        self.test_npc_merchant = Projet_Avatar.NPC("Joe", "merchant")
        self.test_npc_spectator = Projet_Avatar.NPC("Bill", "spectator")
        self.test_spell = Projet_Avatar.Spell({"name":"test_spell_name", "description":"test_spell_description", "damage_range" : (1,2)})
        self.test_artefact = Projet_Avatar.Artefact("test_artefact", "test_charm", 1, Projet_Avatar.base_spell_list)


    def test_instance_warrior(self): #TODO: one for each class       
        #teste les stats
        self.assertEqual(self.test_warrior.name , "test_warrior_name", "error warrior name")
        self.assertEqual(self.test_warrior.power , 9, "error warrior power")
        self.assertEqual(self.test_warrior.health , 110 , "error warrior health")
        self.assertEqual(self.test_warrior.mana , 20, "error warrior mana")
        self.assertEqual(self.test_warrior.gold , 100, "error warrior gold")
        self.assertEqual(self.test_warrior.greet , "Argh.", "error warrior greet")
        self.assertEqual(self.test_warrior.wielded , [], "error warrior wielded")
        self.assertEqual(self.test_warrior.inventory , [], "error warrior inventory")
        
        
        #teste les méthodes de la classe warrior
        self.test_warrior.attack(self.test_warrior2)
        self.assertTrue(96 <= self.test_warrior2.health <= 99, "erreur warrior.attack() damage output" )
        self.assertEqual(self.test_warrior.salute(self.test_warrior2), 0, "erreur warrior.salute")
     
        #test méthode drink_potion héritée de la classe abstraite.
        self.test_warrior.inventory.append("potion de vie")
        self.test_warrior.health = 20
        self.test_warrior.attack(self.test_warrior2)
        self.assertEqual(self.test_warrior.health, 50, "erreur warrior drink_potion")


        #Test get_gold et set_gold :
        self.assertEqual(self.test_warrior.get_gold(), 100, "error get_gold()")
        self.assertEqual(self.test_warrior.set_gold(10), -10, "erreur set_gold() return")
        self.assertEqual(self.test_warrior.gold, 110, 'erreur set_gold calculation')
        
        #teste méthode buy hérité de la classe abstraite :
        self.test_warrior.health = 40
        self.test_warrior.buy(self.test_npc_merchant)
        self.assertIn("potion de vie", self.test_warrior.inventory, "erreur avatar.buy()")

       

    def test_instance_mage(self):
        #teste la bonne consommation de potions de vie et de mana sur le mage
        self.test_mage.health = 10
        self.test_mage.mana = 10
        self.test_mage.inventory.append("potion de vie")
        self.test_mage.inventory.append("potion de mana")
        self.test_mage.attack(self.test_warrior2)
        self.assertEqual(self.test_mage.health, 40, "erreur drink_potion class mage (health)")
        self.test_mage.attack(self.test_warrior2)
        self.assertEqual(self.test_mage.mana, 40, "erreur drink_potion class mage (mana)")

    def test_instance_rogue(self): #test l'instance du voleur
        self.assertEqual(self.test_rogue.get_gold(), 150, "erreur rogue starting gold")
        test_warrior2_gold_berfore_theft = self.test_warrior2.get_gold()
        self.test_rogue.salute(self.test_warrior2)
        self.assertEqual(self.test_warrior2.get_gold(), test_warrior2_gold_berfore_theft - 25, "erreur warrior gold thievery")
        self.assertEqual(self.test_rogue.get_gold(), 175, "erreur rogue gold thievery")
  
    def test_instance__npc(self): #teste les méthodes du npc
        #teste méthode make_merchant :
        self.assertEqual(self.test_npc_merchant.job, "merchant", "error job merchant npc")
        self.assertEqual(self.test_npc_spectator.job, "spectator", "error job spectator npc")
        self.assertFalse("potion de vie" in self.test_npc_spectator.inventory, "erreur npc.make_merchant()")
        self.assertIn("potion de vie", self.test_npc_merchant.inventory, "erreur npc.make_merchant()")
  
    def test_instance_artefact(self):
        self.test_artefact.appear(self.test_warrior)
        self.assertIn(self.test_artefact, self.test_warrior.wielded, "error artefact assignment")
        self.assertEqual(self.test_warrior.power, 10, "erreur charme artefact")
        self.assertEqual(self.test_artefact.name, "test_artefact", "error name artefact")
        self.test_artefact.add_spell()
        self.assertNotEqual(self.test_artefact.spell, [], "error spell assignment")
    
    def test_instance_spell(self):
        self.assertEqual(self.test_spell.name, "test_spell_name", "erreur spell name")
        self.assertEqual(self.test_spell.damage_range, (1, 2), "erreur spell damage range")
        self.assertEqual(self.test_spell.description, "test_spell_description", "erreur spell description")
        self.assertTrue(1 <= self.test_spell.spell_effect() <=2, "erreur spell damage output") 

if __name__ == '__main__':
    unittest.main()
