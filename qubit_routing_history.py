"""
This is based around routing algorithms.
Compare initial qubit layouts with final ones after the routing alg.
Green means in both initial and final layout.
Red means only in initial.
Blue means only in final.
"""
# Testing
from qiskit.providers import BackendV2
from qiskit_ibm_runtime.fake_provider import FakeAuckland, FakeWashingtonV2
from qiskit.circuit.library import QFT

# Needed in tool
from qiskit.visualization import plot_gate_map
from qiskit.utils import optionals as _optionals
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager, PassManager, Layout
 
@_optionals.HAS_MATPLOTLIB.require_in_call
@_optionals.HAS_GRAPHVIZ.require_in_call
def plot_layout_difference(backend: BackendV2, circuit: QuantumCircuit, filename: str, pass_manager: PassManager = None):
    """
    Take a circuit, plot it on backend on some initial config, run layout alg, plot output with differences.
    """
    if pass_manager is None:
        pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend, layout_method="trivial")
    post_transpile = pass_manager.run(circuit).layout
    init_layout = post_transpile.initial_virtual_layout(filter_ancillas=True)
    final_layout = post_transpile.final_virtual_layout()
    color_list = color_layout_difference(backend, init_layout, final_layout)
    plot_gate_map(backend=backend, qubit_color=color_list, filename=filename)


def color_layout_difference(backend: BackendV2, lay_init: Layout, lay_final: Layout) -> list[str]:
    """
    Used to generate qubit_color lists for use with plot_gate_map()
    """
    num_qubits = backend.num_qubits
    phys_init = lay_init.get_physical_bits()
    phys_final = lay_final.get_physical_bits()
    color_list = ["grey" for i in range(num_qubits)]
    for phys_q in phys_init.keys():
        if phys_q in phys_final.keys():
            color_list[phys_q] = "green"
        else:
            color_list[phys_q] = "red"
    for phys_q in phys_final.keys():
        if phys_q not in phys_init.keys():
            color_list[phys_q] = "blue"
    return color_list

def main():
    backend = FakeWashingtonV2()
    num_qubits = 50
    test_QFT = QFT(num_qubits=num_qubits)
    #triv_lay = [i + 1 for i in range(num_qubits)]
    pass_mng = generate_preset_pass_manager(optimization_level=3, backend=backend, layout_method="sabre", routing_method="basic")
    plot_layout_difference(backend, test_QFT, "test.png", pass_mng)


if __name__ == "__main__":
    main()