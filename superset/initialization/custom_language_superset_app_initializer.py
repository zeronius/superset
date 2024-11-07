from __future__ import annotations

import logging
import types
from typing import TYPE_CHECKING

from superset import appbuilder
from superset.initialization import SupersetAppInitializer
from superset.initialization.request_locale_resolver import get_locale

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class CustomSupersetAppInitializer(SupersetAppInitializer):

    def configure_fab(self) -> None:
        """
        Replaces method for localization in the appbuilder's BabelManager instance with custom one.
        """
        super().configure_fab()
        appbuilder.bm.get_locale = types.MethodType(get_locale, appbuilder.bm)
        appbuilder.bm.babel.locale_selector_func = appbuilder.bm.get_locale
