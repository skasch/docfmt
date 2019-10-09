#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The google module.

The Google module handles Google-style docstrings.

Created by Romain Mondon-Cancel on 2019/10/08 20:04.
"""

import dataclasses as dc
import enum
import typing as t


class SectionName(enum.Enum):
    Args = "Arguments:"
    Arguments = "Arguments:"
    Attention = "Attention:"
    Attributes = "Attributes:"
    Caution = "Caution:"
    Danger = "Danger:"
    Error = "Error:"
    Example = "Examples:"
    Examples = "Examples:"
    Hint = "Hint:"
    Important = "Important:"
    KeywordArgs = "Keyword Arguments:"
    KeywordArguments = "Keyword Arguments:"
    Methods = "Methods:"
    Notes = "Notes:"
    OtherParameters = "Other Parameters:"
    Parameters = "Parameters:"
    Return = "Returns:"
    Returns = "Returns:"
    Raises = "Raises:"
    References = "References:"
    SeeAlso = "See Also:"
    Tip = "Tip:"
    Todo = "Todo:"
    Warning = "Warnings:"
    Warnings = "Warnings:"
    Warns = "Warns:"
    Yield = "Yields:"
    Yields = "Yields:"

    def __str__(self) -> str:
        return self.value


@dc.dataclass
class NamedBlock:
    name: str
    content: "Block"
    option: t.List[str] = dc.field(default_factory=list)


@dc.dataclass
class CodeBlock:
    content: str
    output: t.Optional[str] = None


@dc.dataclass
class Section:
    name: t.Union[SectionName, str]
    content: "Block"


SingleBlock = t.Union[str, CodeBlock, NamedBlock]
Block = t.Union[SingleBlock, t.List[SingleBlock]]


@dc.dataclass
class SyntaxTree:
    description: str
    sections: t.List[t.Union[Block, Section]]
    long_description: t.List[str] = dc.field(default_factory=list)


class Error(Exception):
    def __init__(self, docstring: str, message: t.Optional[str] = None):
        self.docstring = docstring
        if message is None:
            message = f"An error occurred with docstring {docstring}."
        super().__init__(message)


class MissingDescriptionError(Error):
    """Exception raised when a docstring is missing the mandatory description."""

    def __init__(self, docstring: str):
        super().__init__(docstring, "Missing mandatory description in docstring.")


def clear_empty_lines(lines: t.List[str]) -> t.Tuple[t.List[str], bool]:
    has_cleared_something = False
    while lines and lines[0].strip() == "":
        has_cleared_something = True
        lines = lines[1:]
    return lines, has_cleared_something


def is_section_header(line: str) -> t.Tuple[bool, t.Optional[SectionName]]:
    section_name = None
    line = line.strip()
    is_section_ = line and line[-1] == ":" or False
    if is_section_:
        section_string = line[:-1].replace(" ", "")
        is_section_ = is_section_ and section_string in SectionName.__members__
        if is_section_:
            section_name = SectionName[section_string]
    return is_section_, section_name


def is_line_valid(line: str, with_indent: t.Optional[int]) -> bool:
    return line.strip() != "" and (
        with_indent is None or line[:with_indent] == " " * with_indent
    )


def extract_paragraph(
    lines: t.List[str], with_indent: t.Optional[int] = None
) -> t.Tuple[str, t.List[str]]:
    paragraph_lines = []
    while lines and is_line_valid(lines[0], with_indent):
        paragraph_lines.append(lines[0].strip())
        lines = lines[1:]
    return (" ".join(paragraph_lines), lines)


def build_tree(docstring: str) -> SyntaxTree:
    description = ""
    long_description = []
    sections = []
    lines = docstring.split("\n")
    lines, _ = clear_empty_lines(lines)
    if not lines:
        raise MissingDescriptionError(docstring)
    description, lines = extract_paragraph(lines)
    lines, _ = clear_empty_lines(lines)
    if not lines:
        return SyntaxTree(description, sections, long_description)
    while lines and not is_section_header(lines[0])[0]:
        single_long_description, lines = extract_paragraph(lines)
        long_description.append(single_long_description)
        lines, _ = clear_empty_lines(lines)
    return SyntaxTree(description, sections, long_description)
