import psycopg2
import json
import csv
import ast

product_table = []
reference_info_table = []
company_table = []
db_info = []

drs_product_columns = [
    'supplierKcode', 'productNameEnglish', 'productNameLocal', 'proposalProductCategory', 'brand',
    'brandEng',
    'baseProductCode', 'manufacturerLeadTime', 'allergy', 'allergyName', 'materials',
    'referenceLinks',
    'applicableRegionBP', 'productWithVariation', 'variationType1', 'variationType2', 'products',
    'originalPlace', 'medical', 'wirelessTech', 'documentationForSupplierSideCountry',
    'otherWirelessTechs',
    'hsCode', 'referenceFiles', 'containedMaterial', 'hazardousMaterials', 'batteries', 'note',
    'innerNote',
    'status'
]

drs_company_columns = [
    'k_code', 'name_en_us', 'name_local', 'short_name_en_us', 'short_name_local',
    'currency_id',
    'country_id', 'notes', 'handler_company_id', 'is_drs_company', 'is_supplier', 'allow_locale',
    'address', 'phone_number', 'official_registration_number', 'bank_name', 'bank_branch_name',
    'bank_account_code', 'bank_account_name'
]

odoo_company_columns = [
    'int_id', 'id', 'name', 'name_local', 'short_name_en_us', 'short_name_local',
    'company_currency',
    'company_country', 'notes', 'handler_company_id', 'is_drs_company', 'is_supplier', 'allow_locale',
    'street', 'phone', 'official_registration_number', 'bank_name', 'bank_branch_name',
    'bank_account_code', 'bank_account_name'
]

odoo_product_columns = [

    'company_id/id', 'name', 'product_name_chi', 'product_category', 'brand_name_chi', 'brand_name_eng',
    'id', 'mlt', 'allergy_warning', 'allergyName', 'product_material_percentage',
    'product_link',
    'applicableRegionBP', 'productWithVariation', 'variationType1', 'variationType2', 'otherinfo',
    'countryoforigin', 'medicaldevice', 'wireless', 'importexport', 'otherwireless',
    'hscode', 'referenceFiles', 'containmaterial', 'potentialhazards', 'batteries', 'notes',
    'innerNote', 'status'
]

odoo_reference_info_columns = [
    'product_name', 'filename', 'link', 'type', 'appliedVariationProduct', 'applicableRegion',
    'description'
]


def _ref_info_writer(current_record):
    reference_info_row = []
    decoded_json = json.loads(current_record['referenceFiles'])
    for entry in decoded_json:
        for column in odoo_reference_info_columns:
            if column is 'name':
                reference_info_row.append(current_record['productNameEnglish'])
            elif column not in entry:
                reference_info_row.append('')
            else:
                reference_info_row.append(entry[column])
        reference_info_table.append(reference_info_row)
        reference_info_row = []

    _write_to_csv('referencefields.csv', odoo_reference_info_columns, reference_info_table)


def product_parser():
    cur.execute('SELECT data from draft_product_info_source')

    for record in cur:
        product_row = []
        for column in drs_product_columns:
            if column not in record[0]:
                product_row.append('')
                continue
            elif column is 'materials' or column is 'referenceLinks':
                product_row.append(record[0][column][len(column) + 5:-3])
            elif column is 'otherWirelessTechs':
                product_row.append(record[0][column][len(column) + 6:-3])
            elif column is 'referenceFiles':
                _ref_info_writer(record[0])
            else:
                product_row.append(record[0][column])
        product_table.append(product_row)

    _write_to_csv('products.csv', odoo_product_columns, product_table)


def company_parser():
    cur.execute('SELECT * FROM company WHERE handler_company_id > 1')

    for record in cur:
        company_row = []
        for column in record:
            if column is None:
                company_row.append(" ")
            else:
                company_row.append(column)
        company_table.append(company_row)

    currency_values = {1: 'TWD', 2: 'USD', 3: 'GBP', 4: 'CAD', 5: 'EUR'}
    country_values = {1: 'TW', 2: 'US', 3: 'UK', 4: 'CA', 5: 'DE', 6: 'FR', 7: 'IT', 8: 'ES'}

    for row in company_table:
        row[6] = currency_values[row[6]]
        row[7] = country_values[row[7]]

    _write_to_csv('company.csv', odoo_company_columns, company_table)


def _write_to_csv(filename, header, table):
    with open(filename, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(header)
        writer.writerows(table)


def run_parsers(option=None):
    if option == 1:
        company_parser()
    elif option == 2:
        product_parser()
    elif option is None:
        company_parser()
        product_parser()


def load_db_info():
with open("database.txt") as file:
    for line in file:
        db_info = ast.literal_eval(line)



load_db_info()

conn = psycopg2.connect(host=db_info[0], database=db_info[1], user=db_info[2], password=db_info[3])

run_parsers()

cur = conn.cursor()
cur.close()

