# Honeybee: A Plugin for Environmental Analysis (GPL)
# This file is part of Honeybee.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>


"""
Get a validation report that contains a summary of all issues with the Model.
_
This includes basic properties like adjacency checks and all geometry checks.
Furthermore, all extension attributes for Energy and Radiance will be checked
to ensure that the model can be simulated correctly in these engines.
-

    Args:
        _model: A Honeybee Model object to be validated. This can also be the file path
            to a Model HBJSON that will be validated.
        extension_: Optional text for the name of the honeybee extension for which
            validation will occur. The value input here is case-insensitive such
            that "radiance" and "Radiance" will both result in the model being
            checked for validity with honeybee-radiance. This value can also be
            set to "Generic" in order to run checks for all installed extensions.
            Using "Generic" will run all except the most limiting of checks (like
            DOE2's lack of support for courtyards) with the goal of producing a
            model that is export-able to multiple engines (albeit with a little
            extra postprocessing for particularly limited engines). Some common
            honeybee extension names that can be input here if they are installed
            include  the following. (Default: Generic).
                * Radiance
                * EnergyPlus
                * OpenStudio
                * DesignBuilder
                * DOE2
                * IES
                * IDAICE
        _validate: Set to "True" to validate the the Model and get a report of all
            issues with the model.

    Returns:
        report: A report summarizing any issues with the input _model. If anything is
            invalid about the input model, this component will give a warning
            and this report will contain information about the specific parts
            of the model that are invalid. Otherwise, this report will simply
            say that the input model is valid.
"""

ghenv.Component.Name = 'HB Validate Model'
ghenv.Component.NickName = 'ValidateModel'
ghenv.Component.Message = '1.9.0'
ghenv.Component.Category = 'Honeybee'
ghenv.Component.SubCategory = '3 :: Serialize'
ghenv.Component.AdditionalHelpFromDocStrings = '0'

import os

try:  # import the core honeybee dependencies
    from honeybee.config import folders
    from honeybee.model import Model
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

try:  # import the core ladybug_rhino dependencies
    from ladybug_rhino.grasshopper import all_required_inputs, give_warning
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))


if all_required_inputs(ghenv.Component) and _validate:
    # re-serialize the model if it is a HBJSON file
    if isinstance(_model, Model):
        parsed_model = _model
    elif isinstance(_model, str) and os.path.isfile(_model):
        parsed_model = Model.from_hbjson(_model)
    else:
        raise ValueError(
            'Expected Honeybee Model object or path to a HBJSON file. '
            'Got {}.'.format(type(_model))
        )

    # validate the model
    print(
        'Validating Model using honeybee-core=={} and honeybee-schema=={}'.format(
            folders.honeybee_core_version_str, folders.honeybee_schema_version_str)
    )
    # perform several checks for geometry rules
    extension_ = 'Generic' if extension_ is None else extension_
    report = parsed_model.check_for_extension(extension_, raise_exception=False)
    print('Model checks completed.')
    # check the report and write the summary of errors
    if report == '':
        print('Congratulations! Your Model is valid!')
    else:
        error_msg = 'Your Model is invalid for the following reasons:'
        print('\n'.join([error_msg, report]))
        give_warning(ghenv.Component, report)
