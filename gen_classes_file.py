import os
import re
from pprint import pprint
from tqdm import tqdm
from matplotlib import pyplot as plt

def generate_classes_file(datadir, tgtfile):
    files = os.listdir(datadir)
    items = [(file, float(re.findall(r"_([\d]+)CM", file)[0]))for file in files]
    items.sort(key=lambda i:i[1])
    pprint(items)

    classes = []
    for item in tqdm(items, desc="GenClassesFile"):
        
        with open(os.path.join(datadir, item[0])) as fr:
            class_count = max([float(l.strip().split(" ")[-1]) for l in fr])
        classes.append(class_count)
    pprint(classes)
    with open(tgtfile, "w") as fw:
        fw.writelines([ str(int(c))+'\n' for c in classes])

def show_classes(classes_file):
    with open(classes_file) as fr:
        classes = [int(l.strip()) for l in fr.readlines() if l.strip()]

    plt.bar([ i for i in range(len(classes))], classes)
    plt.title("AVE: %.2f"%(sum(classes)/len(classes)))
    plt.show()


if __name__ == "__main__":
    # generate_classes_file("NEW CLUST 27T 25C FOR HUANGSIYUAN/CO2", 'MSCK25-DATA-NEW-HUANGSIYUAN/CO2.classes')
    generate_classes_file("NEW CLUST 27T 25C FOR HUANGSIYUAN/H2O", 'MSCK25-DATA-NEW-HUANGSIYUAN/H2O.classes')
    # show_classes("MSCK25-DATA-NEW-HUANGSIYUAN/H2O.classes")
    show_classes("/home/manager/Desktop/bysj/CODE 2018 FOR HUANGSIYUAN/MSCK25_1D-NEW/H2O/CASE-11-20/400X4_E7_E-6_adam_E-6_E-4/H2O.classes")
