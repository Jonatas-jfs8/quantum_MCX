from qiskit import QuantumCircuit, QuantumRegister
from qclib.util import get_state
import math

def quantum_mcx(circuito, controles, alvo):

    num_controles = len(controles)
    eh_par = num_controles % 2 == 0
    qubit_alvo = circuito.qubits[alvo]

    aux = QuantumRegister(1, name='auxiliares')
    circuito.add_register(aux)

    # Passo 1
    circuito.ccx(controles[0], controles[1], aux[0])

    for i in range(1, num_controles - 2, 2):
        circuito.ccx(controles[i+1], controles[i+2], controles[i])

    circuito.barrier()

    # Passo 2
    start = 0
    end = num_controles - 3
    if eh_par:
        end += 1
    for i in range(start, end):
        circuito.x(controles[i])

    circuito.barrier()

    # Passo 3
    if eh_par:
        circuito.cx(controles[num_controles - 3], controles[num_controles - 4])
        for i in range(num_controles - 4, 1, -2):
            circuito.ccx(controles[i], controles[i - 1], controles[i - 2])
    else:
        circuito.ccx(controles[num_controles - 1], controles[num_controles - 4], controles[num_controles - 5])
        for i in range(num_controles - 5, 1, -2):
            circuito.ccx(controles[i], controles[i - 1], controles[i - 2])

    circuito.barrier()

    # Passo 4
    circuito.ccx(controles[0], aux[0], qubit_alvo)

    circuito.barrier()

    # Passo 5
    if eh_par:
        for i in range(0, num_controles - 4, 2):
            circuito.ccx(controles[i+1], controles[i+2], controles[i])
        circuito.cx(controles[num_controles - 3], controles[num_controles - 4])
    else:
        for i in range(0, num_controles - 5, 2):
            circuito.ccx(controles[i+1], controles[i+2], controles[i])
        circuito.ccx(controles[num_controles - 1], controles[num_controles - 4], controles[num_controles - 5])

    circuito.barrier()

    # Passo 6
    start = 0
    end = num_controles - 3
    if eh_par:
        end += 1
    for i in range(start, end):
        circuito.x(controles[i])

    circuito.barrier()

    # Passo 7
    start = num_controles - 2
    end = 1
    if eh_par:
        start += 1
        end += 1
    for i in range(start, end, -2):
        circuito.ccx(controles[i], controles[i-1], controles[i-2])
    circuito.ccx(controles[0], controles[1], aux[0])
    
def quantum_mcx_log(circuito, controles, alvo):
    num_controles = len(controles)
    
    aux = QuantumRegister(1, name='auxiliares_log')
    circuito.add_register(aux)
    
    last_step = False
    i = 1
    operacoes = []
    
    # Passo 1
    circuito.ccx(controles[0], controles[1], aux[0])
    
    circuito.barrier()
    
    # Passo 2
    while i - 1 + pow(2, i) < num_controles:
        p0 = list(range(i, i + pow(2, i)))
        q0 = list(range(i + pow(2, i), min(i + pow(2, i + 1) + 1, num_controles + 1)))
        p1 = list(range(i, i + pow(2, i)))
        q1 = list(range(i + pow(2, i), min(i + pow(2, i + 1) + 1, num_controles + 1)))
        print(p0)
        print(q0)
        for j in range(0, i + 1):
            if j == i:
                if len(q0) == 1:
                    circuito.x(controles[p0[0] - 1])
                    circuito.cx(controles[q0[0] - 1], controles[p0[0] - 1])
                    operacoes.append([controles[q0[0] - 1], -1, controles[p0[0] - 1]])
                else:
                    circuito.x(controles[p0[0] - 1])
                    circuito.ccx(controles[q0[0] - 1], controles[q0[1] - 1], controles[p0[0] - 1])
                    operacoes.append([controles[q0[0] - 1], controles[q0[1] - 1], controles[p0[0] - 1]])
            else:
                for k in range(0, pow(2, i - j - 1)):
                    if 2 * k + 2 < len(q0):
                        circuito.x(controles[p0[pow(2, i - j) - 1 - k] - 1])
                        circuito.ccx(controles[q0[2 * k + 1] - 1], controles[q0[2 * k + 2] - 1], controles[p0[pow(2, i - j) - 1 - k] - 1])
                        operacoes.append([controles[q0[2 * k + 1] - 1], controles[q0[2 * k + 2] - 1], controles[p0[pow(2, i - j) - 1 - k] - 1]])
                        q1.remove(q0[2 * k + 2])
                        q1.remove(q0[2 * k + 1])
                        q1.insert(0, p0[pow(2, i - j) - 1 - k])
                        p1.remove(p0[pow(2, i - j) - 1 - k])
                        print("new k-step: " + str(p1) + " " + str(q1))
            p0 = p1
            q0 = q1
            print("new j-step: " + str(p0) + " " + str(q0))
        i += 1
        #print(operacoes)
        
    circuito.barrier()
        
    # Passo 3
    if i == 2:
        circuito.ccx(aux[0], controles[0], alvo)
    elif i == 3:
        aux_2 = QuantumRegister(1, name='auxiliares')
        circuito.add_register(aux_2)
        
        circuito.ccx(aux[0], controles[0], aux_2[0])
        circuito.x(aux[0])
        circuito.ccx(controles[0], controles[1], aux[0])
        
        circuito.ccx(aux[0], aux_2[0], alvo)
        
        circuito.ccx(controles[0], controles[1], aux[0])
        circuito.x(aux[0])
        circuito.ccx(aux[0], controles[0], aux_2[0])
    else:
        new_controles = []
        for x in range(0, i):
            new_controles.append(controles[i])
        new_controles.append(aux[0])
        quantum_mcx(circuito, new_controles, alvo)
        
    circuito.barrier()
        
    # Passo 4
    y = len(operacoes)
    for x in range(1, y + 1):
        if operacoes[y - x][1] == -1:
            circuito.cx(operacoes[y - x][0], operacoes[y - x][2])
            circuito.x(operacoes[y - x][2])
        else:
            circuito.ccx(operacoes[y - x][0], operacoes[y - x][1], operacoes[y - x][2])
            circuito.x(operacoes[y - x][2])
        
    circuito.barrier()
    
    # Passo 5
    circuito.ccx(controles[0], controles[1], aux[0])
        
            
        

if __name__ == '__main__':

    circuito = QuantumCircuit(8)
    controles = [1,2,3,4,5,6,7]
    alvo = 0

    for i in controles:
        circuito.h(i)
    
    quantum_mcx_log(circuito, controles, alvo)

    print(circuito)
    print(get_state(circuito))