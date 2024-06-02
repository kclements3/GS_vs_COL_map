from bs4 import BeautifulSoup
import requests
import os
import pickle as pkl


# url = 'https://www.opm.gov/policy-data-oversight/pay-leave/salaries-wages/2024/general-schedule'
#
# res = requests.get(url)
#
# if res.status_code == 200:
#     soup = BeautifulSoup(res.text, 'html.parser')
# else:
#     raise ('No response for ' + url)
#
# data_tables = soup.find_all('table', class_='DataTable')
#
# main_table = data_tables[1]
#
# trs = main_table.find_all('tr')
#
# for tr in trs[1:]:
#     base='https://www.opm.gov/'
#     xml = tr.find('a', class_='XML')['href']
#     xml_url = base+xml
#     fn = xml.split('/')
#     res = requests.get(xml_url)
#
#     if os.path.basename(fn[-1]) not in os.listdir('XML_2024'):
#         xml_file = open(os.path.join('XML_2024', os.path.basename(fn[-1])),
#                          'wb')
#         print('Downloading ' + os.path.basename(fn[-1]))
#         for chunk in res.iter_content(100000):
#             xml_file.write(chunk)
#         xml_file.close()


url = 'https://www.opm.gov/policy-data-oversight/pay-leave/salaries-wages/2024/locality-pay-area-definitions'
result = requests.get(url)

if result.status_code == 200:
    soup = BeautifulSoup(result.text, 'html.parser')
else:
    raise ('No response for ' + url)


id_abbrev_map = {
    'Alaska': 'AK.xml',
    'Albany-SchenectadyNY-MA': 'AL.xml',
    'Albuquerque-SantaFe-LasVegasNM': 'AQ.xml',
    'Atlanta--Athens-ClarkeCounty--SandySpringsGA-AL': 'ATL.xml',
    'Austin-RoundRock-GeorgetownTX': 'AU.xml',
    'Birmingham-Hoover-TalladegaAL': 'BH.xml',
    'Boston-Worcester-ProvidenceMA-RI-NH-CT-ME-VT': 'BOS.xml',
    'Buffalo-Cheektowaga-OleanNY': 'BU.xml',
    'Burlington-SouthBurlington-BarreVT': 'BN.xml',
    'Charlotte-ConcordNC-SC': 'CT.xml',
    'Chicago-NapervilleIL-IN-WI': 'CHI.xml',
    'Cincinnati-Wilmington-MaysvilleOH-KY-IN': 'CIN.xml',
    'Cleveland-Akron-CantonOH-PA': 'CLE.xml',
    'ColoradoSpringsCO': 'CS.xml',
    'Columbus-Marion-ZanesvilleOH': 'COL.xml',
    'CorpusChristi-Kingsville-AliceTX': 'CC.xml',
    'Dallas-FortWorthTX-OK': 'DFW.xml',
    'Davenport-MolineIA-IL': 'DV.xml',
    'Dayton-Springfield-KetteringOH': 'DAY.xml',
    'Denver-AuroraCO': 'DEN.xml',
    'DesMoines-Ames-WestDesMoinesIA': 'DM.xml',
    'Detroit-Warren-AnnArborMI': 'DET.xml',
    'Fresno-Madera-HanfordCA': 'FN.xml',
    'Harrisburg-LebanonPA': 'HB.xml',
    'Hartford-EastHartfordCT-MA': 'HAR.xml',
    'Hawaii': 'HI.xml',
    'Houston-TheWoodlandsTX': 'HOU.xml',
    'Huntsville-DecaturAL-TN': 'HNT.xml',
    'Indianapolis-Carmel-MuncieIN': 'IND.xml',
    'KansasCity-OverlandPark-KansasCityMO-KS': 'KC.xml',
    'LaredoTX': 'LR.xml',
    'LasVegas-HendersonNV-AZ': 'LV.xml',
    'LosAngeles-LongBeachCA': 'LA.xml',
    'Miami-PortStLucie-FortLauderdaleFL': 'MFL.xml',
    'Milwaukee-Racine-WaukeshaWI': 'MIL.xml',
    'Minneapolis-StPaulMN-WI': 'MSP.xml',
    'NewYork-NewarkNY-NJ-CT-PA': 'NY.xml',
    'Omaha-CouncilBluffs-FremontNE-IA': 'OM.xml',
    'PalmBay-Melbourne-TitusvilleFL': 'PB.xml',
    'Philadelphia-Reading-CamdenPA-NJ-DE-MD': 'PHL.xml',
    'Phoenix-MesaAZ': 'PX.xml',
    'Pittsburgh-NewCastle-WeirtonPA-OH-WV': 'PIT.xml',
    'Portland-Vancouver-SalemOR-WA': 'POR.xml',
    'Raleigh-Durham-CaryNC': 'RA.xml',
    'Reno-FernleyNV': 'RN.xml',
    'RichmondVA': 'RCH.xml',
    'Rochester-Batavia-SenecaFallsNY': 'RT.xml',
    'Sacramento-RosevilleCA-NV': 'SAC.xml',
    'SanAntonio-NewBraunfels-PearsallTX': 'SO.xml',
    'SanDiego-ChulaVista-CarlsbadCA': 'SD.xml',
    'SanJose-SanFrancisco-OaklandCA': 'SF.xml',
    'Seattle-TacomaWA': 'SEA.xml',
    'Spokane-SpokaneValley-CoeurdAleneWA-ID': 'SN.xml',
    'StLouis-StCharles-FarmingtonMO-IL': 'SL.xml',
    'Tucson-NogalesAZ': 'TU.xml',
    'VirginiaBeach-NorfolkVA-NC': 'VB.xml',
    'Washington-Baltimore-ArlingtonDC-MD-VA-WV-PA': 'DCB.xml'
}

tables = soup.find_all('table', class_='usa-table')
h3s = soup.find_all('h3')
fip_xml_map = {}
place_abbrev = 'AL.xml'
for elem in h3s[3].next_siblings:
    if elem.name == 'h3':
        place_id = elem.find('a')['id']
        if place_id == 'RestofUS':
            break
        place_abbrev = id_abbrev_map[place_id]
    elif elem.name == 'table':
        trs = elem.find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            fip = tds[1].text
            fip_xml_map[fip] = place_abbrev
pkl.dump(fip_xml_map, open('fip_xml_map.pkl', 'wb'))