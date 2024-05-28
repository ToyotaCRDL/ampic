import sys

args = sys.argv

assert(len(args) == 2)
networkData = args[1]

with open('src/tmp.sumocfg', 'r', encoding='utf-8') as file:
    filedata = file.read()

# 置換する
filedata = filedata.replace("Xnet", networkData)
filedata = filedata.replace("Xrou", networkData)

# ファイルに書き込む
with open(networkData+'.sumocfg', "w", encoding="utf-8") as file:
    file.write(filedata)
