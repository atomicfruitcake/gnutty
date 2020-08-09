"""!
@author atomicfruitcake

@date 2020

Authorization mechanisms for authorizing HTTP requests
"""

from srv.dummy.credentials import basic_auth_credentials
from srv.request import Request


def _authorize_basic(request: Request) -> bool:
    """
    Authorize and HTTP request with BASIC Access Authentication
    :param request: HTTP Request object
    :return: bool - True if authorization succeeds, False otherwis
    """
    for cred in basic_auth_credentials:
        if cred[0] == request.basic_auth_creds["username"]:
            try:
                assert cred[1] == request.basic_auth_creds["password"]
                return True
            except AssertionError:
                return False
    return False

def authorize(request: Request, auth=None) -> bool:
    """
    Authorize the HTTP Request object if an authorization method is required
    :param request: HTTP Request object
    :param auth: str - authorization method requested
    :return: True if request passes authorization, False otherwise
    """
    if not auth:
        return True
    if auth.lower() == "basic":
        return _authorize_basic(request)
