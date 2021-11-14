#! /usr/bin/env python3

import csv
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Sequence
from optparse import OptionParser


parser = OptionParser()
parser.add_option(
    "-p", "--prod", action="store_true", default=False, help="production mode"
)

(options, args) = parser.parse_args()

print(f"Options: {options}")


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
    """Base template. All template classes inherit from here."""

    BASE_PATH_PROD = "/dietista.it/directory/"
    BASE_PATH_DEV = "/dist/"

    TITLE = "Dietista.it - I migliori dietisti in Italia"
    DESCRIPTION = "La lista dei migliori dietisti italiani"

    HEAD = """
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="utf-8" />
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="stylesheet" type="text/css" href="/style.css" />
</head>
"""

    HEADER = """
<div id="header_container">
    <div class="page" id="header">
        <h1 id="header_logo"><a href="/">Dietista.it</a></h1>
        <ul id="header_menu">
            <li><a href="/iscriviti">Iscriviti</a></li>
        </ul>
    </div>
</div>
"""

    FOOTER = """
<div id="footer_container">
    <div class="page" id="footer">
        <p id="disclaimer">&copy; 2021 Dietista.it</p>
        <ul id="footer_menu">
            <li><a href="/">Home</a></li>
            <li><a href="/iscriviti">Iscriviti</a></li>
        </ul>
    </div>
</div>
"""

    PAGE = """
<!DOCTYPE html>
<html lang="it">

{head}

<body>
    {header}

    <div id="content_container">
        <div class="page" id="content">
            {content}
        </div>
    </div>

    {footer}
</body>

</html>
"""

    def render(
        self, content: str, title: str = TITLE, description: str = DESCRIPTION
    ) -> str:
        head = self.HEAD.format(title=title, description=description)
        return self._filter(
            self.PAGE.format(
                head=head, header=self.HEADER, footer=self.FOOTER, content=content
            )
        )

    def _filter(self, content: str) -> str:
        return re.sub(
            'href="/',
            f'href="{self.BASE_PATH_PROD if options.prod else self.BASE_PATH_DEV}',
            content,
        )


@dataclass
class HomeTemplate(BaseTemplate):
    """Home page template."""

    states: Sequence[str]

    CONTENT = """
<h1>La lista dei migliori dietisti italiani</h1>

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
class SubscribeTemplate(BaseTemplate):
    """Subscribe page template."""

    CONTENT = """
<h1>Iscriviti</h1>

<p>
    Pubblica il tuo profilo ed entra a far parte della più grande lista di
    dietisti in Italia.
</p>

<p>
    <a href="mailto:info@dietista.it?subject=Dietista.it, vorrei saperne di più">Sono interessat@</a>
</p>
"""

    def render(self) -> str:
        return super().render(content=self.CONTENT)


@dataclass
class StateTemplate(BaseTemplate):
    """State page template."""

    state: str
    cities: Sequence[str]

    CONTENT = """
<h1>I migliori dietisti nella provincia di {state}</h1>

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
<h1>I migliori dietisti nella città di {city}</h1>

<ul>
    {pros}
</ul>
"""

    def render(self) -> str:
        content = self.CONTENT.format(city=self.city, pros=self._pros_items())
        return super().render(content=content)

    def _pros_items(self) -> str:
        return "\n".join(
            f'<li><a href="{slug(pro.full_name())}/">{pro.full_name()}</a></li>'
            for pro in self.pros
        )


@dataclass
class ProTemplate(BaseTemplate):
    """Pro page template."""

    pro: Pro

    CONTENT = """
<h1>{full_name}</h1>

<p>
    <strong>Indirizzo:</strong><br/>
    {full_address}
</p>

<p>
    <strong>Telefono:</strong><br/>
    {phone_1}
</p>

<p>
    <strong>Sito Internet:</strong><br/>
    <a href="{web}">{web}</a>
</p>
"""

    def render(self) -> str:
        content = self.CONTENT.format(
            full_name=self.pro.full_name(),
            full_address=self._full_address(),
            phone_1=self.pro.phone_1,
            web=self.pro.web,
        )
        return super().render(content=content)

    def _full_address(self) -> str:
        output = f"{self.pro.address_line_1}<br/>"
        output += f"{self.pro.address_line_2}<br/>" if self.pro.address_line_2 else ""
        output += f"{self.pro.zip}, {self.pro.city}, {self.pro.state}"
        return output


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

# Remove existing content
shutil.rmtree(dist)

# Copy static files
shutil.copytree(Path("static"), dist)

print(f"Building home")
home_file = dist.joinpath("index.html")
with home_file.open("w") as f:
    template = HomeTemplate(list(states.keys()))
    f.write(template.render())
print(f" - {home_file}")

print(f"Building subscribe")
subscribe_dir = dist.joinpath("iscriviti")
subscribe_dir.mkdir(parents=True, exist_ok=True)
subscribe_file = subscribe_dir.joinpath("index.html")
with subscribe_file.open("w") as f:
    template = SubscribeTemplate()
    f.write(template.render())
print(f" - {subscribe_file}")

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
            pro_dir = city_dir.joinpath(slug(pro.full_name()))
            pro_dir.mkdir(parents=True, exist_ok=True)
            pro_file = pro_dir.joinpath("index.html")
            with pro_file.open("w") as f:
                template = ProTemplate(pro)
                f.write(template.render())
            print(f" - {pro_file}")
