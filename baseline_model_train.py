from data.load_mecab_data import *
from baseline_model import *
from utils import *

if __name__ == '__main__':
    # load data
    train_dataset, test_dataset = load_mecab_dataset()
    # load model
    device = get_device_name_agnostic()
    model = BaselineModel(input_size=768, hidden_size=128).to(device)
    # set hyper parameters
    optimizer = torch.optim.Adam(model.parameters(), lr=0.000001)
    loss_function = torch.nn.BCELoss()
    epochs = 800
    print_interval = 1
    batch_size = 16
    # train loop
    train_loop(train_data_set=train_dataset, test_data_set=test_dataset, epochs=epochs, model=model, device=device,
               batch_size=batch_size, loss_function=loss_function, optimizer=optimizer, print_interval=print_interval,
               accuracy_function=calculate_accuracy, X_on_the_fly_function=model.embed_texts, test_first=True)
