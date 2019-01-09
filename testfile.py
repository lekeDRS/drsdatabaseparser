import json
reference_info_columns = ['drs_product_code', 'file', 'link', 'type', 'appliedVariationProduct', 'applicableRegion',
                          'description']

jsson = [{'file': 'X5 CE Declaration_20160909.pdf', 'link': '', 'type': ['ce'], 'appliedVariationProduct': ['X5', 'X5-Combo', 'X5-IT', 'X5-DE'], 'applicableRegion': ['UK'], 'description': ''}]


print(jsson[0]['file'])

'''def refinfowriter(record, i):
    reference_info_row = []
    decoded_json = json.loads(record[0][i])
    for entry in decoded_json:
        for column in odoo_reference_info_columns:
            if column is 'drs_product_code':
                reference_info_row.append(record[0]['baseProductCode'])
            else:
                if column not in entry:
                    product_row.append('')
                    continue
                print(column)
                print(entry)
                reference_info_row.append(column[entry])
        reference_info_table.append(reference_info_row)
        reference_info_row = []'''
