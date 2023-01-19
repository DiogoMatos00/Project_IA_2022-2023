import itertools;


class Sudoku:

    """ Para criar um objeto "Sudoku" é necessário introduzir o grid que será:
                Uma string com todos os números do puzzle dos quais os espaços
            vazios são zeros iterando linha a linha(row a row).  """
    def __init__(self, board:str) -> None:
        self.rows = "123456789";
        self.cols = "ABCDEFGHI";

        #Transformar o nosso board de string em lista
        self.grid = list(board);

        #Gerar todas as coordenadas de um sudoku
        self.coords = list();
        self.coords = self.coord_gen();

        #Gerar todas as possibilidades em cada coordenada
        self.possibilities = self.possibilities_generator(self.grid);

        #Delimitar as restrições do CSP e transformar em restrições binárias
        self.constraints = self.constraints_gen();

        """
        Gerar todas restrições relacionadas entre si, para cada uma delas.
        Exemplo:
        No A1 temos de considerar as restrições de B1-I1 + A2-A9 + B2 B3 C2 C3
        """
        self.related_constraints = self.related_const();


    def coord_gen(self) -> list:
        """ Este função irá gerar todas as coordenadas do jogo:
                * As linhas(rows) irão ser números (1,2,3,4,5,6,7,8,9)
                * As colunas(cols) irão ser letras (A,B,C,D,E,F,G,H,I) 
                * Esta função vai retornar uma lista([A1, A2, ..., I8, I9])"""

        list_coords = []
        
        #A, B, C, ..., H, I;
        for col in self.cols:
            #1,2,3, ..., 8,9
            for row in self.rows:

                #A1, A2, A3, ..., I8, i9
                list_coords.append(col+str(row));
        

        return list_coords;

    def possibilities_generator(self, grid:list) -> dict:

        """Esta função irá gerar todas as possibilidades em cada espaço do jogo
            Exemplo:Se o tabuleiro não tem valor as possibilidades são de 1-9
                    Se o tabuleiro tiver um numero a única possibilidade é o próprio numero"""
        
        possibilities = dict();

        for i, coords in enumerate(self.coords):
            if(self.grid[i] == "0"):
                #possibilities.append(list(range(1,10)));
                possibilities[coords] = list(range(1,10));
            else:
                #possibilities.append([int(grid[i])]);
                possibilities[coords] = [int(self.grid[i])];

        return possibilities;

    def constraints_gen(self) -> list:
        """Delimitar as restrições do CSP com estes arcos de restrição:
                * Colunas (cols)
                * Linhas  (rows)
                * Quadrados (Square) """

        column_const = [];
        row_const = [];
        square_const = [];
        constraints = [];

        #Conseguir o arco das colunas(cols)
        for row in self.rows:
            row_const.append([col + str(row) for col in self.cols]);


        

        #Conseguir o arco das linhas(rows)
        for col in self.cols:
            column_const.append([col + str(row) for row in self.rows]);


        #Conseguir o arco dos quadrados(Squares)
        squareA = [];
        squareB = [];
        squareC = [];
        i = 0;

        for column in column_const:
            i += 1;
            squareA.append(column[0:3]);
            squareB.append(column[3:6]);
            squareC.append(column[6:9]);

            if(i == 3):
                square_const.append(squareA[0] + squareA[1] + squareA[2]);
                square_const.append(squareB[0] + squareB[1] + squareB[2]);
                square_const.append(squareC[0] + squareC[1] + squareC[2]);
                squareA = [];
                squareB = [];
                squareC = [];
                i = 0;

        
        
        constraints = row_const + column_const +  square_const;

        """ Criar as restrições binárias a partir dos arcos do grafos de restrição.
            Nesta parte do código nós queremos pegar em cada arco e transformar em arcos binários

        """
        
        binary_const_list = list();

        for const in constraints:
            binary_list = list();

            #Irá ser utilizado a biblioteca itertools para utilizando a função permutations
            # https://docs.python.org/3/library/itertools.html#itertools.permutations
            
            for i in itertools.permutations(const, 2):
                #Lista de tuplas 
                binary_list.append(i);

            # Agora com a nossa binary_list vamos fazer uma limpeza para termos a certeza que não existem arcos repetidos.

            for i_tuple in binary_list:
                i_list = list(i_tuple);
                if(i_list not in binary_const_list):
                    #binary_const_list.append(i_list);
                    binary_const_list.append(i_list)

        return binary_const_list;
       
    def related_const(self) -> dict:
        related_const = dict();


        #Vai mostrar todas as restrições relacionadas em cada célula do tabuleiro 
        for coord in self.coords:
            related_const[coord] = list();

            for constraint in self.constraints:
                if coord == constraint[0]:
                    related_const[coord].append(constraint[1]);

        return related_const;

    # Vê se o Sudoku foi preenchido
    def isdone(self):
        for possibilities in self.possibilities.values():
            if(len(possibilities) > 1):
                return False;
        return True;



"""
Aqui está o código python para o algoritmo AC3
Ele terá como atributos um CSP (constraint satisfaction problems)
"""
def ac3(csp, queue=None):
    if(queue == None):
        queue = list(csp.constraints)

    while queue:
        (xi, xj) = queue.pop(0);

        if remove_inconsistent_values(csp, xi, xj):
            if(len(csp.possibilities[xi]) == 0):
                return False;

            for xk in csp.related_constraints[xi]:
                if(xk != xi):
                    queue.append((xk, xi));
    
    
    return True;

"""
Dá remove a todos a valores nao consistentes
"""
def remove_inconsistent_values(csp, cell_i, cell_j) -> bool:

    #Bool para ver se algum item foi removido
    removed = False

    for value in csp.possibilities[cell_i]:
        if (not any(is_different(value, poss) for poss in csp.possibilities[cell_j])):
            csp.possibilities[cell_i].remove(value);
            removed = True;
    
    return removed;

def is_different(cell_i, cell_j):
    result = cell_i != cell_j
    return result

def print_Result(result):
    print("""
    Resultado do Sudoku com AC-3:

        A B C   D E F   G H I
      +-------+-------+-------+
    1 | {} {} {} | {} {} {} | {} {} {} |
    2 | {} {} {} | {} {} {} | {} {} {} |
    3 | {} {} {} | {} {} {} | {} {} {} |
      +-------+-------+-------+
    4 | {} {} {} | {} {} {} | {} {} {} |
    5 | {} {} {} | {} {} {} | {} {} {} |
    6 | {} {} {} | {} {} {} | {} {} {} |
      +-------+-------+-------+
    7 | {} {} {} | {} {} {} | {} {} {} |
    8 | {} {} {} | {} {} {} | {} {} {} |
    9 | {} {} {} | {} {} {} | {} {} {} |
    # +-------+-------+-------+
    
    
    
    
    
    
    
    """.format(result['A1'][0], result['A2'][0], result['A3'][0], result['A4'][0], result['A5'][0], result['A6'][0], result['A7'][0], result['A8'][0], result['A9'][0], result['B1'][0], result['B2'][0], result['B3'][0], result['B4'][0], result['B5'][0], result['B6'][0], result['B7'][0], result['B8'][0], result['B9'][0], result['C1'][0], result['C2'][0], result['C3'][0], result['C4'][0], result['C5'][0], result['C6'][0], result['C7'][0], result['C8'][0], result['C9'][0], result['D1'][0], result['D2'][0], result['D3'][0], result['D4'][0], result['D5'][0], result['D6'][0], result['D7'][0], result['D8'][0], result['D9'][0], result['E1'][0], result['E2'][0], result['E3'][0], result['E4'][0], result['E5'][0], result['E6'][0], result['E7'][0], result['E8'][0], result['E9'][0], result['F1'][0], result['F2'][0], result['F3'][0], result['F4'][0], result['F5'][0], result['F6'][0], result['F7'][0], result['F8'][0], result['F9'][0], result['G1'][0], result['G2'][0], result['G3'][0], result['G4'][0], result['G5'][0], result['G6'][0], result['G7'][0], result['G8'][0], result['G9'][0], result['H1'][0], result['H2'][0], result['H3'][0], result['H4'][0], result['H5'][0], result['H6'][0], result['H7'][0], result['H8'][0], result['H9'][0], result['I1'][0], result['I2'][0], result['I3'][0], result['I4'][0], result['I5'][0], result['I6'][0], result['I7'][0], result['I8'][0], result['I9'][0]))

if __name__ == "__main__":
    board = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
    s = Sudoku(board)
    #print(s.possibilities)
    ac3(s)
    print_Result(s.possibilities)