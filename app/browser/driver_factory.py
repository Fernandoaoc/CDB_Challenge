import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


def create_driver(download_dir, headless: bool = True):
    options = Options()
    prefs = {
        "download.default_directory": str(Path(download_dir).resolve()),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        logger.info("Creating Chrome driver in headless mode with download directory: %s", prefs["download.default_directory"])
    else:
        options.add_argument("--window-size=800,600")
        logger.info("Creating Chrome driver with download directory: %s", prefs["download.default_directory"])

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
