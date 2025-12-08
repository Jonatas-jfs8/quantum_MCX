import numpy as np
import qiskit
from qclib.util import get_state
from qiskit.quantum_info import partial_trace, Statevector
    
if __name__ == '__main__':
    circuito_original = qiskit.QuantumCircuit(6)
    
    for i in range (1, 6):
        circuito_original.h(i)
    circuito_original.mcx([1, 2, 3, 4, 5], 0)
    
    print(circuito_original)
    print(get_state(circuito_original))
    
    circuito_novo = qiskit.QuantumCircuit(7)
    
    for i in range(1, 6):
        circuito_novo.h(i)
    # Passo 1
    circuito_novo.mcx([1, 2], 6)
    circuito_novo.x(2)
    circuito_novo.mcx([3, 4], 2)
    circuito_novo.x(1)
    circuito_novo.mcx([2, 5], 1)
    
    #Passo 2
    circuito_novo.mcx([1, 6], 0)
    
    #Passo 3
    circuito_novo.mcx([2, 5], 1)
    circuito_novo.x(1)
    circuito_novo.mcx([3, 4], 2)
    circuito_novo.x(2)
    circuito_novo.mcx([1, 2], 6)
    print(circuito_novo)
    print(get_state(circuito_novo))