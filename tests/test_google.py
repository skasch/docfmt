#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for module google.

Created by Romain Mondon-Cancel on 2019/10/08 22:02.
"""

from docfmt import google


def test_clear_empty_lines():
    assert google.clear_empty_lines([]) == ([], False)
    assert google.clear_empty_lines([""]) == ([], True)
    assert google.clear_empty_lines(["   ", " ", "Hello", ""]) == (["Hello", ""], True)
    assert google.clear_empty_lines(["Hello", ""]) == (["Hello", ""], False)


def test_is_section_header():
    assert google.is_section_header("") == (False, None)
    assert google.is_section_header("    Args:") == (True, google.SectionName.Args)
    assert google.is_section_header("    ") == (False, None)
    assert google.is_section_header("    Arks:") == (False, None)
    assert google.is_section_header("    Yield") == (False, None)
    assert google.is_section_header("  Yield:") == (True, google.SectionName.Yields)


def test_build_tree():
    assert google.build_tree("Describe a simple docstring.") == google.SyntaxTree(
        "Describe a simple docstring.", [], []
    )
    assert (
        google.build_tree(
            """
        Describe a simple docstring.

        This docstring also has a long description.

        Long descriptions can have multiple paragraphs.
        """
        )
        == google.SyntaxTree(
            "Describe a simple docstring.",
            [],
            [
                "This docstring also has a long description.",
                "Long descriptions can have multiple paragraphs.",
            ],
        )
    )

