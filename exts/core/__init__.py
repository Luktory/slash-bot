"""
Root file for exts/core.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions
from const import EXT_CORE


class Core(interactions.Extension):
    """exts/core Extension."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        [self.client.load(f"exts.core.{ext}") for ext in EXT_CORE]


def setup(client) -> None:
    """Setup the extension"""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Core(client)
    logging.debug("""[%s] Loaded Core extension.""", log_time)
    print(f"[{log_time}] Loaded Core extension.")
