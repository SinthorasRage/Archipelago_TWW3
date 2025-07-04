from worlds.generic.Rules import set_rule, add_rule

def set_rules(self) -> None:
    
    # sphere_amount = self.options.spheres_option.value
    # sphere_distance = self.options.sphere_distance.value
    # for location in self.multiworld.get_locations(self.player):
    #     if location.address != None:
    #         faction: str = self.sm.settlement_to_faction(location.name)
    #         distance: int = self.sm.get_distance(faction)
    #         required_spheres = int(distance/sphere_distance)
    #         if ((required_spheres != 0) and (required_spheres < sphere_amount)):
    #             set_rule(location, lambda state, spheres=required_spheres: state.has("Sphere of Influence", self.player, spheres))
    #             self.locations_to_spheres["test"] = 2
    #         elif ((required_spheres >= sphere_amount) and (self.options.sphere_world.value)):
    #             set_rule(location, lambda state, spheres=required_spheres: state.has("Sphere of Influence", self.player, spheres - 1))
    #             self.locations_to_spheres[location.name] = required_spheres
    #         elif ((required_spheres >= sphere_amount) and (not self.options.sphere_world.value)):
    #             continue

    set_rule(self.multiworld.get_location("World Domination", self.player),
             lambda state: state.has("Orb of Domination", self.player, self.options.domination_option.value))
    
    self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    