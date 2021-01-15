#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest  # noqa: F401
"""Tests for handling Molfiles."""

cif_cu = """\
# CIF file 

data_findsym-output
_audit_creation_method FINDSYM

_chemical_name_mineral 'Copper'
_chemical_formula_sum 'Cu'
 
loop_
_publ_author_name
 'M. E. Straumanis'
 'L. S. Yu'
_journal_name_full
;
Acta Crystallographica A
;
_journal_volume 25
_journal_year 1969
_journal_page_first 676
_journal_page_last 682
_publ_Section_title
;
 Lattice parameters, densities, expansion coefficients and perfection of structure of Cu and of Cu-In $\alpha$ phase
;

_aflow_proto 'A_cF4_225_a' 
_aflow_params 'a' 
_aflow_params_values '3.61491' 
_aflow_Strukturbericht 'A1' 
_aflow_Pearson 'cF4' 

_symmetry_space_group_name_Hall "-F 4 2 3"
_symmetry_space_group_name_H-M "F m -3 m"
_symmetry_Int_Tables_number 225

_cell_length_a    3.61491
_cell_length_b    3.61491
_cell_length_c    3.61491
_cell_angle_alpha 90.00000
_cell_angle_beta  90.00000
_cell_angle_gamma 90.00000
 
loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1 x,y,z
2 x,-y,-z
3 -x,y,-z
4 -x,-y,z
5 y,z,x
6 y,-z,-x
7 -y,z,-x
8 -y,-z,x
9 z,x,y
10 z,-x,-y
11 -z,x,-y
12 -z,-x,y
13 -y,-x,-z
14 -y,x,z
15 y,-x,z
16 y,x,-z
17 -x,-z,-y
18 -x,z,y
19 x,-z,y
20 x,z,-y
21 -z,-y,-x
22 -z,y,x
23 z,-y,x
24 z,y,-x
25 -x,-y,-z
26 -x,y,z
27 x,-y,z
28 x,y,-z
29 -y,-z,-x
30 -y,z,x
31 y,-z,x
32 y,z,-x
33 -z,-x,-y
34 -z,x,y
35 z,-x,y
36 z,x,-y
37 y,x,z
38 y,-x,-z
39 -y,x,-z
40 -y,-x,z
41 x,z,y
42 x,-z,-y
43 -x,z,-y
44 -x,-z,y
45 z,y,x
46 z,-y,-x
47 -z,y,-x
48 -z,-y,x
49 x,y+1/2,z+1/2
50 x,-y+1/2,-z+1/2
51 -x,y+1/2,-z+1/2
52 -x,-y+1/2,z+1/2
53 y,z+1/2,x+1/2
54 y,-z+1/2,-x+1/2
55 -y,z+1/2,-x+1/2
56 -y,-z+1/2,x+1/2
57 z,x+1/2,y+1/2
58 z,-x+1/2,-y+1/2
59 -z,x+1/2,-y+1/2
60 -z,-x+1/2,y+1/2
61 -y,-x+1/2,-z+1/2
62 -y,x+1/2,z+1/2
63 y,-x+1/2,z+1/2
64 y,x+1/2,-z+1/2
65 -x,-z+1/2,-y+1/2
66 -x,z+1/2,y+1/2
67 x,-z+1/2,y+1/2
68 x,z+1/2,-y+1/2
69 -z,-y+1/2,-x+1/2
70 -z,y+1/2,x+1/2
71 z,-y+1/2,x+1/2
72 z,y+1/2,-x+1/2
73 -x,-y+1/2,-z+1/2
74 -x,y+1/2,z+1/2
75 x,-y+1/2,z+1/2
76 x,y+1/2,-z+1/2
77 -y,-z+1/2,-x+1/2
78 -y,z+1/2,x+1/2
79 y,-z+1/2,x+1/2
80 y,z+1/2,-x+1/2
81 -z,-x+1/2,-y+1/2
82 -z,x+1/2,y+1/2
83 z,-x+1/2,y+1/2
84 z,x+1/2,-y+1/2
85 y,x+1/2,z+1/2
86 y,-x+1/2,-z+1/2
87 -y,x+1/2,-z+1/2
88 -y,-x+1/2,z+1/2
89 x,z+1/2,y+1/2
90 x,-z+1/2,-y+1/2
91 -x,z+1/2,-y+1/2
92 -x,-z+1/2,y+1/2
93 z,y+1/2,x+1/2
94 z,-y+1/2,-x+1/2
95 -z,y+1/2,-x+1/2
96 -z,-y+1/2,x+1/2
97 x+1/2,y,z+1/2
98 x+1/2,-y,-z+1/2
99 -x+1/2,y,-z+1/2
100 -x+1/2,-y,z+1/2
101 y+1/2,z,x+1/2
102 y+1/2,-z,-x+1/2
103 -y+1/2,z,-x+1/2
104 -y+1/2,-z,x+1/2
105 z+1/2,x,y+1/2
106 z+1/2,-x,-y+1/2
107 -z+1/2,x,-y+1/2
108 -z+1/2,-x,y+1/2
109 -y+1/2,-x,-z+1/2
110 -y+1/2,x,z+1/2
111 y+1/2,-x,z+1/2
112 y+1/2,x,-z+1/2
113 -x+1/2,-z,-y+1/2
114 -x+1/2,z,y+1/2
115 x+1/2,-z,y+1/2
116 x+1/2,z,-y+1/2
117 -z+1/2,-y,-x+1/2
118 -z+1/2,y,x+1/2
119 z+1/2,-y,x+1/2
120 z+1/2,y,-x+1/2
121 -x+1/2,-y,-z+1/2
122 -x+1/2,y,z+1/2
123 x+1/2,-y,z+1/2
124 x+1/2,y,-z+1/2
125 -y+1/2,-z,-x+1/2
126 -y+1/2,z,x+1/2
127 y+1/2,-z,x+1/2
128 y+1/2,z,-x+1/2
129 -z+1/2,-x,-y+1/2
130 -z+1/2,x,y+1/2
131 z+1/2,-x,y+1/2
132 z+1/2,x,-y+1/2
133 y+1/2,x,z+1/2
134 y+1/2,-x,-z+1/2
135 -y+1/2,x,-z+1/2
136 -y+1/2,-x,z+1/2
137 x+1/2,z,y+1/2
138 x+1/2,-z,-y+1/2
139 -x+1/2,z,-y+1/2
140 -x+1/2,-z,y+1/2
141 z+1/2,y,x+1/2
142 z+1/2,-y,-x+1/2
143 -z+1/2,y,-x+1/2
144 -z+1/2,-y,x+1/2
145 x+1/2,y+1/2,z
146 x+1/2,-y+1/2,-z
147 -x+1/2,y+1/2,-z
148 -x+1/2,-y+1/2,z
149 y+1/2,z+1/2,x
150 y+1/2,-z+1/2,-x
151 -y+1/2,z+1/2,-x
152 -y+1/2,-z+1/2,x
153 z+1/2,x+1/2,y
154 z+1/2,-x+1/2,-y
155 -z+1/2,x+1/2,-y
156 -z+1/2,-x+1/2,y
157 -y+1/2,-x+1/2,-z
158 -y+1/2,x+1/2,z
159 y+1/2,-x+1/2,z
160 y+1/2,x+1/2,-z
161 -x+1/2,-z+1/2,-y
162 -x+1/2,z+1/2,y
163 x+1/2,-z+1/2,y
164 x+1/2,z+1/2,-y
165 -z+1/2,-y+1/2,-x
166 -z+1/2,y+1/2,x
167 z+1/2,-y+1/2,x
168 z+1/2,y+1/2,-x
169 -x+1/2,-y+1/2,-z
170 -x+1/2,y+1/2,z
171 x+1/2,-y+1/2,z
172 x+1/2,y+1/2,-z
173 -y+1/2,-z+1/2,-x
174 -y+1/2,z+1/2,x
175 y+1/2,-z+1/2,x
176 y+1/2,z+1/2,-x
177 -z+1/2,-x+1/2,-y
178 -z+1/2,x+1/2,y
179 z+1/2,-x+1/2,y
180 z+1/2,x+1/2,-y
181 y+1/2,x+1/2,z
182 y+1/2,-x+1/2,-z
183 -y+1/2,x+1/2,-z
184 -y+1/2,-x+1/2,z
185 x+1/2,z+1/2,y
186 x+1/2,-z+1/2,-y
187 -x+1/2,z+1/2,-y
188 -x+1/2,-z+1/2,y
189 z+1/2,y+1/2,x
190 z+1/2,-y+1/2,-x
191 -z+1/2,y+1/2,-x
192 -z+1/2,-y+1/2,x
 
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_label
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
Cu1 Cu   4 a 0.00000 0.00000 0.00000 1.00000
"""  # noqa: E501, W291, W293


def test_to_mmcif_text(AceticAcid):
    """Write a manually created system to mmcif"""
    correct = """\
# Generated by MolSSI SEAMM
data_CH2O
_chem_comp.name 'C2 H4 O2'
_chem_comp.id 'CH2O'
_chem_comp.formula   'C2 H4 O2'
_chemical_formula_structural   'C H2 O'
_chemical_formula_sum   'C2 H4 O2'
loop_
 _chem_comp_atom.comp_id
 _chem_comp_atom.atom_id
 _chem_comp_atom.type_symbol
 _chem_comp_atom.model_Cartn_x
 _chem_comp_atom.model_Cartn_y
 _chem_comp_atom.model_Cartn_z
 _chem_comp_atom.pdbx_model_Cartn_x_ideal
 _chem_comp_atom.pdbx_model_Cartn_y_ideal
 _chem_comp_atom.pdbx_model_Cartn_z_ideal
 _chem_comp_atom.pdbx_component_comp_id
 _chem_comp_atom.pdbx_residue_numbering
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


def test_from_cif_text(configuration):
    """Test converting a cif file into a configuration."""

    configuration.from_cif_text(cif_cu)

    assert configuration.atoms.n_atoms == 4
