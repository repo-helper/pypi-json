==========
pypi-json
==========

.. start short_desc

.. documentation-summary::
	:meta:

.. end short_desc

.. start shields

.. only:: html

	.. list-table::
		:stub-columns: 1
		:widths: 10 90

		* - Docs
		  - |docs| |docs_check|
		* - Tests
		  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
		* - PyPI
		  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
		* - Anaconda
		  - |conda-version| |conda-platform|
		* - Activity
		  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
		* - QA
		  - |codefactor| |actions_flake8| |actions_mypy|
		* - Other
		  - |license| |language| |requires|

	.. |docs| rtfd-shield::
		:project: pypi-json
		:alt: Documentation Build Status

	.. |docs_check| actions-shield::
		:workflow: Docs Check
		:alt: Docs Check Status

	.. |actions_linux| actions-shield::
		:workflow: Linux
		:alt: Linux Test Status

	.. |actions_windows| actions-shield::
		:workflow: Windows
		:alt: Windows Test Status

	.. |actions_macos| actions-shield::
		:workflow: macOS
		:alt: macOS Test Status

	.. |actions_flake8| actions-shield::
		:workflow: Flake8
		:alt: Flake8 Status

	.. |actions_mypy| actions-shield::
		:workflow: mypy
		:alt: mypy status

	.. |requires| image:: https://dependency-dash.repo-helper.uk/github/repo-helper/pypi-json/badge.svg
		:target: https://dependency-dash.repo-helper.uk/github/repo-helper/pypi-json/
		:alt: Requirements Status

	.. |coveralls| coveralls-shield::
		:alt: Coverage

	.. |codefactor| codefactor-shield::
		:alt: CodeFactor Grade

	.. |pypi-version| pypi-shield::
		:project: pypi-json
		:version:
		:alt: PyPI - Package Version

	.. |supported-versions| pypi-shield::
		:project: pypi-json
		:py-versions:
		:alt: PyPI - Supported Python Versions

	.. |supported-implementations| pypi-shield::
		:project: pypi-json
		:implementations:
		:alt: PyPI - Supported Implementations

	.. |wheel| pypi-shield::
		:project: pypi-json
		:wheel:
		:alt: PyPI - Wheel

	.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/pypi-json?logo=anaconda
		:target: https://anaconda.org/domdfcoding/pypi-json
		:alt: Conda - Package Version

	.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/pypi-json?label=conda%7Cplatform
		:target: https://anaconda.org/domdfcoding/pypi-json
		:alt: Conda - Platform

	.. |license| github-shield::
		:license:
		:alt: License

	.. |language| github-shield::
		:top-language:
		:alt: GitHub top language

	.. |commits-since| github-shield::
		:commits-since: v0.3.0
		:alt: GitHub commits since tagged version

	.. |commits-latest| github-shield::
		:last-commit:
		:alt: GitHub last commit

	.. |maintained| maintained-shield:: 2023
		:alt: Maintenance

	.. |pypi-downloads| pypi-shield::
		:project: pypi-json
		:downloads: month
		:alt: PyPI - Downloads

.. end shields


Overview
--------------

.. latex-section::


``pypi-json`` is a client library for the Python JSON API. With it, you can query the Python Package Index (PyPI), and other repositories using the same API, for project metadata, including available releases and downloadable package files.


Installation
---------------

.. start installation

.. installation:: pypi-json
	:pypi:
	:github:
	:anaconda:
	:conda-channels: conda-forge, domdfcoding

.. end installation


Example
----------

.. code-block:: pycon

	>>> from pypi_json import PyPIJSON
	>>> from pprint import pprint
	>>> with PyPIJSON() as client:
	... 	requests_metadata = client.get_metadata("requests")
	>>> pkg = requests_metadata.urls[0]
	>>> pprint(pkg)
	{'comment_text': '',
	 'digests': {'md5': 'deb79adc50b8205783221cfff7075d1e',
	             'sha256': '6c1246513ecd5ecd4528a0906f910e8f0f9c6b8ec72030dc9fd154dc1a6efd24'},
	 'downloads': -1,
	 'filename': 'requests-2.26.0-py2.py3-none-any.whl',
	 'has_sig': False,
	 'md5_digest': 'deb79adc50b8205783221cfff7075d1e',
	 'packagetype': 'bdist_wheel',
	 'python_version': 'py2.py3',
	 'requires_python': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, '
	                    '!=3.5.*',
	 'size': 62251,
	 'upload_time': '2021-07-13T14:55:06',
	 'upload_time_iso_8601': '2021-07-13T14:55:06.933494Z',
	 'url': 'https://files.pythonhosted.org/packages/92/96/144f70b972a9c0eabbd4391ef93ccd49d0f2747f4f6a2a2738e99e5adc65/requests-2.26.0-py2.py3-none-any.whl',
	 'yanked': False,
	 'yanked_reason': None}
	>>> list(requests_metadata.releases.keys())[:10]
	['0.0.1', '0.10.0', '0.10.1', '0.10.2', '0.10.3', '0.10.4', '0.10.6', '0.10.7', '0.10.8', '0.11.1']



Contents
-----------

.. html-section::

.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 3
	:glob:

	api/pypi-json
	api/*
	Source
	license

.. sidebar-links::
	:caption: Links
	:github:
	:pypi: pypi-json

	Contributing Guide <https://contributing.repo-helper.uk>


.. start links

.. only:: html

	View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

	:github:repo:`Browse the GitHub Repository <repo-helper/pypi-json>`

.. end links
