import pandas as pd
import pprint

from pyaddepar.request import Request, PortfolioType

if __name__ == '__main__':
    f = Request().view_csv(view_id=53676, portfolio_id=6076, portfolio_type=PortfolioType.GROUP)
    #import io
    #x = io.BytesIO(r.content)
    #print(x)
    #f = pd.read_csv(x, index_col=["Top Level Owner [Entity ID]", "Top Level Owner"])
    # do the renaming

    #f = f.reset_index()
    print(f)

    offset=300
    date = pd.Timestamp("today")
    f = Request().view_csv(view_id=49702, portfolio_id=1, portfolio_type=PortfolioType.FIRM, start_date=date - pd.offsets.Day(n=offset), end_date=date)

    print(f)
    #print(f.keys())

    # print(Request().users().keys())
    # print(Request().entity().keys())
    #
    # for key, user in Request().users().items():
    #     print(key)
    #     print(user)
    #
    for key, entity in Request().entity().items():
        if entity.model_type == "PERSON_NODE":
            pprint.pprint(entity.original_name)

    #assert False

    #pyaddepar_1  | 804365
    #pyaddepar_1  | {'id': '804365', 'type': 'entities', 'attributes': {'_custom_06_mobile_number_165467': [{'date': None, 'value': '+65 96 634 684', 'weight': 1.0}], '_custom_billing_name_263489': [{'date': None, 'value': 'JV Energy Consulting Pte. Ltd', 'weight': 1.0}], '_custom_02_first_name_165465': [{'date': None, 'value': 'Etienne', 'weight': 1.0}], '_custom_19_manager_name_180885': [{'date': None, 'value': 'Lobnek Wealth Management S.A.', 'weight': 1.0}], '_custom_04_home_address_114947': [{'date': None, 'value': '72 Tras Street, Singapore 079011', 'weight': 1.0}], '_custom_09_nationality_165468': [{'date': None, 'value': 'Swiss', 'weight': 1.0}], '_custom_14_bank_account_number_165473': [{'date': None, 'value': '4141071711', 'weight': 1.0}], '_custom_05_country_of_domicile_248500': [{'date': None, 'value': 'Singapore', 'weight': 1.0}], '_custom_22_lwm_client_nickname_248537': [{'date': None, 'value': 'Latour', 'weight': 1.0}], '_custom_15_reference_currency_165485': [{'date': None, 'value': 'USD', 'weight': 1.0}], '_custom_10_passport_number_165469': [{'date': None, 'value': 'X0926638', 'weight': 1.0}], '_custom_16_lwm_risk_profile_114480': [{'date': None, 'value': 'Balanced', 'weight': 1.0}], '_custom_17_lwm_management_agreement_date_165471': [{'date': None, 'value': '2014-06-06', 'weight': 1.0}], 'currency_factor': 'USD', '_custom_18_lwm_management_fee_165472': [{'date': None, 'value': 0.015, 'weight': 1.0}], '_custom_13_client_risk_level_lba_248501': [{'date': None, 'value': 'Normal', 'weight': 1.0}], '_custom_01_family_104439': [{'date': None, 'value': 'WALDERSTON', 'weight': 1.0}], 'model_type': 'PERSON_NODE', '_custom_00_entity_name_166731': [{'date': None, 'value': 'JV Energy Consulting Pte. Ltd', 'weight': 1.0}], '_custom_13_custodian_name_166730': [{'date': None, 'value': 'Maybank, Singapore', 'weight': 1.0}], '_custom_11_passport_expiry_165470': [{'date': None, 'value': '2023-01-27', 'weight': 1.0}], '_custom_23_legal_entity_type_248503': [{'date': None, 'value': 'Legal Person', 'weight': 1.0}], '_custom_lobnek_currency_code_308318': [{'date': None, 'value': 2, 'weight': 1.0}], '_custom_07_birth_date_114946': [{'date': None, 'value': '1966-05-04', 'weight': 1.0}], '_custom_26_soumis_lba_377040': [{'date': None, 'value': True, 'weight': 1.0}], '_custom_08_email_114950': [{'date': None, 'value': 'ekb@jvenercon.com.sg', 'weight': 1.0}], '_custom_05_phone_number_114949': [{'date': None, 'value': '+65 6220 8098', 'weight': 1.0}], 'original_name': 'Latour 03 Maybank', '_custom_23_lwm_aum_type_293536': [{'date': None, 'value': 'LWM Discretionary (passive)', 'weight': 1.0}], '_custom_03_last_name_165466': [{'date': None, 'value': 'Kiss Borlase', 'weight': 1.0}], '_custom_12_pep_politically_exposed_person_165463': [{'date': None, 'value': False, 'weight': 1.0}]}, 'links': {'self': '/v1/entities/804365'}}
    #pyaddepar_1  | 804366
    pprint.pprint(Request().entity(id=804365))

    for key, entity in Request().group().items():
        #print(entity)
        print(key)
        attributes = AttrDict(entity["attributes"])
        print(attributes.name)


