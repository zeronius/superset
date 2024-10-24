from flask import has_request_context, request, session

SESSION_LOCALE_KEY = "locale"


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
                    session[SESSION_LOCALE_KEY] = value
                    return session[SESSION_LOCALE_KEY]
                else:
                    session[SESSION_LOCALE_KEY] = self.babel_default_locale
                    return session[SESSION_LOCALE_KEY]

        locale = session.get(SESSION_LOCALE_KEY)
        if locale:
            return locale
        session[SESSION_LOCALE_KEY] = self.babel_default_locale
        return session[SESSION_LOCALE_KEY]
