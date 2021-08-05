# stdlib
import os
from pathlib import Path
from typing import Callable, Type, TypeVar

# 3rd party
import pytest
from _pytest.fixtures import FixtureRequest
from apeye.url import URL
from betamax import Betamax  # type: ignore
from domdf_python_tools.paths import PathPlus
from packaging.tags import Tag
from pytest_regressions.data_regression import RegressionYamlDumper  # type: ignore
from shippinglabel.pypi import PYPI_API

# this package
from pypi_json import PyPIJSON

pytest_plugins = ("coincidence", )

_C = TypeVar("_C", bound=Callable)

with Betamax.configure() as config:
	config.cassette_library_dir = PathPlus(__file__).parent / "cassettes"


@pytest.fixture()
def cassette(request: FixtureRequest):
	"""
	Provides a Betamax cassette scoped to the test function
	which record and plays back interactions with the PyPI API.
	"""  # noqa: D400

	with PyPIJSON() as client, Betamax(client.endpoint.session) as vcr:
		vcr.use_cassette(request.node.name, record="once")

		yield client


@pytest.fixture()
def module_cassette(request: FixtureRequest):
	"""
	Provides a Betamax cassette scoped to the test module
	which record and plays back interactions with the PyPI API.
	"""  # noqa: D400

	cassette_name = request.module.__name__.split('.')[-1]

	with PyPIJSON() as client, Betamax(client.endpoint.session) as vcr:
		# print(f"Using cassette {cassette_name!r}")
		vcr.use_cassette(cassette_name, record="none")

		yield client


def _representer_for(*data_type: Type):

	def deco(representer_fn: _C) -> _C:
		for dtype in data_type:
			RegressionYamlDumper.add_custom_yaml_representer(dtype, representer_fn)

		return representer_fn

	return deco


@_representer_for(URL, Tag)
def _represent_sequences(dumper: RegressionYamlDumper, data):
	return dumper.represent_str(str(data))
