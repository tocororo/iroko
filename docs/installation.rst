..
    Copyright (C) 2022 UPR.

    iroko is free software; you can redistribute it and/or modify it under
    the terms of the MIT License; see LICENSE file for more details.

Dev environment for iroko:

1- to install pyenv follow:
https://github.com/pyenv/pyenv#automatic-installer

2- install and set python 3.9.16:
pyenv install 3.9.16
pyenv global 3.9.16

3- install node v14

4- to install poetry follow:
https://python-poetry.org/docs/#installing-with-pipx

5- setup env
poetry shell
poetry install
poetry run iroko collect -v
poetry run iroko webpack buildall

6- run server
./server-local

Deployment
============
iroko 0.3.4

python 3.9

Debian 11 Bullseye


.. include:: ../INSTALL.rst

