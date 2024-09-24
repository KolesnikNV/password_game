import aiohttp
import datetime
import ephem

from consts import sequences, elements_symbols, pokemons_abilities


async def fetch_wordle_answer() -> str | None:
    """Fetch the Wordle answer for the current date."""
    today = datetime.date.today()
    url = f"https://www.nytimes.com/svc/wordle/v2/{today:%Y-%m-%d}.json"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        return data["solution"].lower()

    except Exception:
        return None


async def get_current_moon_phase() -> str:
    """Get the current phase of the moon as an emoji."""
    today = datetime.datetime.now()
    moon = ephem.Moon()
    moon.compute(today)

    phase = moon.phase
    if phase < 1:
        return "🌑"  # New Moon
    elif phase < 50:
        return "🌒"  # Waxing Crescent
    elif phase < 100:
        return "🌓"  # First Quarter
    elif phase < 150:
        return "🌔"  # Waxing Gibbous
    elif phase < 200:
        return "🌕"  # Full Moon
    elif phase < 250:
        return "🌖"  # Waning Gibbous
    elif phase < 300:
        return "🌗"  # Last Quarter
    else:
        return "🌘"  # Waning Crescent


async def check_letter_count(password: str) -> str:
    """Check for excessive occurrences of specific letters."""

    for char in ["а", "c", "z", "1"]:
        if password.count(char) > 3:
            return f"Password cannot have more than three '{char}'s in a row."


async def check_episode_title(password: str) -> str:
    """Check if the password contains a title from the Supernatural episodes."""
    with open("episodes_title.txt", "r") as file:
        episode_titles = [line.strip().lower() for line in file]

    if not any(title in password.lower() for title in episode_titles):
        return "Password must contain the title of one of the Supernatural episodes."


async def validate_password(password: str) -> str:
    """Validate the provided password against several criteria."""

    if len(password) < 8:
        return "Password must be at least 8 characters long."

    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit."
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return "Password must contain at least one lowercase letter."
    if any(seq in password for seq in sequences):
        return (
            "Password cannot contain common sequences like 'abc', '123', or 'qwerty'."
        )

    if sum(int(char) for char in password if char.isdigit()) != 45:
        return "Password's digits sum should be 45."

    if "3.14" not in password:
        return "Password must include the first three digits of Pi."

    if password.find("4") == -1:
        return "Password must contain the 17th digit after the decimal of Pi (4)."

    if not any(char in password for char in elements_symbols):
        return "The password must include at least one symbol from the list of chemical elements."

    if "1976" not in password:
        return "Password must contain the birth year of Benedict Cumberbatch."

    if not any(ability.lower() in password.lower() for ability in pokemons_abilities):
        return "Password must contain at least one Pokémon’s ability from the first 30 Pokémon listed on https://pokeapi.co/."

    if await get_current_moon_phase() not in password:
        return "Password must include the current phase of the moon as an emoji."

    res = await fetch_wordle_answer()
    if res is not None and res not in password.lower():
        return "Password must include today's answer to the Wordle game."

    if "Ghana" not in password:
        return "Password must include cities name where Adonten S. E. Road is located."

    if episode_title_error := await check_episode_title(password):
        return episode_title_error

    if letter_count_error := await check_letter_count(password):
        return letter_count_error

    return "Password is valid!"
