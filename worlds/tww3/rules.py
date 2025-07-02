from worlds.generic.Rules import set_rule, add_rule

def set_rules(self) -> None:

    set_rule(self.multiworld.get_location("World Domination", self.player),
             lambda state: state.has("Orb of Domination", self.player, self.options.domination_option.value))
    
    self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    