from flask import has_request_context, request, session
from superset import conf

SESSION_LOCALE_KEY = "locale"

D3_NUMBER_FORMATS = {
    "de": {
        "decimal": ",",
        "thousands": ".",
        "grouping": [3],
        "currency": ["", "€"],
    },
}

D3_TIME_FORMATS = {
    "de": {
        "dateTime": "%x, %X",
        "date": "%d.%m.%Y",  # Format as DD.MM.YYYY
        "time": "%H:%M:%S",  # 24-hour format, no AM/PM
        "periods": ["", ""],  # German typically doesn't use AM/PM notation
        "days": ["Sonntag", "Montag", "Dienstag", "Mittwoch",
                 "Donnerstag", "Freitag", "Samstag"],
        "shortDays": ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"],
        "months": ["Januar", "Februar", "März", "April",
                   "Mai", "Juni", "Juli", "August",
                   "September", "Oktober", "November", "Dezember"],
        "shortMonths": ["Jan", "Feb", "Mär", "Apr",
                        "Mai", "Jun", "Jul", "Aug",
                        "Sep", "Okt", "Nov", "Dez"]
    },
}


def get_locale(self):
    """
    Enhanced implementation of locale resolving that can set locale from request 'lang' parameter.
    It sets locale in session as a side effect.
    See original version at  https://github.com/dpgaspar/Flask-AppBuilder/blob/master/flask_appbuilder/babel/manager.py#L50
    """
    if has_request_context():
        for arg, value in request.args.items():
            if arg == "_l_":
                if value in self.languages:
                    return value
                else:
                    return self.babel_default_locale
            if arg == "lang":
                if value in self.languages:
                    return set_locale(value)
                else:
                    return set_locale(self.babel_default_locale)

        locale = session.get(SESSION_LOCALE_KEY)
        if locale:
            return locale
        return set_locale(self.babel_default_locale)


def set_locale(new_locale):
    # from superset.config import D3_TIME_FORMAT, D3_FORMAT
    session[SESSION_LOCALE_KEY] = new_locale
    session['currency'] = 'EUR'
    # conf["D3_FORMAT"] = D3_NUMBER_FORMATS.get(new_locale, D3_FORMAT)
    # conf["D3_TIME_FORMAT"] = D3_TIME_FORMATS.get(new_locale, D3_TIME_FORMAT)
    return new_locale
