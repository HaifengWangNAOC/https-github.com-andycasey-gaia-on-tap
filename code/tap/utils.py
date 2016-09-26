
""" General utility functions for accessing Gaia data using TAP """

__all__ = ["login", "logout", "get_tables"]


import requests
from ..config import config


class TAPQueryException(Exception):

    def __init__(self, response, message=None):

        # Try parsing out an error message.
        if message is None:
            try:
                message = response.text\
                    .split('<INFO name="QUERY_STATUS" value="ERROR">')[1]\
                    .split('</INFO>')[0].strip()

            except:
                message = "{} code returned".format(response.status_code)

        super(TAPQueryException, self).__init__(message)

        self.errors = response
        return None
    

def login(session=None):
    """
    Return a `requests.Session` object with the user logged in.

    :param session: [optional]
        Optionally provide a session to use.
    """

    session = session or requests.Session()
    r = session.post("{}/login".format(config.url),
        data=dict(username=config.username, password=config.password))
    if not r.ok:
        raise TAPQueryException(r, "authorization denied")
    return session


def logout(session):
    """
    Logout of the ESA Gaia database.

    :param session:
        An authenticated session.
    """
    session.post("{}/logout".format(config.url))
    return None


def get_tables(authenticate=False):
    """
    Get a list of public tables (and user tables, if authenticated).

    :param authenticate: [optional]
        Login to the ESA Gaia archive using your credentials.
    """

    session = requests.Session()
    if authenticate:
        login(session)
        
    # FUCK me they give me XML what the fuck?
    response = session.get("{}/tap/tables".format(config.url))
    return response.text