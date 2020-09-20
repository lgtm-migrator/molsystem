#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest  # noqa: F401
"""Tests for handling Molfiles."""


def test_to_mmcif_text(AceticAcid):
    """Write a manually created system to mmcif"""
    correct = """\
# Generated by MolSSI SEAMM
data_CH2O
_chem_comp.name 'C2 H4 O2'
_chem_comp.id 'CH2O'
_chem_comp.formula   'C2 H4 O2'
_chemical_formula_structural   CH2O
_chemical_formula_sum   'C2 H4 O2'
loop_
 _atom_site_type_symbol
 _atom_site_label
 _atom_site_symmetry_multiplicity
 _atom_site_fract_x
 _atom_site_fract_y
 _atom_site_fract_z
 _atom_site_occupancy
MOL1 C C 1.080 0.018 -0.018 1.080 0.018 -0.018 HET 1
MOL1 H H 0.578 3.138 0.281 0.578 3.138 0.281 HET 1
MOL1 H2 H 0.721 -0.674 -0.786 0.721 -0.674 -0.786 HET 1
MOL1 H3 H 0.705 -0.314 0.953 0.705 -0.314 0.953 HET 1
MOL1 C2 C 0.571 1.390 -0.316 0.571 1.390 -0.316 HET 1
MOL1 O O -0.132 1.714 -1.257 -0.132 1.714 -1.257 HET 1
MOL1 O2 O 0.976 2.297 0.592 0.976 2.297 0.592 HET 1
MOL1 H4 H 2.172 0.016 -0.031 2.172 0.016 -0.031 HET 1
#
loop_
 _chem_comp_bond.comp_id
 _chem_comp_bond.atom_id_1
 _chem_comp_bond.atom_id_2
 _chem_comp_bond.value_order
MOL1 C H SING
MOL1 C H2 SING
MOL1 C H3 SING
MOL1 C C2 SING
MOL1 C2 O DOUB
MOL1 C2 O2 SING
MOL1 O2 H4 SING"""

    text = AceticAcid.to_mmcif_text()

    if text != correct:
        print(text)

    assert text == correct


def test_to_cif_text(vanadium):
    """Write a manually created system to mmcif"""
    correct = """\
# Generated by MolSSI SEAMM
data_V
_symmetry_space_group_name_H-M   'P 1'
_cell_length_a   3.03
_cell_length_b   3.03
_cell_length_c   3.03
_cell_angle_alpha   90.0
_cell_angle_beta    90.0
_cell_angle_gamma   90.0
_symmetry_Int_Tables_number   1
_cell_volume   27.818126999999997
_cell_formula_units_Z   2
loop_
 _symmetry_equiv_pos_site_id
 _symmetry_equiv_pos_as_xyz
  1  'x, y, z'
_chemical_formula_structural   V
_chemical_formula_sum   'V2'
loop_
 _atom_site_type_symbol
 _atom_site_label
 _atom_site_symmetry_multiplicity
 _atom_site_fract_x
 _atom_site_fract_y
 _atom_site_fract_z
 _atom_site_occupancy
V V  1  0.000 0.000 0.000  1
V V2  1  0.500 0.500 0.500  1"""

    text = vanadium.to_cif_text()

    if text != correct:
        print(text)

    assert text == correct
