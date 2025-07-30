from pydantic import BaseModel, Field
from typing import List


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


class Model(BaseModel):
    """A single model"""
    model_type: str
    profile: Profile
    equipment: List[str]


class Unit(BaseModel):
    """A group of models"""
    unit_name: str
    faction: str
    unit_size: int
    models: List[Model]
    unit_rules: List[str]

# Create BaseModel instances
unit = Unit(
    unit_name="High Elf Spearmen",
    faction="High Elves",
    unit_size=2,
    models=[
        Model(
            model_type="Spearman",
            profile=Profile(M=5, WS=4, BS=4, S=3, T=3, W=1, I=5, A=1, Ld=8),
            equipment=["Spear", "Shield", "Light Armour"]
        ),
        Model(
            model_type="Spearman",
            profile=Profile(M=5, WS=4, BS=4, S=3, T=3, W=1, I=5, A=1, Ld=8),
            equipment=["Spear", "Shield", "Light Armour"]
        )
    ],
    unit_rules=["Martial Prowess", "Always Strikes First"]
)

# Convert to JSON string and save
json_string = unit.model_dump_json(indent=2)
print(json_string)

with open("unit.json", "w") as f:
    f.write(json_string)


# load from JSON string
unit2 = Unit.model_validate_json(json_string)


# Load from JSON file
with open("unit.json") as f:
    unit_data = f.read()

unit3 = Unit.model_validate_json(unit_data)


# Result
print(unit3.models[0].profile.WS)  # 4
print(unit3.unit_rules)            # ['Martial Prowess', 'Always Strikes First']
