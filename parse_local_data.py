from xml.etree import ElementTree as ET
import pandas as pd



def get_min_levels(xml_loc, target):
    tree = ET.parse('XML_2024/'+xml_loc)
    root = tree.getroot()
    Grades = (root.find('{http://schemas.datacontract.org/2004/07/PayTables.Business}Grades')
              .findall('{http://schemas.datacontract.org/2004/07/PayTables.Business}Grade'))


    grade = 1
    step = 1
    min_steps = []
    for Grade in Grades:
        grade = Grade.find('{http://schemas.datacontract.org/2004/07/PayTables.Business}Value').text
        Steps = (Grade.find('{http://schemas.datacontract.org/2004/07/PayTables.Business}Steps')
        .findall('{http://schemas.datacontract.org/2004/07/PayTables.Business}Step'))
        for Step in Steps:
            step = Step.find('{http://schemas.datacontract.org/2004/07/PayTables.Business}Value').text
            val = Step.find('{http://schemas.datacontract.org/2004/07/PayTables.Business}Annual').text
            if int(val) >= target:
                min_steps.append((int(grade), int(step)))
                break
        if len(min_steps) > 0 and min_steps[-1][1] == 1:
            break


    return min_steps

def low_grade(min_steps):
    if len(min_steps) == 0:
        return 0
    else:
        return min_steps[0][0]

def low_step(min_steps):
    if len(min_steps) == 0:
        return 0
    else:
        return min_steps[0][1]

def high_grade(min_steps):
    if len(min_steps) == 0:
        return 0
    else:
        return min_steps[-1][0]

def high_step(min_steps):
    if len(min_steps) == 0:
        return 0
    else:
        return min_steps[-1][1]

if __name__ == '__main__':
    df = pd.read_excel('fbc_data_2024_update.xlsx')
    df2 = df.loc[(df['Family'] == '2p2c') | (df['Family'] == '1p0c')]

    min_steps = df2.apply(lambda row: get_min_levels(row['XML_loc'], row['Total']), axis=1)
    df2['Min Grade'] = min_steps.apply(low_grade)
    df2['Highest Step'] = min_steps.apply(low_step)

    df2['Max Grade'] = min_steps.apply(high_grade)
    df2['Lowest Step'] = min_steps.apply(high_step)

    df2.to_excel('fbc_data_2024_update2.xlsx')
