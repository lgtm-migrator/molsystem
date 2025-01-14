#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bonds` in the `molsystem` package."""

import pytest  # noqa: F401


def test_construction(AceticAcid):
    """Simplest test that we can make an Bonds object"""
    configuration = AceticAcid
    bonds = configuration.bonds
    assert str(type(bonds)) == "<class 'molsystem.bonds._Bonds'>"


def test_iteration(AceticAcid):
    """Test that we can iterate over the bonds."""
    configuration = AceticAcid
    bonds = configuration.bonds
    i = []
    j = []
    order = []
    for bond in bonds.bonds():
        i.append(bond["i"])
        j.append(bond["j"])
        order.append(bond["bondorder"])

    assert order == [1, 1, 1, 1, 2, 1, 1]
    assert i == [1, 1, 1, 1, 5, 5, 7]
    assert j == [2, 3, 4, 5, 6, 7, 8]


def test_contains(AceticAcid):
    """Test that it contains a bond."""
    configuration = AceticAcid
    bonds = configuration.bonds
    assert 5, 7 in bonds
    assert 7, 5 in bonds


def test_does_not_contain(AceticAcid):
    """Test that does not contain a bond."""
    configuration = AceticAcid
    bonds = configuration.bonds
    assert 5, 8 not in bonds
    assert 8, 5 not in bonds


def test_get_item(AceticAcid):
    """Test that we can access a bond."""
    configuration = AceticAcid
    bonds = configuration.bonds
    bond = bonds.get_bond(5, 6)
    assert [*bond] == [5, 5, 6, 2]
    bond = bonds.get_bond(6, 5)
    assert [*bond] == [5, 5, 6, 2]


def test_delete_bond(AceticAcid):
    """Test that we can remove a bond."""
    configuration = AceticAcid
    bonds = configuration.bonds

    bonds.delete_bond(5, 7)
    assert bonds.n_bonds == 6


def test_add_bond(AceticAcid):
    """Test that we can remove a bond."""
    configuration = AceticAcid
    bonds = configuration.bonds
    bond = bonds.get_bond(5, 7)
    bonds.delete_bond(5, 7)
    assert bonds.n_bonds == 6
    bonds.append(bonds=bond)
    assert bonds.n_bonds == 7


def test_str(AceticAcid):
    """Test that we can get a string representation."""
    answer = """\
   i  j  bondorder
1  1  2          1
2  1  3          1
3  1  4          1
4  1  5          1
5  5  6          2
6  5  7          1
7  7  8          1"""
    configuration = AceticAcid
    bonds = configuration.bonds
    if str(bonds) != answer:
        print(str(bonds))
    assert str(bonds) == answer


def test_repr(AceticAcid):
    """Test that we can get a representation."""
    answer = """\
   i  j  bondorder
1  1  2          1
2  1  3          1
3  1  4          1
4  1  5          1
5  5  6          2
6  5  7          1
7  7  8          1"""
    configuration = AceticAcid
    bonds = configuration.bonds
    if repr(bonds) != answer:
        print(repr(bonds))
    assert repr(bonds) == answer


def test_adding_attribute(AceticAcid):
    """Test that we can add an attribute."""
    configuration = AceticAcid
    bonds = configuration.bonds
    bonds.add_attribute("name", coltype="str")
    bond = bonds.get_bond(5, 7)
    assert len(bond) == 5
    assert bond.keys() == ["id", "i", "j", "bondorder", "name"]


def test_adding_attribute_with_values(AceticAcid):
    """Test that we can add an attribute."""
    names = ["C-H", "C-H", "C-H", "C-C", "C=O", "C-O", "O-H"]
    configuration = AceticAcid
    bonds = configuration.bonds
    bonds.add_attribute("name", coltype="str", values=names)
    bond = bonds.get_bond(5, 7)
    assert len(bond) == 5
    assert bond.keys() == ["id", "i", "j", "bondorder", "name"]
    assert bond["name"] == "C-O"


def test_column(AceticAcid):
    """Test getting columns of the bond data."""
    answer = [1, 1, 1, 1, 2, 1, 1]
    configuration = AceticAcid
    bonds = configuration.bonds
    bondorders = bonds.get_column("bondorder")
    if bondorders != answer:
        print(bondorders)
    assert bondorders == answer


def test_set_column(AceticAcid):
    """Test setting columns of the bond data."""
    answer = [1, 1, 1, 1, 2, 3, 1]
    answer2 = """\
   i  j  bondorder
1  1  2          1
2  1  3          1
3  1  4          1
4  1  5          1
5  5  6          2
6  5  7          3
7  7  8          1"""
    configuration = AceticAcid
    bonds = configuration.bonds
    bondorders = bonds.get_column("bondorder")
    bondorders[5] = 3
    if bondorders != answer:
        print(bondorders)
    assert bondorders == answer
    if str(bonds) != answer2:
        print(str(bonds))
    assert str(bonds) == answer2
