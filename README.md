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

- 🤗 Transformers (CLIP Model)
- Torch (PyTorch)
- Datasets (HuggingFace)
- PennyLane & PennyLane-Qiskit (Quantum processing)
- NumPy, Matplotlib
- Google Colab

---

## 📦 Installation

Install dependencies:
```bash
pip install torch transformers datasets matplotlib
pip install pennylane pennylane-qiskit  # For qCLIP only


