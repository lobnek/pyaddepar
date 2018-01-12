from unittest import TestCase
import os

import pandas as pd
import pandas.util.testing as pdt

from pyaddepar.request import addepar2frame

base_dir = os.path.dirname(__file__)

class TestAddepar2frame(TestCase):
    def test_addepar2frame(self):
        r = {'meta': {'columns': [{'key': 'node_id', 'display_name': 'Entity ID', 'output_type': 'Word'},
                                  {'key': '_custom_13_custodian_name_166730', 'display_name': '15. Custodian Name', 'output_type': 'Word'},
                                  {'key': '_custom_15_reference_currency_165485', 'display_name': '17. Reference Currency', 'output_type': 'Currency'},
                                  {'key': '_custom_16_lwm_risk_profile_114480', 'display_name': '18. LWM Risk Profile', 'output_type': 'Word'},
                                  {'key': '_custom_23_lwm_aum_type_293536', 'display_name': '23. LWM - AUM Type', 'output_type': 'Word'},
                                  {'key': 'inception_event_date', 'display_name': 'Inception Date', 'output_type': 'Date'}],
                      'groupings': [{'key': 'top_level_owner', 'display_name': 'Top Level Owner'}]},
             'data': {'type': 'portfolio_views', 'attributes':
                 {'total': {'name': 'Total', 'columns':
                                {'_custom_15_reference_currency_165485': None, 'inception_event_date': '2013-12-31', '_custom_23_lwm_aum_type_293536': None, '_custom_16_lwm_risk_profile_114480': None, '_custom_13_custodian_name_166730': None, 'node_id': None},
                            'children': [{'entity_id': 1146188, 'name': 'A', 'grouping': 'top_level_owner', 'columns': {'_custom_15_reference_currency_165485': 'CHF', 'inception_event_date': '2016-10-31', '_custom_23_lwm_aum_type_293536': 'LWM Consolidation Only', '_custom_16_lwm_risk_profile_114480': 'Balanced', '_custom_13_custodian_name_166730': 'X', 'node_id': 1146188}, 'children': []},
                                         {'entity_id': 1231399, 'name': 'B', 'grouping': 'top_level_owner', 'columns': {'_custom_15_reference_currency_165485': 'CHF', 'inception_event_date': '2016-09-21', '_custom_23_lwm_aum_type_293536': 'LWM Consolidation Only', '_custom_16_lwm_risk_profile_114480': 'Balanced', '_custom_13_custodian_name_166730': 'Y', 'node_id': 1231399}, 'children': []},
                                         {'entity_id': 1511499, 'name': 'C', 'grouping': 'top_level_owner', 'columns': {'_custom_15_reference_currency_165485': 'CHF', 'inception_event_date': '2017-03-31', '_custom_23_lwm_aum_type_293536': 'LWM Consolidation Only', '_custom_16_lwm_risk_profile_114480': 'Conservative', '_custom_13_custodian_name_166730': 'Z', 'node_id': 1511499}, 'children': []},
                                        ]}}, 'links': {'self': '/v1/portfolio_views/null'}}}

        pdt.assert_frame_equal(addepar2frame(r), pd.read_csv(os.path.join(base_dir, "resources", "frame.csv"), parse_dates=True), check_dtype=False)

