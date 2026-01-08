# phosphene-simulation-human-perception
#Phosphene Simulation & Human Perception Analysis
Overview

This project explores how image preprocessing, phosphene configuration, and simulation parameters affect the human interpretability of visual cortical prosthetic outputs. The work combines computer vision, simulation, and human-subject experiments to evaluate perceptual performance quantitatively.

Motivation

Visual cortical prostheses are constrained by low spatial resolution, making it critical to encode visual information in a way that remains interpretable to users. This project investigates how algorithmic choices impact perception and confidence in simulated prosthetic vision.

System Design

Phosphene simulation pipeline built on a biologically inspired model

Image and video preprocessing using computer vision techniques

Parameterized control of phosphene density and shape

Integration with a deep-learning autoencoder (exploratory)

Human perception experiments with controlled stimuli

Human Experiment

Sighted participants evaluated phosphene-rendered video stimuli

Performance measured using Signal Detection Theory (d′)

Confidence ratings used to analyze metacognitive sensitivity

Study conducted with university ethics approval

Key Findings

Higher phosphene density improves perceptual sensitivity

Circular phosphene shapes outperform irregular shapes

Edge-based preprocessing (Canny) significantly increases interpretability

Confidence correlates with accuracy for simpler stimuli

Tech Stack

Python · OpenCV · PyTorch · MATLAB · NumPy · SciPy · Matplotlib

Notes

Raw participant data and identifying information have been excluded. This repository contains a cleaned and representative subset of the original research code.
