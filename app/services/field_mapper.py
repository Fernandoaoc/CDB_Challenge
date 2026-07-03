import logging

logger = logging.getLogger(__name__)


class FieldMapper:
    """
    Passa os nomes das colunas da planilha diretamente para o formulário.
    """

    def map_record(self, record: dict) -> dict:
        logger.debug("Passing through Excel record: %s", record)

        mapped = {}

        for excel_column, value in record.items():
            if excel_column is None:
                logger.warning(
                    "Skipping Excel column with no header for value: %s",
                    value,
                )
                continue

            form_label = str(excel_column).strip()
            mapped[form_label] = value
            logger.debug(
                "Passing through Excel column '%s' with value '%s'",
                form_label,
                value,
            )

        logger.info("Mapped record to form data: %s", mapped)
        return mapped