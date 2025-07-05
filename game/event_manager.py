import random

class EventManager:
    def __init__(self):
        self.current_event = None
        self.event_history = []
        
        # Define various event types
        self.random_events = [
            {
                "name": "Illness",
                "description": "You feel feverish and weak.",
                "effect": lambda player, resources: player.take_damage(15),
                "can_prevent": True,
                "prevention_resource": "medicine",
                "prevention_amount": 2
            },
            {
                "name": "Injury",
                "description": "You trip and injure yourself.",
                "effect": lambda player, resources: player.take_damage(10),
                "can_prevent": True,
                "prevention_resource": "medicine",
                "prevention_amount": 1
            },
            {
                "name": "Equipment Loss",
                "description": "Some of your equipment was lost or damaged.",
                "effect": lambda player, resources: resources.consume_resource("weapons", 1),
                "can_prevent": False
            },
            {
                "name": "Food Spoilage",
                "description": "Some of your food has spoiled.",
                "effect": lambda player, resources: resources.consume_resource("food", random.randint(3, 8)),
                "can_prevent": False
            },
            {
                "name": "Water Contamination",
                "description": "Your water supply may be contaminated.",
                "effect": lambda player, resources: self.contaminated_water_effect(player, resources),
                "can_prevent": True,
                "prevention_resource": "medicine",
                "prevention_amount": 1
            }
        ]
        
        self.encounter_events = [
            {
                "name": "Traveling Merchant",
                "description": "You encounter a traveling merchant.",
                "choices": [
                    {"text": "Trade food for medicine", "cost": ("food", 10), "gain": ("medicine", 5)},
                    {"text": "Trade weapons for food", "cost": ("weapons", 2), "gain": ("food", 15)},
                    {"text": "Continue without trading", "cost": None, "gain": None}
                ]
            },
            {
                "name": "Injured Traveler",
                "description": "You find an injured traveler who needs help.",
                "choices": [
                    {"text": "Help them (use medicine)", "cost": ("medicine", 3), "gain": ("morale", 10)},
                    {"text": "Share food with them", "cost": ("food", 5), "gain": ("morale", 5)},
                    {"text": "Leave them behind", "cost": None, "gain": ("morale", -10)}
                ]
            },
            {
                "name": "Abandoned Campsite",
                "description": "You discover an abandoned campsite.",
                "choices": [
                    {"text": "Search thoroughly", "cost": ("time", 1), "gain": ("random_resource", 1)},
                    {"text": "Take what's visible", "cost": None, "gain": ("food", 3)},
                    {"text": "Avoid it (might be dangerous)", "cost": None, "gain": None}
                ]
            },
            {
                "name": "Wild Animal",
                "description": "A dangerous wild animal blocks your path.",
                "choices": [
                    {"text": "Fight with weapons", "cost": ("weapons", 1), "gain": ("food", 8)},
                    {"text": "Try to scare it away", "cost": None, "gain": None},
                    {"text": "Take a longer route", "cost": ("fuel", 3), "gain": None}
                ]
            },
            {
                "name": "Severe Weather",
                "description": "A severe storm is approaching.",
                "choices": [
                    {"text": "Wait it out (use fuel for warmth)", "cost": ("fuel", 5), "gain": None},
                    {"text": "Push through the storm", "cost": ("health", 20), "gain": None},
                    {"text": "Find shelter", "cost": ("time", 2), "gain": None}
                ]
            }
        ]
    
    def trigger_random_event(self, player, resource_manager):
        """Trigger a random negative event"""
        if self.current_event:
            return  # Already handling an event
        
        event = random.choice(self.random_events)
        self.current_event = event
        
        # Check if event can be prevented
        if event.get("can_prevent", False):
            prevention_resource = event.get("prevention_resource")
            prevention_amount = event.get("prevention_amount", 1)
            
            if resource_manager.consume_resource(prevention_resource, prevention_amount):
                # Event prevented
                self.event_history.append({
                    "name": event["name"],
                    "description": f"{event['description']} (Prevented with {prevention_resource})",
                    "prevented": True
                })
                self.current_event = None
                return
        
        # Apply event effect
        event["effect"](player, resource_manager)
        
        # Record event
        self.event_history.append({
            "name": event["name"],
            "description": event["description"],
            "prevented": False
        })
        
        self.current_event = None
    
    def trigger_daily_event(self, player, resource_manager):
        """Trigger a daily event that might be positive or negative"""
        if random.random() < 0.3:  # 30% chance of daily event
            if random.random() < 0.6:  # 60% chance of encounter (potentially positive)
                self.trigger_encounter_event(player, resource_manager)
            else:  # 40% chance of random negative event
                self.trigger_random_event(player, resource_manager)
    
    def trigger_encounter_event(self, player, resource_manager):
        """Trigger an encounter event that requires player choice"""
        encounter = random.choice(self.encounter_events)
        # For now, automatically make a random choice
        # Later this can be expanded to present choices to the player
        self.auto_resolve_encounter(encounter, player, resource_manager)
    
    def auto_resolve_encounter(self, encounter, player, resource_manager):
        """Automatically resolve an encounter (can be made interactive later)"""
        # Choose a random option
        choice = random.choice(encounter["choices"])
        
        # Apply cost
        if choice["cost"]:
            cost_type, cost_amount = choice["cost"]
            if cost_type == "health":
                player.take_damage(cost_amount)
            elif cost_type == "time":
                pass  # Time cost handled elsewhere
            else:
                resource_manager.consume_resource(cost_type, cost_amount)
        
        # Apply gain
        if choice["gain"]:
            gain_type, gain_amount = choice["gain"]
            if gain_type == "health":
                player.heal(gain_amount)
            elif gain_type == "morale":
                player.morale += gain_amount
            elif gain_type == "random_resource":
                random_resource = random.choice(["food", "water", "medicine", "weapons"])
                resource_manager.add_resource(random_resource, random.randint(1, 5))
            else:
                resource_manager.add_resource(gain_type, gain_amount)
        
        # Record the event
        self.event_history.append({
            "name": encounter["name"],
            "description": f"{encounter['description']} - {choice['text']}",
            "prevented": False
        })
    
    def contaminated_water_effect(self, player, resource_manager):
        """Special effect for contaminated water"""
        # Lose some water
        resource_manager.consume_resource("water", random.randint(5, 10))
        # Take damage
        player.take_damage(random.randint(8, 15))
        # Chance of getting sick
        if random.random() < 0.3:
            player.sick = True
    
    def get_recent_events(self, count=5):
        """Get the most recent events"""
        return self.event_history[-count:] if len(self.event_history) >= count else self.event_history
    
    def clear_history(self):
        """Clear event history"""
        self.event_history = []