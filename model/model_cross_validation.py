import numpy as np
import torch.cuda
import random
from data.load_mecab_data import *
from model import *
from utils import *
from torch.utils.data import Subset
from sklearn.model_selection import KFold
from transformers import logging



if __name__ == '__main__':
    # ignore repetitive error
    logging.set_verbosity_error()
    # set seed
    seed = 2020
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    # load data
    # test_ratio: 1%, train_ratio: 99%
    dataset, _ = load_mecab_dataset(test_ratio=0.01, random_state=seed)
    # set hyper parameters
    loss_function = torch.nn.BCELoss()
    epochs = 10
    print_interval = 1
    batch_size = 16
    k_folds = 10
    shuffle = False
    # cross validation
    kfold = KFold(n_splits=k_folds, shuffle=shuffle)
    accuracies = []
    for fold, (train_indices, val_indices) in enumerate(kfold.split(dataset)):
        print(f"Fold {fold + 1}/{k_folds}")
        # split dataset
        train_set = Subset(dataset, train_indices)
        val_set = Subset(dataset, val_indices)
        # load model & init optimizer
        device = get_device_name_agnostic()
        model = Model(input_size=768, hidden_size=512).to(device)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.000001)
        # train loop
        current_accuracy = train_loop(train_data_set=train_set, test_data_set=val_set, epochs=epochs, model=model,
                                      device=device, batch_size=batch_size, loss_function=loss_function, optimizer=optimizer,
                                      print_interval=print_interval,
                                      X_on_the_fly_function=model.embed_texts, test_first=False, shuffle=shuffle,
                                      print_tsne=False, drop_last=False, print_graph=False)
        accuracies.append(current_accuracy)
    print("Accuracies = {}".format(accuracies))
    print("Average accuracy = {}\n".format(np.average(accuracies)))
