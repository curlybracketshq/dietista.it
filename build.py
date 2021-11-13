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


class BaseTemplate:
    TITLE = "Dietista.it - I migliori dietisti in Italia"
    DESCRIPTION = "La lista dei migliori dietisti italiani"

    HEADER = """
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="utf-8" />
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="stylesheet" type="text/css" href="style.css" />
</head>
"""

    PAGE = """
<!DOCTYPE html>
<html lang="it">

{header}

<body>
    {content}
</body>

</html>
"""

    def render(
        self, content: str, title: str = TITLE, description: str = DESCRIPTION
    ) -> str:
        header = self.HEADER.format(title=title, description=description)
        return self.PAGE.format(header=header, content=content)


@dataclass
class HomeTemplate(BaseTemplate):
    """Home page template."""

    states: Sequence[str]

    CONTENT = """
<h1>Dietista.it - I migliori dietisti in Italia</h1>
<h2>La lista dei migliori dietisti italiani</h2>

<ul>
    {states}
</ul>
"""

    def render(self) -> str:
        content = self.CONTENT.format(states=self._states_items())
        return super().render(content=content)

    def _states_items(self) -> str:
        return "\n".join(
            f'<li><a href="{slug(state)}/">{state}</a></li>' for state in self.states
        )


@dataclass
class StateTemplate(BaseTemplate):
    """State page template."""

    state: str
    cities: Sequence[str]

    CONTENT = """
<h1>Dietista.it - I migliori dietisti in Italia</h1>
<h2>I migliori dietisti nella provincia di {state}</h2>

<ul>
    {cities}
</ul>
"""

    def render(self) -> str:
        content = self.CONTENT.format(state=self.state, cities=self._cities_items())
        return super().render(content=content)

    def _cities_items(self) -> str:
        return "\n".join(
            f'<li><a href="{slug(city)}/">{city}</a></li>' for city in self.cities
        )


@dataclass
class CityTemplate(BaseTemplate):
    """City page template."""

    city: str
    pros: Sequence[Pro]

    CONTENT = """
<h1>Dietista.it - I migliori dietisti in Italia</h1>
<h2>I migliori dietisti nella città di {city}</h2>

<ul>
    {pros}
</ul>
"""

    def render(self) -> str:
        content = self.CONTENT.format(city=self.city, pros=self._pros_items())
        return super().render(content=content)

    def _pros_items(self) -> str:
        return "\n".join(
            f'<li><a href="{slug(pro.full_name())}.html">{pro.full_name()}</a></li>'
            for pro in self.pros
        )


@dataclass
class ProTemplate(BaseTemplate):
    """Pro page template."""

    pro: Pro

    CONTENT = """
<h1>Dietista.it - I migliori dietisti in Italia</h1>
<h2>{full_name}</h2>

<p>{full_address}</p>
"""

    def render(self) -> str:
        content = self.CONTENT.format(
            full_name=self.pro.full_name(), full_address=self.pro.full_address()
        )
        return super().render(content=content)


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
    template = HomeTemplate(list(states.keys()))
    f.write(template.render())
print(f" - {home_file}")

for (state, cities) in states.items():
    print(f"Building state: {state}")
    state_dir = dist.joinpath(slug(state))
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file = state_dir.joinpath("index.html")
    with state_file.open("w") as f:
        template = StateTemplate(state, list(cities.keys()))
        f.write(template.render())
    print(f" - {state_file}")

    for (city, pros) in cities.items():
        print(f"Building city: {city}")
        city_dir = state_dir.joinpath(slug(city))
        city_dir.mkdir(parents=True, exist_ok=True)
        city_file = city_dir.joinpath("index.html")
        with city_file.open("w") as f:
            template = CityTemplate(city, pros)
            f.write(template.render())
        print(f" - {city_file}")

        for pro in pros:
            print(f"Building pro: {pro.full_name()}")
            pro_file = city_dir.joinpath(f"{slug(pro.full_name())}.html")
            with pro_file.open("w") as f:
                template = ProTemplate(pro)
                f.write(template.render())
            print(f" - {pro_file}")
