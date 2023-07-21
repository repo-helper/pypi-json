# stdlib
import gzip
import re
import tarfile
import zipfile
from typing import Union
from urllib.parse import urlparse

# 3rd party
import pytest
from apeye import URL
from apeye.requests_url import RequestsURL
# from apeye.url import URL
from coincidence.params import param
from coincidence.regressions import AdvancedDataRegressionFixture
from domdf_python_tools.paths import PathPlus
from packaging.requirements import InvalidRequirement
from packaging.version import Version

# this package
from pypi_json import PyPIJSON


def uri_validator(x) -> bool:  # noqa: MAN001
	# Based on https://stackoverflow.com/a/38020041
	# By https://stackoverflow.com/users/1668293/alemol and https://stackoverflow.com/users/953553/andilabs
	result = urlparse(x)
	return all([result.scheme, result.netloc, result.path])


def test_get_metadata(
		advanced_data_regression: AdvancedDataRegressionFixture,
		module_cassette: PyPIJSON,
		):
	metadata = module_cassette.get_metadata("OctoCheese")
	advanced_data_regression.check(metadata)

	assert metadata.name == "octocheese"
	assert metadata.version == Version("0.3.0")


def test_get_latest_version(
		advanced_data_regression: AdvancedDataRegressionFixture,
		cassette: PyPIJSON,
		):
	metadata = cassette.get_metadata("OctoCheese", "0.1.0")
	advanced_data_regression.check(metadata)

	assert metadata.name == "octocheese"
	assert metadata.version == Version("0.1.0")
	assert metadata.get_latest_version() == Version("0.3.0")


def test_changes_to_api_july_2022():
	with PyPIJSON() as client:
		metadata = client.get_metadata("OctoCheese", "0.1.0")

		assert metadata.releases is None

		match_string = re.escape(
				"The 'releases' key is no longer included in the JSON responses for individual versions. Please call the .metadata() method without supplying a version."
				)
		with pytest.raises(DeprecationWarning, match=match_string):
			metadata.get_latest_version()

		with pytest.raises(DeprecationWarning, match=match_string):
			metadata.get_releases_with_digests()

	assert metadata.name == "octocheese"
	assert metadata.version == Version("0.1.0")
	assert isinstance(metadata.urls, list)


@pytest.mark.parametrize("version", [None, "0.1.0"])
def test_get_pypi_releases(
		advanced_data_regression: AdvancedDataRegressionFixture,
		version: str,
		module_cassette: PyPIJSON,
		):
	metadata = module_cassette.get_metadata("OctoCheese", version)

	releases = metadata.get_releases()
	assert isinstance(releases, dict)

	release_url_list = releases["0.0.2"]
	assert isinstance(release_url_list, list)

	for url in release_url_list:
		print(url)
		assert isinstance(url, str)
		assert uri_validator(url)

	advanced_data_regression.check(release_url_list)


@pytest.mark.parametrize("version", [None, "0.1.0"])
def test_get_releases_with_digests(
		advanced_data_regression: AdvancedDataRegressionFixture,
		version: str,
		module_cassette: PyPIJSON,
		):
	metadata = module_cassette.get_metadata("OctoCheese", version)

	releases = metadata.get_releases_with_digests()
	assert isinstance(releases, dict)

	release_url_list = releases["0.0.2"]
	assert isinstance(release_url_list, list)

	for url in release_url_list:
		print(url)
		assert isinstance(url, dict)

	advanced_data_regression.check(release_url_list)


@pytest.mark.parametrize(
		"url",
		[
				pytest.param((
						"https://files.pythonhosted.org/packages/fa/fb"
						"/d301018af3f22bdbf34b624037e851561914c244a26add8278e4e7273578/octocheese-0.0.2.tar.gz"
						),
								id='%'),
				pytest.param(
						URL("https://files.pythonhosted.org/packages/fa/fb")
						/ "d301018af3f22bdbf34b624037e851561914c244a26add8278e4e7273578/octocheese-0.0.2.tar.gz",
						id='^'
						),
				]
		)
def test_download_file(
		advanced_data_regression: AdvancedDataRegressionFixture, tmp_pathplus: PathPlus, url: Union[str, URL]
		):

	the_file = tmp_pathplus / "octocheese-0.0.2.tar.gz"

	with PyPIJSON() as client:
		response = client.download_file(url)

	assert response.status_code == 200
	the_file.write_bytes(response.content)

	assert the_file.is_file()

	# Check it isn't a wheel or Windows-built sdist
	assert not zipfile.is_zipfile(the_file)

	with gzip.open(the_file, 'r'):
		# Check can be opened as gzip file
		assert True

	listing = {
			"octocheese-0.0.2",  # top level directory
			"octocheese-0.0.2/octocheese",  # module
			"octocheese-0.0.2/octocheese/__init__.py",
			"octocheese-0.0.2/octocheese/__main__.py",
			"octocheese-0.0.2/octocheese/action.py",
			"octocheese-0.0.2/octocheese/colours.py",
			"octocheese-0.0.2/octocheese/core.py",
			"octocheese-0.0.2/octocheese.egg-info",  # egg-info
			"octocheese-0.0.2/octocheese.egg-info/dependency_links.txt",
			"octocheese-0.0.2/octocheese.egg-info/entry_points.txt",
			"octocheese-0.0.2/octocheese.egg-info/not-zip-safe",
			"octocheese-0.0.2/octocheese.egg-info/PKG-INFO",
			"octocheese-0.0.2/octocheese.egg-info/requires.txt",
			"octocheese-0.0.2/octocheese.egg-info/SOURCES.txt",
			"octocheese-0.0.2/octocheese.egg-info/top_level.txt",
			"octocheese-0.0.2/__pkginfo__.py",  # metadata
			"octocheese-0.0.2/LICENSE",
			"octocheese-0.0.2/MANIFEST.in",
			"octocheese-0.0.2/PKG-INFO",
			"octocheese-0.0.2/README.rst",
			"octocheese-0.0.2/requirements.txt",
			"octocheese-0.0.2/setup.cfg",
			"octocheese-0.0.2/setup.py",
			}

	with tarfile.open(the_file, "r:gz") as tar:
		assert {f.name for f in tar.getmembers()} == listing
		advanced_data_regression.check(sorted({f.name for f in tar.getmembers()}))


def test_metadata_nonexistant(cassette: PyPIJSON):
	with pytest.raises(InvalidRequirement, match="No such project 'FizzBuzz'"):
		cassette.get_metadata("FizzBuzz")


@pytest.mark.parametrize(
		"name, version",
		[
				param("domdf_python_tools", "1.0.0", idx=0),
				param("mathematical", "0.4.0", idx=0),
				param("shippinglabel", Version("0.12.0"), idx=0),
				param("numpy", Version("1.20.3"), idx=0),
				param("apeye", None, idx=0),
				param("scipy", None, idx=0),
				param("pyyaml", None, idx=0),
				param("coverage", None, idx=0),
				]
		)
def test_get_wheel_tag_mapping(
		name: str,
		version: str,
		advanced_data_regression: AdvancedDataRegressionFixture,
		cassette: PyPIJSON,
		):
	metadata = cassette.get_metadata(name, version)

	tag_url_map, non_wheel_urls = metadata.get_wheel_tag_mapping(version)
	tag_url_map_str = dict(sorted((str(k), v) for k, v in tag_url_map.items()))
	advanced_data_regression.check((tag_url_map_str, non_wheel_urls))


@pytest.mark.parametrize("name, version", [param("microsoft", "0.0.1", idx=0)])
def test_get_wheel_tag_mapping_no_files(name: str, version: str, cassette: PyPIJSON):
	metadata = cassette.get_metadata(name, version)

	with pytest.raises(ValueError, match=f"Version {version} has no files on PyPI."):
		metadata.get_wheel_tag_mapping(version)


@pytest.mark.parametrize("name, version", [param("microsoft", "0.0.1", idx=0)])
def test_get_wheel_tag_mapping_no_version(name: str, version: str, cassette: PyPIJSON):
	metadata = cassette.get_metadata(name, version)

	with pytest.raises(ValueError, match="Cannot find version 1.2.3 on PyPI."):
		metadata.get_wheel_tag_mapping(Version("1.2.3"))


def test_get_metadata_not_found(cassette: PyPIJSON):
	with pytest.raises(InvalidRequirement, match="No such project 'pypi-json'"):
		cassette.get_metadata("pypi-json", None)

	with pytest.raises(InvalidRequirement, match="No such project/version 'pypi-json' 1.2.3"):
		cassette.get_metadata("pypi-json", "1.2.3")


def test_class_misc():

	with PyPIJSON(auth=("username", "password"), endpoint="https://my.custom.pypi/") as client:
		assert client.endpoint == RequestsURL("https://my.custom.pypi/")
		assert client.endpoint_url == "https://my.custom.pypi/"
		assert client.endpoint.session.auth == ("username", "password")
		assert repr(client) == "<PyPIJSON('https://my.custom.pypi/')>"


# def test_signature():
# 	expected = "https://files.pythonhosted.org/packages/0a/6e/dd532144bcaf242417f9bacccdc0e1901e0d06e3367826193c84ea7a347b/build-0.6.0-py3-none-any.whl.asc"

# 	with PyPIJSON() as client:
# 		metadata = client.get_metadata("build", "0.6.0")
# 		assert metadata.urls[0]["has_sig"]

# 		assert client.get_signature_url(metadata.urls[0]["url"]) == expected

# 		response = client.download_file(client.get_signature_url(metadata.urls[0]["url"]))
# 		assert response.status_code == 200
# 		assert response.content.startswith(b"-----BEGIN PGP SIGNATURE-----\n\n")
# 		assert response.content.endswith(b"-----END PGP SIGNATURE-----\n")

# 		response = client.download_file(URL(client.get_signature_url(metadata.urls[0]["url"])))
# 		assert response.status_code == 200
# 		assert response.content.startswith(b"-----BEGIN PGP SIGNATURE-----\n\n")
# 		assert response.content.endswith(b"-----END PGP SIGNATURE-----\n")

# 		response = client.download_file(client.get_signature_url(URL(metadata.urls[0]["url"])))
# 		assert response.status_code == 200
# 		assert response.content.startswith(b"-----BEGIN PGP SIGNATURE-----\n\n")
# 		assert response.content.endswith(b"-----END PGP SIGNATURE-----\n")

# 		response = client.download_file(URL(client.get_signature_url(URL(metadata.urls[0]["url"]))))
# 		assert response.status_code == 200
# 		assert response.content.startswith(b"-----BEGIN PGP SIGNATURE-----\n\n")
# 		assert response.content.endswith(b"-----END PGP SIGNATURE-----\n")


def test_custom_endpoint():

	my_endpoint = RequestsURL("http://my.pypi")
	fake_session = object()
	my_endpoint.session = fake_session  # type: ignore[assignment]

	client = PyPIJSON(my_endpoint)
	assert client.endpoint == my_endpoint
	assert client.endpoint.session is fake_session

	my_endpoint = RequestsURL("http://my.pypi")
	fake_session = object()

	client = PyPIJSON(my_endpoint, session=fake_session)  # type: ignore[arg-type]
	assert client.endpoint == my_endpoint
	assert client.endpoint.session is fake_session
