# ReadMe

This project provides a Python framework for simulating and localizing airborne rotor noise in urban environments. It combines source modeling, sound propagation, and microphone array-based localization using beamforming. The goal is to generate physically consistent acoustic signals and test localization algorithms under realistic conditions.

## Project Structure

- `AeroacousticSource.py`: Implements rotor noise generation, including tonal and broadband components, and combines them into a single source signal.

- `SoundPropagation.py`: Models acoustic propagation from the source to microphones, including distance attenuation, directivity, multipath reflections from obstacles, and environmental noise.

- `Localization.py`: Implements passive beamforming to estimate the source position by scanning a spatial grid and aligning signals from multiple sensors.

- `Theory/`: Contains explanatory notes on the modeling assumptions, limitations, and theoretical background for source generation, propagation, and localization methods.

- `example.py`: Demonstrates the full workflow, from generating the source signal to propagating it through an environment with obstacles, adding noise, and estimating its position using beamforming.

## Features

- Rotor noise modeling with adjustable tonal and broadband components.

- Sound propagation with adjustable microphone arrays and obstacle reflections.

- Source directivity modeled in 3D space.

- Recursive multipath reflection support.

- Noise addition with user-defined SNR.

- Beamforming-based localization with customizable spatial grids.

This framework serves as a testbed for acoustic localization algorithms and can be extended for more complex urban scenarios, including full 3D environments and higher-order reflections.
