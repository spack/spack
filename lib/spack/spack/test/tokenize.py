# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import pytest

from spack.tokenize import Token, TokenBase, Tokenizer, fast_regex


class DummyTokens(TokenBase):
    KEYVALUE = r"(?P<key>[a-zA-Z]+)=(?P<val>[0-9]+)"
    WORD = r"[a-zA-Z]+"
    NUMBER = r"[0-9]+"


def test_token_base():
    assert DummyTokens.WORD.regex == r"[a-zA-Z]+"
    assert str(DummyTokens.WORD) == "WORD"


def test_token_equality():
    t1 = Token(DummyTokens.WORD, "hello", 0, 5)
    t2 = Token(DummyTokens.WORD, "hello", 1, 6)  # Equal despite diff position
    t3 = Token(DummyTokens.NUMBER, "hello", 0, 5)
    t4 = Token(DummyTokens.WORD, "world", 0, 5)

    assert t1 == t2
    assert t1 != t3
    assert t1 != t4


def test_token_str_repr():
    t = Token(DummyTokens.WORD, "hello")
    assert "WORD" in str(t)
    assert "hello" in str(t)
    
    t_sub = Token(DummyTokens.KEYVALUE, "a=1", key="a", val="1")
    assert "key" in str(t_sub)
    assert "val" in str(t_sub)
    assert repr(t_sub) == str(t_sub)


def test_tokenizer():
    tokenizer = Tokenizer(DummyTokens)
    
    # Test simple tokenization
    tokens = list(tokenizer.tokenize("hello123world"))
    assert len(tokens) == 3
    assert tokens[0] == Token(DummyTokens.WORD, "hello")
    assert tokens[1] == Token(DummyTokens.NUMBER, "123")
    assert tokens[2] == Token(DummyTokens.WORD, "world")

    # Test subvalues parsing
    tokens = list(tokenizer.tokenize("age=25"))
    assert len(tokens) == 1
    assert tokens[0] == Token(DummyTokens.KEYVALUE, "age=25", key="age", val="25")
    assert tokens[0].subvalues == {"key": "age", "val": "25"}


def test_fast_regex():
    mapping = {"WORD": r"[a-zA-Z]+", "NUM": r"\d+"}
    
    # with skip_whitespace=True
    pattern = fast_regex(mapping)
    assert isinstance(pattern, re.Pattern)
    scanner = pattern.scanner("  hello 123")
    m1 = scanner.match()
    assert m1.lastgroup == "WORD"
    assert m1.group("WORD") == "hello"
    
    m2 = scanner.match()
    assert m2.lastgroup == "NUM"
    assert m2.group("NUM") == "123"

    # with skip_whitespace=False
    pattern_no_ws = fast_regex(mapping, skip_whitespace=False)
    scanner2 = pattern_no_ws.scanner("hello123")
    assert scanner2.match().lastgroup == "WORD"
    assert scanner2.match().lastgroup == "NUM"
