#! /usr/bin/env python3

import csv
import re
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Dict, Sequence


@dataclass
class Pro:
    """A professionist."""

    id: int
    first_name: str
    last_name: str
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zip: str
    phone_1: str
    phone_2: str
    email: str
    web: str

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def full_address(self) -> str:
        return f"{self.address_line_1}\n{self.address_line_2}\n{self.zip}, {self.city}, {self.state}"


@dataclass
class HomeTemplate:
    """Home page template."""

    states: Sequence[str]

    def states_out(self) -> str:
        return "\n".join(
            f'<li><a href="{slug(state)}/">{state}</a></li>' for state in self.states
        )


@dataclass
class StateTemplate:
    """State page template."""

    state: str
    cities: Sequence[str]

    def state_out(self) -> str:
        return self.state

    def cities_out(self) -> str:
        return "\n".join(
            f'<li><a href="{slug(city)}/">{city}</a></li>' for city in self.cities
        )


@dataclass
class CityTemplate:
    """City page template."""

    city: str
    pros: Sequence[Pro]

    def city_out(self) -> str:
        return self.city

    def pros_out(self) -> str:
        return "\n".join(
            f'<li><a href="{slug(pro.full_name())}.html">{pro.full_name()}</a></li>'
            for pro in self.pros
        )


@dataclass
class ProTemplate:
    """Pro page template."""

    full_name: str
    full_address: str

    def full_name_out(self) -> str:
        return self.full_name

    def full_address_out(self) -> str:
        return self.full_address


def compile_template(template: str, klass, obj) -> str:
    with open(template, "r") as t:
        template_content = t.read()

    field_types = {field.name: field.type for field in fields(klass)}
    for (name, _) in field_types.items():
        template_content = re.sub(
            f"{{{{\s*{name}\s*}}}}",
            str(getattr(obj, f"{name}_out")()),
            template_content,
        )

    return template_content


def slug(input: str) -> str:
    return re.sub("\s", "-", input).lower()


states: Dict[str, Dict[str, Sequence[Pro]]] = {}


with open("data.csv", newline="") as data:
    data_reader = csv.DictReader(data)

    for row in data_reader:
        cities = states.get(row["state"], {})
        states[row["state"]] = cities
        pros: Sequence[Pro] = cities.get(row["city"], [])
        cities[row["city"]] = pros
        pros.append(Pro(**row))

dist = Path("dist")
dist.mkdir(parents=True, exist_ok=True)

print(f"Building home")
home_file = dist.joinpath("index.html")
with home_file.open("w") as f:
    f.write(
        compile_template(
            "templates/home.html", HomeTemplate, HomeTemplate(list(states.keys()))
        )
    )
print(f" - {home_file}")

for (state, cities) in states.items():
    print(f"Building state: {state}")
    state_dir = dist.joinpath(slug(state))
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file = state_dir.joinpath("index.html")
    with state_file.open("w") as f:
        f.write(
            compile_template(
                "templates/state.html",
                StateTemplate,
                StateTemplate(state, list(cities.keys())),
            )
        )
    print(f" - {state_file}")

    for (city, pros) in cities.items():
        print(f"Building city: {city}")
        city_dir = state_dir.joinpath(slug(city))
        city_dir.mkdir(parents=True, exist_ok=True)
        city_file = city_dir.joinpath("index.html")
        with city_file.open("w") as f:
            f.write(
                compile_template(
                    "templates/city.html",
                    CityTemplate,
                    CityTemplate(city, pros),
                )
            )
        print(f" - {city_file}")

        for pro in pros:
            print(f"Building pro: {pro.full_name()}")
            pro_file = city_dir.joinpath(f"{slug(pro.full_name())}.html")
            with pro_file.open("w") as f:
                f.write(
                    compile_template(
                        "templates/pro.html",
                        ProTemplate,
                        ProTemplate(pro.full_name(), pro.full_address()),
                    )
                )
            print(f" - {pro_file}")
