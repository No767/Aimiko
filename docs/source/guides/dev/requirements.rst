Requirements
==================================


Software Requirements
---------------------
Before you get started, please ensure you have the following installed:

- `Git <https://git-scm.com>`_
- `Python 3 <https://python.org>`_
- `Poetry <https://python-poetry.org>`_
- `Docker <https://docker.com>`_
- Discord Account + App

.. CAUTION::
   Aiko is natively developed for Linux. Development should work on Windows but it is highly untested.

Package Prerequisites
----------------------

Debian/Ubuntu
^^^^^^^^^^^^^

.. code-block:: bash

    sudo apt-get install libffi-dev python3-dev libsodium-dev libopus-dev  \
    libssl-dev curl git


Fedora
^^^^^^^^^^

.. code-block:: bash

    sudo dnf install libffi-devel libsodium-devel python3.11-devel openssl-devel \
    opus-devel curl git

OpenSUSE
^^^^^^^^

.. code-block:: bash

    sudo zypper install openssl-devel libffi-devel \
    python311-devel libsodium git curl

Arch Linux
^^^^^^^^^^

.. code-block:: bash

    sudo pacman -S --needed openssl libffi python libsodium opus git curl

MacOS
^^^^^

.. code-block:: bash

    brew install python openssl libffi git curl make opus libsodium