# Honeybee: A Plugin for Environmental Analysis (GPL)
# This file is part of Honeybee.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>

"""
Set text for the zone identifier for honeybee Rooms.
_
Rooms sharing the same zone identifier are considered part of the same zone
in a Model. If a zone identifier has not been specified for a given Room, it
will be the same as the Room identifier.
-

    Args:
        _rooms: Honeybee Rooms to which the input _zone identifier should be assigned.
        _zone: Text for the zone identifier to which the rooms belong.

    Returns:
        report: ...
        rooms: The input Rooms with their zones set.
"""

ghenv.Component.Name = 'HB Set Zone'
ghenv.Component.NickName = 'SetZone'
ghenv.Component.Message = '1.9.0'
ghenv.Component.Category = 'Honeybee'
ghenv.Component.SubCategory = '0 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = '0'


try:  # import the honeybee-energy extension
    from honeybee.room import Room
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

try:  # import the ladybug_rhino dependencies
    from ladybug_rhino.grasshopper import all_required_inputs, longest_list
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))


if all_required_inputs(ghenv.Component):
    rooms = []
    for i, room in enumerate(_rooms):
        assert isinstance(room, Room), \
            'Expected honeybee room. Got {}.'.format(type(room))
        zone_id = longest_list(_zone, i)
        room_dup = room.duplicate()
        room_dup.zone = zone_id
        rooms.append(room_dup)
