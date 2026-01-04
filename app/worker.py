import sys
import signal

# Handle Windows specific signal missing
if sys.platform == "win32":
    import asyncio

    # Windows does not support add_signal_handler, so we mock it to avoid crash
    asyncio.AbstractEventLoop.add_signal_handler = lambda *args, **kwargs: None

    if not hasattr(signal, "SIGQUIT"):
        signal.SIGQUIT = signal.SIGTERM

from hatchet_sdk import Hatchet
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting Hatchet Worker...")

    # Initialize Hatchet
    hatchet = Hatchet()

    # Create a worker
    worker = hatchet.worker("lender-worker")

    # Start the worker
    worker.start()


if __name__ == "__main__":
    main()
