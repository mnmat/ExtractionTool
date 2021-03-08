import os
import csv

run = "325001"

with open (run+".py","r") as f:
    data = f.read()

# Create dictionary with HLT paths as key and hltL1s objects as values

HLT_paths={}
for item in data.split('\n'):
    if "cms.Path(" in item and "process.hltL1s" in item:
        hlt = item.split("_v")[0].split("process.")[1]
        HLT_paths[hlt] = []
        temp = item.split("process.hltL1s")
        for i in range(1,len(temp)):
            l1 = item.split("process.hltL1s")[i].split(" +")[0]
            HLT_paths[hlt].append(l1)

# hltL1s combine multiple L1 seeds. Create mapping between hltl1s objects to all L1 seeds

L1_seeds={}
new = data.split("\n)\n")

for ele in new:
    if " = cms.EDFilter" in ele:
        for seed in HLT_paths.values():
            for ding in seed:
                if ding in ele and "cms.string( " in ele:
                    L1_seeds[ding] = ele.split('cms.string( "')[1].split('" ),\n')[0]

# Create dictionary mapping HLT paths to L1 seeds

combined = {}
for key in HLT_paths.keys():
    combined[key] = []
    for path in HLT_paths[key]:
        try:
            combined[key].append(L1_seeds[path])
        except:
            pass

with open("test_"+run+".csv","w") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["HLT","Seed"])
    for key in combined.keys():
        for ele in combined[key]:
            writer.writerow([key,ele])

