###################################################################
# Customised Search in OpenITI | by Maroussia Bednarkiewicz
###################################################################

from ripgrepy import Ripgrepy
import pandas as pd
import json
import subprocess

###################################################################
# SearchITI using RipGrepy
###################################################################

def grepy(search:str, path:str):
    """Returns a json list of dictionaries with the results
    of the search using the Python module `RipGrepy` based
    on RipGrep.
    The search is the string that will be searched in the path.
    The path leads to the file or folder which will be searched.
    """
    rg = Ripgrepy(search, path).json()
    output = rg.run().as_json
    return json.loads(output)

def get_grepy(search:str, in_path:str, out_path:str, format='html'):
    """Returns the output of the search with `RipGrepy`
    in a table with 3 columns:
    (1) the file_name where the search was found,
    (2) the line_number matching the search, and
    (3) the text where the search was found, 
    in html (by default) or csv if specified (format='csv').
    """
    rgpy = grepy(search, in_path)
    res = {} # empty dictionray to store the matches
    for index, match in enumerate(rgpy):
        res[index+1] = {'paths': match['data']['path']['text'].split('/')[-1],# selects only the file_name
                    'lines':f"{match['data']['line_number']}",
                    'texts':f"{match['data']['lines']['text']}"}
    
    df_res = pd.DataFrame.from_dict(res, orient='index', columns=['path', 'lines', 'text'])
    
    if format == 'html':
        return df_res.to_html(out_path)
    else:
        return df_res.to_csv(out_path)

###################################################################
# SearchITI using RipGrep
###################################################################

def ripgreper(search:str, path:str, cxt=0):
    """Returns a list of dictionaries in json format with listing all the results.
    The context (cxt) is set to 0, which means that only the line with
    the matching results will be resply in the DataFrame. To get more 
    lines displayed before and after the matching results, the cxt can
    be increased to 1 or 2.
    The search is the string that will be searched in the path.
    The path leads to the file or folder which will be searched.
    """

    result_json = subprocess.run(['rg', # the commandline to run RipGrep
                            search, # the term(s) that will be searched
                            path, # leads to the file or folder where the search will occur
                            '-C', # adds a the Context flag to add more lines around the match
                            str(cxt), # defaults to 0, can be increased to 1 or 2
                            '--stats', # outputs a list of dictionaries in the json format
                            '--json'],
                            stdout=subprocess.PIPE)

    return [json.loads(line) for line in result_json.stdout.decode('utf-8').splitlines()]

def rg_to_df(search:str, path:str, cxt=0):
    """Returns a Pandas DataFrame storing the match to the search.
    The context (cxt) is set to 0, which means that only the line with
    the matching results will be resply in the DataFrame. To get more 
    lines displayed before and after the matching results, the cxt can
    be increased to 1 or 2.
    The search is the string that will be searched in the path.
    The path leads to the file or folder which will be searched.
    """

    json_lines = ripgreper(search, path, cxt)

    stats = json_lines[-1]['data']['stats']

    print(f"""
    Search statistics:\n
    {stats['elapsed']['human']} seconds
    {stats['matched_lines']} matched lines
    {stats['matches']} matches
    {stats['searches_with_match']} files contained matches""")

    res = {} # empty dictionary to store the matches

    if cxt>0: # with context, the results contains the match and the cxt number of lines around the match
        for index, line in enumerate(json_lines):
            if line['type'] == 'match': # excludes begin, end and summary
                # attributes to each index a dictionary that contains
                # the path, line_number and text for each search match
                # and merges the context lines with the match line.
                res[index] = {'paths': line['data']['path']['text'].split('/')[-1],
                            'lines':f"{json_lines[index-1]['data']['line_number']}-{json_lines[i+1]['data']['line_number']}",
                            'texts':f"{json_lines[index-1]['data']['lines']['text']} {line['data']['lines']['text']} {json_lines[index+1]['data']['lines']['text']}"}

    else: # without context, the result contains only the match line
        for index, line in enumerate(json_lines):
            if line['type'] == 'match': # excludes begin, end and summary
                # creates a dict of dict that contains the path,
                # line_number and text for each search match and
                res[index] = {'paths': line['data']['path']['text'].split('/')[-1],
                            'lines':f"{line['data']['line_number']}",
                            'texts':f"{line['data']['lines']['text']}"}

    return pd.DataFrame.from_dict(res, orient='index', columns=['paths', 'lines', 'texts'])

def rg_to_csv(out_path:str, search:str, in_path:str, cxt=0):
    """Returns a csv file with all the matches to `search` within in_path.
    It uses RipGrep to search in the file or folder within in_path.
    The out_path is the path to the csv file in which the results will be written.
    The search is the string that will be searched in the in_path.
    The in_path leads to a file or folder which will be searched.
    The cxt (context) flag gives the number of lines that will be displayed around
    the match, it defaults to 0 but can be increased to 1 or 2.
    """
    df = rg_to_df(search, in_path, cxt)
    return df.to_csv(out_path)

def rg_to_html(out_path:str, search:str, in_path:str, cxt=0):
    """Returns an html file with all the matches to `search` within in_path.
    It uses RipGrep to search in the file or folder within in_path.
    The out_path is the path to the csv file in which the results will be written.
    The search is the string that will be searched in the in_path.
    The in_path leads to a file or folder which will be searched.
    The cxt (context) flag gives the number of lines that will be displayed around
    the match, it defaults to 0 but can be increased to 1 or 2.
    """
    df = rg_to_df(search, in_path, cxt)
    return df.to_html(out_path)