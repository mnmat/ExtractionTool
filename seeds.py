import os
import csv

dir = "data/runs/"
files = os.listdir(dir)

runs = {}

for file in files:
    with open(dir + file,"r") as f:
        
        data = f.read()

    # Create dictionary with HLT paths as key and hltL1s objects as values

    HLT_paths={}
    for item in data.split('\n'):
        if "cms.Path(" in item and "process.hltL1s" in item:
            hlt = item.split("_v")[0].split("process.")[1]
            HLT_paths[hlt] = []
            temp = item.split("process.hltL1s")
            for i in range(1,len(temp)): # An HLT path can contain multiple hltL1s structures
                l1 = item.split("process.hltL1s")[i].split(" +")[0]
                HLT_paths[hlt].append(l1)

    # hltL1s combine multiple L1 seeds. Create mapping between hltl1s objects to all L1 seeds

    L1_seeds={}
    for ele in data.split("\n)\n"):
        if " = cms.EDFilter" in ele:
            for seed in HLT_paths.values():
                for ding in seed:
                    if ding in ele and "cms.string( " in ele:
                        L1_seeds[ding] = ele.split('cms.string( "')[1].split('" ),\n')[0]

    # Create dictionary mapping HLT paths to L1 seeds

    combined = {}
    for key in HLT_paths.keys():
        if key not in combined.keys():
            combined[key] = []
        for path in HLT_paths[key]:
            try:
                combined[key].append(L1_seeds[path])
            except:
                pass

    runs[file.split(".py")[0]] = combined

keys = set(runs[runs.keys()[1]].keys())|set(runs[runs.keys()[0]].keys())

if not os.path.exists("output"):
    os.mkdir("output")

with open("output/test.csv","w") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["HLT"] + runs.keys())

    for key in keys:
        # Count the max number of hltL1s structures for single HLT path
        ls = []
        for run in runs.keys():
            try:
                ls.append(len(runs[run][key]))
            except KeyError:
                ls.append(len([]))
        m = max(ls)

        for i in range(m): # Iterate through all seeds in possible multiple hltL1s structures for a single HLT path
            ls = []
            ls.append(key)
            for run in runs.keys():
                try:
                    ls.append(runs[run][key][i])
                except KeyError:
                    ls.append(None)

            writer.writerow(ls)