import torchmetrics.classification
from extract_data import DataExtractor
import torch
import torch.nn as nn
import pandas as pd
import torch.optim as optim
import torchmetrics
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split

features = pd.read_csv("kingfisher-chess/features.csv")
features = features.to_numpy().reshape(-1, 6, 8, 8)

labels = pd.read_csv("kingfisher-chess/labels.csv")
labels = labels.to_numpy().reshape(-1)

label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)
num_classes = len(label_encoder.classes_)

X_train, X_test, y_train, y_test = train_test_split(features, encoded_labels, test_size=0.2, random_state=30)

model = nn.Sequential(
    nn.Conv2d(6, 64, 3, padding=1),
    nn.ReLU(),
    nn.Conv2d(64, 128, 3, padding=1),
    nn.ReLU(),
    nn.Conv2d(128, 128, 3, padding=1),
    nn.ReLU(),

    nn.Flatten(),
    nn.Linear(128 * 8 * 8, 256),
    nn.ReLU(),
    nn.Linear(256, num_classes)
)

batch_size = 64
epochs = 100
learning_rate = 0.01

X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.long)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.long)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

loss_fn = nn.CrossEntropyLoss()

optimizer = optim.SGD(model.parameters(), lr=learning_rate)

acc = torchmetrics.classification.Accuracy(task='multiclass', num_classes=num_classes).to(device)

train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

for epoch in range(epochs):
    model.train()
    train_loss, train_acc = 0, 0

    for X_data, y_data in train_dataloader:
        X_data, y_data = X_data.to(device), y_data.to(device)

        optimizer.zero_grad()
        predictions = model(X_data)
        
        loss = loss_fn(predictions, y_data)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        train_acc += acc(predictions, y_data)

    avg_loss = train_loss / len(train_dataloader)
    avg_acc = train_acc / len(train_dataloader)

    print(f"Epoch {epoch+1}/{epochs} \nLoss: {avg_loss:.4f} \nAccuracy: {avg_acc:.4f} \n")

model.eval()
test_loss, test_acc = 0, 0
with torch.no_grad():
    for X_data, y_data in test_dataloader:
        X_data, y_data = X_data.to(device), y_data.to(device)

        predictions = model(X_data)
        loss = loss_fn(predictions, y_data)

        test_loss += loss.item()
        test_acc += acc(predictions, y_data)

test_loss /= len(test_dataloader)
test_acc /= len(test_dataloader)

print(f"Test Loss: {test_loss:.4f} \nTest Accuracy: {test_acc:.4f} \n")