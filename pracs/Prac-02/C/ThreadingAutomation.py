import os

threadVar = "#define Thread_Count"
txtFileNaming = "fileOut = fopen"

for i in range(1, 6):
    # Change thread count
    f = open("./src/CHeterodyning_threaded.h", "r")
    lines = f.read()
    lines = lines.split("\n")
    f.close()

    for j in range(len(lines)):
        if lines[j].find(threadVar) > -1:
            print("============================")
            print("= " + str(2**i) + " threads =")
            print("=============================")
            lines[j] = threadVar + " " + str(2**i) + "\n"
            break

    f = open("./src/CHeterodyning_threaded.h", "w")
    f.write("\n".join(lines))
    f.close()

    # change output file
    f = open("./src/CHeterodyning_threaded.c", "r")
    lines = f.read()
    lines = lines.split("\n")
    f.close()

    for k in range(len(lines)):
        if lines[k].find(txtFileNaming) > -1:
            lines[k] = "    fileOut = fopen(\"output/CHeterodyning_threaded_x" + str(
                2**i) + ".txt\", \"w\");"
            break

    f = open("./src/CHeterodyning_threaded.c", "w")
    f.write("\n".join(lines))
    f.close()

    os.system("make clean")
    os.system("make threaded")
    os.system("make run_threaded")
