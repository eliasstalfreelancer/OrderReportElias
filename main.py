import logging

from order_report.config import ReportConfig
from order_report.data_io import load_orders, save_reports
from order_report.logging_config import configure_logging
from order_report.processing import prepare_orders
from order_report.reports import generate_reports

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the complete order reporting workflow."""
    configure_logging()
    config = ReportConfig()

    logger.info("Startar orderrapport.")

    try:
        raw_data = load_orders(config.input_path)
        prepared_data = prepare_orders(raw_data)
        reports = generate_reports(prepared_data)
        save_reports(reports, config.output_dir)
        
    except (FileNotFoundError, ValueError) as error:
        logger.error("Orderrapporten kunde inte skapas: %s", error)
        raise SystemExit(1) from error

    logger.info("Orderrapport klar.")


if __name__ == "__main__":
    main()
