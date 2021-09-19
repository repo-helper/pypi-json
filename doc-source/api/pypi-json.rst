====================
:mod:`pypi_json`
====================

.. automodule:: pypi_json
	:member-order: bysource
	:no-members:
	:autosummary-members:

.. autosummary-widths:: 40/100

.. autoclass:: pypi_json.PyPIJSON
	:member-order: bysource
	:no-show-inheritance:

.. autonamedtuple:: pypi_json.ProjectMetadata
	:member-order: bysource
	:exclude-members: __repr__

.. autovariable:: pypi_json.USER_AGENT
	:no-value:

	The structure of the User-Agent is:

	.. code-block:: python

		' '.join([
				f"pypi-json/{__version__} (https://github.com/repo-helper/pypi-json)",
				f"requests/{requests.__version__}",
				f"{platform.python_implementation()}/{platform.python_version()}",
				#  ^^^ e.g. CPython                   ^^^ e.g. 3.8.10
				])

	This global attribute should not be changed by other code.
