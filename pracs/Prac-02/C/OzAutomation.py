import os

os.system('rm -r -f ozout')
os.system('mkdir ozout')
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
    if not(lines[k].find("double t") > -1):
        lines[k] = lines[k].replace("__fp16", "float")

    if lines[k].find(txtFileNaming) > -1:
        lines[k] = "    fileOut = fopen(\"ozout/floatOz.txt\", \"w\");"

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

f = open("./src/globals.h", "w")
f.write("\n".join(lines))
f.close()

os.system('make clean')
os.system('make make BIGOOPT=-Oz')
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
        lines[k] = "    fileOut = fopen(\"ozout/doubleOz.txt\", \"w\");"

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
os.system('make BIGOOPT=-Oz')
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
        lines[k] = "    fileOut = fopen(\"ozout/fpOz.txt\", \"w\");"

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
os.system('make BIGOOPT=-Oz FPFLAG=-mfp16-format=ieee')
os.system('make run')


# float avg
f = open("./ozout/floatOz", "r")
floatVals = f.read()
floatVals = floatVals.split("\n")
f.close()

floatAvg = 0

for val in floatVals:
    floatAvg += float(val)

floatAvg = floatAvg / len(floatVals)

# double avg
f = open("./ozout/doubleOz", "r")
doubleVals = f.read()
doubleVals = doubleVals.split("\n")
f.close()

doubleAvg = 0

for val in doubleVals:
    doubleAvg += float(val)

doubleAvg = doubleAvg / len(doubleVals)

# fp16 avg
f = open("./ozout/fpOz", "r")
fpVals = f.read()
fpVals = fpVals.split("\n")
f.close()

fpAvg = 0

for val in fpVals:
    fpAvg += float(val)

fpAvg = fpAvg / len(fpVals)

print("Float Avg:", floatAvg)
print("Double Avg:", doubleAvg)
print("fp16 Avg:", fpAvg)
