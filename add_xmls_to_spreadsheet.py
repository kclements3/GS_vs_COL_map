import pandas as pd
import pickle as pkl


df = pd.read_excel('fbc_data_2024_ds.xlsx', sheet_name='County')
fip_xml_map = pkl.load(open('fip_xml_map.pkl', 'rb'))

for fip, abbrev in fip_xml_map.items():
    df.loc[df['county_fips'] == int(fip), 'XML_loc'] = abbrev

df.to_excel('fbc_data_2024_update.xlsx')
