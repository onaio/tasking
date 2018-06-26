# -*- coding: utf-8 -*-
"""
Common strings used in the tasking app
"""
from __future__ import unicode_literals

from django.utils.translation import ugettext as _

TARGET_DOES_NOT_EXIST = _('The target content type does not exist.')
INVALID_TIMING_RULE = _('Invalid Timing Rule.')
RADIUS_MISSING = _('The Radius for Geopoint is missing.')
GEODETAILS_ONLY = _('Cannot Import Geopoint and Radius with Shapefile.')
SHAPEFILE_RADIUS = _('Cannot import Shapefile with radius.')
GEOPOINT_MISSING = _('The Geopoint for Radius is missing.')
CANT_EDIT_TASK = _('Cannot Change Task.')
NO_SHAPEFILE = _('Could not find the .shp in imported zip.')
MISSING_FILE = _('Either the .dbf , .shx or .shp file is missing.')
UNNECESSARY_FILE = _(
    'Uploaded an unnecessary file. Please make sure only a .shx , .shp and '
    '.dbf file is being uploaded.'
)
INVALID_START_DATE = _('The start date cannnot be greater than the end date')
INVALID_END_DATE = _('The end date cannnot be lesser than the start date.')
