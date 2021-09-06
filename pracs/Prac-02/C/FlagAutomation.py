import os

flagList = ['O0', 'O1', 'O2', 'O3', 'Ofast', 'Os', 'Og']
txtFileNaming = "fileOut = fopen"

for flag in flagList:
    # change output file
    f = open("./src/CHeterodyning.c", "r")
    lines = f.read()
    lines = lines.split("\n")
    f.close()

    for k in range(len(lines)):
        if lines[k].find(txtFileNaming) > -1:
            lines[k] = "    fileOut = fopen(\"output/CHeterodyning_" + \
                flag + ".txt\", \"w\");"
            break

    f = open("./src/CHeterodyning.c", "w")
    f.write("\n".join(lines))
    f.close()

    os.system('make clean')
    os.system('make BIGOOPT=-' + flag + ' FUNROLL=')
    os.system('make run')

    # change output file
    f = open("./src/CHeterodyning.c", "r")
    lines = f.read()
    lines = lines.split("\n")
    f.close()

    for k in range(len(lines)):
        if lines[k].find(txtFileNaming) > -1:
            lines[k] = "    fileOut = fopen(\"output/CHeterodyning_" + \
                flag + "_funroll.txt\", \"w\");"
            break

    f = open("./src/CHeterodyning.c", "w")
    f.write("\n".join(lines))
    f.close()

    os.system('make clean')
    os.system('make BIGOOPT=-' + flag + ' FUNROLL=-funroll-loops')
    os.system('make run')
