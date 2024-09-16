"""
This is based around routing algorithms.
Compare initial qubit layouts with final ones after the routing alg.
Green means in both initial and final layout.
Red means only in initial.
Blue means only in final.
"""

from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.visualization import plot_gate_map
 
backend = GenericBackendV2(num_qubits=4)
 
plot_gate_map(backend, filename="test.png")