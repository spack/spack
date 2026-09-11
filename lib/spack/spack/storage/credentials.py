# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from typing import Optional

import spack.error


class Credentials:
    """Class for storing credentials"""

    _attributes = [
        "token",
        "token_variable",
        "access_pair_id",
        "access_pair_id_variable",
        "access_pair_secret",
        "access_pair_secret_variable",
    ]

    def __init__(self, **kwargs):

        for k, v in kwargs.items():
            if k in self._attributes:
                setattr(self, "_" + k, v)
            elif k == "access_pair":
                assert type(v) in (tuple, list)

                setattr(self, "access_pair_id", v[0])
                setattr(self, "access_pair_secret", v[1])

    @property
    def token(self) -> Optional[str]:
        token = getattr(self, "_token", None)
        if token:
            return self.token
        else:
            return self._get_cred_from_env("_token_variable")

    @property
    def access_id(self) -> Optional[str]:
        access_pair_id = getattr(self, "_access_pair_id", None)
        if access_pair_id:
            return access_pair_id
        else:
            return self._get_cred_from_env("_access_pair_id_variable")

    @property
    def access_secret(self) -> Optional[str]:
        access_pair_secret = getattr(self, "_access_pair_secret", None)
        if access_pair_secret:
            return access_pair_secret
        else:
            return self._get_cred_from_env("_access_pair_secret_variable")
        return None

    @property
    def access_profile(self) -> Optional[str]:
        access_profile = getattr(self, "_access_profile", None)
        if access_profile:
            return access_profile
        return None

    def _get_cred_from_env(self, attribute) -> Optional[str]:
        var = getattr(self, attribute, None)
        if var:
            try:
                return os.environ[var]
            except KeyError as e:
                label = " ".join([part.capitalize() for part in attribute.split("_")[:-1]])
                raise CredentialVariableNotFound(f"{label}: {var}") from e
        else:
            return None


class CredentialVariableNotFound(spack.error.SpackError):
    """Could not find the given credential variable in environment"""
