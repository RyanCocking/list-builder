from pydantic import BaseModel, Field
from typing import List, Dict, Tuple, Union, Optional


class Profile(BaseModel):
    M: int = Field(ge=0)
    WS: int
    BS: int
    S: int
    T: int
    W: int
    I: int
    A: int
    Ld: int
    Int: int
    Cl: int
    WP: int


class Weapon(BaseModel):
    name: str
    points: float
    description: str | None = None


class MissileWeapon(BaseModel):
    name: str
    points: float
    distance: str
    strength: str
    save_modifier: str
    description: str | None = None


class Armour(BaseModel):
    name: str
    points: float
    description: str | None = None


class MagicStandard(BaseModel):
    name: str
    points: float
    description: str | None = None


class Model(BaseModel):
    """A single model"""
    name: str
    race: str
    troop_type: str | None = None
    points: float
    weapons: List[str]  # modified by Unit
    armour: List[str]   # modified by Unit
    profile: Profile


class Unit(BaseModel):
    """A group of models"""
    name: str
    faction: str
    min_models: int
    max_models: int
    troops: Model
    options: List  # all possible options

    # set by user
    num_models: int = 0
    champion: Model | None = None

    def set_unit_size(self):
        while True:
            try:
                num = int(input("Number of models in unit: "))
            except ValueError:
                continue

            if not (self.min_models <= num <= self.max_models):
                print(f"Must be between {self.min_models} and {self.max_models}")
                continue
            else:
                self.num_models = num
                break

    def equip_troops(self):
        """Modify equipment of troops assigned to unit"""

        display = "".join([f"{op.name}\t{op.points}\t({i})\n" for i, op in enumerate(self.options)])

        while True:

            index = input(f"Select equipment:\n{display}")

            try:
                index = int(index)
                option = self.options[index]
            except ValueError:
                break
            except IndexError:
                break

            if isinstance(option, Weapon):
                self.troops.weapons = self.options[index]
            elif isinstance(option, Armour):
                self.troops.armour = self.options[index]

            print(f"Equipped {option.name}\n")


# Model defaults
clanrat = Model(
    name = "Clanrat Warrior",
    race = "Skaven",
    troop_type = None,
    points = 7.5,
    weapons = ["Hand Weapon"],
    armour = ["Light Armour", "Shield"],
    profile = Profile(M=5, WS=3, BS=3, S=3, T=3, W=1, I=4, A=1, Ld=6, Int=6, Cl=5, WP=7)
)

# Unit defaults
clanrats = Unit(
    name = "Clanrat Warriors",
    faction = "Skaven",
    min_models = 20,
    max_models = 40,
    troops = clanrat,
    options = (
        Weapon(name="Spears", points=0.5),
        Weapon(name="Double-Handed Weapons", points=1)
    )
)

# User-defined values
clanrats.set_unit_size()
clanrats.equip_troops()

# Convert to JSON string and save
json_string = clanrats.model_dump_json(indent=2)
print(json_string)

with open("unit.json", "w") as f:
    f.write(json_string)


# # load from JSON string
# unit2 = Unit.model_validate_json(json_string)


# # Load from JSON file
# with open("unit.json") as f:
#     unit_data = f.read()

# unit3 = Unit.model_validate_json(unit_data)
