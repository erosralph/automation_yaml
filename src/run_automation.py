import argparse
import pandas as pd

default_entity_file = 'entity_to_csv'
default_group_file = 'group_to_csv'
default_tab_file = 'tab_to_csv'
default_item_file = 'item_to_csv'
default_dictionary_col = ['periodData','query','result','type']

def parse_args():
    parser = argparse.ArgumentParser(
        prog='run_automation',
        description='convert csv to yaml')
    parser.add_argument(
        '-F', '--file', dest='file_name',
        required=True, help='File Name')
    parser.add_argument(
        '-D', '--report', dest='da_report',
        required=True, help='The Report')
    return parser.parse_args()

def screenon_item_group_tab_converter(df_file):
    columns = list(df_file.columns)
    print(columns)
    converted_to_yaml = ''
    for colName, colData in df_file.iterrows():
        converted_to_yaml += '---\n'
        for column in columns:
            # if colData[column] == '' and column not in  default_dictionary_col:
            if colData[column] == 'None':
                continue
            else:
                if column in default_dictionary_col:
                    converted_to_yaml += f'{column}:\n'
                else:
                    if column == '  types' and str(colData[column]) != 'nan':
                        # print(colData[column])
                        converted_to_yaml += f'{column}:\n'
                        item_list = colData[column].split(',')
                        for i in range(len(item_list)):
                            converted_to_yaml += f'  - {item_list[i]}\n'
                    elif ':' in str(colData[column]) and str(colData[column]) != 'nan':
                        converted_to_yaml += f'{column}: "{colData[column]}"\n'
                    else:
                        if str(colData[column]) != 'nan':
                            converted_to_yaml += f'{column}: {colData[column]}\n'
    return converted_to_yaml

def screenon_converter_to_yaml(file_name):
    df_file = pd.read_csv(f'{file_name}.csv')
    columns = list(df_file.columns)
    converted_to_yaml = ''
    for colName, colData in df_file.iterrows():
        converted_to_yaml += '---\n'
        for column in columns:
            if colData[column] == '' and column not in  default_dictionary_col:
                continue
            else:
                if column in default_dictionary_col:
                    converted_to_yaml += f'{column}:\n'
                else:
                    converted_to_yaml += f'{column}: {colData[column]}\n'
    return converted_to_yaml

def screenon_entity_converter(df_file):
    converted_to_yaml = ''
    first_list = True
    first_list_name = ''
    for colName, colData in df_file.iterrows():

        if str(colData['parent']) == 'nan':
            if str(colData['value']) == 'nan':
                converted_to_yaml += f"{colData['key']}:\n"
            else:
                converted_to_yaml += f"{colData['key']}: {colData['value']}\n"
            first_list = True
            first_list_name = ''
        else:
            if first_list_name == colData['key']:
                first_list = True
                first_list_name = ''
            if first_list == True:
                converted_to_yaml += f"  - {colData['key']}: {colData['value']}\n"
                first_list_name = colData['key']
            else:
                
                converted_to_yaml += f"    {colData['key']}: {colData['value']}\n"
            first_list = False
    return converted_to_yaml

def convert_to_yaml(file_name, da_report):
    all_yaml = ''
    if da_report == 'fds':
        print('under construction')
        # with open(f'{file_name}.txt', 'w') as f:
        #     f.write(fds_converter_to_yaml(file_name))

    elif da_report == 'screenon':
        screenon_entity = screenon_entity_converter(pd.read_csv(f'{default_entity_file}.csv'))
        screenon_group = screenon_item_group_tab_converter(pd.read_csv(f'{default_group_file}.csv'))
        screenon_tab = screenon_item_group_tab_converter(pd.read_csv(f'{default_tab_file}.csv'))
        screenon_item = screenon_item_group_tab_converter(pd.read_csv(f'{file_name}.csv'))
        all_yaml = {'entity':screenon_entity,'group':screenon_group,'tab':screenon_tab,'item':screenon_item}
    return all_yaml
        

def main():
    args = parse_args()
    file_name = args.file_name
    da_report = args.da_report
    converted_files_to_yaml = convert_to_yaml(file_name,da_report)
    for key, value in converted_files_to_yaml.items():
        with open(f'yaml_files/{key}.yaml', 'w') as f:
            f.write(value)

if __name__ == '__main__':
    # samp = 'sample'
    # samp = samp.split(',')
    # with open(f'samp.txt', 'w') as f:
    #     f.write(screenon_item_group_tab_converter(pd.read_csv(f'{default_item_file}.csv')))
    # print(screenon_item_group_tab_converter(pd.read_csv(f'{default_group_file}.csv')))
    main()