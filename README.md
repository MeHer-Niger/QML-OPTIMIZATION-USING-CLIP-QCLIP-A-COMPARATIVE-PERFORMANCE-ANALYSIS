# QML-OPTIMIZATION-USING-CLIP-QCLIP-A-COMPARATIVE-PERFORMANCE-ANALYSIS

# 🧠 CLIP & Quantum CLIP (qCLIP) Implementations

This repository contains two implementations of the CLIP model — one classical and one quantum-enhanced — for image-text similarity matching and classification using the **Food101** dataset. The goal is to evaluate how quantum circuits can enhance or complement traditional deep learning models.

---

## 📁 Project Structure


---

## 🔍 Overview

| Model  | Description |
|--------|-------------|
| **CLIP**   | Uses OpenAI's `clip-vit-base-patch32` to encode image features from Food101 and perform similarity matching based on cosine scores. |
| **qCLIP**  | Enhances the classical pipeline with a PennyLane-based quantum circuit using simulated qubits. Processes an image’s grayscale pixel intensities as quantum inputs and optimizes them for embedding. |

---

## 🧪 Technologies Used

- Transformers (CLIP Model)
- Torch (PyTorch)
- Datasets (HuggingFace)
- PennyLane & PennyLane-Qiskit (Quantum processing)
- NumPy, Matplotlib
- Google Colab

---

## 📦 Install dependencies

    ```bash
    pip install torch transformers datasets matplotlib
    pip install pennylane pennylane-qiskit  # For qCLIP only

---

## 🚀 How to Run

**🧠 Classical CLIP**
   
    ```bash
    python clip_implementation.py

- Loads Food101 dataset
- Extracts embeddings from random image samples
- Compares a user-provided image to top-50 most similar dataset images
- Plots results and accuracy

**🧠 Quantum CLIP (qCLIP)**
    
    ```bash
    python qclip_implementation.py

- Converts uploaded image into grayscale
- Uses PennyLane to encode the image into quantum parameters
- Optimizes a quantum circuit (RX/RY/CNOT gates)
- Uses final quantum state string as part of the CLIP model’s text-image similarity pipeline

---

## 📊 Example Use Case

- Query image: 🍕 Pizza Margarita
- Task: Find visually or semantically similar images from Food101
- Output: Top 50 similar samples with label matching accuracy

---

## 🔬 Notes

- The qCLIP is experimental and leverages classical simulation (default.qubit) in PennyLane.
- You can plug in a real quantum backend (like IBMQ) for actual quantum inference.

---

## 📈 Accuracy Evaluation

After matching 50 images using cosine similarity:
Accuracy (percentage of top-k matches with the correct label)
accuracy = (max_occurrences(label_arr) / top_k) * 100

---

## 📄 License
MIT License. Use freely and contribute!

