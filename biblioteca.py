import heapq #uso para o metodo dijkstra
import math #uso para numeros infinitos
tempo = 0 #usei o tempo de forma global para tentar diminuir o espaco de recursividade usado pelo computador em dfs
class Digrafo:
    def __init__(self, caminho): #dou o caminho de onde estara o grafo
        self.tipo = "digrafo"
        self.listaAdj = ListaAdj(self.tipo)
        self.qnt_arestas = 0
        with open(caminho, 'r') as arquivo:  # adicionando os vertices e arestas a lista
            for linha in arquivo:
                splitted_linha = linha.split(" ")
                if splitted_linha[0] == "a":
                    self.qnt_arestas += 1
                    if splitted_linha[1] not in self.listaAdj.lista:
                        self.listaAdj.addVertice(splitted_linha[1])
                    if splitted_linha[2] not in self.listaAdj.lista:
                        self.listaAdj.addVertice(splitted_linha[2])
                    self.listaAdj.addAresta(splitted_linha[1], splitted_linha[2], splitted_linha[3])

    def Gn(self):# retorna o numero de vertices do digrafo
        qnt_vertices = 0
        for i in self.listaAdj.lista:
            qnt_vertices+=1
        return qnt_vertices

    def Gm(self):# retorna o numero de arestas do digrafo
        return self.qnt_arestas

    def Gvizpos(self, vertice): #o parametro e passado como string, retorna a vizinhanca positiva
        vizinhos = []
        for vizinho in self.listaAdj.lista[vertice]:
            vizinhos.append(vizinho[0])
        return vizinhos

    def Gvizneg(self,vertice):#a logica esta em verificar a pos[0] da listaAdj (vertice de destino) e pegar a chave do dicionario(vertice de origem)
        vizinhos = []
        for i in self.listaAdj.lista.keys():
            for j in self.listaAdj.lista[i]:
                if (j[0] == vertice):
                    vizinhos.append(i)
        return vizinhos

    def Gdpos(self, vertice): #retorna o grau de um vertice para sua vizinhanca positiva
        if vertice in self.listaAdj.lista:
            return len(self.listaAdj.lista[vertice])

    def Gdneg(self, vertice): #retorna o grau de um vertice para sua vizinhanca negativa
        vizinhosNegativos = self.Gvizneg(vertice)
        return len(vizinhosNegativos)

    def Gw(self, u, v): #retorna o peso da aresta que vai de u a v
        arestas = self.listaAdj.lista[u]
        for i in arestas:
            if v == i[0]:
                return i[1].split("\n")[0]

    def Gmind(self):  # retorna o vertice com menor grau e seu grau
        menorGrau = ["", math.inf] #aqui teremos o vertice e o maior grau do digrafo, inicialei com um grau infinito para ir trocando depois
        for key in self.listaAdj.lista:
            if len(self.listaAdj.lista[key]) < menorGrau[1]:
                menorGrau[0] = key
                menorGrau[1] = len(self.listaAdj.lista[key])
        return menorGrau #observacao, pode ser que o vertice nao seja o unico a ter o menor grau, pego o primeiro vertice com o menor grau

    def Gmaxd(self): #retorna o vertice com maior grau e seu grau (a primeira ocorrencia dele)
        maiorGrau = ["", 0] #aqui teremos o vertice e o maior grau do grafo
        for key in self.listaAdj.lista:
            if len(self.listaAdj.lista[key]) > maiorGrau[1]:
                maiorGrau[0] = key
                maiorGrau[1] = len(self.listaAdj.lista[key])
        return maiorGrau

    def bfs(self, vertice): #deixarei o usuario escolher qual vertice ele quer iniciar
        vertices = {} #aqui inicializo um dicionario em que o vertice seria a chave, o valor seria uma lista com cor, distancia e predecessor, respectivamente
        d = {} #aqui inicializo um dicionario em que a key sera o vertice em que o laco passou e o valor sera a distancia em relacao ao vertice passado como parametro
        pi = {} #aqui inicializo um dicionario em que a key sera o vertice em que o laco passou e o valor sera o seu predecessor
        Q = [] #lista com os vertices a serem visitados
        for key in self.listaAdj.lista: #inicializo cada vertice com a cor branca, distancia infinita e sem predecessor
            vertices[key] = ["branco", math.inf, None]
        Q.append(vertice)
        vertices[vertice] = ["cinza", 0, None] #altero o vertice inicial (origem) para cor cinza, distancia 0 e sem predecessor
        while len(Q) > 0: 
            Q.remove(vertice)
            for i in self.listaAdj.lista[vertice]:
                if vertices[i[0]][0] == "branco":
                    vertices[i[0]] = ["cinza", vertices[vertice][1]+1, vertice]
                    Q.append(i[0])
            vertices[vertice][0] = "preto"
            if len(Q) > 0:
                vertice = Q[0]
        for i in vertices: #retorno os valores de distancia e predecessor de cada vértice através dos dicionários "d" e "pi"
            d[i] = vertices[i][1]
            pi[i] = vertices[i][2]
        return d,pi

    def inicia_dfs(self, vInicial): #deixarei o usuario escolher qual o vertice ele quer iniciar
        vertices = {}  # aqui inicializo um dicionario em que o vertice seria a chave, o valor seria uma lista com cor, tempo (tempo estaram e uma lista, a posicao 0 seria o tempo de inicio e a pos 1 tempo final e predecessor, respectivamente
        pi = {} #aqui inicializo um dicionario em que a key sera o vertice em que o laco passou e o valor sera o seu predecessor
        temp_ini = {} #aqui inicialico um dicionario em que a key sera o vertice e o valor o tempo inicial em que o algortimo acessou o vertice
        temp_final = {} #aqui inicialico um dicionario em que a key sera o vertice e o valor o tempo final em que o algortimo acessou o vertice
        for key in self.listaAdj.lista: #inicializo os vertices com a cor branca, uma lista vazia que conterá os tempos, e sem pais/predecessores
            vertices[key] = ["branco", [], None]
        if vertices[vInicial][0] == "branco":
            self.busca_dfs(vInicial,vertices)
        for v in vertices:
            if vertices[v][0] == "branco":
                self.busca_dfs(v, vertices)
        for v in vertices: #insiro as informações de predecessores, tempo inicial e final de cada vertices nos dicionários "pi", "temp_ini" e "temp_final"
            pi[v] = vertices[v][2]
            temp_ini[v] = vertices[v][1][0]
            temp_final[v] = vertices[v][1][1]
        return pi, temp_ini, temp_final

    def busca_dfs(self, v, vertices): #adiciono o tempo ao vertice de origem e altero sua cor para cinza na linha seguinte, e percorro sua vizinhança positiva 
        global tempo
        tempo = tempo + 1
        vertices[v][1].append(tempo) 
        vertices[v][0] = "cinza"
        for vizinho in self.listaAdj.lista[v]:
            if vertices[vizinho[0]][0] == "branco": #se o vertice da vizinhança positiva tiver a cor branca, ele n foi visitado ainda e seu predecessor é alterado para o vertice v
                vertices[vizinho[0]][2] = v
                self.busca_dfs(vizinho[0], vertices)#aqui se faz uso de recursão para a busca continuar para os outros vertices 
        tempo += 1
        vertices[v][1].append(tempo) #quando todos seus vizinhos nao forem mais brancos, o tempo para o vertice é incrementado e sua cor é alterada para preto
        vertices[v][0] = "preto"
        #print(v,vertices[v])
    def relaxa(self, origem, destino, vertices): #funcao para atualizar distancia entre dois vertices, levando em consideraçao o peso das arestas
        for valor in self.listaAdj.lista[origem]:
            if valor[0] == destino:
                peso = int(valor[1])
        if float(vertices[destino][0]) > float(vertices[origem][0]) + int(peso):# se a distancia do vertice de origem for maior que a distancia do vertice de destino mais seu peso:
            vertices[destino][0] = int(vertices[origem][0]) + peso #altera-se a distancia do vertice para o valor da distancia do vertice de origem mais seu peso
            vertices[destino][1] = origem # altera seu predecessor para o vertice de origem
        return vertices #por fim, retorna o dicionário com os vertices, suas distancias, e seus predecessores após o relaxamento
    def inicializa(self, v): #funçao usada para inicializar os vertices (exceto o de origem) com a distancia infina e sem predecessor
        vertices = {}
        vertices[v] = [0, None]
        for key in self.listaAdj.lista:
            if key != v:
                vertices[key] = [math.inf, None] #pos 0 = distancia, pos 1 = pai
        return vertices
    def bf(self, v): #essa funcao representa o algoritmo de Bellman-Ford de busca de caminho mínimo
        d = {}
        pi = {}
        vertices = self.inicializa(v) #inicializa os vertices com distancia infinita e sem predecessor (e origem com distancia 0 e sem predecssor)
        total_vertices = self.Gn()
        for i in range(1, total_vertices-1):
            for arco in self.listaAdj.lista:
                for aresta in self.listaAdj.lista[arco]:
                    destino = aresta[0]
                    vertices = self.relaxa(arco, destino, vertices)
        for arco in self.listaAdj.lista:
            for aresta in self.listaAdj.lista[arco]:
                u = arco
                v = aresta[0]
                if int(vertices[v][0]) > int(vertices[u][0]) + int(aresta[1]): #se o grafo tiver ciclos negativos, ele retorna a mensagem
                    print("grafo com ciclo negativo")
                    return
        for i in vertices: #por fim, retorna dois dicionários, um contendo a distancia dos vertices da orgem, e outro seus predecessores
            d[i] = vertices[i][0]
            pi[i] = vertices[i][1]
        return d, pi
    def cria_heap(self,v): #funcao criada para organizar os vertices por fila de proridade baseado na distancia
        Q = []
        Q.append((0, v))
        for i in self.listaAdj.lista.keys():
            if i == v:
                continue
            else:
                Q.append((math.inf, i))
        return Q
    def mantem_heap(self, Q, tupla): #funcao chamada caso a distancia do vertice tenha sido modificada
        Q.append(tupla)
        heapq.heapify(Q)
        return Q
    def djikstra(self, v): #função que representa o algoritmo de Djikstra de caminhos minimos 
        S=set()
        vertices = self.inicializa(v) #inicializa os vertices com suas distancias infinitas e sem predecessores 
        Q = self.cria_heap(v) #vertices em fila de prioridades
        d = {}
        pi = {}
        while len(Q)>0:
            u = Q.pop(0)
            if u[1] in S:
                continue
            S.add(u[1])
            for v in self.listaAdj.lista[u[1]]: #chama a funcao para fazer o relaxa dos vertices e atualizar suas distancias e predecessores
                vertices = self.relaxa(u[1],v[0],vertices)
                tupla = (vertices[v[0]][0],v[0])
                Q = self.mantem_heap(Q, tupla)
        for i in vertices: #por fim, a funcao retorna os atributos distancia e predecssor por meio dos dois dicionários d e pi
            d[i] = vertices[i][0]
            pi[i] = vertices[i][1]
        return d, pi
    def detectaCiclos(self, vInicial, tamDesejado): #funcao para detectar ciclo  no digrafo
        pi, tempi, tempf = self.inicia_dfs(vInicial)
        for u in self.listaAdj.lista:
            for aresta in self.listaAdj.lista[u]:
                v = aresta[0] #aresta[0] armazena o vertice de destino, no caso o v
                if int(tempi[v]) < int(tempi[u]) and int(tempf[v]) > int(tempf[u]):
                    #para evitar caminhos muitos grandes, restringi os caminhos a 15
                    if (int(tempi[u]) - int(tempi[v])) < tamDesejado and (int(tempi[u]) - int(tempi[v])) < 15:
                        filho = u  # descendente de v, u deve ser guardado
                        caminho = [filho]  # o ciclo é inicializado com u, vou guardando o caminho em uma lista
                        pai = pi[filho]  # pai = u.pi
                        while pai != v:
                            caminho.append(pi[filho])  # adiciona os novos vértices ancestrais de u no ciclo para v
                            pai = pi[pai]  # pai = pai.pi
                            filho = pi[filho]  # filho = filho.pi
                        caminho.append(pai)  # adiciona v ao final do ciclo
                        if len(caminho) >= tamDesejado: #retorno o primeiro ciclo achado com o tamanho desejado, no caso do item e, seria 5, entao passo 5 como parametro
                            return caminho

    def achaCaminho(self, vOrigem, vDestino): #função para encontrar caminhos no digrafo
        d, pi = self.bfs(vOrigem)
        caminho = []
        atual = vDestino
        while atual != vOrigem: #vou acessando os pais dos pais, comeco no destino e termino quando eu encontrar a origem, o grafo precisa ser conexo para sempre dar certo
            caminho.append(atual)
            atual = pi[atual]
        caminho.append(vOrigem)
        caminho.reverse()# inverto a ordem, pois comecei no vertice de destino
        return caminho

class ListaAdj: #resolvemos criar uma classe de lista adj para evitar repeticao de codigo, tambem escolhemos a lista por menor complexidade
    def __init__(self, tipo):
        self.lista = {} #dicionario, a chave seria o vertice, o valor seria uma lista [[vertice de chegada, peso da aresta], ...]
        self.tipo = tipo #diz o tipo do grafo, digito "grafo" para grafo e "digrafo" para digrafo.

    def addVertice(self, vertice): #adicionando um vertice a lista adjacente.
        self.lista[vertice] = []

    def addAresta(self, origem, destino, peso): #adicionando uma aresta
        aresta = [destino, peso]
        arestaVolta=[origem, peso]
        self.lista[origem].append(aresta)
        if self.tipo == "grafo": #se nao for digrafo, tambem deve-se adicionar o vizinho no vertice de destino
            self.lista[destino].append(arestaVolta)

class Grafo: #classe criada para grafos nao roeintados
    def __init__(self, caminho): #dou o caminho de onde estara o grafo
        self.tipo = "grafo"
        self.listaAdj = ListaAdj(self.tipo)
        self.qnt_arestas = 0
        with open(caminho, 'r') as arquivo: #adicionando os vertices e arestas a lista, e contabiliza a qnt de arestas
            for linha in arquivo:
                splitted_linha = linha.split(" ")
                if splitted_linha[0] == "a": #as arestas começam quando se encontra o caractere "a"
                    self.qnt_arestas += 1
                    if splitted_linha[1] not in self.listaAdj.lista:
                        self.listaAdj.addVertice(splitted_linha[1])
                    if splitted_linha[2] not in self.listaAdj.lista:
                        self.listaAdj.addVertice(splitted_linha[2])
                    self.listaAdj.addAresta(splitted_linha[1], splitted_linha[2], splitted_linha[3])

    def Gn(self):# retorna o numero de vertices do grafo
        qnt_vertices = 0
        for i in self.listaAdj.lista:
            qnt_vertices+=1
        return qnt_vertices
    def Gm(self):# retorna o numero de arestas do grafo
        return self.qnt_arestas

    def Gviz(self, vertice): #o parametro e passado como string, retorna a vizinhanca do vertice
        vizinhos = []
        for vizinho in self.listaAdj.lista[vertice]:
            vizinhos.append(vizinho[0])
        return vizinhos

    def Gd(self, vertice): #retorna o grau de um vertice
        if vertice in self.listaAdj.lista:
            return len(self.listaAdj.lista[vertice])

    def Gw(self, u, v): #retorna o peso da aresta que vai de u a v
        arestas = self.listaAdj.lista[u]
        for i in arestas:
            if v == i[0]:
                return i[1].split("\n")[0]

    def Gmind(self):  # retorna o vertice com menor grau e seu grau
        menorGrau = ["", math.inf]  # aqui teremos o vertice e o maior grau do grafo, inicialei com um grau infinito para ir trocando depois
        for key in self.listaAdj.lista:
            if len(self.listaAdj.lista[key]) < menorGrau[1]:
                menorGrau[0] = key
                menorGrau[1] = len(self.listaAdj.lista[key])
        return menorGrau #observacao, pode ser que o vertice nao seja o unico a ter o menor grau, pego o primeiro vertice com o menor grau

    def Gmaxd(self): #retorna o vertice com maior grau e seu grau (a primeira ocorrencia dele)
        maiorGrau = ["", 0] #aqui teremos o vertice e o maior grau do grafo
        for key in self.listaAdj.lista:
            if len(self.listaAdj.lista[key]) > maiorGrau[1]:
                maiorGrau[0] = key
                maiorGrau[1] = len(self.listaAdj.lista[key])
        return maiorGrau
    def bfs(self, vertice): #deixarei o usuario escolher qual vertice ele quer iniciar
        vertices = {} #aqui inicializo um dicionario em que o vertice seria a chave, o valor seria uma lista com cor, distancia e predecessor, respectivamente
        d = {} #aqui inicializo um dicionario em que a key sera o vertice em que o laco passou e o valor sera a distancia em relacao ao vertice passado como parametro
        pi = {} #aqui inicializo um dicionario em que a key sera o vertice em que o laco passou e o valor sera o seu predecessor
        Q = [] #lista com os vertices a serem visitados
        for key in self.listaAdj.lista:
            vertices[key] = ["branco", math.inf, None]
        Q.append(vertice)
        vertices[vertice] = ["cinza", 0, None] #inicializa o vertice de origem com cor cinza, distancia 0 e sem predecessor
        while len(Q) > 0:
            Q.remove(vertice)
            for i in self.listaAdj.lista[vertice]: #verifica se seus vizinhos sao brancos (ainda n visitados)
                if vertices[i[0]][0] == "branco":
                    vertices[i[0]] = ["cinza", vertices[vertice][1]+1, vertice] #altera sua cor, distancia e predecessor 
                    Q.append(i[0])
            vertices[vertice][0] = "preto"
            if len(Q) > 0:
                vertice = Q[0]
        for i in vertices: #por fim, retorna dois dicionários com as distancias e predecessores dos vertices
            d[i] = vertices[i][1]
            pi[i] = vertices[i][2]
        return d,pi
    def inicia_dfs(self): #deixarei o usuario escolher qual o vertice ele quer iniciar
        vertices = {}  # aqui inicializo um dicionario em que o vertice seria a chave, o valor seria uma lista com cor, tempo (tempo estaram e uma lista, a posicao 0 seria o tempo de inicio e a pos 1 tempo final e predecessor, respectivamente
        pi = {} #aqui inicializo um dicionario em que a key sera o vertice em que o laco passou e o valor sera o seu predecessor
        temp_ini = {} #aqui inicialico um dicionario em que a key sera o vertice e o valor o tempo inicial em que o algortimo acessou o vertice
        temp_final = {} #aqui inicialico um dicionario em que a key sera o vertice e o valor o tempo final em que o algortimo acessou o vertice
        for key in self.listaAdj.lista:
            vertices[key] = ["branco", [], None] #inicializa os vertices com a cor branca, uma lista vazia que conterá os tempos e sem predecessor
        for v in vertices:
            if vertices[v][0] == "branco": # se o vertice ainda não foi visitado, ele chama a funcao busca_dfs
                self.busca_dfs(v, vertices)
        for v in vertices:# por fim, retorna três dicionários, um contendo o seu predecessor, outro o tempo inicial e outro com o tempo final
            pi[v] = vertices[v][2]
            temp_ini[v] = vertices[v][1][0]
            temp_final[v] = vertices[v][1][1]
        return pi, temp_ini, temp_final
    def busca_dfs(self, v, vertices): 
        global tempo
        tempo = tempo + 1 #incrementa o tempo mais 1 e atribui seu valor ao vertice atual v
        vertices[v][1].append(tempo)
        vertices[v][0] = "cinza" #e altera sua cor para cinza
        for vizinho in self.listaAdj.lista[v]: #percorre seus vizinhos na lista de adjacencia, e caso eles tenham a cor branca, atribui seu predecessor como o vertice atual
            if vertices[vizinho[0]][0] == "branco":
                vertices[vizinho[0]][2] = v
                self.busca_dfs(vizinho[0], vertices) #uso de recursao para chamar aprofundar a busca nos vertices 
        tempo += 1
        vertices[v][1].append(tempo)
        vertices[v][0] = "preto" #quando todos os vizinhos do vertices forem visitados, sua cor é alterada para preto
    def relaxa(self, origem, destino, vertices): #funcao relaxa usada para atualizar a distancia entre vertices através dos pesos
        for valor in self.listaAdj.lista[origem]:
            if valor[0] == destino:
                peso = int(valor[1])
        if float(vertices[destino][0]) > float(vertices[origem][0]) + int(peso): # verrifica se a distancia do vertice de destino é maior que a do vertice de origem mais seu peso 
            vertices[destino][0] = int(vertices[origem][0]) + peso # se sim, atualiza sua distancia e seu predecssor
            vertices[destino][1] = origem
        return vertices
    def inicializa(self, v): #funcao usada para inicializar os vertices (exceto a origem) com distancia infinita e sem predecessor
        vertices = {}
        vertices[v] = [0, None] #o vertice origem tem disatancia 0 e sem predecessor
        for key in self.listaAdj.lista:
            if key != v:
                vertices[key] = [math.inf, None] #pos 0 = distancia, pos 1 = pai
        return vertices
    def bf(self, v): # funcao que representa o algoritmo de Bellman-Ford
        d = {}
        pi = {}
        vertices = self.inicializa(v) #chama a funcao inicializa para iniciar o vertices 
        total_vertices = self.Gn()
        for i in range(1, total_vertices-1):
            for arco in self.listaAdj.lista:
                for aresta in self.listaAdj.lista[arco]:#aqui a funcao relaxa é chamada duas vezes, ja que o grafo é nao orientado
                    destino = aresta[0]
                    vertices = self.relaxa(arco, destino, vertices)
                    vertices = self.relaxa(destino, arco, vertices)
        for arco in self.listaAdj.lista:
            for aresta in self.listaAdj.lista[arco]:
                u = arco
                v = aresta[0]
                if int(vertices[v][0]) > int(vertices[u][0]) + int(aresta[1]): #verifica se ha ciclos no grafo
                    print("grafo com ciclo negativo")
                    return
        for i in vertices: #por fim, retorna o dicionário com as distancias e predecessores de cada vértice 
            d[i] = vertices[i][0]
            pi[i] = vertices[i][1]
        return d, pi
    def cria_heap(self,v): #função criada para organizar os vértices numa fila de prioridade com base em suas distancias
        Q = []
        Q.append((0, v))
        for i in self.listaAdj.lista.keys():
            if i == v:
                continue
            else:
                Q.append((math.inf, i))
        return Q
    def mantem_heap(self, Q, tupla): #funcao chamada caso a distancia do vertice tenha sido atualizada 
        Q.append(tupla)
        heapq.heapify(Q)
        return Q
    def djikstra(self, v): #funcao que representa o algoritmo de Djikstra
        S=set() 
        vertices = self.inicializa(v)
        Q = self.cria_heap(v) #chamada da funcao para criar uma fila de proridade
        d = {}
        pi = {}
        while len(Q)>0: #enquanto tiver elementos na fila 
            u = Q.pop(0)
            if u[1] in S:
                continue
            S.add(u[1])
            for v in self.listaAdj.lista[u[1]]: #novamente a  funcao relaxa é chamada duas vezes para o par de vertices no caso do grafo nao orientado
                vertices = self.relaxa(u[1],v[0],vertices)
                vertices = self.relaxa(v[0], u[1], vertices)
                tupla = (vertices[v[0]][0],v[0]) #atualiza a informcao do vertice
                Q = self.mantem_heap(Q, tupla) #atualiza a lista de proridade Q
        for i in vertices:#funcao retorna dois dicionarios d e pi contendo as distancias e predecessores dos vertices, respectivamente
            d[i] = vertices[i][0]
            pi[i] = vertices[i][1]
        return d, pi
    def detectaCiclos(self, vInicial, tamDesejado): #funcao criada para detectar ciclos no grafo 
        pi, tempi, tempf = self.inicia_dfs(vInicial)
        for u in self.listaAdj.lista:
            for aresta in self.listaAdj.lista[u]:
                v = aresta[0] #aresta[0] armazena o vertice de destino, no caso o v
                if float(tempi[v]) < float(tempi[u]) and float(tempf[v]) > float(tempf[u]):
                    #para evitar caminhos muitos grandes, restringi os caminhos a 15
                    if (float(tempi[u]) - float(tempi[v])) < tamDesejado and (float(tempi[u]) - float(tempi[v])) < 15:
                        filho = u  # descendente de v, u deve ser guardado
                        caminho = [filho]  # o ciclo é inicializado com u, vou guardando o caminho em uma lista
                        pai = pi[filho]  # pai = u.pi
                        while pai != v:
                            caminho.append(pi[filho])  # adiciona os novos vértices ancestrais de u no ciclo para v
                            pai = pi[pai]  # pai = pai.pi
                            filho = pi[filho]  # filho = filho.pi
                        caminho.append(pai)  # adiciona v ao final do ciclo
                        if len(caminho) >= tamDesejado: #retorno o ciclo com o tamanho desejado, no caso do item e, seria 5, entao passo 5 como parametro
                            return caminho

    def achaCaminho(self, vOrigem, vDestino): #função criada para encontrar caminhos no grafo
        d, pi = self.bfs(vOrigem)
        caminho = []
        atual = vDestino
        while atual != vOrigem: #vou acessando os pais dos pais, comeco no destino e termino quando eu encontrar a origem, o grafo precisa ser conexo para sempre dar certo
            caminho.append(atual)
            atual = pi[atual]
        caminho.append(vOrigem)
        caminho.reverse()# inverto a ordem, pois comecei no vertice de destino
        return caminho
