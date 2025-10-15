import torch
print(torch.__version__)          # PyTorch version
print(torch.version.cuda)         # Should be 12.8
print(torch.cuda.is_available())  # Should return True

