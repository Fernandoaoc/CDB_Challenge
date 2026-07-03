from pathlib import Path
import time
import logging

logger = logging.getLogger(__name__)


def wait_download(download_dir, name="challenge.xlsx", timeout=30):
    path = Path(download_dir)/name
    logger.info("Waiting for download of %s in %s", name, download_dir)
    init_time = time.time()
    while time.time()-init_time < timeout:
        if path.exists() and not list(Path(download_dir).glob("*.crdownload")):
            logger.info("Download complete: %s", path)
            return path
        time.sleep(.5)
    logger.error("Timeout waiting for download: %s", path)
    raise TimeoutError(f"Timeout waiting for {name} in {download_dir}")
