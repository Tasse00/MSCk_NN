
# from sklearn.datasets.samples_generator import make_classification
from sklearn.neural_network import MLPClassifier
import logging
logging.basicConfig(level=logging.DEBUG)
from Data import DataReader
# import pickle
import os
from pathlib import Path
from sklearn import preprocessing
import multiprocessing
# queue = multiprocessing.Queue()

def worker(cfg, target_file, tgt_dir, queue=None):
    data_reader = DataReader()
    data_reader.load_file(target_file)

    X, y, raw_x_lines = data_reader.X, data_reader.y, data_reader._raw_x_str
    
    # X = preprocessing.scale(X)


    TOTAL_LEN = len(X)
    TRAIN_PERCENT = cfg['training_percent']
    SEP = int(TOTAL_LEN*TRAIN_PERCENT)
    X_train, X_test = X[:SEP], X[SEP:]
    y_train, y_test = y[:SEP], y[SEP:]
    mlp = MLPClassifier(**cfg['mlp_params'])

    # print("training")
    mlp.fit(X_train, y_train)
    # print("train done")
    _total_predicted_y = mlp.predict(X)
    _map = list(set(_total_predicted_y))
    total_predicted_y = [_map.index(y)+1 for y in _total_predicted_y]

    tgt_file = Path(tgt_dir)/Path(target_file).name

    os.makedirs((str(Path(tgt_file).parent)), exist_ok=True)

    with open(str(tgt_file), 'w') as fw:
        for _x, _y, raw_x_line in zip(X, total_predicted_y, raw_x_lines):
            # fw.writelines( "    "+"     ".join(["%.10e"%(_/data_reader.TIMES) for _ in _x]) +"   "+str(_y)+"\n")
            fw.write(raw_x_line + "%4d"%_y + "\n")

    data = {
            # "train": mlp.score(X_train, y_train),
            # "test": mlp.score(X_test, y_test),
            # "file":str(target_file)
    }
    if queue:
        queue.put(data)
    else:
        return data

cfg = {
    "mlp_params":{
        "hidden_layer_sizes":tuple([48,200,25]), # now 400
        "max_iter":10000000, 
        "alpha":1e-6,
        "solver":'adam', 
        "verbose":False, 
        "tol":1e-6, 
        "random_state":1,
        "learning_rate_init":.0001
        
    },
    "training_percent": 0.99
}


if __name__ == "__main__":
    import os
    from tqdm import tqdm
    import multiprocessing

    queue = multiprocessing.Manager().Queue()
    pool = multiprocessing.Pool(1)
    
    files = []
    for root, dirs, _files in os.walk('NEW CLUST 27T 25C/H2O'):
        files.extend([str(Path(root)/f) for f in _files])

    res = []
   
    to_deal_files = []
    for f in tqdm(files):
        if str(f).endswith("27T_25C") and "CLUST" in str(f):
        # if not str(f).endswith("27T_25C"):
            to_deal_files.append(str(f))
    
    to_deal_files.sort()


    # to_deal_files = to_deal_files[400:450]
    # to_deal_files = [i for i in to_deal_files if "_66" in i]

    for f in tqdm(to_deal_files):
        # res.append(worker(cfg, f, "predict/H2O"))
        pool.apply_async(worker, (cfg, f, "predict/H2O", queue))
        
    res = [queue.get() for f in tqdm(to_deal_files)]
    # with open("score.json", "w") as fw:
    #     import json
    #     json.dump(res, fw)
