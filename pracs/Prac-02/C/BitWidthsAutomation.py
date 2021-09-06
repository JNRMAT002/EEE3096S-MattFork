import os

txtFileNaming = "fileOut = fopen"

##########################
# Compile Float Bitwidth #
##########################
# Change bitwidth in CHeterodyning.c
f = open("./src/CHeterodyning.c", "r")
lines = f.read()
lines = lines.split("\n")
f.close()

for k in range(len(lines)):
    if lines[k].find(txtFileNaming) > -1:
        lines[k] = "    fileOut = fopen(\"output/CHeterodyning_float.txt\", \"w\");"
        break

f = open("./src/CHeterodyning.c", "w")
f.write("\n".join(lines))
f.close()

os.system('make clean')
os.system('make FPFLAG=')
os.system('make run')


###########################
# Compile Double Bitwidth #
###########################
# Change bitwidth in CHeterodyning.c
f = open("./src/CHeterodyning.c", "r")
lines = f.read()
lines = lines.split("\n")
f.close()

for k in range(len(lines)):
    if not(lines[k].find("double t") > -1):
        lines[k] = lines[k].replace("float", "double")

    if lines[k].find(txtFileNaming) > -1:
        lines[k] = "    fileOut = fopen(\"output/CHeterodyning_double.txt\", \"w\");"

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
os.system('make FPFLAG=')
os.system('make run')


###########################
# Compile __fp16 Bitwidth #
###########################

# Change bitwidth in CHeterodyning.c
f = open("./src/CHeterodyning.c", "r")
lines = f.read()
lines = lines.split("\n")
f.close()

for k in range(len(lines)):
    if not(lines[k].find("double t") > -1):
        lines[k] = lines[k].replace("double", "__fp16")

    if lines[k].find(txtFileNaming) > -1:
        lines[k] = "    fileOut = fopen(\"output/CHeterodyning_fp16.txt\", \"w\");"

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
os.system('make FPFLAG=-mfp16-format=ieee')
os.system('make run')
