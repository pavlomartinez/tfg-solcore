import numpy as np
import matplotlib.pyplot as plt
from solcore import material, si
from solcore.structure import Junction, Layer
from solcore.solar_cell_solver import solar_cell_solver, SolarCell
from solcore.state import State
from solcore.light_source import LightSource
import optuna

#DEFINIMOS LAS OPCIONES ################################################
options = State()
# Fuente láser 808 nm
options.light_source = LightSource(
    source_type='laser',
    center=808,        # nm
    linewidth=1,       # cuanto menor más monocromático
    power=5e4,         # W/m2 = 5 W/cm2
    output_units='power_density_per_nm'
)
options.theta = 0 # Incidencia perpendicular
options.pol = 'u' # Luz no polarizada
options.wavelength = np.linspace(790, 840, 300) * 1e-9  #no necesitamos todo el espectro
options.voltages = np.linspace(0, 1.2, 150)
options.internal_voltages = np.linspace(0, 1.2, 150)
options.light_iv = True
options.mpp = True
options.optics_method = 'TMM'
options.no_back_reflection = False
options.recalculate_absorption = True

def build_solar_cell(design_parameters):

    emitter_thickness = design_parameters.get("emitter_thickness", 500)  # nm
    base_thickness = design_parameters.get("base_thickness", 3500)       # nm
    emitter_doping = design_parameters.get("emitter_doping", 2e18)       # cm-3
    base_doping = design_parameters.get("base_doping", 1e17)             # cm-3

    TiO2 = material("TiO2")()
    SiO2 = material("SiO2")()

    ARC_layers = [
        Layer(si("94nm"), material=SiO2),
        Layer(si("61nm"), material=TiO2),
    ]

    GaInP_window = material("GaInP")(
        In=0.49,
        Na=si("5e18cm-3"),
        relative_permittivity=11.8,
        electron_minority_lifetime=5e-10,
        hole_minority_lifetime=5e-10,
    )

    GaAs_emitter = material("GaAs")(
        Na=si(f"{emitter_doping}cm-3"),
        electron_minority_lifetime=8e-10,
        hole_minority_lifetime=2e-9,
    )

    GaAs_base = material("GaAs")(
        Nd=si(f"{base_doping}cm-3"),
        electron_minority_lifetime=1e-8,
        hole_minority_lifetime=5e-9,
    )

    AlGaAs_bsf = material("AlGaAs")(
        Al=0.3,
        Nd=si("5e18cm-3"),
        relative_permittivity=11.6,
        electron_minority_lifetime=5e-10,
        hole_minority_lifetime=5e-10,
    )

    GaAs_buffer = material("GaAs")(
        Nd=si("5e18cm-3"),
        electron_minority_lifetime=5e-10,
        hole_minority_lifetime=5e-10,
    )

    GaAs_substrate = material("GaAs")(
        Nd=si("5e18cm-3"),
    )

    junction_layers = [
        Layer(si("50nm"), GaInP_window, role="window"),
        Layer(si(f"{emitter_thickness}nm"), GaAs_emitter, role="emitter"),
        Layer(si(f"{base_thickness}nm"), GaAs_base, role="base"),
        Layer(si("50nm"), AlGaAs_bsf, role="bsf"),
    ]

    solar_cell = SolarCell(
        ARC_layers + [
            Junction(
                junction_layers,
                kind="sesame_PDD",
                sn=1e4,
                sp=1e4,
                R_shunt=495.98e-4,
            ),
            Layer(si("1000nm"), GaAs_buffer),
            Layer(si("350um"), GaAs_substrate),
        ],
        substrate=None,
        R_series=1.444e-6,
        area=1e-4,
    )

    return solar_cell

def solar_cell_simulation(design_parameters):

    solar_cell = build_solar_cell(design_parameters)

    solar_cell_solver(solar_cell, "iv", options)

    results = {
        "Eff": solar_cell.iv["Eta"],
        "Voc": solar_cell.iv["Voc"],
        "Isc": solar_cell.iv["Isc"],
        "FF": solar_cell.iv["FF"],
        "Pmpp": solar_cell.iv["Pmpp"],
        "Vmpp": solar_cell.iv["Vmpp"],
        "Impp": solar_cell.iv["Impp"],
    }

    return results,solar_cell,solar_cell_solver

def objective(x):

    design_parameters = {

        "emitter_thickness": x.suggest_float(
            "emitter_thickness", 200, 3000
        ),

        "base_thickness": x.suggest_float(
            "base_thickness", 200, 3000
        ),

        "emitter_doping": x.suggest_float(
            "emitter_doping", 1e17, 8e18, log=True
        ),

        "base_doping": x.suggest_float(
            "base_doping", 1e16, 8e17, log=True
        ),
    }

    results = solar_cell_simulation(design_parameters)

    eff = results["Eff"]

    return eff


def plot_iv(solar_cell):
    plt.figure(figsize=(7, 5))

    V_sim = solar_cell.iv['IV'][0]
    J_sim = solar_cell.iv['IV'][1]      # A/m2
    I_sim = J_sim * solar_cell.area     # A

    
    
    plt.plot(
        V_sim,
        I_sim,
        color="#1f77b4",
         linestyle="-",
         linewidth=2.5,
         label="Célula optimizada"
    )

    

    # ESTÉTICA
    plt.xlabel("Voltaje (V)")
    plt.ylabel("Corriente (A)")
    plt.ylim(0, 3)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(right=0.75)
    plt.tight_layout()
    plt.savefig("direccion_guardado")  # poner la direccion/nombre archivo 
    plt.show()
    return results

    
if __name__ == "__main__":
    study = optuna.create_study(
        direction="maximize",
        sampler=optuna.samplers.TPESampler(seed=42),
        study_name="optimizacion_eff_5W_def", 
        storage="sqlite:///direccion_guardado",#poner la direccion y nombre del archivo
        load_if_exists=True,
    )
    study.optimize(
        objective,
        n_trials=50, #elegir el numero deseado de iteraciones
        n_jobs=1, # no se puede paralelizar (mezcla matrices y hace mal los calculos)
        show_progress_bar=True,
        catch=(ValueError, RuntimeError)
    )
    print("\nTotal trials:")
    print(len(study.trials))
    
    print("\nBest efficiency:")
    print(study.best_value)

    print("\nBest parameters:")
    print(study.best_params)

   