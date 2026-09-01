Sign and Verify RPI PICO UF2 Firmware Binaries
-----------------------------------------------

**picosign** is a Python boot tool for signing and verifying Raspberry Pi Pico UF2 firmware binaries.

Developed in `python <https://www.python.org/>`_ code.

The README is used to introduce the tool and provide instructions on
how to install the tool, any machine dependencies it may have and any
other information that should be provided before the tool is installed.

|picosign python checker| |picosign python package| |picosign interface checker| |picosign isp checker| |picosign srp checker| |github issues| |documentation status| |github contributors|

.. |picosign python checker| image:: https://github.com/vroncevic/picosign/actions/workflows/picosign_python_checker.yml/badge.svg
   :target: https://github.com/vroncevic/picosign/actions/workflows/picosign_python_checker.yml

.. |picosign python package| image:: https://github.com/vroncevic/picosign/actions/workflows/picosign_package_checker.yml/badge.svg
   :target: https://github.com/vroncevic/picosign/actions/workflows/picosign_package.yml

.. |picosign interface checker| image:: https://github.com/vroncevic/picosign/actions/workflows/picosign_interface_checker.yml/badge.svg
   :target: https://github.com/vroncevic/picosign/actions/workflows/picosign_interface_checker.yml

.. |picosign isp checker| image:: https://github.com/vroncevic/picosign/actions/workflows/picosign_isp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/picosign/actions/workflows/picosign_isp_checker.yml

.. |picosign srp checker| image:: https://github.com/vroncevic/picosign/actions/workflows/picosign_srp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/picosign/actions/workflows/picosign_srp_checker.yml

.. |github issues| image:: https://img.shields.io/github/issues/vroncevic/picosign.svg
   :target: https://github.com/vroncevic/picosign/issues

.. |github contributors| image:: https://img.shields.io/github/contributors/vroncevic/picosign.svg
   :target: https://github.com/vroncevic/picosign/graphs/contributors

.. |documentation status| image:: https://readthedocs.org/projects/picosign/badge/?version=latest
   :target: https://picosign.readthedocs.io/en/latest/?badge=latest

.. toctree::
   :maxdepth: 4
   :caption: Contents

   self
   modules

🚀 Installation
---------------

|picosign python3 build|

.. |picosign python3 build| image:: https://github.com/vroncevic/picosign/actions/workflows/picosign_python3_build.yml/badge.svg
   :target: https://github.com/vroncevic/picosign/actions/workflows/picosign_python3_build.yml

Navigate to release `page`_ download and extract release archive.

.. _page: https://github.com/vroncevic/picosign/releases

To install **picosign** type the following

.. code-block:: bash

    tar xvzf picosign-x.y.z.tar.gz
    cd picosign-x.y.z/
    # python3
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py 
    python3 -m pip install --upgrade setuptools
    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade build
    pip3 install -r requirements.txt
    python3 -m build --no-isolation --wheel
    pip3 install ./dist/picosign-*-py3-none-any.whl
    rm -f get-pip.py

You can use pip to install directly:

.. code-block:: bash

    # python3
    pip3 install picosign

📦 Dependencies
---------------

**picosign** requires next modules and libraries:

* `ats-utilities - Python App/Tool/Script Utilities <https://pypi.org/project/ats-utilities/>`_

📁 Tool structure
-----------------

**picosign** is based on OOP and Hexagonal Architecture (Ports & Adapters).

Tool structure:

.. code-block:: bash

    picosign/
         ├── core/
         │   ├── __init__.py
         │   ├── model/
         │   │   ├── __init__.py
         │   │   └── signature_data.py
         │   └── service/
         │       ├── engine.py
         │       ├── __init__.py
         │       ├── iservice.py
         │       └── isubprocessor.py
         ├── engine.py
         ├── infrastructure/
         │   ├── cli/
         │   │   ├── engine.py
         │   │   ├── icli.py
         │   │   ├── __init__.py
         │   │   └── setup/
         │   │       ├── bundle.py
         │   │       ├── dep_validator.py
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── keys.py
         │   │       ├── opt_validator.py
         │   │       ├── options.py
         │   │       ├── registry.py
         │   │       └── validator.py
         │   ├── command/
         │   │   ├── command.py
         │   │   ├── icommand_definition.py
         │   │   ├── icommand_executor.py
         │   │   ├── __init__.py
         │   │   ├── read_command_definition.py
         │   │   ├── read_command_executor.py
         │   │   ├── sign_command_definition.py
         │   │   └── sign_command_executor.py
         │   ├── config/
         │   │   ├── picosign.cfg
         │   │   └── picosign.logo
         │   ├── __init__.py
         │   └── subprocessor.py
         ├── __init__.py
         ├── py.typed
         └── setup/
             ├── bundle.py
             ├── dep_validator.py
             ├── dependencies.py
             ├── factory.py
             ├── __init__.py
             ├── keys.py
             ├── opt_validator.py
             ├── options.py
             ├── registry.py
             └── validator.py

     10 directories, 45 files

✨ Features
-----------

* Adds and reads textual signatures from 220-byte padding in the first 512-byte block of UF2 binaries.
* Validates UF2 block boundaries and magic header constants.
* Provides a modular and extensible architecture based on OOP and SOLID principles.
* Includes command line interface (CLI) support via a command/executor structure.
* Robust validation of project bundles, dependencies, and options.
* High code quality with full type checking and 100% unit test coverage.

📊 Code coverage
----------------

.. csv-table:: Code coverage
   :file: coverage_table.csv
   :widths: 60, 10, 10, 20
   :header-rows: 1

🛠 Usage
--------

Install package

.. code-block:: bash

    pip3 install picosign

Embed signature into a UF2 firmware binary:

.. code-block:: bash

    python3 main.py sign --file firmware.uf2 --signature "AUTHOR: Vladimir Roncevic | VERSION: 1.0.0"

Read signature from a UF2 firmware binary:

.. code-block:: bash

    python3 main.py read --file firmware.uf2

📚 Docs
-------

More documentation and info at:

* `picosign.readthedocs.io <https://picosign.readthedocs.io>`_
* `www.python.org <https://www.python.org/>`_

👥 Contributing
---------------

`Contributing to picosign <https://github.com/vroncevic/picosign/blob/dev/CONTRIBUTING.md>`_

📄 Copyright and licence
-------------------------

Copyright (C) 2026 by `vroncevic.github.io/picosign <https://vroncevic.github.io/picosign>`_

**picosign** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

|psf logo|

.. |psf logo| image:: https://raw.githubusercontent.com/vroncevic/picosign/dev/docs/psf-logo-alpha.png
   :target: https://www.python.org/psf/

|donate|

.. |donate| image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif
   :target: https://www.python.org/psf/donations/

