import random

class ResourceManager:
    def __init__(self):
        # Starting resources
        self.food = 50
        self.water = 40
        self.medicine = 10
        self.weapons = 5
        self.fuel = 20
        
        # Maximum resources
        self.max_food = 100
        self.max_water = 100
        self.max_medicine = 50
        self.max_weapons = 20
        self.max_fuel = 100
        
        # Daily consumption rates
        self.food_consumption = 3
        self.water_consumption = 5
        self.fuel_consumption = 2
        
        # Resource history for tracking
        self.resource_history = []
        
    def update(self):
        # Record current state
        self.resource_history.append({
            "food": self.food,
            "water": self.water,
            "medicine": self.medicine,
            "weapons": self.weapons,
            "fuel": self.fuel
        })
        
        # Keep only last 7 days of history
        if len(self.resource_history) > 7:
            self.resource_history.pop(0)
    
    def consume_daily_resources(self):
        """Called once per day to consume resources"""
        self.food -= self.food_consumption
        self.water -= self.water_consumption
        self.fuel -= self.fuel_consumption
        
        # Prevent negative values
        self.food = max(0, self.food)
        self.water = max(0, self.water)
        self.fuel = max(0, self.fuel)
    
    def add_resource(self, resource_type, amount):
        """Add resources with maximum limits"""
        if resource_type == "food":
            self.food = min(self.max_food, self.food + amount)
        elif resource_type == "water":
            self.water = min(self.max_water, self.water + amount)
        elif resource_type == "medicine":
            self.medicine = min(self.max_medicine, self.medicine + amount)
        elif resource_type == "weapons":
            self.weapons = min(self.max_weapons, self.weapons + amount)
        elif resource_type == "fuel":
            self.fuel = min(self.max_fuel, self.fuel + amount)
    
    def consume_resource(self, resource_type, amount):
        """Consume a specific resource and return if successful"""
        if resource_type == "food" and self.food >= amount:
            self.food -= amount
            return True
        elif resource_type == "water" and self.water >= amount:
            self.water -= amount
            return True
        elif resource_type == "medicine" and self.medicine >= amount:
            self.medicine -= amount
            return True
        elif resource_type == "weapons" and self.weapons >= amount:
            self.weapons -= amount
            return True
        elif resource_type == "fuel" and self.fuel >= amount:
            self.fuel -= amount
            return True
        return False
    
    def get_resource_status(self):
        """Return a dict of resource statuses"""
        return {
            "food": {
                "current": self.food,
                "max": self.max_food,
                "status": self.get_resource_level_status(self.food, self.max_food)
            },
            "water": {
                "current": self.water,
                "max": self.max_water,
                "status": self.get_resource_level_status(self.water, self.max_water)
            },
            "medicine": {
                "current": self.medicine,
                "max": self.max_medicine,
                "status": self.get_resource_level_status(self.medicine, self.max_medicine)
            },
            "weapons": {
                "current": self.weapons,
                "max": self.max_weapons,
                "status": self.get_resource_level_status(self.weapons, self.max_weapons)
            },
            "fuel": {
                "current": self.fuel,
                "max": self.max_fuel,
                "status": self.get_resource_level_status(self.fuel, self.max_fuel)
            }
        }
    
    def get_resource_level_status(self, current, maximum):
        """Return status string based on resource level"""
        percentage = current / maximum if maximum > 0 else 0
        
        if percentage > 0.7:
            return "Good"
        elif percentage > 0.4:
            return "Moderate"
        elif percentage > 0.2:
            return "Low"
        elif percentage > 0:
            return "Critical"
        else:
            return "Empty"
    
    def get_critical_resources(self):
        """Return list of critically low resources"""
        critical = []
        status = self.get_resource_status()
        
        for resource, data in status.items():
            if data["status"] in ["Critical", "Empty"]:
                critical.append(resource)
        
        return critical
    
    def can_survive_days(self, days):
        """Calculate if current resources can sustain for given days"""
        food_days = self.food / self.food_consumption if self.food_consumption > 0 else float('inf')
        water_days = self.water / self.water_consumption if self.water_consumption > 0 else float('inf')
        fuel_days = self.fuel / self.fuel_consumption if self.fuel_consumption > 0 else float('inf')
        
        min_days = min(food_days, water_days, fuel_days)
        return min_days >= days
    
    def reset(self):
        """Reset to starting resources"""
        self.food = 50
        self.water = 40
        self.medicine = 10
        self.weapons = 5
        self.fuel = 20
        self.resource_history = []
    
    def find_resources(self, terrain_type):
        """Find resources based on terrain type"""
        resources_found = {}
        
        if terrain_type == "water":
            # Can refill water
            water_found = random.randint(5, 15)
            resources_found["water"] = water_found
        
        elif terrain_type == "grass":
            # Can find food (berries, small game)
            if random.random() < 0.3:  # 30% chance
                food_found = random.randint(2, 8)
                resources_found["food"] = food_found
        
        elif terrain_type == "mountain":
            # Can find medicine (herbs) or weapons (materials)
            if random.random() < 0.2:  # 20% chance
                if random.random() < 0.5:
                    medicine_found = random.randint(1, 3)
                    resources_found["medicine"] = medicine_found
                else:
                    weapons_found = random.randint(1, 2)
                    resources_found["weapons"] = weapons_found
        
        return resources_found