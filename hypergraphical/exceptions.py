"""Hypergraphical exceptions."""


class HypergraphicalException(Exception):
    """Base exception class for any hypergraphical exception."""


class S3BucketException(HypergraphicalException):
    """A generic S3 bucket exception."""


class S3BucketNotFoundException(HypergraphicalException):
    """The given S3 bucket does not exist."""


class S3BucketForbiddenException(HypergraphicalException):
    """Permissions are not granted to access the given S3 bucket."""
