# Sign and verify RPI PICO UF2 firmware binaries

<img align="right" src="https://raw.githubusercontent.com/vroncevic/picosign/dev/docs/psf-logo-alpha.png" width="20%">

**picosign** is a Python boot tool for signing and verifying Raspberry Pi Pico UF2 firmware binaries.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![picosign python checker](https://github.com/vroncevic/picosign/actions/workflows/picosign_python_checker.yml/badge.svg)](https://github.com/vroncevic/picosign/actions/workflows/picosign_python_checker.yml) [![picosign package checker](https://github.com/vroncevic/picosign/actions/workflows/picosign_package_checker.yml/badge.svg)](https://github.com/vroncevic/picosign/actions/workflows/picosign_package.yml) [![picosign interface checker](https://github.com/vroncevic/picosign/actions/workflows/picosign_interface_checker.yml/badge.svg)](https://github.com/vroncevic/picosign/actions/workflows/picosign_interface_checker.yml) [![picosign isp checker](https://github.com/vroncevic/picosign/actions/workflows/picosign_isp_checker.yml/badge.svg)](https://github.com/vroncevic/picosign/actions/workflows/picosign_isp_checker.yml) [![picosign srp checker](https://github.com/vroncevic/picosign/actions/workflows/picosign_srp_checker.yml/badge.svg)](https://github.com/vroncevic/picosign/actions/workflows/picosign_srp_checker.yml) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/picosign.svg)](https://github.com/vroncevic/picosign/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/picosign.svg)](https://github.com/vroncevic/picosign/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [🚀 Installation](#-installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [📦 Dependencies](#-dependencies)
- [📁 Tool structure](#-tool-structure)
  - [✨ Features](#-features)
- [📊 Code coverage](#-code-coverage)
- [🛠 Usage](#-usage)
- [📚 Docs](#-docs)
- [👥 Contributing](#-contributing)
- [📄 Copyright and licence](#-copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### 🚀 Installation

Used next development environment

![debian linux os](https://raw.githubusercontent.com/vroncevic/picosign/dev/docs/debtux.png)

[![picosign python3 build](https://github.com/vroncevic/picosign/actions/workflows/picosign_python3_build.yml/badge.svg)](https://github.com/vroncevic/picosign/actions/workflows/picosign_python3_build.yml)

Currently there are four ways to install package
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

**picosign** is located at **[pypi.org](https://pypi.org/project/picosign/)**.

You can install by using pip

```bash
# python3
pip3 install picosign
```

##### Install using build

Navigate to release **[page](https://github.com/vroncevic/picosign/releases/)** download and extract release archive.

To install **picosign** type the following

```bash
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
```

##### Install using py setup

Navigate to **[release page](https://github.com/vroncevic/picosign/releases)** download and extract release archive.

To install **picosign** locate and run setup.py with arguments

```bash
tar xvzf picosign-x.y.z.tar.gz
cd picosign-x.y.z
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_egg_info
```

##### Install using docker

You can use Dockerfile to create image/container.

### 📦 Dependencies

**picosign** requires next modules and libraries

* [ats-utilities - Python App/Tool/Script Utilities](https://pypi.org/project/ats-utilities/)

### 📁 Tool structure

**picosign** is based on OOP and Hexagonal Architecture.

Tool structure

<details>
<summary><b>Click to expand framework structure</b></summary>

```bash
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
```
</details>

#### ✨ Features

* Adds and reads textual signatures from 220-byte padding in the first 512-byte block of UF2 binaries.
* Validates UF2 block boundaries and magic header constants (`0x0A324655`, `0x9E5D5157`).
* Provides a modular and extensible architecture based on OOP and SOLID principles.
* Includes command line interface (CLI) support via a command/executor structure.
* Robust validation of project bundles, dependencies, and options.
* High code quality with full type checking and 100% unit test coverage.

### 📊 Code coverage

<details>
<summary><b>Click to expand code coverage</b></summary>

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| `picosign/__init__.py` | 9 | 0 | 100%|
| `picosign/core/__init__.py` | 9 | 0 | 100%|
| `picosign/core/model/__init__.py` | 9 | 0 | 100%|
| `picosign/core/model/signature_data.py` | 15 | 0 | 100%|
| `picosign/core/service/__init__.py` | 9 | 0 | 100%|
| `picosign/core/service/engine.py` | 29 | 0 | 100%|
| `picosign/core/service/iservice.py` | 14 | 0 | 100%|
| `picosign/core/service/isubprocessor.py` | 14 | 0 | 100%|
| `picosign/engine.py` | 57 | 0 | 100%|
| `picosign/infrastructure/__init__.py` | 9 | 0 | 100%|
| `picosign/infrastructure/cli/__init__.py` | 9 | 0 | 100%|
| `picosign/infrastructure/cli/engine.py` | 43 | 0 | 100%|
| `picosign/infrastructure/cli/icli.py` | 15 | 0 | 100%|
| `picosign/infrastructure/cli/setup/__init__.py` | 9 | 0 | 100%|
| `picosign/infrastructure/cli/setup/bundle.py` | 22 | 0 | 100%|
| `picosign/infrastructure/cli/setup/dep_validator.py` | 36 | 0 | 100%|
| `picosign/infrastructure/cli/setup/dependencies.py` | 18 | 0 | 100%|
| `picosign/infrastructure/cli/setup/factory.py` | 40 | 0 | 100%|
| `picosign/infrastructure/cli/setup/keys.py` | 26 | 0 | 100%|
| `picosign/infrastructure/cli/setup/opt_validator.py` | 34 | 0 | 100%|
| `picosign/infrastructure/cli/setup/options.py` | 15 | 0 | 100%|
| `picosign/infrastructure/cli/setup/registry.py` | 31 | 0 | 100%|
| `picosign/infrastructure/cli/setup/validator.py` | 43 | 0 | 100%|
| `picosign/infrastructure/command/__init__.py` | 9 | 0 | 100%|
| `picosign/infrastructure/command/command.py` | 16 | 0 | 100%|
| `picosign/infrastructure/command/icommand_definition.py` | 14 | 0 | 100%|
| `picosign/infrastructure/command/icommand_executor.py` | 14 | 0 | 100%|
| `picosign/infrastructure/command/read_command_definition.py` | 26 | 0 | 100%|
| `picosign/infrastructure/command/read_command_executor.py` | 29 | 0 | 100%|
| `picosign/infrastructure/command/sign_command_definition.py` | 26 | 0 | 100%|
| `picosign/infrastructure/command/sign_command_executor.py` | 29 | 0 | 100%|
| `picosign/infrastructure/subprocessor.py` | 101 | 0 | 100%|
| `picosign/setup/__init__.py` | 9 | 0 | 100%|
| `picosign/setup/bundle.py` | 23 | 0 | 100%|
| `picosign/setup/dep_validator.py` | 36 | 0 | 100%|
| `picosign/setup/dependencies.py` | 19 | 0 | 100%|
| `picosign/setup/factory.py` | 43 | 0 | 100%|
| `picosign/setup/keys.py` | 27 | 0 | 100%|
| `picosign/setup/opt_validator.py` | 34 | 0 | 100%|
| `picosign/setup/options.py` | 12 | 0 | 100%|
| `picosign/setup/registry.py` | 32 | 0 | 100%|
| `picosign/setup/validator.py` | 48 | 0 | 100%|
| **Total** | 1062 | 0 | 100% |

</details>

### 🛠 Usage

Install package

```bash
pip3 install picosign
```

Prepare main entry point by downloading [main.py](https://raw.githubusercontent.com/vroncevic/picosign/main/main.py) or create your own.

```bash
wget -O main.py https://raw.githubusercontent.com/vroncevic/picosign/main/main.py
```

Embed signature into a UF2 firmware binary:

```bash
python3 main.py sign --file firmware.uf2 --signature "AUTHOR: Vladimir Roncevic | VERSION: 1.0.0"
```

Read signature from a UF2 firmware binary:

```bash
python3 main.py read --file firmware.uf2
```

### 📚 Docs

[![Documentation Status](https://readthedocs.org/projects/picosign/badge/?version=latest)](https://picosign.readthedocs.io/en/latest/?badge=latest)

More documentation and info at

* [picosign.readthedocs.io](https://picosign.readthedocs.io)
* [www.python.org](https://www.python.org/)

### 👥 Contributing

[Contributing to picosign](CONTRIBUTING.md)

### 📄 Copyright and licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2026 by [vroncevic.github.io/picosign](https://vroncevic.github.io/picosign)

**picosign** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/picosign/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)