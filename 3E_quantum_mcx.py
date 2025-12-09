from qiskit import QuantumCircuit, QuantumRegister
from qclib.util import get_state

def quantum_mcx(circuito, controles, alvo):

    num_controles = len(controles)
    qubit_alvo = circuito.qubits[alvo]

    aux = QuantumRegister(1, name='auxiliares')
    circuito.add_register(aux)

    # Passo 1
    circuito.ccx(controles[0], controles[1], aux[0])

    for i in range(1, num_controles - 2, 2):
        circuito.ccx(controles[i+1], controles[i+2], controles[i])

    circuito.barrier()

    # Passo 2
    for i in range(0, num_controles-3):
        circuito.x(controles[i])

    circuito.barrier()

    # Passo 3
    circuito.ccx(controles[num_controles - 1], controles[num_controles - 4], controles[num_controles - 5])
    for i in range(num_controles - 5, 1, -2):
        circuito.ccx(controles[i], controles[i - 1], controles[i - 2])

    circuito.barrier()

    # Passo 4
    circuito.ccx(controles[0], aux[0], qubit_alvo)

    circuito.barrier()

    # Passo 5
    for i in range(0, num_controles - 5, 2):
        circuito.ccx(controles[i+1], controles[i+2], controles[i])
    circuito.ccx(controles[num_controles - 1], controles[num_controles - 4], controles[num_controles - 5])

    circuito.barrier()

    # Passo 6
    for i in range(0, num_controles - 3):
        circuito.x(controles[i])

    circuito.barrier()

    # Passo 7
    for i in range(num_controles - 2, 1, -2):
        circuito.ccx(controles[i], controles[i-1], controles[i-2])
    circuito.ccx(controles[0], controles[1], aux[0])



if __name__ == '__main__':

    circuito = QuantumCircuit(6)
    controles = [1,2,3,4,5]
    alvo = 0

    for i in controles:
        circuito.h(i)
    
    quantum_mcx(circuito, controles, alvo)

    print(circuito)
    print(get_state(circuito))
