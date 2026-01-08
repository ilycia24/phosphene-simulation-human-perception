# Phosphene Simulation & Human Perception Analysis

## Overview
This project investigates how algorithmic design choices in phosphene simulation affect human interpretability of visual cortical prosthetic outputs. The work combines computer vision, simulation, and human-subject experimentation to evaluate perceptual performance quantitatively.

## Motivation
Visual cortical prostheses are constrained by low spatial resolution, making it critical to encode visual information in a way that remains interpretable to users. This project explores how image preprocessing, phosphene configuration, and simulation parameters influence human perception and confidence.

## System Design
- Biologically inspired phosphene simulation pipeline
- Image and video preprocessing using computer vision techniques
- Parameterized control of phosphene density and shape
- Exploratory integration with a deep-learning autoencoder
- Human perception experiments with controlled stimuli

## Human Experiment
- Sighted participants evaluated phosphene-rendered video stimuli
- Performance measured using Signal Detection Theory (d′)
- Confidence ratings analyzed to assess metacognitive sensitivity
- Study conducted under university ethics approval

## Key Findings
- Higher phosphene density improves perceptual sensitivity
- Circular phosphene shapes outperform irregular shapes
- Edge-based preprocessing (Canny) significantly increases interpretability
- Confidence correlates with accuracy for simpler stimuli

## Tech Stack
Python · OpenCV · PyTorch · MATLAB · NumPy · SciPy · Matplotlib

## Repository Structure
