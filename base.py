from pydantic import BaseModel, Field
from typing import List, Dict, Union, Literal
from copy import deepcopy


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


class Equipment(BaseModel):
    name: str
    points: float
    category: Literal["weapon", "armour"]
    description: str | None = None

    def get_equipment_dict(self):
        return {self.name: self}


class MissileWeapon(Equipment):
    distance: str
    strength: str
    save_modifier: str


EquipmentDict = Dict[str, Equipment]


def equipment_from_data(filename) -> EquipmentDict | None:
    """Generate Equipment objects from input data"""

    # TODO
    # e.g. a .csv containing ALL skaven equipment
    # instantiate many Equipment objects and place into a dict
    # later on, we can get equipment objects using only the name
    # validation test: all keys are identical to the corresponding Equipment.name
    return None


class Model(BaseModel):
    """A single model"""

    name: str
    race: str
    points: float
    equipment: EquipmentDict  # modified by Unit
    profile: Profile

    def set_equipment(self, equipment_name: str, equipment: Equipment):
        self.equipment[equipment_name] = equipment

    def get_equipment(self):
        return self.equipment


class Unit(BaseModel):
    """A group of models"""

    name: str
    faction: str
    min_models: int
    max_models: int
    troops: Model
    troop_type: str | None = None  # elite, levy, etc.
    options: EquipmentDict  # all possible options

    # set by user
    num_models: int = 0
    champion: Model | None = None

    def set_unit_size(self, size: int):
        if not (self.min_models <= size <= self.max_models):
            print(f"Must be between {self.min_models} and {self.max_models}")
        self.num_models = size

    def _equipment_in_options(self, equipment_name: str):
        if equipment_name in self.options.keys():
            return True
        return False

    def equip_troops(self, equipment_name: str):
        if not self._equipment_in_options(equipment_name):
            raise ValueError(
                f"Equipment '{equipment_name}' not in options for unit '{self.name}'"
            )
        self.troops.set_equipment(equipment_name, self.options[equipment_name])

    def unequip_troops(self, equipment_name: str):
        if not self._equipment_in_options(equipment_name):
            raise ValueError(
                f"Equipment '{equipment_name}' not in options for unit '{self.name}'"
            )
        self.troops.get_equipment().pop(equipment_name)


# TODO this data will eventually be read from tabular data, i.e. equipment_from_data(foobar)
# TODO how to handle equipment costs factored into the base points of the model itself?
# TODO should this be a tuple? don't want master equipment to be mutable. would also
#      prevent liberal usage of deepcopy() when instantiating units
all_equipment = {
    "Hand Weapon": Equipment(name="Hand Weapon", points=0, category="weapon"),
    "Spear": Equipment(name="Spear", points=0.5, category="weapon"),
    "Double-handed Weapon": Equipment(name="Double-handed Weapon", points=1, category="weapon"),
    "Shield": Equipment(name="Shield", points=0.5, category="armour"),
    "Light Armour": Equipment(name="Shield", points=0.5, category="armour"),
}


def select_from_all_equipment(
    selection: Union[str, List[str]], global_equipment: EquipmentDict = all_equipment
) -> EquipmentDict:
    """Get a selection from the global equipment"""
    return {k: deepcopy(all_equipment[k]) for k in selection}


# Model defaults
clanrat = Model(
    name="Clanrat Warrior",
    race="Skaven",
    points=7.5,
    equipment=select_from_all_equipment(["Hand Weapon", "Shield", "Light Armour"]),
    profile=Profile(M=5, WS=3, BS=3, S=3, T=3, W=1, I=4, A=1, Ld=6, Int=6, Cl=5, WP=7),
)

# Unit defaults
clanrats = Unit(
    name="Clanrat Warriors",
    faction="Skaven",
    min_models=20,
    max_models=40,
    troops=clanrat,
    troop_type=None,
    options=select_from_all_equipment(["Spear", "Double-handed Weapon"]),
)

# User-defined values
clanrats.set_unit_size(36)
clanrats.equip_troops("Spear")

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
