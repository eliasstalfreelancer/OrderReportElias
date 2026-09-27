import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_orders(input_path: Path) -> pd.DataFrame:
    """Read order data from a CSV file."""
    
    logger.info("Läser orderdata från %s", input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Datafilen finns inte: {input_path}")

    try:
        data = pd.read_csv(input_path)
    
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"Datafilen är tom: {input_path}") from exc
    
    except pd.errors.ParserError as exc:
        raise ValueError(f"Datafilen kunde inte tolkas som CSV: {input_path}") from exc

    logger.info("Läste in %d rader.", len(data))
    return data


def save_reports(reports: dict[str, pd.DataFrame], output_dir: Path) -> None:
    """Save generated reports as CSV files."""
    
    output_dir.mkdir(parents=True, exist_ok=True)

    for filename, report in reports.items():
        output_path = output_dir / filename
        report.to_csv(output_path, index=False)
        logger.info("Sparade rapport: %s", output_path)
