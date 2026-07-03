import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage

logger = logging.getLogger(__name__)


class ChallengePage(BasePage):

    URL = "https://rpachallenge.com/"

    def open(self):
        logger.info("Opening challenge site %s", self.URL)
        self.driver.get(self.URL)

    def download_excel(self):
        logger.info("Clicking Excel download link")
        self.driver.find_element(
            By.XPATH,
            "//a[contains(@href,'challenge.xlsx')]"
        ).click()

    def start(self):
        logger.info("Clicking start button")
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class,'btn-large') and normalize-space()='Start']"
                )
            )
        ).click()

    def _find_input_by_label(self, label_text: str):
        logger.info("Locating input field for label '%s'", label_text)

        try:
            label = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        f"//label[normalize-space()='{label_text}']"
                    )
                )
            )

            container = label.find_element(By.XPATH, "./..")

            element = container.find_element(
                By.XPATH,
                ".//input | .//textarea | .//select"
            )
            logger.info(
                "Found input by label '%s': %s",
                label_text,
                element.get_attribute('outerHTML'),
            )
            return element

        except Exception:
            pass

        fallback = {
            "First Name": "labelFirstName",
            "Last Name": "labelLastName",
            "Company Name": "labelCompanyName",
            "Role in Company": "labelRole",
            "Address": "labelAddress",
            "Email": "labelEmail",
            "Phone Number": "labelPhone",
        }

        if label_text in fallback:
            logger.warning(
                "Label '%s' not found by visible text, using fallback ng-reflect-name '%s'",
                label_text,
                fallback[label_text],
            )
            element = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        f"//input[@ng-reflect-name='{fallback[label_text]}']"
                    )
                )
            )
            logger.debug(
                "Fallback element for '%s': %s",
                label_text,
                element.get_attribute('outerHTML'),
            )
            return element

        logger.error(
            "Field lookup failed for label '%s' and no fallback available",
            label_text,
        )
        raise RuntimeError(
            f"Não foi possível localizar o campo para o rótulo '{label_text}'"
        )

    def fill_form(self, form_data: dict, record_index: int | None = None):

        for field_label, value in form_data.items():
            logger.info(
                "Record %s: filling field '%s' with value '%s'",
                record_index,
                field_label,
                value,
            )

            element = self._find_input_by_label(field_label)
            logger.debug(
                "Resolved element for '%s': %s",
                field_label,
                element.get_attribute('outerHTML'),
            )

            element.clear()
            element.send_keys("" if value is None else str(value))

            logger.info(
                "Record %s: input value '%s' into element '%s' for label '%s'",
                record_index,
                value,
                element.get_attribute('outerHTML'),
                field_label,
            )

    def submit(self):
        logger.info("Waiting for submit button and clicking it")
        submit_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[type='submit']")
            )
        )
        logger.debug("Submit button outerHTML: %s", submit_button.get_attribute('outerHTML'))
        submit_button.click()
