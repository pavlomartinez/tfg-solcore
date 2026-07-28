# tfg-solcore
# Optimization of GaAs Photovoltaic Converters with Solcore

Python-based simulation and optimization tool for the design and analysis of GaAs photovoltaic converters under monochromatic laser illumination.

This project was developed as part of my Bachelor's Thesis. It uses [Solcore](https://github.com/qpv-research-group/solcore5) to model the electrical and optical performance of photovoltaic devices and to optimize selected design parameters.

## Project overview

The script simulates a GaAs photovoltaic converter illuminated by a monochromatic laser source.

Its main purpose is to study how the device structure and operating conditions affect its photovoltaic performance and to identify configurations that maximize conversion efficiency.

## Main features

* Definition of a multilayer GaAs photovoltaic structure.
* Simulation under monochromatic laser illumination.
* Calculation of current–voltage characteristics.
* Evaluation of photovoltaic parameters such as:

  * Short-circuit current density.
  * Open-circuit voltage.
  * Fill factor.
  * Maximum output power.
  * Conversion efficiency.
* Optimization of selected device parameters.
* Comparison of different photovoltaic converter configurations.
* Generation of plots for the analysis of the results.

## Optimization

The script varies selected parameters of the photovoltaic converter to find the configuration that maximizes its performance.

Depending on the selected configuration, the optimized parameters may include:

* Layer thicknesses.
* Doping concentrations.
* Laser wavelength.
* Incident optical power.
* Parameters of the antireflection coating.

The optimization objective is primarily the maximization of the photovoltaic conversion efficiency.

## Technologies

* Python
* Solcore
* NumPy
* Matplotlib

## Installation

Clone the repository:

```bash
git clone https://github.com/[your-username]/[repository-name].git
cd [repository-name]
```

It is recommended to create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main script with:

```bash
python [script_name].py
```

The simulation parameters can be modified in the corresponding configuration section of the script.

After execution, the program generates the simulated photovoltaic parameters and the corresponding result plots.


## Academic context

This project was developed as part of the Bachelor's Thesis:

**“[Estudio de células solares a través de Solcore]”**

[USC]
[Physics]
[2026]

The repository contains the code developed for the simulation, analysis and optimization stages of the project. The complete thesis document is not necessarily included.

## References

* Solcore documentation and source code.
* Shan, T., & Qi, X. (2015). *Design and optimization of GaAs photovoltaic converter for laser power beaming*. Infrared Physics & Technology, 71, 144–150.

## Disclaimer

This repository was created for academic and educational purposes.

The simulation results depend on the physical models, material parameters and assumptions used in Solcore. They should not be interpreted as experimental validation of a fabricated device.

## Author

**[Pablo Martínez Regueira]**

* GitHub: https://github.com/pavlomartinez
* LinkedIn: [www.linkedin.com/in/pablo-martínez-a205b237b]
