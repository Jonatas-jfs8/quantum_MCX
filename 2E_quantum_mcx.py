from qiskit import QuantumCircuit, QuantumRegister
from qclib.util import get_state

def quantum_mcx(circuito, controles, alvo):

    num_controles = len(controles)
    qubits_controle = [circuito.qubits[i] for i in controles]
    qubit_alvo = circuito.qubits[alvo]

    num_aux = num_controles - 2

    aux = QuantumRegister(num_aux, name='auxiliares')
    circuito.add_register(aux)
    qubits_aux = [aux[i] for i in range(num_aux)]

    # Passo 1
    circuito.ccx(controles[0], controles[1], qubits_aux[0])

    for i in range(2, num_controles):
        indice_aux = i - 1
        indice_aux_ant = i - 2

        if indice_aux < num_aux:
            circuito.ccx(qubits_aux[indice_aux_ant], qubits_controle[i], qubits_aux[indice_aux])
    
    #Passo 2
    ultimo_aux = qubits_aux[-1]
    ultimo_controle = qubits_controle[-1]
    circuito.ccx(ultimo_aux, ultimo_controle, qubit_alvo)

    #Passo 3
    for i in range(num_controles-1, 1, -1):
        indice_aux = i - 1
        indice_aux_ant = i - 2

        if (indice_aux-1) >= 0 and indice_aux < num_aux:
            circuito.ccx(qubits_aux[indice_aux_ant], qubits_controle[i], qubits_aux[indice_aux])
    
    circuito.ccx(controles[0], controles[1], qubits_aux[0])


if __name__ == '__main__':

    circuito = QuantumCircuit(6)
    controles = [0,1,2,3,4]
    alvo = 5

    for i in controles:
        circuito.h(i)
    
    quantum_mcx(circuito, controles, alvo)

    print(circuito)
    print(get_state(circuito))
