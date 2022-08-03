#%%
import subprocess
import os
import json
import shlex
import requests

#%%
def parse_lnk_file(file_path):
    output_dir = './output'
    p = subprocess.run(shlex.split("./parser/LECmd.exe -f {} --json ./output".format(file_path)), capture_output=False)
    # print(p)
    files = os.listdir(output_dir)
    data = None
    if len(files) > 0:
        with open(os.path.join(output_dir, files[0]), 'r') as f:
            data = f.read()
    else:
        return None
    for file in files:
        os.remove(os.path.join(output_dir, file))
    
    return json.loads(data)

#%%
js = parse_lnk_file(r'./parser/example.lnk')
print(js)
# %%
resp = requests.get('http://localhost:8000/', data=json.dumps(js))
# %%
