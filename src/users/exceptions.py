from rest_framework import exceptions, status


class ExternalReferenceExistsException(exceptions.APIException):
    """
    If the username is already in use.
    """

    status_code = status.HTTP_409_CONFLICT
    default_detail = "Username is already in use."