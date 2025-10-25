from typing import List, Set
from enum import Enum
import random

# ----------------------------
# CLASSES
# ----------------------------

class InvalidPickError(Exception):
    """Invalid pick/ban!"""
    pass


class Champion:
    def __init__(self, name: str, roles: Set[str]):
        self.name = name
        self.roles = roles


class Team:
    def __init__(self, name: str):
        self.name = name
        self.picks: List[Champion] = []

    def lock_in(self, champ_name: str, filone=None):
        if len(self.picks) >= 5:
            raise InvalidPickError(f"{self.name} ha già 5 campioni!")
        if champ_name not in CHAMPION_POOL:
            raise InvalidPickError(f"{champ_name} non esiste!")
        if any(c.name == champ_name for c in self.picks):
            raise InvalidPickError(f"{champ_name} già preso da {self.name}!")
        if filone and champ_name in filone.fearless_locked:
            raise InvalidPickError(f"{champ_name} non disponibile (fearless)!")
        self.picks.append(CHAMPION_POOL[champ_name])
        print(f"{self.name} picka {champ_name}")


class Filone:
    def __init__(self):
        self.fearless_locked: Set[str] = set()

    def register_pick(self, champ_name: str):
        self.fearless_locked.add(champ_name)


# ----------------------------
# CHAMPION POOL
# ----------------------------

CHAMPION_POOL = {
    "Aatrox": {"roles": {"Top", "Fighter"}},
    "Darius": {"roles": {"Top", "Fighter", "Tank"}},
    "Fiora": {"roles": {"Top", "Fighter"}},
    "Garen": {"roles": {"Top", "Fighter", "Tank"}},
    "Riven": {"roles": {"Top", "Fighter", "Assassin"}},

    "Amumu": {"roles": {"Jungle", "Tank", "Mage"}},
    "Lee Sin": {"roles": {"Jungle", "Fighter", "Assassin"}},
    "Vi": {"roles": {"Jungle", "Fighter"}},
    "Nunu": {"roles": {"Jungle", "Tank", "Support"}},
    "Sejuani": {"roles": {"Jungle", "Tank"}},

    "Ahri": {"roles": {"Mid", "Mage", "Assassin"}},
    "Akali": {"roles": {"Mid", "Assassin"}},
    "Anivia": {"roles": {"Mid", "Mage"}},
    "Annie": {"roles": {"Mid", "Mage"}},
    "Katarina": {"roles": {"Mid", "Assassin", "Mage"}},
    "Orianna": {"roles": {"Mid", "Mage"}},
    "Zed": {"roles": {"Mid", "Assassin"}},
    "Ziggs": {"roles": {"Mid", "Mage"}},
    "Yasuo": {"roles": {"Mid", "Fighter", "Assassin"}},

    "Ashe": {"roles": {"ADC", "Marksman"}},
    "Caitlyn": {"roles": {"ADC", "Marksman"}},
    "Ezreal": {"roles": {"ADC", "Marksman", "Mage"}},
    "Jinx": {"roles": {"ADC", "Marksman"}},
    "Miss Fortune": {"roles": {"ADC", "Marksman"}},

    "Alistar": {"roles": {"Support", "Tank"}},
    "Braum": {"roles": {"Support", "Tank"}},
    "Janna": {"roles": {"Support", "Mage"}},
    "Leona": {"roles": {"Support", "Tank"}},
    "Lux": {"roles": {"Support", "Mage"}},
    "Nautilus": {"roles": {"Support", "Tank"}},
    "Soraka": {"roles": {"Support", "Mage"}},
    "Thresh": {"roles": {"Support", "Tank", "Control"}},
}

# Mappa lowercase -> nome corretto
CHAMPION_NAME_MAP = {name.lower(): name for name in CHAMPION_POOL.keys()}


# ----------------------------
# DRAFT TYPES
# ----------------------------

class DraftType(Enum):
    FEARLESS = 1
    TOURNAMENT = 2
    TROLL = 3


# ----------------------------
# DRAFT FUNCTIONS
# ----------------------------

def fearless(filone, team_a, team_b):
    print("\n--- Fearless Draft: Fase Ban 1 ---")
    first_ban_order = [team_a, team_b, team_b, team_a, team_a, team_b]
    for team in first_ban_order:
        while True:
            champ_input = input(f"{team.name} banna: ").strip().lower()
            if champ_input not in CHAMPION_NAME_MAP:
                print("Campione inesistente. Riprova.")
                continue
            champ_name = CHAMPION_NAME_MAP[champ_input]
            if champ_name in filone.fearless_locked:
                print("Campione già bannato/pickato!")
                continue
            filone.register_pick(champ_name)
            print(f"{team.name} banna {champ_name}")
            break

    print("\n--- Fearless Draft: Fase Pick 1 ---")
    first_pick_order = [team_a, team_b, team_b, team_a, team_a, team_b]
    for team in first_pick_order:
        while True:
            champ_input = input(f"{team.name} picka: ").strip().lower()
            if champ_input not in CHAMPION_NAME_MAP:
                print("Campione inesistente. Riprova.")
                continue
            champ_name = CHAMPION_NAME_MAP[champ_input]
            try:
                team.lock_in(champ_name, filone)
                filone.register_pick(champ_name)
                break
            except InvalidPickError as e:
                print(e)

    print("\n--- Fearless Draft: Fase Ban 2 ---")
    second_ban_order = [team_b, team_a, team_a, team_b]
    for team in second_ban_order:
        while True:
            champ_input = input(f"{team.name} banna: ").strip().lower()
            if champ_input not in CHAMPION_NAME_MAP:
                print("Campione inesistente. Riprova.")
                continue
            champ_name = CHAMPION_NAME_MAP[champ_input]
            if champ_name in filone.fearless_locked:
                print("Campione già bannato/pickato!")
                continue
            filone.register_pick(champ_name)
            print(f"{team.name} banna {champ_name}")
            break

    print("\n--- Fearless Draft: Fase Pick 2 ---")
    second_pick_order = [team_b, team_a, team_a, team_b]
    for team in second_pick_order:
        while True:
            champ_input = input(f"{team.name} picka: ").strip().lower()
            if champ_input not in CHAMPION_NAME_MAP:
                print("Campione inesistente. Riprova.")
                continue
            champ_name = CHAMPION_NAME_MAP[champ_input]
            try:
                team.lock_in(champ_name, filone)
                filone.register_pick(champ_name)
                break
            except InvalidPickError as e:
                print(e)

    print("\nFearless Draft completata!")
    print(f"{team_a.name}: {[c.name for c in team_a.picks]}")
    print(f"{team_b.name}: {[c.name for c in team_b.picks]}")
    return "Fearless"


def tournament(team_a, team_b):
    print("\n--- Tournament Draft: Fase Ban 1 ---")
    first_ban_order = [team_a, team_b, team_b, team_a, team_a, team_b]
    for team in first_ban_order:
        while True:
            champ_input = input(f"{team.name} banna: ").strip().lower()
            if champ_input not in CHAMPION_NAME_MAP:
                print("Campione inesistente. Riprova.")
                continue
            champ_name = CHAMPION_NAME_MAP[champ_input]
            print(f"{team.name} banna {champ_name}")
            break

    print("\n--- Tournament Draft: Fase Pick 1 ---")
    first_pick_order = [team_a, team_b, team_b, team_a, team_a, team_b]
    for team in first_pick_order:
        while True:
            champ_input = input(f"{team.name} picka: ").strip().lower()
            if champ_input not in CHAMPION_NAME_MAP:
                print("Campione inesistente. Riprova.")
                continue
            champ_name = CHAMPION_NAME_MAP[champ_input]
            try:
                team.lock_in(champ_name)
                break
            except InvalidPickError as e:
                print(e)

    print("\n--- Tournament Draft: Fase Ban 2 ---")
    second_ban_order = [team_a, team_b, team_a, team_b]
    for team in second_ban_order:
        while True:
            champ_input = input(f"{team.name} banna: ").strip().lower()
            if champ_input not in CHAMPION_NAME_MAP:
                print("Campione inesistente. Riprova.")
                continue
            champ_name = CHAMPION_NAME_MAP[champ_input]
            print(f"{team.name} banna {champ_name}")
            break

    print("\n--- Tournament Draft: Fase Pick 2 ---")
    second_pick_order = [team_b, team_a, team_a, team_b]
    for team in second_pick_order:
        while True:
            champ_input = input(f"{team.name} picka: ").strip().lower()
            if champ_input not in CHAMPION_NAME_MAP:
                print("Campione inesistente. Riprova.")
                continue
            champ_name = CHAMPION_NAME_MAP[champ_input]
            try:
                team.lock_in(champ_name)
                break
            except InvalidPickError as e:
                print(e)

    print("\nTournament Draft completata!")
    print(f"{team_a.name}: {[c.name for c in team_a.picks]}")
    print(f"{team_b.name}: {[c.name for c in team_b.picks]}")
    return "Tournament"


def random_draft(team_a, team_b):
    available_champs = list(CHAMPION_POOL.keys())
    print("\n--- Random Draft (stile ARAM) ---")
    while len(team_a.picks) < 5 or len(team_b.picks) < 5:
        for team in [team_a, team_b]:
            if len(team.picks) >= 5:
                continue
            choices = random.sample(available_champs, 3)
            print(f"\n{team.name}, le tue opzioni: {', '.join(choices)}")
            while True:
                champ_input = input(f"Scegli il tuo campione ({', '.join(choices)}): ").strip().lower()
                if champ_input not in [c.lower() for c in choices]:
                    print("Scelta non valida. Riprova.")
                    continue
                champ_name = CHAMPION_NAME_MAP[champ_input]
                try:
                    team.lock_in(champ_name)
                    available_champs.remove(champ_name)
                    break
                except InvalidPickError as e:
                    print(e)

    print("\nRandom Draft completata!")
    print(f"{team_a.name}: {[c.name for c in team_a.picks]}")
    print(f"{team_b.name}: {[c.name for c in team_b.picks]}")
    return "Random"