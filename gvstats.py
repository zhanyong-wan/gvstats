#!/usr/bin/env python3

from typing import Dict
import collections
import dataclasses

import data

year_to_population: Dict[int, int] = collections.defaultdict(int)
# State => year => deathes per capita.
state_code_to_annual_death_rates: Dict[str, Dict[int, float]] = collections.defaultdict(
    dict
)
# State => year => deathes.
state_code_to_annual_deathes: Dict[str, Dict[int, int]] = collections.defaultdict(dict)

for year, state_code, deathes_per_capita, deathes, _ in data.GUN_MORTALITY:
    if year < 2014 or year > 2020:
        continue
    num_capitas = deathes / deathes_per_capita
    population = int(num_capitas * 100 * 1000)
    # print(f"{state_code} has {population} people in {year}.")
    year_to_population[year] += population

    state_code_to_annual_deathes[state_code][year] = deathes
    state_code_to_annual_death_rates[state_code][year] = deathes_per_capita

for year in sorted(year_to_population.keys()):
    population = year_to_population[year]
    # print(f"US has ~{population} people in {year}")


@dataclasses.dataclass
class MassShootingStats:
    state_name: str
    pop2023: int
    num_mass_shootings: int
    mass_shootings_per_capita: float


@dataclasses.dataclass
class ShootingStats:
    state_name: str
    annual_deathes: int
    annual_deaths_per_capita: float


_STATE_NAME_TO_SHOOTING_STATS: Dict[str, ShootingStats] = {}
for state_code in sorted(state_code_to_annual_death_rates):
    annual_deathes = state_code_to_annual_deathes[state_code]
    avg_deathes = sum(annual_deathes.values()) // len(annual_deathes)

    annual_death_rates = state_code_to_annual_death_rates[state_code]
    avg_death_rates = sum(annual_death_rates.values()) / len(annual_death_rates)

    print(f"{state_code}'s average deathes/capita in 2014-2020: {avg_death_rates:.2f}")
    state_name = data.STATE_CODE_TO_NAME[state_code]
    _STATE_NAME_TO_SHOOTING_STATS[state_name] = ShootingStats(
        state_name=state_name,
        annual_deathes=avg_deathes,
        annual_deaths_per_capita=avg_death_rates,
    )

# Maps a state name to the state's mass shooting stats.
_STATE_NAME_TO_MASS_SHOOTING_STATS = {
    state_name: MassShootingStats(
        state_name=state_name,
        pop2023=pop2023,
        num_mass_shootings=num_mass_shootings,
        mass_shootings_per_capita=mass_shootings_per_capita,
    )
    for (
        _,
        state_name,
        _,
        pop2023,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        num_mass_shootings,
        mass_shootings_per_capita,
    ) in data.RAW_GV_STATS
}


sorted_by_ms_per_capita = sorted(
    _STATE_NAME_TO_MASS_SHOOTING_STATS.values(),
    key=lambda s: s.mass_shootings_per_capita,
    reverse=True,
)
print("Sorted by annual mass shootings per capita.")
for idx, stats in enumerate(sorted_by_ms_per_capita):
    code = data.STATE_NAME_TO_CODE[stats.state_name]
    color = data.STATE_CODE_TO_COLOR[code]
    print(
        f"{idx + 1}, {stats.state_name}, {color}, {stats.mass_shootings_per_capita:0.2f}, "
        f"{stats.num_mass_shootings}"
    )
print()

sorted_by_deathes_per_capita = sorted(
    _STATE_NAME_TO_SHOOTING_STATS.values(),
    key=lambda s: s.annual_deaths_per_capita,
    reverse=True,
)
print("Sorted by annual deathes per capita.")
print("Gun death rate rank, State, Color, Death rate, Deathes")
for idx, stats in enumerate(sorted_by_deathes_per_capita):
    code = data.STATE_NAME_TO_CODE[stats.state_name]
    color = data.STATE_CODE_TO_COLOR[code]
    print(
        f"{idx + 1}, {stats.state_name}, {color}, {stats.annual_deaths_per_capita:.2f}, "
        f"{stats.annual_deathes}"
    )
print()

print("Sorted by annual deathes per capita.")
print("Gun death rate rank, State, Gun law strength rank, Deathes per capita, Deathes")
for idx, stats in enumerate(sorted_by_deathes_per_capita):
    gun_law_strength_rank = data.STATE_NAME_TO_GUN_LAW_STRENGTH_RANK[stats.state_name]
    print(
        f"{idx + 1}, {stats.state_name}, {gun_law_strength_rank}, {stats.annual_deaths_per_capita:.2f}, "
        f"{stats.annual_deathes}"
    )
