# Human Perception Study Design

## Overview
This study evaluated how algorithmic design choices in phosphene-based visual simulations affect human interpretability and confidence. The experiment focused on understanding perceptual performance under varying simulation and preprocessing conditions, using controlled visual stimuli and quantitative evaluation metrics.

The study was conducted as part of an undergraduate honors thesis and followed approved human-subject research protocols.

---

## Experimental Objective
The primary objective was to assess how variations in:
- image preprocessing strategies
- phosphene density
- phosphene shape

influence human recognition accuracy and confidence when viewing phosphene-rendered visual stimuli.

---

## Experimental Platform
The experiment was implemented using an online survey platform to enable controlled presentation of visual stimuli and standardized response collection. Stimuli were generated offline and embedded into the survey environment.

All participant interactions were limited to visual perception tasks and self-reported responses.

---

## Stimulus Generation
Stimuli were generated using a phosphene simulation pipeline built on a biologically inspired cortical model. Input images and video frames were preprocessed using computer vision techniques prior to phosphene rendering.

Key stimulus parameters included:
- phosphene density
- phosphene spatial arrangement and shape
- preprocessing method (e.g., edge-based filtering)

Stimuli were generated programmatically to ensure consistency and reproducibility across experimental conditions.

---

## Task Design
Participants were presented with phosphene-rendered visual stimuli and asked to complete recognition tasks under controlled conditions.

For each stimulus, participants:
- selected a response corresponding to the perceived content
- provided a confidence rating for their response

Trials were organized into blocks to minimize fatigue and learning effects. Presentation order was randomized to reduce ordering bias.

---

## Data Collected
The following data were collected for each trial:
- binary response accuracy (correct / incorrect)
- confidence rating on a discrete scale
- stimulus condition metadata (parameter labels only)

No personally identifying information was collected.

---

## Performance Metrics
Perceptual performance was evaluated using Signal Detection Theory (SDT), with sensitivity quantified using d′ (d-prime). Confidence ratings were analyzed to assess metacognitive alignment with task accuracy.

Analysis focused on relative comparisons between experimental conditions rather than absolute performance thresholds.

---

## Ethics and Privacy
The study was conducted with institutional ethics approval. All participants provided informed consent prior to participation.

To protect participant privacy:
- raw response data are not included in this repository
- survey instruments and platform-specific configuration files are excluded
- only anonymized and aggregated analyses are discussed in accompanying documentation

---

## Scope of Repository Inclusion
This repository includes:
- scripts used to generate experimental stimuli
- analysis code used to compute perceptual performance metrics
- documentation describing experimental methodology

The full survey implementation and raw participant data are intentionally excluded.

---

## Notes
This document is intended to provide transparency into the experimental design without reproducing the full experimental dataset or survey implementation. Detailed results and statistical analyses are available for discussion in an interview setting.
