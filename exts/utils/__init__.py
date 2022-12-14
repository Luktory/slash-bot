"""
Root file for exts/utils.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions
from const import EXT_UTILS


class Utils(interactions.Extension):
    """exts/utils Extension."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        [self.client.load(f"exts.utils.{ext}") for ext in EXT_UTILS]


def setup(client) -> None:
    """Setup the extension"""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Utils(client)
    logging.debug("""[%s] Loaded Utils extension.""", log_time)
    print(f"[{log_time}] Loaded Utils extension.")
