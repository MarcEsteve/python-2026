import os
import time
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

#Ejemplos de selectores CSS para los botones de "Me gusta" en Strava:

#feed-entry-1773050313734 > div > div.IHNiS > div > div.VFziQ > button:nth-child(1) > svg > path

#feed-entry-1773049808304 > div > div.IHNiS > div > div.VFziQ > button:nth-child(1) > svg

#feed-entry-1773049522739 > div > div.IHNiS > div > div.VFziQ > button:nth-child(1) > svg > path

#feed-entry-1773049095139 > div > div.IHNiS > div > div.VFziQ > button:nth-child(1) > svg

#feed-entry-1773047577803 > div > div.IHNiS > div > div.VFziQ > button:nth-child(1) > svg > path


def get_firefox_profile_path() -> str:
    """Return Firefox profile path from env var or profiles.ini default profile."""
    from configparser import ConfigParser

    env_profile = os.getenv("FIREFOX_PROFILE_PATH")
    if env_profile:
        return env_profile

    appdata = os.getenv("APPDATA", "")
    profiles_ini = os.path.join(appdata, "Mozilla", "Firefox", "profiles.ini")

    if not os.path.exists(profiles_ini):
        raise ValueError(
            "No se encontro profiles.ini de Firefox. Define FIREFOX_PROFILE_PATH manualmente."
        )

    config = ConfigParser()
    config.read(profiles_ini, encoding="utf-8")
    profiles_root = os.path.join(appdata, "Mozilla", "Firefox")

    default_candidate = ""
    for section in config.sections():
        if not section.startswith("Profile"):
            continue

        path = config.get(section, "Path", fallback="")
        is_relative = config.get(section, "IsRelative", fallback="1") == "1"
        is_default = config.get(section, "Default", fallback="0") == "1"

        if not path:
            continue

        candidate = os.path.join(profiles_root, path) if is_relative else path
        if is_default and os.path.exists(candidate):
            return candidate

        if not default_candidate and os.path.exists(candidate):
            default_candidate = candidate

    if default_candidate:
        return default_candidate

    raise ValueError(
        "No se pudo resolver el perfil de Firefox. Define FIREFOX_PROFILE_PATH manualmente."
    )


def is_kudos_already_pressed(button) -> bool:
    """Best-effort detection of an already liked/kudoed button."""
    aria_pressed = (button.get_attribute("aria-pressed") or "").strip().lower()
    if aria_pressed == "true":
        return True

    class_name = (button.get_attribute("class") or "").lower()
    if any(state in class_name for state in ("active", "selected", "liked", "kudoed")):
        return True

    label = " ".join(
        filter(
            None,
            [
                button.get_attribute("aria-label"),
                button.get_attribute("title"),
                button.text,
            ],
        )
    ).lower()
    if any(state in label for state in ("quitar kudos", "liked", "unlike", "kudoed")):
        return True

    return False


def click_kudos_pass(driver, like_button_suffix: str, delay_seconds: float = 0.1) -> int:
    """Click one pass of available kudos buttons and return total clicks done."""
    clicks_done = 0
    feed_entries = driver.find_elements(By.CSS_SELECTOR, '[id^="feed-entry-"]')
    feed_ids = [entry.get_attribute("id") for entry in feed_entries if entry.get_attribute("id")]

    for feed_id in feed_ids:
        css_selector = f'#{feed_id}{like_button_suffix}'
        buttons = driver.find_elements(By.CSS_SELECTOR, css_selector)

        if not buttons:
            continue

        like_button = buttons[0]
        if is_kudos_already_pressed(like_button):
            continue

        try:
            like_button.click()  # Clic normal
        except ElementClickInterceptedException:
            # Fallback por si hay overlays o el clic queda interceptado
            driver.execute_script("arguments[0].click();", like_button)

        clicks_done += 1
        time.sleep(delay_seconds)  # Pequeño delay entre clics para no hacerlo tan rapido

    return clicks_done

# Configuracion para usar Firefox con Selenium
profile_path = get_firefox_profile_path()
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)
driver = Firefox(service=Service(GeckoDriverManager().install()), options=options) # Iniciamos el driver de Firefox

# Abrimos una nueva pestaña en el mismo navegador y vamos al dashboard
driver.switch_to.new_window("tab")
driver.get("https://www.strava.com/dashboard?num_entries=300")

#Como buscarias el botón desde el primero hasta el ultimo? 

# Patrón común de selector CSS de cada botón "Me gusta" dentro de cada feed-entry
like_button_suffix = ' > div > div.IHNiS > div > div.VFziQ > button:nth-child(1)'

# Primera pasada de kudos
first_pass = click_kudos_pass(driver, like_button_suffix, delay_seconds=0.1)

driver.refresh()  # Refrescar la página
time.sleep(1)  # Pequeña pausa para que el feed se estabilice tras el refresh

# Segunda pasada de kudos tras refresh
second_pass = click_kudos_pass(driver, like_button_suffix, delay_seconds=0.1)
print(f"Kudos en primera pasada: {first_pass} | segunda pasada: {second_pass}")

#Finalizamos la sesión de Selenium cerrando el navegador
driver.quit() # Cerrar el driver de Firefox