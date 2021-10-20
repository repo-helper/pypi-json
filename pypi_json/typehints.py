#!/usr/bin/env python3
#
#  typehints.py
"""
Type hints.
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
import typing

if typing.TYPE_CHECKING:
	# 3rd party
	from typing_extensions import TypedDict
else:  # pragma: no cover
	try:
		# 3rd party
		import typing_extensions
		TypedDict = typing_extensions.TypedDict
	except ImportError:
		TypedDict = dict

__all__ = ["DistributionPackageDict", "FileURL", "ProjectInfoDict", "VulnerabilityInfoDict", "Self"]

Self = typing.TypeVar("Self")


class ProjectInfoDict(TypedDict):
	"""
	Generic information about a specific version of a project.
	"""

	#: The name of the company or individual who created the project.
	author: str

	#: The author's email address.
	author_email: str

	#: URL to find issues and bugs for the project.
	bugtrack_url: typing.Optional[str]

	#: Trove Classifiers for the project.
	classifiers: typing.List[str]

	description: str

	description_content_type: str

	#: URL to the project's documentation.
	docs_url: typing.Optional[str]

	#: Deprecated
	download_url: str

	#: Deprecated
	downloads: typing.Dict[str, int]

	#: URL to project home page
	home_page: str

	#: Keywords to use for project searching.
	keywords: str

	#: The project's open source license.
	license: str  # noqa: A003  # pylint: disable=redefined-builtin

	#: Project maintainer name.
	maintainer: str

	#: Project maintainer email address.
	maintainer_email: str

	#: Project's raw (non-normailzed name).
	name: str

	#: URL to the project page.
	package_url: str

	#: Deprecated
	platform: str

	#: URL to the project page.
	project_url: str

	#: Additional URLs that are relevant to the project.
	project_urls: typing.Dict[str, str]

	#: URL of the release page of this version of the project.
	release_url: str

	#: Project dependencies.
	requires_dist: typing.Optional[typing.List[str]]

	#: Python runtime version required for project.
	requires_python: typing.Optional[str]

	#: A one-line summary of what the distribution does.
	summary: str

	#: A string containing the distribution’s version number in the format specified in :pep:`440`.
	version: str

	#: Whether this version has been yanked. As defined in :pep:`592`.
	yanked: bool

	#: The reason for applying a :pep:`592` version yank.
	yanked_reason: typing.Optional[str]


class DistributionPackageDict(TypedDict):
	"""
	Information about a versioned archive file from which a Python project release can be installed.
	"""

	#: Deprecated
	comment_text: str

	#: The file checksums.
	digests: typing.Dict[str, str]

	#: Deprecated
	downloads: int

	#: The basename of the package file (including extension).
	filename: str

	#: Whether the package file is accompanied by a PGP signature file.
	has_sig: bool

	#: Deprecated
	md5_digest: str

	packagetype: str
	"""
	The distribution package type.

	Possible values include ``'bdist_wheel'``, ``'sdist'``, ``'bdist_wininst'``, ``'bdist_egg'``, ``'bdist_msi'``,
	``'bdist_dumb'``, ``'bdist_rpm'``, and ``'bdist_dmg'``.
	"""

	#: Either ``'source'`` or a :pep:`425` Python tag.
	python_version: str

	#: Python runtime version required for project.
	requires_python: typing.Optional[str]

	#: The file size in bytes
	size: int

	#: The time the file was uploaded, in the format ``'%Y-%m-%dT%H:%M:%S'``.
	upload_time: str

	#: The time the file was uploaded, in ISO 8601 format.
	upload_time_iso_8601: str

	#: The URL from which the package file can be downloaded.
	url: str

	#: Whether this version has been yanked. As defined in :pep:`592`.
	yanked: bool

	#: The reason for applying a :pep:`592` version yank.
	yanked_reason: typing.Optional[str]


class FileURL(TypedDict):
	"""
	Represents the output of
	:meth:`ProjectMetadata.get_releases_with_digests <pypi_json.ProjectMetadata.get_releases_with_digests>`.
	"""  # noqa: D400

	url: str
	digest: str


class VulnerabilityInfoDict(TypedDict):
	"""
	Information about a vulnerability affecting a project's.

	PyPI receives reports on vulnerabilities in the packages hosted on it from the
	`Open Source Vulnerabilities project <https://osv.dev/>`_,
	which in turn ingests vulnerabilities from the
	`Python Packaging Advisory Database <https://github.com/pypa/advisory-db>`_.

	.. versionadded:: 0.2.0
	"""

	#: The unique identifier of the vulnerability, e.g. ``"PYSEC-001"``.
	id: str  # noqa: A003  # pylint: disable=redefined-builtin

	#: The source of the vulnerability information.
	source: str

	#: A URL giving further information about the vulnerability.
	link: str

	#: Aliases of the vulnerability.
	aliases: typing.List[str]

	#: Additional details about the vulnerability.
	details: str

	#: The version(s) the vulnerability was fixed in, e.g. ``["3.3.2"]``.
	fixed_in: typing.List[str]
