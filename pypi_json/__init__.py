#!/usr/bin/env python3
#
#  __init__.py
"""
PyPI JSON API client library.
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  General API layout and some documentation from
#  https://github.com/jwodder/pypi-simple
#  Copyright (c) 2018-2020 John Thorvald Wodder II
#  MIT Licensed
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import platform
from typing import Any, ClassVar, Dict, List, NamedTuple, Optional, Tuple, Union
from urllib.parse import urlparse, urlunparse

# 3rd party
import requests
from apeye import URL
from apeye.requests_url import RequestsURL, TrailingRequestsURL
from packaging.requirements import InvalidRequirement
from packaging.tags import Tag
from packaging.utils import canonicalize_name, parse_wheel_filename
from packaging.version import Version

# this package
from pypi_json.typehints import DistributionPackageDict, FileURL, ProjectInfoDict, Self, VulnerabilityInfoDict

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.2.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["PyPIJSON", "ProjectMetadata", "USER_AGENT"]

#: The User-Agent header used for requests; not used when the user provides their own session object.
USER_AGENT: str = ' '.join([
		f"pypi-json/{__version__} (https://github.com/repo-helper/pypi-json)",
		f"requests/{requests.__version__}",
		f"{platform.python_implementation()}/{platform.python_version()}",
		])


class ProjectMetadata(NamedTuple):
	"""
	Represents a project's metadata from the PyPI JSON API.

	:param info: Generic information about a specific version of a project.

	:bold-title:`Attributes:`

	.. autosummary::

		~pypi_json.ProjectMetadata.name
		~pypi_json.ProjectMetadata.version

	**Methods:**

	.. autosummary::

		~pypi_json.ProjectMetadata.get_latest_version
		~pypi_json.ProjectMetadata.get_releases_with_digests
		~pypi_json.ProjectMetadata.get_releases
		~pypi_json.ProjectMetadata.get_wheel_tag_mapping
	"""

	#: Generic information about a specific version of a project.
	info: ProjectInfoDict

	#: Monotonically increasing integer sequence that changes every time the project is updated.
	last_serial: int

	#: A mapping of version numbers to a list of artifacts associated with a version.
	releases: Dict[str, List[DistributionPackageDict]]

	#: A list of release artifacts associated with this version.
	urls: List[DistributionPackageDict]

	vulnerabilities: List[VulnerabilityInfoDict] = []
	"""
	Details of vulnerabilities from the `Open Source Vulnerabilities project <https://osv.dev/>`_.

	(*New in version 0.2.0*)
	"""

	@property
	def name(self) -> str:
		"""
		Return the normalized project name.
		"""

		return canonicalize_name(self.info["name"])

	@property
	def version(self) -> Version:
		"""
		Return the release version.
		"""

		return Version(self.info["version"])

	def get_latest_version(self) -> Version:
		"""
		Returns the version number of the latest release on PyPI for this project.

		Version numbers are sorted using the rules in :pep:`386`.
		"""

		return max(map(Version, self.releases))

	def get_releases_with_digests(self) -> Dict[str, List[FileURL]]:
		"""
		Returns a dictionary mapping PyPI release versions to download URLs and the sha256sum of the file contents.
		"""

		pypi_releases = {}

		for release, release_data in self.releases.items():

			release_urls: List[FileURL] = []

			for file in release_data:
				release_urls.append({"url": file["url"], "digest": file["digests"]["sha256"]})
			pypi_releases[release] = release_urls

		return pypi_releases

	def get_releases(self) -> Dict[str, List[str]]:
		"""
		Returns a dictionary mapping PyPI release versions to download URLs.
		"""

		pypi_releases = {}

		for release, release_data in self.get_releases_with_digests().items():
			pypi_releases[release] = [file["url"] for file in release_data]

		return pypi_releases

	def get_wheel_tag_mapping(
			self,
			version: Union[str, int, Version, None] = None,
			) -> Tuple[Dict[Tag, URL], List[URL]]:
		"""
		Constructs a mapping of wheel tags to the download URL of the wheel with relevant tag.

		This can be used alongside :func:`packaging.tags.sys_tags` to select the best wheel for the current platform.

		:param version: The version to return the mapping for. If :py:obj:`None` the current version is used.

		:returns: A tuple containing the ``tag: url`` mapping,
			and a list of download URLs for non-wheel artifacts (e.g. sdists).
		"""

		releases = self.get_releases()

		if version is None:
			version = self.info["version"]

		version = str(version)

		if version not in releases:
			raise InvalidRequirement(f"Cannot find version {version} on PyPI.")

		download_urls = list(map(URL, releases[version]))

		if not download_urls:
			raise ValueError(f"Version {version} has no files on PyPI.")

		tag_url_map = {}
		non_wheel_urls = []

		for url in download_urls:
			if url.suffix == ".whl":
				tags = parse_wheel_filename(url.name)[3]
				for tag in tags:
					tag_url_map[tag] = url
			else:
				non_wheel_urls.append(url)

		return tag_url_map, non_wheel_urls


class PyPIJSON:
	"""
	A client for fetching package information from a Python JSON API.

	If necessary, login/authentication details for the repository can be specified
	at initialization by setting the ``auth`` parameter to either a ``(username, password)``
	pair or `another authentication object accepted by requests`_.

	If more complicated session configuration is desired (e.g., setting up caching),
	the user must create and configure a :class:`requests.Session` object appropriately
	and pass it to the constructor as the ``session`` parameter.

	A :class:`~.PyPIJSON` instance can be used as a context manager that will automatically
	close its session on exit, regardless of where the session object came from.

	:param endpoint: The base URL of the JSON API to query;
		defaults to the base URL for PyPI's simple API.
		If this is a :class:`~apeye.requests_url.RequestsURL` object,
		and ``session`` or ``auth`` are not provided,
		the values are taken from the :class:`~apeye.requests_url.RequestsURL` object.

	:param auth: Optional login/authentication details for the repository;
		either a ``(username, password)`` pair or `another authentication object accepted by requests`_.

	:param session: Optional :class:`requests.Session` object to use instead of creating a fresh one.

	.. _another authentication object accepted by requests: https://requests.readthedocs.io/en/master/user/authentication/

	.. latex:clearpage::
	"""

	timeout: ClassVar[int] = 10
	"""
	The timeout for HTTP requests, in seconds.

	.. versionadded:: 0.1.1
	"""

	endpoint: TrailingRequestsURL
	"""
	The :class:`apeye.requests_url.TrailingRequestsURL` object
	representing the PyPI JSON API, with an authenticated requests session.
	"""

	def __init__(
			self,
			endpoint: Union[str, URL] = "https://pypi.org/pypi",
			auth: Any = None,
			session: Optional[requests.Session] = None
			) -> None:

		if isinstance(endpoint, RequestsURL):
			# Use the session from the RequestsURL object if the argument was not provided
			if session is None:
				session = endpoint.session

		self.endpoint = TrailingRequestsURL(endpoint)

		if session is None:
			session = requests.Session()
			session.headers["User-Agent"] = USER_AGENT

		if auth is not None:
			session.auth = auth

		self.endpoint.session = session

	@property
	def endpoint_url(self) -> str:
		"""
		The URL of the JSON API endpoint.
		"""

		return str(self.endpoint)

	def __enter__(self: Self) -> Self:
		return self

	def __exit__(self, exc_type: Any, exc_value: Any, exc_tb: Any) -> None:
		self.endpoint.session.close()

	def __repr__(self) -> str:
		"""
		Returns a string representation of the :class:`~.PyPIJSON` object.
		"""

		return f"<{self.__class__.__name__}({self.endpoint_url!r})>"

	def get_metadata(self, project: str, version: Union[str, Version, None] = None) -> ProjectMetadata:
		"""
		Returns metadata for the given project on PyPI.

		:param project:
		:param version: The desired version.
			If :py:obj:`None` the metadata for the latest release if returned.

		:raises:

			* :exc:`packaging.requirements.InvalidRequirement` if the project cannot be found on PyPI.
			* :exc:`requests.HTTPError` if an error occurs when communicating with PyPI.
		"""

		if version is None:
			query_url = self.endpoint / project / "json"
		else:
			query_url = self.endpoint / project / str(version) / "json"

		response: requests.Response = query_url.get(timeout=self.timeout)

		if response.status_code == 404:
			if version is None:
				raise InvalidRequirement(f"No such project {project!r}")
			else:
				raise InvalidRequirement(f"No such project/version {project!r} {str(version)}")
		elif response.status_code != 200:
			raise requests.HTTPError(
					f"An error occurred when obtaining project metadata for {project!r}: "
					f"HTTP Status {response.status_code}",
					response=response,
					)

		return ProjectMetadata(**response.json())

	def download_file(self, url: Union[str, URL]) -> requests.Response:
		"""
		Download the file with the given URL from PyPI.

		:param url:
		"""

		if isinstance(url, URL):
			url = str(url)

		return self.endpoint.session.get(url)

	@staticmethod
	def get_signature_url(download_url: Union[str, URL]) -> str:
		"""
		Returns the URL of the PGP signature for the download URL.

		A file only has a PGP signature if it's ``has_sig`` key is :py:obj:`True`.

		:param download_url:
		"""

		if isinstance(download_url, URL):
			download_url = str(download_url)

		u = urlparse(download_url)
		return urlunparse((u[0], u[1], u[2] + ".asc", '', '', ''))
