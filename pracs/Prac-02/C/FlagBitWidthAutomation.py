import os

os.system('rm -r -f optout')
os.system('mkdir optout')
# os.system('sudo apt install zip')

flagList = ['O0', 'O1', 'O2', 'O3', 'Ofast', 'Os', 'Og']
txtFileNaming = "fileOut = fopen"

##########################
# Compile Float Bitwidth #
##########################


def compileFloat(bigOFlag, funRollFlag):
    # Change bitwidth in CHeterodyning.c
    f = open("./src/CHeterodyning.c", "r")
    lines = f.read()
    lines = lines.split("\n")
    f.close()

    for k in range(len(lines)):
        if not(lines[k].find("double t") > -1):
            lines[k] = lines[k].replace("__fp16", "float")
            lines[k] = lines[k].replace("double", "float")

        if lines[k].find(txtFileNaming) > -1:
            if funRollFlag:
                lines[k] = "    fileOut = fopen(\"optout/" + \
                    flag + "_float_funroll.txt\", \"w\");"
            else:
                lines[k] = "    fileOut = fopen(\"optout/" + \
                    flag + "_float.txt\", \"w\");"

    f = open("./src/CHeterodyning.c", "w")
    f.write("\n".join(lines))
    f.close()

    # Change bitwidth in globals.h
    f = open("./src/globals.h", "r")
    lines = f.read()
    lines = lines.split("\n")
    f.close()

    for k in range(len(lines)):
        if not(lines[k].find("double t") > -1):
            lines[k] = lines[k].replace("__fp16", "float")
            lines[k] = lines[k].replace("double", "float")

    f = open("./src/globals.h", "w")
    f.write("\n".join(lines))
    f.close()

    os.system('make clean')

    if funRollFlag:
        os.system('make FPFLAG= BIGOOPT=-' +
                  bigOFlag + ' FUNROLL=-funroll-loops')
    else:
        os.system('make FPFLAG= BIGOOPT=-' +
                  bigOFlag + ' FUNROLL=')

    os.system('make run')


###########################
# Compile double Bitwidth #
###########################


def compileDouble(bigOFlag, funRollFlag):
    # Change bitwidth in CHeterodyning.c
    f = open("./src/CHeterodyning.c", "r")
    lines = f.read()
    lines = lines.split("\n")
    f.close()

    for k in range(len(lines)):
        if not(lines[k].find("double t") > -1):
            lines[k] = lines[k].replace("float", "double")

        if lines[k].find(txtFileNaming) > -1:
            if funRollFlag:
                lines[k] = "    fileOut = fopen(\"optout/" + \
                    flag + "_double_funroll.txt\", \"w\");"
            else:
                lines[k] = "    fileOut = fopen(\"optout/" + \
                    flag + "_double.txt\", \"w\");"

    f = open("./src/CHeterodyning.c", "w")
    f.write("\n".join(lines))
    f.close()

    # Change bitwidth in globals.h
    f = open("./src/globals.h", "r")
    lines = f.read()
    lines = lines.split("\n")
    f.close()

    for k in range(len(lines)):
        if not(lines[k].find("double t") > -1):
            lines[k] = lines[k].replace("float", "double")

    f = open("./src/globals.h", "w")
    f.write("\n".join(lines))
    f.close()

    os.system('make clean')

    if funRollFlag:
        os.system('make FPFLAG= BIGOOPT=-' +
                  bigOFlag + ' FUNROLL=-funroll-loops')
    else:
        os.system('make FPFLAG= BIGOOPT=-' +
                  bigOFlag + ' FUNROLL=')

    os.system('make run')


###########################
# Compile __fp16 Bitwidth #
###########################


def compilefp16(bigOFlag, funRollFlag):
    # Change bitwidth in CHeterodyning.c
    f = open("./src/CHeterodyning.c", "r")
    lines = f.read()
    lines = lines.split("\n")
    f.close()

    for k in range(len(lines)):
        if not(lines[k].find("double t") > -1):
            lines[k] = lines[k].replace("double", "__fp16")

        if lines[k].find(txtFileNaming) > -1:
            if funRollFlag:
                lines[k] = "    fileOut = fopen(\"optout/" + \
                    flag + "_fp16_funroll.txt\", \"w\");"
            else:
                lines[k] = "    fileOut = fopen(\"optout/" + \
                    flag + "_fp16.txt\", \"w\");"

    f = open("./src/CHeterodyning.c", "w")
    f.write("\n".join(lines))
    f.close()

    # Change bitwidth in globals.h
    f = open("./src/globals.h", "r")
    lines = f.read()
    lines = lines.split("\n")
    f.close()

    for k in range(len(lines)):
        if not(lines[k].find("double t") > -1):
            lines[k] = lines[k].replace("double", "__fp16")

    f = open("./src/globals.h", "w")
    f.write("\n".join(lines))
    f.close()

    os.system('make clean')

    if funRollFlag:
        os.system('make FPFLAG=-mfp16-format=ieee BIGOOPT=-' +
                  bigOFlag + ' FUNROLL=-funroll-loops')
    else:
        os.system('make FPFLAG=-mfp16-format=ieee BIGOOPT=-' +
                  bigOFlag + ' FUNROLL=')

    os.system('make run')


def printHeading(bigOFlag, funRollFlag, bitWidth):
    if funRollFlag:
        print('##########################################################')
        print('#######     ' + bigOFlag +
              ' - Funroll Active - ' + bitWidth + '     ######')
        print('##########################################################')
    else:
        print('##########################################################')
        print('#######     ' + bigOFlag +
              ' - No Funroll - ' + bitWidth + '     ######')
        print('##########################################################')


###############################################


for flag in flagList:
    printHeading(flag, True, 'Float')
    compileFloat(flag, True)

    printHeading(flag, False, 'Float')
    compileFloat(flag, False)

    printHeading(flag, True, 'Double')
    compileDouble(flag, True)

    printHeading(flag, False, 'Double')
    compileDouble(flag, False)

    printHeading(flag, True, 'fp16')
    compilefp16(flag, True)

    printHeading(flag, False, 'fp16')
    compilefp16(flag, False)

os.system('zip -r optimisation.zip optout')
