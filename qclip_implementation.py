# -*- coding: utf-8 -*-
"""qCLIP_implementation(experimental).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18t1hzKi7DsnV-aGT8L8To5zk8UFFhOdF
"""

!pip install torch transformers datasets pennylane pennylane-qiskit

import pennylane as qml
from transformers import CLIPTokenizerFast, CLIPProcessor, CLIPModel
from PIL import Image
import requests
from datasets import load_dataset
import torch
import numpy as np

from transformers import AutoModel
access_token = "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"

dataset = load_dataset(
    'food101',
    split='train',
    ignore_verifications=False,  # set to True if seeing splits Error
    token=access_token
)

# Quantum circuit using PennyLane
dev = qml.device("default.qubit", wires=8)

@qml.qnode(dev)
def quantum_circuit(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.PauliZ(0))

# if you have CUDA or MPS, set it to the active device like this
device = "cuda" if torch.cuda.is_available() else \
         ("mps" if torch.backends.mps.is_available() else "cpu")
model_id = "openai/clip-vit-base-patch32"

# we initialize a tokenizer, image processor, and the model itself
tokenizer = CLIPTokenizerFast.from_pretrained(model_id,token=access_token)
processor = CLIPProcessor.from_pretrained(model_id,token=access_token)
model = CLIPModel.from_pretrained(model_id,token=access_token).to(device)

np.random.seed(0)
# select 100 random image index values
sample_idx = np.random.randint(0, len(dataset)+1, 10000).tolist()
# extract the image sample from the dataset
images = [dataset[i]['image'] for i in sample_idx]

from tqdm.auto import tqdm

batch_size = 16
image_arr = None

for i in tqdm(range(0, len(images), batch_size)):
    # select batch of images
    batch = images[i:i+batch_size]
    # process and resize
    batch = processor(
        text=None,
        images=batch,
        return_tensors='pt',
        padding=True
    )['pixel_values'].to(device)
    # get image embeddings
    batch_emb = model.get_image_features(pixel_values=batch)
    # convert to numpy array
    batch_emb = batch_emb.squeeze(0)
    batch_emb = batch_emb.cpu().detach().numpy()
    # add to larger array of all image embeddings
    if image_arr is None:
        image_arr = batch_emb
    else:
        image_arr = np.concatenate((image_arr, batch_emb), axis=0)

# from google.colab import files
# from PIL import Image

# # Upload an image file
# uploaded = files.upload()

# # Get the uploaded file name
# file_name = list(uploaded.keys())[0]

# # Open the uploaded image using PIL
# uploaded_image = Image.open(file_name)

# load image from link
from PIL import Image
import requests
url = 'https://images.unsplash.com/photo-1600028068383-ea11a7a101f3?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8UGl6emElMjBNYXJnaGVyaXRhfGVufDB8fDB8fHww'
uploaded_image = Image.open(requests.get(url, stream=True).raw)
uploaded_image

# Random initial parameters for the quantum circuit
image = uploaded_image.convert('L')
pixel_values = np.array(image) / 255.0
initial_params = pixel_values

# Quantum circuit optimization using PennyLane
def cost(params):
    return quantum_circuit(params)

# Optimize the quantum circuit parameters
learning_rate = 0.1
optimizer = qml.GradientDescentOptimizer(learning_rate)

# Number of optimization steps
steps = 100
for i in range(steps):
    initial_params = optimizer.step(cost, initial_params)

# Get quantum state as a string
quantum_state_str = str(quantum_circuit(initial_params))

# # Assuming quantum_state_str is a long text
# # Split the text into chunks of 512 tokens (adjust the size based on the model's limit)
# chunks = [quantum_state_str[i:i+100] for i in range(0, len(quantum_state_str), 100)]

# # Process each chunk separately
# for chunk in chunks:
#     inputs = processor(text=chunk, images=None, return_tensors="pt", max_length=100, truncation=True)
#     # Further processing or model inference with the inputs

# # use CLIP to encode tokens into a meaningful embedding
# text_emb = model.get_text_features(**inputs)
# # text_emb = model.get_text_features(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])

image = processor(
    text=quantum_state_str,
    images=uploaded_image,
    return_tensors='pt'
)['pixel_values'].to(device)

img_emb = model.get_image_features(image)

# import matplotlib.pyplot as plt
# # we can still visualize the processed image
# plt.imshow(image.squeeze(0).T)

text_emb2 = img_emb.cpu().detach().numpy()
scores = np.dot(text_emb2, image_arr.T)
scores.shape

top_k = 50
# get the top k indices for most similar vecs
idx = np.argsort(-scores[0])[:top_k]
idx

label_arr = []

def find_label(idx,dataset):
  for j in range(len(idx)):
    for i in range(len(dataset)):
        # Check if the current entry's image path matches the target image path
        if dataset[i]['image'] == images[idx[j]]:
            label_arr.append(dataset[i]['label'])
            break

# Find the label for the given image
find_label(idx, dataset)
label_arr

from collections import Counter
data_size = 50

def max_occurrences(arr):
    # Use Counter to count occurrences of each element in the array
    count_dict = Counter(arr)

    # Find the maximum occurrence
    max_occurrence = max(count_dict.values())

    return max_occurrence

(max_occurrences(label_arr)/data_size)*100

label_arr
max_element = max(label_arr)
# max_element
label_arr