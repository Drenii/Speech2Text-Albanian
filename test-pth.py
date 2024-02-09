import torch
import torch.nn as nn

# Define the language model class
class LanguageModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super(LanguageModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.rnn = nn.GRU(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        embed = self.embedding(x)
        output, _ = self.rnn(embed)
        output = self.fc(output)
        return output

# Set the hyperparameters
vocab_size = 128  # Number of unique characters in the Albanian language
embedding_dim = 64
hidden_dim = 128

# Load the trained model
model = LanguageModel(vocab_size, embedding_dim, hidden_dim)
model.load_state_dict(torch.load('albanian_language_model.pth'))
model.eval()

# Use the model for text generation
start_text = 'Hello'
max_length = 100
with torch.no_grad():
    inputs = torch.tensor([ord(char) for char in start_text]).unsqueeze(0)
    hidden_state = None

    for _ in range(max_length):
        outputs, hidden_state = model(inputs, hidden_state)
        predicted = torch.argmax(outputs[:, -1, :], dim=1)
        next_char = chr(predicted.item())
        print(next_char, end='')

        inputs = predicted.unsqueeze(0)

