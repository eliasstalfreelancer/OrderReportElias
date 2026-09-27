import logging


def configure_logging() -> None:
    """Configure application logging in one central place."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
