# -*- coding: utf-8 -*-
import logging
import json
import re

logger = logging.getLogger(__name__)

class ClientError(Exception):
    """Generic error class, catch-all for most client issues.
    """
    def __init__(self, msg, code=None):
        self.code = code or 0
        super(ClientError, self).__init__(msg)

    @property
    def msg(self):
        return self.args[0]


class ClientLoginError(ClientError):
    """Raised when login fails."""
    pass


class ClientLoginRequiredError(ClientError):
    """Raised when login is required."""
    pass


class ClientCookieExpiredError(ClientError):
    """Raised when cookies have expired."""
    pass


class ClientThrottledError(ClientError):
    """Raised when client detects an http 429 Too Many Requests response."""
    pass


class ClientReqHeadersTooLargeError(ClientError):
    """Raised when client detects an http 431 Request Header Fields Too Large response."""
    pass


class ClientConnectionError(ClientError):
    """Raised due to network connectivity-related issues"""
    pass


class ClientCheckpointRequiredError(ClientError):
    """Raise when IG detects suspicious activity from your account"""

    @property
    def challenge_url(self):
        try:
            error_info = json.loads(self.error_response)
            return error_info.get('challenge', {}).get('url') or error_info.get('checkpoint_url')
        except ValueError as ve:
            logger.warning('Error parsing error response: {}'.format(str(ve)))
        return None


class ClientChallengeRequiredError(ClientCheckpointRequiredError):
    """Raise when IG detects suspicious activity from your account"""
    pass


class ClientSentryBlockError(ClientError):
    """Raise when IG has flagged your account for spam or abusive behavior"""
    pass


class ClientFeedbackRequiredError(ClientError):
    """Raise when IG has flagged your account for spam or abusive behavior"""
    pass

