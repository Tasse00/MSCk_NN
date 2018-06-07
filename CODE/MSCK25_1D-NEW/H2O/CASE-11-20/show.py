'''
显示曲线
'''

from openpyxl import load_workbook
from math import fabs
import matplotlib.pyplot as plt

# RESDIR = "200X4_E7_E-6_adam_E-6_E-4"
# RESDIR = "49-200-25_E7_E-6_adam_E-6_E-4"
RESDIR = "all_case_result"
book = load_workbook('result.xlsx')
sheet = book.active

STD_IDX = 3
CASE_IDX = 0
cases = []
stds = []

CK1s = []
CK25s = []
MSCK25s = []

for row in list(sheet.rows)[1:]:
    stds.append(row[STD_IDX].value)
    cases.append(row[CASE_IDX].value)
    CK1s.append(row[6].value)
    CK25s.append(row[7].value)
    MSCK25s.append(row[8].value)

def loadResult(DIR):
    NNs = []
    for case in cases:
        with open('{}/{}.dat'.format(DIR, case)) as fr:
            NNs.append(-float(fr.readlines()[-1].strip().split()[0]))
    NNs = [ fabs((nn-std)/std) for nn,std in zip(NNs, stds)]
    return NNs

NNs400X4 = loadResult("400X4_E7_E-6_adam_E-6_E-4")
NNs200X4 = loadResult("0607_200X4_22.93")
NNs200X5 = loadResult("200X5_E7_E-6_adam_E-6_E-4")
NNs600X4 = loadResult("600X4_E7_E-6_adam_E-6_E-4")
NNs400X1 = loadResult("400X1_E7_E-6_adam_E-6_E-4")
NNs49_200_25 = loadResult("49-200-25_E7_E-6_adam_E-6_E-4")

cases = [int(c) for c in cases]


# exclude = [60, 80, 400]
exclude = []
idxs = [ cases.index(ec) for ec in exclude ]

# NNs = 
# CK1s = [ p for idx,p in enumerate(CK1s) if idx not in idxs]
# CK25s = [ p for idx,p in enumerate(CK25s) if idx not in idxs]
# MSCK25s = [ p for idx,p in enumerate(MSCK25s) if idx not in idxs]

# cases = 


handles = [
    # plt.plot(cases, NNs200X4)[0],
    plt.plot(cases, NNs400X4, '-*')[0],
    # plt.plot(cases, NNs200X5)[0],
    # plt.plot(cases, NNs600X4)[0],
    # plt.plot(cases, NNs400X1)[0],
    # plt.plot(cases, NNs49_200_25)[0],
    # plt.plot([ c for c in cases if c not in exclude], [ p for idx,p in enumerate(NNs) if idx not in idxs] ,  '-x')[0],
    plt.plot(cases,CK1s, '-x')[0],
    plt.plot(cases,CK25s,'-x')[0],
    plt.plot(cases,MSCK25s, '-x')[0],
]
labels = [ 
    # "NN200X4", 
    "NN400X4", 
    # "NN600X4", "NNs400X1", "NNs49_200_25", 
    "CK1", "CK25", "MSCK25"]
plt.xlabel("Case")
plt.ylabel("(M-LBL)/LBL")
plt.title("Relative LBL Error of Each Model")
plt.legend(handles=handles, labels=labels, loc="best")
plt.show()