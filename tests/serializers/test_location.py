# -*- coding: utf-8 -*-
"""
Tests for LocationSerializer
"""
from __future__ import unicode_literals

import os
from collections import OrderedDict

from django.test import TestCase
from django.utils import six
from model_mommy import mommy
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework_gis.fields import GeoJsonDict

from tasking.common_tags import (GEODETAILS_ONLY, GEOPOINT_MISSING,
                                 RADIUS_MISSING)
from tasking.exceptions import (InvalidShapeFile, MissingFiles,
                                ShapeFileNotFound, UnnecessaryFiles)
from tasking.serializers import LocationSerializer

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class TestLocationSerializer(TestCase):
    """
    Test the LocationSerializer
    """

    def test_location_create(self):
        """
        Test that the serializer can create Location Objects
        """
        data = {
            'name': 'Nairobi',
            'country': 'KE',
        }
        serializer_instance = LocationSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())

        location = serializer_instance.save()

        self.assertEqual('Nairobi', location.name)
        self.assertEqual('KE', location.country)
        self.assertEqual('Kenya - Nairobi', six.text_type(location))

        expected_fields = [
            'id', 'modified', 'parent', 'radius', 'country', 'location_type',
            'description', 'created', 'geopoint', 'name', 'shapefile'
        ]
        self.assertEqual(
            set(expected_fields), set(list(serializer_instance.data)))

    def test_location_parent_link(self):
        """
        Test the parent link between locations
        """
        mocked_location_parent = mommy.make('tasking.Location', name='Nairobi')
        data = {'name': 'Nairobi', 'parent': mocked_location_parent.id}

        serializer_instance = LocationSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())

        location = serializer_instance.save()

        self.assertEqual(mocked_location_parent, location.parent)

    def test_validate_bad_data(self):
        """
        Test validate method of LocationSerializer works as expected
        for bad data
        """
        mocked_location_with_shapefile = mommy.make(
            'tasking.Location', name='Nairobi', _fill_optional=['shapefile'])
        missing_radius = OrderedDict(name='Nairobi', geopoint='30,10')
        missing_geopoint = OrderedDict(name='Montreal', radius=45.678)
        shapefile_radius = OrderedDict(
            name='Arusha',
            radius=56.6789,
            geopoint='30,10',
            shapefile=mocked_location_with_shapefile.shapefile)

        with self.assertRaises(ValidationError) as missing_radius_cm:
            LocationSerializer().validate(missing_radius)

        radius_error_detail = missing_radius_cm.exception.detail['radius']
        self.assertEqual(RADIUS_MISSING, six.text_type(radius_error_detail))

        with self.assertRaises(ValidationError) as missing_geopoint_cm:
            LocationSerializer().validate(missing_geopoint)

        geopnt_error_detail = missing_geopoint_cm.exception.detail['geopoint']
        self.assertEqual(GEOPOINT_MISSING, six.text_type(geopnt_error_detail))

        with self.assertRaises(ValidationError) as shapefile_radius_cm:
            LocationSerializer().validate(shapefile_radius)

        shape_error_detail = shapefile_radius_cm.exception.detail['shapefile']
        self.assertEqual(GEODETAILS_ONLY, six.text_type(shape_error_detail))

    def test_location_serializer_validate_shapefile(self):
        """
        Test validate method of TaskSerializer works as expected for shapefile
        """
        mocked_location_with_shapefile = mommy.make(
            'tasking.Location', name='Nairobi', _fill_optional=['shapefile'])
        data = OrderedDict(
            name='Montreal',
            shapefile=mocked_location_with_shapefile.shapefile)

        validated_data = LocationSerializer().validate(data)
        self.assertDictEqual(dict(data), dict(validated_data))

    def test_location_serializer_validate_geodetails(self):
        """
        Test validate method of TaskSerializer works as expecter for
        geopoint and radius
        """
        data = OrderedDict(
            name='Spain',
            geopoint='30,10',
            radius=45.986,
        )
        validated_data = LocationSerializer().validate(data)
        self.assertDictEqual(dict(data), dict(validated_data))

    def test_geopoint_field_output(self):
        """
        Test the geopoint field outputs valid GEOJSON
        """
        data = OrderedDict(
            name='Spain',
            geopoint='30,10',
            radius=45.986,
        )
        serializer_instance = LocationSerializer(data=data)

        self.assertTrue(serializer_instance.is_valid())
        self.assertEqual(
            type(serializer_instance.data['geopoint']), GeoJsonDict)

    def test_shapefile_field_output(self):
        """
        Test the shapefile field outputs valid GEOJSON
        """
        path = os.path.join(BASE_DIR, 'fixtures', 'test_shapefile.zip')

        with open(path, 'r+b') as shapefile:
            data = OrderedDict(
                name='Nairobi', country='KE', shapefile=shapefile)
            serializer_instance = LocationSerializer(data=data)

            self.assertTrue(serializer_instance.is_valid())
            self.assertEqual(
                type(serializer_instance.data['shapefile']), GeoJsonDict)

    def test_location_create_given_binary_shapefile_data(self):
        """
        Test create location given binary shapefile binary data:
         - create location with given data
         - shapefile field outputs GeoJsonDict
        """
        shapefile = {
            '0': 80,
            '1': 75,
            '2': 3,
            '3': 4,
            '4': 20,
            '5': 0,
            '6': 0,
            '7': 0,
            '8': 8,
            '9': 0,
            '10': 17,
            '11': 14,
            '12': 206,
            '13': 76,
            '14': 169,
            '15': 217,
            '16': 164,
            '17': 120,
            '18': 29,
            '19': 0,
            '20': 0,
            '21': 0,
            '22': 76,
            '23': 0,
            '24': 0,
            '25': 0,
            '26': 18,
            '27': 0,
            '28': 28,
            '29': 0,
            '30': 116,
            '31': 101,
            '32': 115,
            '33': 116,
            '34': 95,
            '35': 115,
            '36': 104,
            '37': 97,
            '38': 112,
            '39': 101,
            '40': 102,
            '41': 105,
            '42': 108,
            '43': 101,
            '44': 46,
            '45': 100,
            '46': 98,
            '47': 102,
            '48': 85,
            '49': 84,
            '50': 9,
            '51': 0,
            '52': 3,
            '53': 66,
            '54': 159,
            '55': 33,
            '56': 91,
            '57': 66,
            '58': 159,
            '59': 33,
            '60': 91,
            '61': 117,
            '62': 120,
            '63': 11,
            '64': 0,
            '65': 1,
            '66': 4,
            '67': 232,
            '68': 3,
            '69': 0,
            '70': 0,
            '71': 4,
            '72': 232,
            '73': 3,
            '74': 0,
            '75': 0,
            '76': 99,
            '77': 46,
            '78': 99,
            '79': 227,
            '80': 99,
            '81': 100,
            '82': 96,
            '83': 96,
            '84': 112,
            '85': 100,
            '86': 224,
            '87': 102,
            '88': 192,
            '89': 6,
            '90': 60,
            '91': 93,
            '92': 224,
            '93': 76,
            '94': 63,
            '95': 16,
            '96': 193,
            '97': 133,
            '98': 38,
            '99': 207,
            '100': 171,
            '101': 0,
            '102': 7,
            '103': 6,
            '104': 0,
            '105': 80,
            '106': 75,
            '107': 3,
            '108': 4,
            '109': 20,
            '110': 0,
            '111': 0,
            '112': 0,
            '113': 8,
            '114': 0,
            '115': 17,
            '116': 14,
            '117': 206,
            '118': 76,
            '119': 122,
            '120': 68,
            '121': 81,
            '122': 16,
            '123': 95,
            '124': 0,
            '125': 0,
            '126': 0,
            '127': 236,
            '128': 0,
            '129': 0,
            '130': 0,
            '131': 18,
            '132': 0,
            '133': 28,
            '134': 0,
            '135': 116,
            '136': 101,
            '137': 115,
            '138': 116,
            '139': 95,
            '140': 115,
            '141': 104,
            '142': 97,
            '143': 112,
            '144': 101,
            '145': 102,
            '146': 105,
            '147': 108,
            '148': 101,
            '149': 46,
            '150': 115,
            '151': 104,
            '152': 112,
            '153': 85,
            '154': 84,
            '155': 9,
            '156': 0,
            '157': 3,
            '158': 66,
            '159': 159,
            '160': 33,
            '161': 91,
            '162': 66,
            '163': 159,
            '164': 33,
            '165': 91,
            '166': 117,
            '167': 120,
            '168': 11,
            '169': 0,
            '170': 1,
            '171': 4,
            '172': 232,
            '173': 3,
            '174': 0,
            '175': 0,
            '176': 4,
            '177': 232,
            '178': 3,
            '179': 0,
            '180': 0,
            '181': 99,
            '182': 96,
            '183': 80,
            '184': 231,
            '185': 98,
            '186': 192,
            '187': 14,
            '188': 202,
            '189': 94,
            '190': 48,
            '191': 51,
            '192': 48,
            '193': 176,
            '194': 2,
            '195': 25,
            '196': 9,
            '197': 23,
            '198': 206,
            '199': 58,
            '200': 156,
            '201': 79,
            '202': 116,
            '203': 114,
            '204': 40,
            '205': 105,
            '206': 80,
            '207': 175,
            '208': 45,
            '209': 56,
            '210': 253,
            '211': 101,
            '212': 63,
            '213': 144,
            '214': 175,
            '215': 112,
            '216': 38,
            '217': 205,
            '218': 201,
            '219': 161,
            '220': 103,
            '221': 197,
            '222': 230,
            '223': 191,
            '224': 70,
            '225': 109,
            '226': 95,
            '227': 246,
            '228': 227,
            '229': 208,
            '230': 143,
            '231': 12,
            '232': 24,
            '233': 129,
            '234': 216,
            '235': 129,
            '236': 24,
            '237': 179,
            '238': 64,
            '239': 10,
            '240': 89,
            '241': 161,
            '242': 154,
            '243': 64,
            '244': 114,
            '245': 188,
            '246': 73,
            '247': 78,
            '248': 14,
            '249': 59,
            '250': 118,
            '251': 43,
            '252': 6,
            '253': 236,
            '254': 155,
            '255': 0,
            '256': 86,
            '257': 139,
            '258': 85,
            '259': 239,
            '260': 253,
            '261': 57,
            '262': 63,
            '263': 175,
            '264': 106,
            '265': 29,
            '266': 3,
            '267': 243,
            '268': 23,
            '269': 108,
            '270': 69,
            '271': 50,
            '272': 11,
            '273': 93,
            '274': 63,
            '275': 0,
            '276': 80,
            '277': 75,
            '278': 3,
            '279': 4,
            '280': 20,
            '281': 0,
            '282': 0,
            '283': 0,
            '284': 8,
            '285': 0,
            '286': 17,
            '287': 14,
            '288': 206,
            '289': 76,
            '290': 80,
            '291': 196,
            '292': 2,
            '293': 229,
            '294': 56,
            '295': 0,
            '296': 0,
            '297': 0,
            '298': 108,
            '299': 0,
            '300': 0,
            '301': 0,
            '302': 18,
            '303': 0,
            '304': 28,
            '305': 0,
            '306': 116,
            '307': 101,
            '308': 115,
            '309': 116,
            '310': 95,
            '311': 115,
            '312': 104,
            '313': 97,
            '314': 112,
            '315': 101,
            '316': 102,
            '317': 105,
            '318': 108,
            '319': 101,
            '320': 46,
            '321': 115,
            '322': 104,
            '323': 120,
            '324': 85,
            '325': 84,
            '326': 9,
            '327': 0,
            '328': 3,
            '329': 66,
            '330': 159,
            '331': 33,
            '332': 91,
            '333': 66,
            '334': 159,
            '335': 33,
            '336': 91,
            '337': 117,
            '338': 120,
            '339': 11,
            '340': 0,
            '341': 1,
            '342': 4,
            '343': 232,
            '344': 3,
            '345': 0,
            '346': 0,
            '347': 4,
            '348': 232,
            '349': 3,
            '350': 0,
            '351': 0,
            '352': 99,
            '353': 96,
            '354': 80,
            '355': 231,
            '356': 98,
            '357': 192,
            '358': 14,
            '359': 204,
            '360': 94,
            '361': 48,
            '362': 51,
            '363': 48,
            '364': 176,
            '365': 2,
            '366': 25,
            '367': 9,
            '368': 23,
            '369': 206,
            '370': 58,
            '371': 156,
            '372': 79,
            '373': 116,
            '374': 114,
            '375': 40,
            '376': 105,
            '377': 80,
            '378': 175,
            '379': 45,
            '380': 56,
            '381': 253,
            '382': 101,
            '383': 63,
            '384': 144,
            '385': 175,
            '386': 112,
            '387': 38,
            '388': 205,
            '389': 201,
            '390': 161,
            '391': 103,
            '392': 197,
            '393': 230,
            '394': 191,
            '395': 70,
            '396': 109,
            '397': 95,
            '398': 246,
            '399': 227,
            '400': 208,
            '401': 143,
            '402': 12,
            '403': 140,
            '404': 128,
            '405': 216,
            '406': 1,
            '407': 0,
            '408': 80,
            '409': 75,
            '410': 1,
            '411': 2,
            '412': 30,
            '413': 3,
            '414': 20,
            '415': 0,
            '416': 0,
            '417': 0,
            '418': 8,
            '419': 0,
            '420': 17,
            '421': 14,
            '422': 206,
            '423': 76,
            '424': 169,
            '425': 217,
            '426': 164,
            '427': 120,
            '428': 29,
            '429': 0,
            '430': 0,
            '431': 0,
            '432': 76,
            '433': 0,
            '434': 0,
            '435': 0,
            '436': 18,
            '437': 0,
            '438': 24,
            '439': 0,
            '440': 0,
            '441': 0,
            '442': 0,
            '443': 0,
            '444': 0,
            '445': 0,
            '446': 0,
            '447': 0,
            '448': 164,
            '449': 129,
            '450': 0,
            '451': 0,
            '452': 0,
            '453': 0,
            '454': 116,
            '455': 101,
            '456': 115,
            '457': 116,
            '458': 95,
            '459': 115,
            '460': 104,
            '461': 97,
            '462': 112,
            '463': 101,
            '464': 102,
            '465': 105,
            '466': 108,
            '467': 101,
            '468': 46,
            '469': 100,
            '470': 98,
            '471': 102,
            '472': 85,
            '473': 84,
            '474': 5,
            '475': 0,
            '476': 3,
            '477': 66,
            '478': 159,
            '479': 33,
            '480': 91,
            '481': 117,
            '482': 120,
            '483': 11,
            '484': 0,
            '485': 1,
            '486': 4,
            '487': 232,
            '488': 3,
            '489': 0,
            '490': 0,
            '491': 4,
            '492': 232,
            '493': 3,
            '494': 0,
            '495': 0,
            '496': 80,
            '497': 75,
            '498': 1,
            '499': 2,
            '500': 30,
            '501': 3,
            '502': 20,
            '503': 0,
            '504': 0,
            '505': 0,
            '506': 8,
            '507': 0,
            '508': 17,
            '509': 14,
            '510': 206,
            '511': 76,
            '512': 122,
            '513': 68,
            '514': 81,
            '515': 16,
            '516': 95,
            '517': 0,
            '518': 0,
            '519': 0,
            '520': 236,
            '521': 0,
            '522': 0,
            '523': 0,
            '524': 18,
            '525': 0,
            '526': 24,
            '527': 0,
            '528': 0,
            '529': 0,
            '530': 0,
            '531': 0,
            '532': 0,
            '533': 0,
            '534': 0,
            '535': 0,
            '536': 164,
            '537': 129,
            '538': 105,
            '539': 0,
            '540': 0,
            '541': 0,
            '542': 116,
            '543': 101,
            '544': 115,
            '545': 116,
            '546': 95,
            '547': 115,
            '548': 104,
            '549': 97,
            '550': 112,
            '551': 101,
            '552': 102,
            '553': 105,
            '554': 108,
            '555': 101,
            '556': 46,
            '557': 115,
            '558': 104,
            '559': 112,
            '560': 85,
            '561': 84,
            '562': 5,
            '563': 0,
            '564': 3,
            '565': 66,
            '566': 159,
            '567': 33,
            '568': 91,
            '569': 117,
            '570': 120,
            '571': 11,
            '572': 0,
            '573': 1,
            '574': 4,
            '575': 232,
            '576': 3,
            '577': 0,
            '578': 0,
            '579': 4,
            '580': 232,
            '581': 3,
            '582': 0,
            '583': 0,
            '584': 80,
            '585': 75,
            '586': 1,
            '587': 2,
            '588': 30,
            '589': 3,
            '590': 20,
            '591': 0,
            '592': 0,
            '593': 0,
            '594': 8,
            '595': 0,
            '596': 17,
            '597': 14,
            '598': 206,
            '599': 76,
            '600': 80,
            '601': 196,
            '602': 2,
            '603': 229,
            '604': 56,
            '605': 0,
            '606': 0,
            '607': 0,
            '608': 108,
            '609': 0,
            '610': 0,
            '611': 0,
            '612': 18,
            '613': 0,
            '614': 24,
            '615': 0,
            '616': 0,
            '617': 0,
            '618': 0,
            '619': 0,
            '620': 0,
            '621': 0,
            '622': 0,
            '623': 0,
            '624': 164,
            '625': 129,
            '626': 20,
            '627': 1,
            '628': 0,
            '629': 0,
            '630': 116,
            '631': 101,
            '632': 115,
            '633': 116,
            '634': 95,
            '635': 115,
            '636': 104,
            '637': 97,
            '638': 112,
            '639': 101,
            '640': 102,
            '641': 105,
            '642': 108,
            '643': 101,
            '644': 46,
            '645': 115,
            '646': 104,
            '647': 120,
            '648': 85,
            '649': 84,
            '650': 5,
            '651': 0,
            '652': 3,
            '653': 66,
            '654': 159,
            '655': 33,
            '656': 91,
            '657': 117,
            '658': 120,
            '659': 11,
            '660': 0,
            '661': 1,
            '662': 4,
            '663': 232,
            '664': 3,
            '665': 0,
            '666': 0,
            '667': 4,
            '668': 232,
            '669': 3,
            '670': 0,
            '671': 0,
            '672': 80,
            '673': 75,
            '674': 5,
            '675': 6,
            '676': 0,
            '677': 0,
            '678': 0,
            '679': 0,
            '680': 3,
            '681': 0,
            '682': 3,
            '683': 0,
            '684': 8,
            '685': 1,
            '686': 0,
            '687': 0,
            '688': 152,
            '689': 1,
            '690': 0,
            '691': 0,
            '692': 0,
            '693': 0
        }

        shapefile_keys_list = shapefile.keys()
        sorted_key_list = [
            '{}'.format(y)
            for y in sorted([int(x) for x in shapefile_keys_list])
        ]
        shapefile_tuples_list = [(x, shapefile[x]) for x in sorted_key_list]
        shapefile_ordered_dict = OrderedDict(shapefile_tuples_list)

        data = OrderedDict(
            name='Nairobi', country='KE', shapefile=shapefile_ordered_dict)
        serializer_instance = LocationSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        location = serializer_instance.save()
        self.assertEqual('Nairobi', location.name)
        self.assertEqual('KE', location.country)
        self.assertEqual('Kenya - Nairobi', six.text_type(location))
        self.assertEqual(
            type(serializer_instance.data['shapefile']), GeoJsonDict)

    def test_bad_shapefile_data(self):
        """
        Test upload of a bad shapefile returns relevant error message
        - missing files
        - shapefile not found
        - unnecessary files
        """
        # test missing files
        missing_files_path = os.path.join(BASE_DIR, 'fixtures',
                                          'test_missing_files.zip')

        with open(missing_files_path, 'r+b') as shapefile:
            data = OrderedDict(
                name='Nairobi', country='KE', shapefile=shapefile)
            serializer_instance = LocationSerializer(data=data)

            self.assertFalse(serializer_instance.is_valid())
            self.assertEqual(
                serializer_instance.errors, {
                    "shapefile": [
                        ErrorDetail(
                            string=MissingFiles().message, code="invalid")
                    ]
                })

        # test shapefile not found
        shapefile_not_found_files_path = os.path.join(BASE_DIR, 'fixtures',
                                                      'missing_shp.zip')

        with open(shapefile_not_found_files_path, 'r+b') as shapefile:
            data = OrderedDict(
                name='Nairobi', country='KE', shapefile=shapefile)
            serializer_instance = LocationSerializer(data=data)

            self.assertFalse(serializer_instance.is_valid())
            self.assertEqual(
                serializer_instance.errors, {
                    "shapefile": [
                        ErrorDetail(
                            string=ShapeFileNotFound().message, code="invalid")
                    ]
                })

        # test unnecessary files
        with self.settings(CHECK_NUMBER_OF_FILES_IN_SHAPEFILES_DIR=True):
            unnecessary_files_path = os.path.join(
                BASE_DIR, 'fixtures', 'test_unnecessary_files.zip')

            with open(unnecessary_files_path, 'r+b') as shapefile:
                data = OrderedDict(
                    name='Nairobi', country='KE', shapefile=shapefile)
                serializer_instance = LocationSerializer(data=data)

                self.assertFalse(serializer_instance.is_valid())
                self.assertEqual(
                    serializer_instance.errors, {
                        "shapefile": [
                            ErrorDetail(
                                string=UnnecessaryFiles().message,
                                code="invalid")
                        ]
                    })

    @patch('tasking.serializers.location.MultiPolygon')
    def test_invalid_shapefile(self, mock):
        """
        Test invalid shapefile
        The appropriate exception is raised when we encounter an invalid
        shapefile    
        """
        mock.side_effect = TypeError

        path = os.path.join(BASE_DIR, 'fixtures', 'test_shapefile.zip')

        with open(path, 'r+b') as shapefile:
            data = OrderedDict(
                name='Nairobi', country='KE', shapefile=shapefile)
            serializer_instance = LocationSerializer(data=data)
            self.assertFalse(serializer_instance.is_valid())
            self.assertEqual(
                serializer_instance.errors, {
                    "shapefile": [
                        ErrorDetail(
                            string=InvalidShapeFile().message, code="invalid")
                    ]
                })
