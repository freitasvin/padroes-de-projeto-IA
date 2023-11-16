import numpy as np 
from collections import deque

# Defina a interface de estratégia
class BuscaEstrategia:
    def executar(self, ori_i, ori_j, dest_i, dest_j, mapa, linhas, colunas):
        pass

# Estratégia de busca em profundidade
class ProfundidadeBusca(BuscaEstrategia):
    def executar(self, ori_i, ori_j, dest_i, dest_j, mapa, linhas, colunas):
        # Lógica existente para a busca em profundidade
        profundidadeVars(ori_i, ori_j, dest_i, dest_j, mapa, linhas, colunas)

# Estratégia de busca gulosa
class BuscaGulosa(BuscaEstrategia):
    def executar(self, ori_i, ori_j, dest_i, dest_j, mapa, linhas, colunas):
        # Lógica existente para a busca gulosa
        buscaGulosaVars(ori_i, ori_j, dest_i, dest_j, mapa, linhas, colunas)

# Classe de contexto que utiliza a estratégia
class ContextoBusca:
    def __init__(self, estrategia):
        self.estrategia = estrategia

    def executar_busca(self, ori_i, ori_j, dest_i, dest_j, mapa, linhas, colunas):
        self.estrategia.executar(ori_i, ori_j, dest_i, dest_j, mapa, linhas, colunas)

linhas = 10
colunas = 7
opt_mhtn = 0 
opt_dtlr = 1 
sw_adjs = 0 
sw_pesos = 1 

def resetMap():
    mapa = [
        [1,  1 ,  1,  1,  1,  20,  -1],      
        [1,  0 ,  0,  0,  0,  1,    0],       
        [1,  4,  10,  10, 0,  1,    1],        
        [0, -1,  10, -1,  0,  0,    1],         
        [-1,  0,   4,  0,  0,  1,    1],          
        [4,  0,  -1,  0,  0,  1,    0],          
        [1,  1,   1,  1,  4,  1,    1],         
        [0,  1,   0,  10, 0,  0,    1],       
        [0,  1,   1,  1, -2,  0,   10],       
        [-1,  4,   0,  0,  4,  4,   -1]
    ]   
    return mapa

def calcAdjaPesos(mapa, linhas, colunas):
    adjacencias = []
    mat_pesos = []

    for l in range(linhas):
        for c in range(colunas):
            elementos = []
            pesos = []
            elemento = l*colunas+c
         
            if mapa[l][c] == 0:
                adjacencias.append(elementos)
                mat_pesos.append(pesos)
            else:
                if l-1 >= 0:
                    if mapa[l-1][c] != 0:
                        pesos.append(mapa[l-1][c])
                        elementos.append([(l-1)*colunas+c, [l-1, c]])
                if c-1 >= 0:
                    if mapa[l][c-1] != 0:
                        pesos.append(mapa[l][c-1])
                        elementos.append([l*colunas+c-1, [l, c-1]])

                if c+1 < colunas:
                    if mapa[l][c+1] != 0:
                        pesos.append(mapa[l][c+1])
                        elementos.append([l*colunas+c+1, [l, c+1]])

                if l+1 < linhas:
                    if mapa[l+1][c] != 0:
                        pesos.append(mapa[l+1][c])
                        elementos.append([(l+1)*colunas+c, [l+1, c]])

                adjacencias.append(elementos)
                mat_pesos.append(pesos)

    return [adjacencias, mat_pesos]

def calcHeuristicas(dest_i, dest_j):
    heuristicas = []
    dest_i = 8
    dest_j = 4

    for i in range(linhas):
        for j in range(colunas):
            aux_i = i
            aux_j = j
            mhtn = 0 
            cat_i = 0 
            cat_j = 0 
            elemento = i*colunas+j
                        
            while aux_i != dest_i: 
                if aux_i < dest_i: 
                    aux_i += 1 

                if aux_i > dest_i: 
                    aux_i -=1 
                
                cat_i += 1 
                mhtn += 1 

            while aux_j != dest_j: 
                if aux_j < dest_j:
                    aux_j += 1

                if aux_j > dest_j:
                    aux_j -= 1
                
                cat_j += 1
                mhtn += 1
            
            linha_reta = (((cat_i ** 2) + (cat_j ** 2)) ** 0.5)
            h = [mhtn, linha_reta]
            heuristicas.append(h)
    
    return heuristicas

def buscaGulosaVars(ori_i, ori_j, dest_i, dest_j, mapa, linhas, colunas):
    visitados = []
    caminho = []
    origem = ori_i*colunas+ori_j
    destino = dest_i*colunas+dest_j

    adjsPesos = calcAdjaPesos(mapa, linhas, colunas)
    adjs = adjsPesos[sw_adjs]
   
    hrstc = calcHeuristicas(dest_i, dest_j)
    h_opt = opt_dtlr 

    caminho = buscaGulosa([origem, [ori_i, ori_j]], [destino, [dest_i, dest_j]], visitados, adjs, hrstc, h_opt, caminho)

    print("::Caminho = ", caminho)
    print("::Saltos = ", len(caminho[0]))

    for elemento, coord in caminho[0]:
        mapa[coord[0]][coord[1]] = 9

    print(":::Mapa:::")
    for i in range(linhas):
        for j in range(colunas):
            print(mapa[i][j], end='\t')
        print()
    
def buscaGulosa(origem, destino, visitados, adjs, hrstc, h_opt, caminho):
    flag = False
    find = False
    menor = 99999999
    if len(visitados) == 0:
        visitados.append(origem)
    
    if origem == destino:
        c = tuple(visitados)
        caminho.append(c)
        find = True

    while not find and len(visitados) > 0:
        for i in adjs[origem[0]]:
            if menor > hrstc[i[0]][h_opt] and i not in visitados and not flag:
                menor = hrstc[i[0]][h_opt]
                prox = i
                
        if menor != 99999999 and flag == False:
            flag = True
            visitados.append(prox)
            return  buscaGulosa(prox, destino, visitados, adjs, hrstc, h_opt, caminho)
        else:
            if flag:
                visitados.pop()
            break

    return caminho

def profundidadeVars(ori_i, ori_j, dest_i, dest_j, mapa, linhas, colunas):
    visitados = []
    caminhos = []
    origem = ori_i*colunas+ori_j
    destino = dest_i*colunas+dest_j
    
    adjpesos = calcAdjaPesos(mapa, linhas, colunas)
    adjs = adjpesos[sw_adjs]

    profundidade([origem, [ori_i, ori_j]], [destino, [dest_i, dest_j]], visitados, caminhos, adjs)

    print(len(caminhos), 'caminhos encontrados')
    menor = range(100000)

    for c in caminhos:
        if len(menor) > len(c):
            menor = c
    
    print("Menor =", menor)
    print("Saltos =", len(menor))

    for elemento, coord in menor: 
        mapa[coord[0]][coord[1]] = 9

    print(":::Mapa:::")
    for i in range(linhas):
        for j in range(colunas):
            print(mapa[i][j], end='\t')
        print()
    
def profundidade(origem, destino, visitados, caminhos, adjs):
    flag = False
    if len(visitados) == 0:
        visitados.append(origem)
    if origem == destino:
        c = tuple(visitados)
        caminhos.append(c)
        flag = True
    else:
            adjcs = adjs[origem[0]]
            for adj in adjcs:
                if adj not in visitados:
                    visitados.append(adj)
                    profundidade(adj, destino, visitados, caminhos, adjs)

            if len(visitados) > 0:
                visitados.pop()
    if flag == True:
        if len(visitados) > 0:
            visitados.pop()    


mapa = resetMap()

# Uso do padrão de projeto Strategy
if __name__ == "__main__":
    linhas = 10
    colunas = 7

    # Define a estratégia desejada
    estrategia_profundidade = ProfundidadeBusca()
    estrategia_gulosa = BuscaGulosa()

    # Crie um contexto com a estratégia desejada
    contexto = ContextoBusca(estrategia_profundidade)

    # Execute a busca usando a estratégia selecionada
    contexto.executar_busca(0, 0, 8, 4, mapa, linhas, colunas)

    # Altere a estratégia se necessário
    contexto.estrategia = estrategia_gulosa
    contexto.executar_busca(0, 0, 8, 4, mapa, linhas, colunas)
