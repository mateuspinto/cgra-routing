CSRC = "c/main.c c/fsm/common.c c/fsm/SimpleWriteOnExec.c"
CC= "gcc"
CFLAGS= "-O2 -march=native -Wall -Wextra -Wno-unused-result"
CLIB= ""
CBIN= "bin/c"

OUTPUT_FOLDER = "mkdir output"
BIN_FOLDER = "mkdir bin"

VLIB = "cd verilog && vlib.exe work"
VLOG = "cd verilog && vlog.exe Testbench.sv SimpleWriteOnExec.sv"
VSIM = "cd verilog && vsim.exe Testbench"

import os
import glob

print("1- Compile C and run code")
print("2- Sinthesize verilog and run simulation")
print("3- Summarize output")
key_pressed = int(input("Select: "))

if key_pressed == 1:
    os.system(BIN_FOLDER)
    os.system(OUTPUT_FOLDER)
    os.system(CC + " " + CSRC + " -o " + CBIN + " " + CFLAGS + " " + CLIB) # Compiling

    edges_count = 0
    for group in sorted(glob.glob("benchmarks/*")):
        output_folder = "output/" + group.split("/")[1] + "/"
        os.system("mkdir " + output_folder)

        for bench in sorted(glob.glob(group + "/edge_list/*")):
            name = bench.split("/")[3]
            grid = (group + "/grid/verilog_" + name + ".out")
            bench_out_folder = output_folder + "/" + name + "/"
            os.system("mkdir " + bench_out_folder)

            for edge_list in sorted(glob.glob(bench + "/*")):
                output_csv = bench_out_folder + edge_list.split("/")[4].split(".")[0] + ".csv"
                os.system("./" + CBIN + " " + grid + " " + edge_list + " " + output_csv)
                if(edges_count==10):
                    break
                edges_count += 1
elif key_pressed == 2:
    os.system(VLIB)
    os.system(VLOG)
    os.system(VSIM)
elif key_pressed == 3:
    import pandas as pd
    import numpy as np
    import glob

    names=[]
    tables=[]
    for bench in sorted(glob.glob("output/cgrame/*")):
        names.append(bench)
        acc=[]
        for csv in sorted(glob.glob(bench + "/*")):
            acc.append(pd.read_csv(csv))
        tables.append((pd.concat(acc).mean()))

    for i in range(12):
        for j in range(len(tables[i])):
            if j==8 or j==9:
                print(str(round(tables[i][j], 10)) + " ", end='')
            elif j==7:
                print(str(round(tables[i][j]*100, 2)) + "% ", end='')
            else:
                print(str(round(tables[i][j],2)) + " ", end='')
        print()
else:
    print("Error")