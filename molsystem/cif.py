# -*- coding: utf-8 -*-

"""Functions for handling CIF files

Bond Orders
-----------
1 sing	single bond
2 doub	double bond
3 trip	triple bond
4 quad	quadruple bond
5 arom	aromatic bond
6 delo	delocalized double bond
7 pi	pi bond
8 poly	polymeric bond
"""

import io
import logging
import math

import CifFile

logger = logging.getLogger(__name__)

bond_order = {
    1: "SING",
    2: "DOUB",
    3: "TRIP",
    4: "QUAD",
    5: "AROM",
    6: "DELO",
    7: "PI",
    8: "POLY",
}
to_bond_order = {j: i for i, j in bond_order.items()}


class CIFMixin:
    """A mixin for handling CIF files."""

    def read_cif_file(self, path):
        """Create new systems from a CIF file.

        Read a CIF file and create a new system from each datablock in
        the file.

        If the datablock has an ensemble, as denoted by a section
        '_pdbx_nmr_ensemble', a configuration will be created for each
        conformer. If there is a representative conformer, the current
        configuration will point to it; otherwise to the last conformer.

        Parameters
        ----------
        path : str or Path
            A string or Path object pointing to the file to be read.

        Returns
        -------
        [_System]
            List of systems created.
        """
        if "SystemDB" in str(type(self)):
            sys_db = self
        else:
            sys_db = self.system_db

        lines = []
        systems = []
        configurations = {}
        in_block = False
        block_name = ""
        with open(path, "r") as fd:
            for line in fd:
                if line[0:5] == "data_":
                    self.logger.debug(f"Found block {line}")
                    if not in_block:
                        in_block = True
                    else:
                        new_systems, new_configurations = self.from_mmcif_text(
                            "\n".join(lines)
                        )
                        self.logger.debug(
                            f"   added system {sys_db.n_systems}: {block_name}"
                        )
                        systems.extend(new_systems)
                        configurations.update(new_configurations)
                    block_name = line[5:].strip()
                    lines = []
                lines.append(line)

            if len(lines) > 0:
                # The last block just ends at the end of the file
                new_systems, new_configurations = self.from_mmcif_text("\n".join(lines))
                self.logger.debug(f"   added system {sys_db.n_systems}: {block_name}")
                systems.extend(new_systems)
                configurations.update(new_configurations)

        return systems, configurations

    def to_cif_text(self):
        """Create the text of a CIF file from this configuration.

        Returns
        -------
        text : str
            The text of the file.
        """

        lines = []

        atoms = self.atoms

        # Get the chemical formula
        formula, empirical_formula, Z = self.formula

        _id = empirical_formula.replace(" ", "")

        # And created the file, line-by-line
        lines = []
        lines.append("# Generated by MolSSI SEAMM")
        lines.append(f"data_{_id}")

        # Cell information
        if self.periodicity == 3:
            cell = self.cell
            a, b, c, alpha, beta, gamma = cell.parameters
            volume = cell.volume
            lines.append("_symmetry_space_group_name_H-M   'P 1'")
            lines.append(f"_cell_length_a   {a}")
            lines.append(f"_cell_length_b   {b}")
            lines.append(f"_cell_length_c   {c}")
            lines.append(f"_cell_angle_alpha   {alpha}")
            lines.append(f"_cell_angle_beta    {beta}")
            lines.append(f"_cell_angle_gamma   {gamma}")
            lines.append("_symmetry_Int_Tables_number   1")
            lines.append(f"_cell_volume   {volume}")
            lines.append(f"_cell_formula_units_Z   {Z}")
            lines.append("loop_")
            lines.append(" _symmetry_equiv_pos_site_id")
            lines.append(" _symmetry_equiv_pos_as_xyz")
            lines.append("  1  'x, y, z'")

        lines.append(f"_chemical_formula_structural   {empirical_formula}")
        lines.append(f"_chemical_formula_sum   '{formula}'")

        # The atoms
        lines.append("loop_")
        lines.append(" _atom_site_type_symbol")
        lines.append(" _atom_site_label")
        lines.append(" _atom_site_symmetry_multiplicity")
        lines.append(" _atom_site_fract_x")
        lines.append(" _atom_site_fract_y")
        lines.append(" _atom_site_fract_z")
        lines.append(" _atom_site_occupancy")

        # Need unique names
        if "names" in atoms:
            original_names = atoms.get_column("names")
        else:
            original_names = atoms.symbols

        names = []
        tmp = {}
        for name in original_names:
            if name in tmp:
                tmp[name] += 1
                names.append(name + str(tmp[name]))
            else:
                tmp[name] = 1
                names.append(name)

        UVW = atoms.get_coordinates(fractionals=True, in_cell="molecule")

        symbols = atoms.symbols
        for element, name, uvw in zip(symbols, names, UVW):
            u, v, w = uvw
            lines.append(f"{element} {name}  1  {u:.3f} {v:.3f} {w:.3f}  1")

        # And that is it!
        return "\n".join(lines)

    def from_cif_text(self, text):
        """Create this configuration from a CIF file..

        Parameters
        ----------
        text : str
            The text from the CIF file

        Returns
        -------
        None
        """

        cif = CifFile.ReadCif(io.StringIO(text))

        data_blocks = [*cif.keys()]

        if len(data_blocks) != 1:
            raise RuntimeError(
                f"There are {len(data_blocks)} data blocks in the cif file."
            )
        data_block = cif[data_blocks[0]]

        # Reset the system
        self.clear()
        self.periodicity = 3
        self.coordinate_system = "fractional"

        # The cell
        a = data_block["_cell_length_a"]
        b = data_block["_cell_length_b"]
        c = data_block["_cell_length_c"]
        alpha = data_block["_cell_angle_alpha"]
        beta = data_block["_cell_angle_beta"]
        gamma = data_block["_cell_angle_gamma"]
        self.cell.parameters = (a, b, c, alpha, beta, gamma)

        # Add the atoms
        # TEMPORARILY lower the symmetry to P1
        delta = 1.0e-04

        # Where is the symmetry info?
        if "_space_group_symop_operation_xyz" in data_block:
            symdata = "_space_group_symop_operation_xyz"
        elif "_symmetry_equiv_pos_as_xyz" in data_block:
            symdata = "_symmetry_equiv_pos_as_xyz"
        else:
            raise RuntimeError(
                "CIF file does not contain required symmetry information. Neither "
                "'_symmetry_equiv_pos_as_xyz' or '_space_group_symop_operation_xyz' "
                "is present."
            )
        xs = []
        ys = []
        zs = []
        symbols = []
        # May have type symbols or labels, or both. Use type symbols by preference
        if "_atom_site_type_symbol" in data_block:
            type_section = "_atom_site_type_symbol"
        elif "_atom_site_label" in data_block:
            type_section = "_atom_site_label"
        else:
            raise KeyError(
                "Neither _atom_site_type_label or _atom_site_label are in file"
            )
        for x, y, z, symbol in zip(
            data_block["_atom_site_fract_x"],
            data_block["_atom_site_fract_y"],
            data_block["_atom_site_fract_z"],
            data_block[type_section],
        ):  # yapf: disable
            if type_section == "_atom_site_label":
                if len(symbol) > 1:
                    if symbol[1].isalpha():
                        symbol = symbol[0:2]
                    else:
                        symbol = symbol[0]
            # These variables *are* used in the eval below.
            x = float(x)
            y = float(y)
            z = float(z)
            for symop in data_block[symdata]:
                x_eq, y_eq, z_eq = symop.split(",")
                x_new = eval(x_eq)
                y_new = eval(y_eq)
                z_new = eval(z_eq)
                # Translate into cell.
                x_new = x_new - math.floor(x_new)
                y_new = y_new - math.floor(y_new)
                z_new = z_new - math.floor(z_new)
                # check for almost 1, should be 0
                if abs(1 - x_new) < delta:
                    x_new = 0.0
                if abs(1 - y_new) < delta:
                    y_new = 0.0
                if abs(1 - z_new) < delta:
                    z_new = 0.0
                found = False
                for x0, y0, z0 in zip(xs, ys, zs):
                    if (
                        abs(x_new - x0) < delta
                        and abs(y_new - y0) < delta
                        and abs(z_new - z0) < delta
                    ):
                        found = True
                        break
                if not found:
                    xs.append(x_new)
                    ys.append(y_new)
                    zs.append(z_new)
                    symbols.append(symbol)
        self.atoms.append(x=xs, y=ys, z=zs, symbol=symbols)

    def to_mmcif_text(self):
        """Create the text of a mmCIF file from this configuration.

        Returns
        -------
        text : str
            The text of the file.
        """

        lines = []

        atoms = self.atoms
        bonds = self.bonds

        # Get the chemical formula
        formula, empirical_formula, Z = self.formula

        _id = empirical_formula.replace(" ", "")

        # And created the file, line-by-line
        lines = []
        lines.append("# Generated by MolSSI SEAMM")
        lines.append(f"data_{_id}")
        lines.append(f"_chem_comp.name '{formula}'")
        lines.append(f"_chem_comp.id '{_id}'")
        lines.append(f"_chem_comp.formula   '{formula}'")

        # Cell information
        if self.periodicity == 3:
            cell = self.cell
            a, b, c, alpha, beta, gamma = cell.parameters
            volume = cell.volume
            # lines.append("_symmetry_space_group_name_H-M   'P 1'")
            lines.append(f"_cell.length_a   {a}")
            lines.append(f"_cell.length_b   {b}")
            lines.append(f"_cell.length_c   {c}")
            lines.append(f"_cell.angle_alpha   {alpha}")
            lines.append(f"_cell.angle_beta    {beta}")
            lines.append(f"_cell.angle_gamma   {gamma}")
            # lines.append("_symmetry_Int_Tables_number   1")
            lines.append(f"_cell.volume   {volume}")
            lines.append(f"_cell.formula_units_Z   {Z}")
            # lines.append("loop_")
            # lines.append(" _symmetry_equiv_pos_site_id")
            # lines.append(" _symmetry_equiv_pos_as_xyz")
            # lines.append("  1  'x, y, z'")

        # lines.append(f"_chemical_formula_structural   '{empirical_formula}'")
        lines.append(f"_chemical_formula.sum   '{formula}'")

        # The atoms
        lines.append("loop_")
        lines.append(" _chem_comp_atom.comp_id")
        lines.append(" _chem_comp_atom.atom_id")
        lines.append(" _chem_comp_atom.type_symbol")
        lines.append(" _chem_comp_atom.model_Cartn_x")
        lines.append(" _chem_comp_atom.model_Cartn_y")
        lines.append(" _chem_comp_atom.model_Cartn_z")
        lines.append(" _chem_comp_atom.pdbx_model_Cartn_x_ideal")
        lines.append(" _chem_comp_atom.pdbx_model_Cartn_y_ideal")
        lines.append(" _chem_comp_atom.pdbx_model_Cartn_z_ideal")
        lines.append(" _chem_comp_atom.pdbx_component_comp_id")
        lines.append(" _chem_comp_atom.pdbx_residue_numbering")

        # Need unique names
        if "names" in atoms:
            original_names = atoms.get_column("names")
        else:
            original_names = atoms.symbols

        names = []
        tmp = {}
        for name in original_names:
            if name in tmp:
                tmp[name] += 1
                names.append(name + str(tmp[name]))
            else:
                tmp[name] = 1
                names.append(name)

        XYZ = atoms.get_coordinates(in_cell="molecule", fractionals=False)
        XYZa = atoms.get_coordinates(fractionals=False)
        XYZa = XYZ

        symbols = atoms.symbols
        for element, name, xyza, xyz in zip(symbols, names, XYZa, XYZ):
            xa, ya, za = xyza
            x, y, z = xyz
            lines.append(
                f"MOL1 {name} {element} {xa:.3f} {ya:.3f} {za:.3f} "
                f"{x:.3f} {y:.3f} {z:.3f} HET 1"
            )

        # The bonds
        lines.append("#")
        lines.append("loop_")
        lines.append(" _chem_comp_bond.comp_id")
        lines.append(" _chem_comp_bond.atom_id_1")
        lines.append(" _chem_comp_bond.atom_id_2")
        lines.append(" _chem_comp_bond.value_order")
        index = {j: i for i, j in enumerate(atoms.ids)}
        for row in bonds.bonds():
            i = index[row["i"]]
            j = index[row["j"]]
            order = bond_order[row["bondorder"]]
            nm1 = names[i]
            nm2 = names[j]
            lines.append(f"MOL1 {nm1} {nm2} {order}")

        # And that is it!
        return "\n".join(lines)

    def from_mmcif_text(self, text):
        """Create this configuration from an MMCIF file..

        Parameters
        ----------
        text : str
            The text from the MMCIF file

        Returns
        -------
        None

        Notes
        -----
        This can be called from a `SystemDB`, `_System` or `_Configuration`
        object. The behavior and errors differ depending on what type of object
        is calling it:

            `SystemDB`

            When called from a `_System` object, a new `_System` will be
            created for each datablock in the CIF data, and a configuration
            will be created to hold the structure, unless their is an NMR
            ensemble, in which case each structure in the ensemble will be
            placed in a different configuration.

            `_System`

            In this case it is an error if there is more than one datablock.
            A new configuration will be created with the structure in the CIF
            datablock, unless the CIF data contains an NMR ensemble, in which
            case a configuration will be added for each conformer.

            `_Configuration`

            It is an error if there is more than one datablock in the CIF data.
            The configuration will be cleared and the structure from CIF data
            inserted into it. If there is an NMR ensemble in the datablock, and
            the representative conformer is identified, it will be loaded into
            the configuration. Otherwise an error will be raised.
        """
        # What type of object is this?
        if "SystemDB" in str(type(self)):
            my_class = "SystemDB"
        elif "_System" in str(type(self)):
            my_class = "System"
        elif "_Configuration" in str(type(self)):
            my_class = "Configuration"

        cif = CifFile.ReadCif(io.StringIO(text))

        if my_class != "SystemDB" and len(cif) != 1:
            raise RuntimeError(f"There are {len(cif)} data blocks in the mmcif file.")

        # Loop over the datablocks, processing as we go.
        systems = []
        configurations = {}
        for name, data in cif.items():
            # Check the sanity of the input
            coordinate_system = "Cartesian"
            if "_atom_site.id" in data:
                if "_chem_comp_atom.atom_id" in data:
                    raise ValueError("Have both atom_site and chem_comp atoms")

                # Fractional or Cartesian coordinates?
                if "_atom_site.fract_x" in data:
                    coordinate_system = "fractional"
                elif "_atom_site.Cartn_x" not in data:
                    raise KeyError("Couldn't find coordinates in atom_site data")
                elif "_chem_comp_atom.atom_id" in data:
                    if "_chem_comp_atom.model_Cartn_x" not in data:
                        raise KeyError(
                            "Couldn't find coordinates in chem_comp_atom data"
                        )

            # Get the name of the system/configuration
            for key in [
                "_entry.id",
                "_chem_comp.id",
                "_chem_comp.name",
                "_chem_comp.three_letter_code",
            ]:
                if key in data:
                    name = data[key]
                    break

            key = "_pdbx_nmr_ensemble.conformers_submitted_total_number"
            ensemble = key in data
            if ensemble:
                n_ensemble = int(data[key])
                key = "_pdbx_nmr_representative.conformer_id"
                configuration_name = "model_1"
                if key in data:
                    representative = int(data[key])
                    if representative == 1:
                        configuration_name == "representative"
                else:
                    representative = None
            else:
                configuration_name = name
            if my_class == "SystemDB":
                system = self.create_system(name)
                systems.append(system)
                configuration = system.create_configuration(configuration_name)
                configurations[system.id] = [configuration]
            elif my_class == "System":
                system = self
                configuration = system.create_configuration(configuration_name)
                configurations[system.id] = [configuration]
            else:
                configuration = self
                # Reset the configuration
                configuration.clear()
                configuration.periodicity = 0
                configuration.coordinate_system = "Cartesian"
                configuration.name = configuration_name

            # Add the atoms
            atoms = configuration.atoms
            kwargs = {}

            # Get the data from the CIF file, creating columns if needed.
            for cif_key, key, _type, default in [
                ("_chem_comp_atom.atom_id", "name", "str", ""),
                ("_chem_comp_atom.alt_atom_id", None, "str", ""),
                ("_chem_comp_atom.type_symbol", "symbol", "str", ""),
                ("_chem_comp_atom.model_Cartn_x", "x", "float", 0.0),
                ("_chem_comp_atom.model_Cartn_y", "y", "float", 0.0),
                ("_chem_comp_atom.model_Cartn_z", "z", "float", 0.0),
                ("_chem_comp_atom.charge", "formal_charge", "int", 0),
                ("_chem_comp_atom.pdbx_align", None, "int", 0),
                ("_chem_comp_atom.pdbx_aromatic_flag", None, "bool", False),
                ("_chem_comp_atom.pdbx_leaving_atom_flag", None, "bool", False),
                ("_chem_comp_atom.pdbx_stereo_config", None, "bool", False),
                ("_chem_comp_atom.pdbx_component_atom_id", None, "bool", False),
                ("_atom_site.group_PDB", None, "str", "HETATOM"),
                ("_atom_site.id", None, "str", None),
                ("_atom_site.type_symbol", "symbol", "str", None),
                ("_atom_site.label_atom_id", None, "str", None),
                ("_atom_site.label_alt_id", None, "str", ""),
                ("_atom_site.label_comp_id", None, "str", None),
                ("_atom_site.label_asym_id", None, "str", None),
                ("_atom_site.label_entity_id", None, "str", None),
                ("_atom_site.label_seq_id", None, "int", None),
                ("_atom_site.pdbx_PDB_ins_code", None, "str", None),
                ("_atom_site.pdbx_PDB_model_num", "ignore", "int", None),
                ("_atom_site.Cartn_x", "x", "float", 0.0),
                ("_atom_site.Cartn_y", "y", "float", 0.0),
                ("_atom_site.Cartn_z", "z", "float", 0.0),
                ("_atom_site.fract_x", "x", "float", 0.0),
                ("_atom_site.fract_y", "y", "float", 0.0),
                ("_atom_site.fract_z", "z", "float", 0.0),
                ("_atom_site.occupancy", "occupancy", "float", 0.0),
                ("_atom_site.B_iso_or_equiv", None, "float", 0.0),
                ("_atom_site.pdbx_formal_charge", "formal_charge", "int", 0),
            ]:
                if cif_key in data:
                    if key is None:
                        key = cif_key
                    if key == "ignore":
                        key = cif_key
                    elif key not in atoms and key != "symbol":
                        atoms.add_attribute(key, _type, default=default)

                    if _type == "bool":
                        kwargs[key] = [
                            None if x in ".?" else x == "N" for x in data[cif_key]
                        ]
                    elif _type == "int":
                        kwargs[key] = [
                            None if x in ".?" else int(x) for x in data[cif_key]
                        ]
                    elif _type == "float":
                        kwargs[key] = [
                            None if x in ".?" else float(x) for x in data[cif_key]
                        ]
                    else:
                        kwargs[key] = [None if x in ".?" else x for x in data[cif_key]]

            if ensemble:
                if "_atom_site.pdbx_PDB_model_num" not in kwargs:
                    raise KeyError("Is an ensemble but no model numbers.")
                model_num = kwargs.pop("_atom_site.pdbx_PDB_model_num")
                first = 0
                last = first
                model = model_num[0]
                for i in model_num:
                    if i == model:
                        last += 1
                    else:
                        atoms = configuration.atoms
                        model_args = {k: v[first:last] for k, v in kwargs.items()}
                        atom_ids = atoms.append(**model_args)

                        # Make the next configuration and reset pointers
                        model = i
                        first = last
                        last += 1
                        if model == representative:
                            configuration_name = "representative"
                        else:
                            configuration_name = f"model_{model}"
                        configuration = system.create_configuration(configuration_name)
                        configurations[system.id].append(configuration)
                # Put in the last model
                atoms = configuration.atoms
                model_args = {k: v[first:last] for k, v in kwargs.items()}
                atom_ids = atoms.append(**model_args)
                if model != n_ensemble:
                    self.logger.warning(
                        f"The actual number of models ({model}) does not "
                        f"match the claimed number ({n_ensemble})."
                    )
            else:
                if coordinate_system != "Cartesian":
                    raise NotImplementedError("Can't handle fractional coords")

                atom_ids = atoms.append(**kwargs)

                if "_chem_comp_bond.atom_id_1" in data:
                    # Prepare for the bonds, which are labeled by atom name
                    atom_id = {name: i for i, name in zip(atom_ids, kwargs["name"])}

                    # And the bonds
                    bonds = configuration.bonds
                    kwargs = {}
                    for cif_key, key, _type, default in [
                        ("_chem_comp_bond.atom_id_1", "i", "str", ""),
                        ("_chem_comp_bond.atom_id_2", "j", "str", ""),
                        ("_chem_comp_bond.value_order", "bondorder", "int", 1),
                        ("_chem_comp_bond.comp_id", None, "str", None),
                        ("_chem_comp_bond.aromatic_flag", None, "bool", False),
                        ("_chem_comp_bond.stereo_flag", None, "str", None),
                        ("_chem_comp_bond.value_dist", None, "float", None),
                        ("_chem_comp_bond.value_dist_esd", None, "float", None),
                    ]:
                        if cif_key in data:
                            if key is None:
                                key = cif_key
                            if key == "ignore":
                                key = cif_key
                            elif key not in bonds:
                                bonds.add_attribute(key, _type, default=default)

                            if key == "i" or key == "j":
                                kwargs[key] = [atom_id[x] for x in data[cif_key]]
                            elif key == "bondorder":
                                kwargs[key] = [to_bond_order[x] for x in data[cif_key]]
                            elif _type == "bool":
                                kwargs[key] = [
                                    None if x in ".?" else x == "N"
                                    for x in data[cif_key]
                                ]
                            elif _type == "int":
                                kwargs[key] = [
                                    None if x in ".?" else int(x) for x in data[cif_key]
                                ]
                            elif _type == "float":
                                kwargs[key] = [
                                    None if x in ".?" else float(x)
                                    for x in data[cif_key]
                                ]
                            else:
                                kwargs[key] = [
                                    None if x in ".?" else x for x in data[cif_key]
                                ]

                    bonds.append(**kwargs)
        return systems, configurations
