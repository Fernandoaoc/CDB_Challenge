from pathlib import Path
import logging
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.browser.driver_factory import create_driver
from app.browser.download_manager import wait_download

from app.pages.challenge_page import ChallengePage

from app.services.excel_reader import ExcelReader
from app.services.field_mapper import FieldMapper

logger = logging.getLogger(__name__)


class ChallengeRunner:

    def __init__(self, headless: bool = True):
        self._setup_logging()

        self.download_dir = Path("downloads")
        self.download_dir.mkdir(exist_ok=True)

        self.artifact_dir = Path("artefacts").resolve()
        self.artifact_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Artifact directory ensured at %s", self.artifact_dir)

        self.final_result_captured = False
        self.last_result_message = None
        self.last_screenshot_path = None

        logger.info("Creating Chrome driver with download dir %s", self.download_dir)
        self.driver = create_driver(self.download_dir, headless=headless)

        self.page = ChallengePage(self.driver)

        self.mapper = FieldMapper()

    def _setup_logging(self):
        root_logger = logging.getLogger()
        if root_logger.handlers:
            return

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler = logging.FileHandler("logs.log", mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        root_logger.setLevel(logging.INFO)

    def execute(self):

        print("=" * 60)
        print("CDB TESTE TÉCNICO")
        print("=" * 60)

        # 1 - Abre o site
        self.page.open()

        print("Baixando planilha...")
        logger.info("Starting spreadsheet download")

        # 1.5 - Remove planilha antiga se já existir
        self._remove_existing_excel()

        # 2 - Download
        self.page.download_excel()

        # 3 - Aguarda download
        excel_file = wait_download(self.download_dir)

        print(f"Planilha encontrada: {excel_file}")
        logger.info("Spreadsheet found: %s", excel_file)

        # 4 - Lê os registros
        reader = ExcelReader(excel_file)

        records = reader.read()

        print(f"{len(records)} registros encontrados")
        logger.info("Loaded %d records from spreadsheet", len(records))

        # 5 - Inicia o desafio
        logger.info("Starting challenge page")
        self.page.start()

        # 6 - Preenche todos os registros
        try:
            for index, record in enumerate(records, start=1):
                print(f"Registro {index}/{len(records)}")
                logger.info("Processing record %d/%d", index, len(records))
                logger.debug("Raw Excel record: %s", record)

                form_data = self.mapper.map_record(record)
                logger.debug("Mapped form data: %s", form_data)

                self.page.fill_form(form_data, record_index=index)
                self.page.submit()
                logger.info("Submitted record %d", index)

            result_message = self._capture_final_result()
            if result_message:
                print(f"Resultado final: {result_message}")
            if self.last_screenshot_path:
                print(f"Screenshot salvo em: {self.last_screenshot_path}")
            else:
                print("Screenshot não pôde ser salvo.")

            print("Desafio finalizado!")
            logger.info("Challenge completed")
        except Exception as exc:
            logger.exception("Challenge execution failed")
            raise
        finally:
            if not self.final_result_captured:
                logger.warning("Final result capture did not complete during execution; attempting capture before exit")
                try:
                    self._capture_final_result()
                except Exception as exc:
                    logger.warning("Final result capture failed in finally block: %s", exc)

    def _remove_existing_excel(self):
        excel_path = self.download_dir / "challenge.xlsx"
        if excel_path.exists():
            try:
                excel_path.unlink()
                logger.info("Removed existing Excel file: %s", excel_path)
            except Exception as exc:
                logger.warning(
                    "Failed to remove existing Excel file %s: %s",
                    excel_path,
                    exc,
                )

    def _capture_final_result(self):
        logger.info("Capturing final result message and screenshot")

        if self.final_result_captured:
            logger.info("Final result has already been captured; skipping duplicate capture")
            return self.last_result_message

        try:
            wait = WebDriverWait(self.driver, 20)
            message_element = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//*[contains(normalize-space(),'Congratulations') or contains(normalize-space(),'success rate') or contains(normalize-space(),'ccess rate') or contains(normalize-space(),'rate is')]"
                    )
                )
            )
            message_text = message_element.text.strip()
            logger.info("Result message: %s", message_text)
            self.last_result_message = message_text
        except Exception as exc:
            logger.warning("Could not capture final result message: %s", exc)
            message_text = None
            self.last_result_message = None

        screenshot_path = self.artifact_dir / f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        try:
            saved = self.driver.save_screenshot(str(screenshot_path))
            if saved:
                self.last_screenshot_path = screenshot_path
                logger.info("Screenshot saved: %s", screenshot_path)
            else:
                logger.warning("Screenshot call returned False; image not saved: %s", screenshot_path)
        except Exception as exc:
            logger.warning("Failed to save screenshot: %s", exc)

        self.final_result_captured = True
        return message_text

    def close(self):
        if not hasattr(self, "driver") or self.driver is None:
            return

        if not self.final_result_captured:
            logger.warning("Closing runner before final result capture; attempting one last capture")
            try:
                self._capture_final_result()
            except Exception as exc:
                logger.warning("Final result capture failed during close: %s", exc)

        try:
            self.driver.quit()
        except Exception as exc:
            logger.warning("Failed to quit WebDriver cleanly: %s", exc)