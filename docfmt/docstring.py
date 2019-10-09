#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The docstring module.

Represent a docstring.

Created by Romain Mondon-Cancel on 2019/10/08 20:14.
"""

import abc


class Docstring(abc.ABC):
    @abc.abstractmethod
    def __init__(self, docstring: str) -> None:
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass
