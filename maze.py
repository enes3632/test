# COMP9021 20T3 - Rachid Hamadi - Enes Şahin 2020
# Assignment 2 *** Due Sunday Week 10 @ 10.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION


# IMPORT ANY REQUIRED MOD
from collections import deque
import numpy as np
from copy import deepcopy
import difflib

class MazeError(Exception):
    def __init__(self, message):
        self.message = message

class Maze:
    def __init__(self, filename):
        self.filename=filename 
        global texname   
        texname = self.filename

        f=open(self.filename, 'r')

        global matrix
        matrix = [ x.split() for x in f] # read the files

        matrix = [x for x in matrix if x!=[]] #delete spaces

        for x in range(len(matrix)): # separate digits with no separators
            if len(matrix[x])==1:
                matrix[x] = list(matrix[x][0])
                
        matrix = [[int(y) for y in x] for x in matrix] # convert to integer


        #checks the metrix's size. it must be at least 2x2
        if len(matrix)==1 or len(matrix[0])==1:  
            raise MazeError('Incorrect input.')

        #checks if hte matrix has invalid character or a line with different size 
        for x,y in enumerate(matrix): 
            
            for t in y:
                if t not in [0,1,2,3]:
                    raise MazeError('Incorrect input.')

                elif x==len(matrix)-1 and t in [2,3]:
                    raise MazeError('Input does not represent a maze.')

                elif t==matrix[x][-1] and t in [1,3]:
                    raise MazeError('Input does not represent a maze.')

            if len(y)!=len(matrix[0]):
                raise MazeError('Incorrect input.')
        
        texname2=[x for x in texname]
        texname2[-2]='e'
        texname2[-1]='x'
        texname=''.join(texname2)

    def analyse_messages(self, name, N): #produce analyse print messages
        self.name = name
        self.N = str(N)

        x = 'The maze has '
        if self.name=='gate':
            if N==0:
                y = 'no gate.'
            elif N==1:
                y = 'a single gate.'
            elif N > 1:
                y = self.N + ' gates.'

        elif self.name=='wall':
            if N==0:
                y = 'no wall.'
            elif N==1:
                y = 'walls that are all connected.'
            elif N > 1:
                y = self.N + ' sets of walls that are all connected.'

        elif self.name=='inner':
            if N==0:
                y = 'no inaccessible inner point.'
            elif N==1:
                y = 'a unique inaccessible inner point.'
            elif N > 1:
                y = self.N + ' inaccessible inner points.'

        elif self.name=='accessible':
            if N==0:
                y = 'no accessible area.'
            elif N==1:
                y = 'a unique accessible area.'
            elif N > 1:
                y = self.N + ' accessible areas.'
        
        elif self.name=='culdesac':
            if N==0:
                y = 'no accessible cul-de-sac.'
            elif N==1:
                y = 'accessible cul-de-sacs that are all connected.'
            elif N > 1:
                y = self.N + ' sets of accessible cul-de-sacs that are all connected.'
        
        elif self.name=='path':
            if N==0:
                y = 'no entry-exit path with no intersection not to cul-de-sacs.'
            elif N==1:
                y = 'a unique entry-exit path with no intersection not to cul-de-sacs.'
            elif N > 1:
                y = self.N + ' entry-exit paths with no intersections not to cul-de-sacs.'

        return x + y

    def analyse(self):
        
        #print('matrix',*matrix,sep='\n')

        ################################################################
        #####################--------gates--------######################
        ################################################################
        top_gates=len([x for x in matrix[0][:-1] if x in [0, 2]])
        left_gates=len([matrix[x][0] for x in range(len(matrix)-1) if matrix[x][0] in [0, 1]])
        right_gates=len([matrix[x][-1] for x in range(len(matrix)-1) if matrix[x][-1]==0])
        bottom_gates=len([x for x in matrix[-1][:-1] if x==0])
        total_gates = top_gates + left_gates + right_gates + bottom_gates

        print(Maze.analyse_messages(self,'gate',total_gates))
        
        ################################################################
        #####################--------wales--------######################
        ################################################################
        def check_visited(matrix, x, y, visited): #checks if it was previously visited
            return (x>-1) and (x<len(visited)) and (y>-1) and (y<len(visited[0])) and (not visited[x][y])

        def check(matrix, i, j, visited, node):
            quit = deque()
            quit.append((i,j))

            visited[i][j] = True

            while quit:

                x,y = quit.popleft()
        
                node = matrix[x][y]

                if node==1:

                    col1=[0,0,-1]
                    row1=[1,-1,0]

                    for k in range(3):
                        if check_visited(matrix, x + col1[k], y + row1[k], visited):

                            if col1[k]==-1 and matrix[x + col1[k]][y + row1[k]] in [2,3]:
                                visited[x + col1[k]][y + row1[k]] = True
                                quit.append((x + col1[k], y + row1[k]))

                            if row1[k]==-1 and matrix[x + col1[k]][y + row1[k]] in [1,3]:
                                visited[x + col1[k]][y + row1[k]] = True
                                quit.append((x + col1[k], y + row1[k]))

                            if row1[k]==1:
                                visited[x + col1[k]][y + row1[k]] = True
                                quit.append((x + col1[k], y + row1[k]))

                elif node==2:

                    col2=[1,-1,0]
                    row2=[0,0,-1]

                    for k in range(3):     
                        if check_visited(matrix, x + col2[k], y + row2[k], visited):
                            
                            if col2[k]==-1 and matrix[x + col2[k]][y + row2[k]] in [2,3]:
                                visited[x + col2[k]][y + row2[k]] = True
                                quit.append((x + col2[k], y + row2[k]))

                            if row2[k]==-1 and matrix[x + col2[k]][y + row2[k]] in [1,3]:
                                visited[x + col2[k]][y + row2[k]] = True
                                quit.append((x + col2[k], y + row2[k]))

                            if col2[k]==1:
                                visited[x + col2[k]][y + row2[k]] = True
                                quit.append((x + col2[k], y + row2[k]))

                elif node==3:

                    col3=[1,-1,0,0]
                    row3=[0,0,-1,1]

                    for k in range(4):
                        if check_visited(matrix, x + col3[k], y + row3[k], visited):

                            if col3[k]==-1 and matrix[x + col3[k]][y + row3[k]] in [2,3]:
                                visited[x + col3[k]][y + row3[k]] = True
                                quit.append((x + col3[k], y + row3[k]))

                            if row3[k]==-1 and matrix[x + col3[k]][y + row3[k]] in [1,3]:
                                visited[x + col3[k]][y + row3[k]] = True
                                quit.append((x + col3[k], y + row3[k]))

                            if col3[k]==1:
                                visited[x + col3[k]][y + row3[k]] = True
                                quit.append((x + col3[k], y + row3[k]))
                                
                            if row3[k]==1:
                                visited[x + col3[k]][y + row3[k]] = True
                                quit.append((x + col3[k], y + row3[k]))

                elif node==0:

                    col0=[-1,0]
                    row0=[0,-1]

                    for k in range(2):     
                        if check_visited(matrix, x + col0[k], y + row0[k], visited):
                            
                            if col0[k]==-1 and matrix[x + col0[k]][y + row0[k]] in [2,3]:
                                visited[x + col0[k]][y + row0[k]] = True
                                quit.append((x + col0[k], y + row0[k]))

                            if row0[k]==-1 and matrix[x + col0[k]][y + row0[k]] in [1,3]:
                                visited[x + col0[k]][y + row0[k]] = True
                                quit.append((x + col0[k], y + row0[k]))
    
        visited = [[False for x in range(len(matrix[0]))] for y in range(len(matrix))]
        walls=0

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):

                if matrix[i][j]!=0 and not visited[i][j]:

                    check(matrix, i, j, visited, matrix[i][j])
                    walls +=1

        print(Maze.analyse_messages(self,'wall',walls))

        ###############################################################
        #######--------inner points & accessible areas--------#########
        ###############################################################
        def check_visited4(matrixx, x, y, visited4): #checks if it was previously visited
            return (x>-1) and (x<len(matrixx)) and (y>-1) and (y<len(matrixx[0])) and visited4[x][y]

        def find_the_size_of_the_culdesac(i, j, matrixwalls): #used to find how deep the culdesac is
                                
            quit = deque()
            quit.append((i,j))


            culdesacs3 = 0
            coordinates2 = []
            coordinates2.append([i,j])
            matrixwalls[i][j] = False

            while quit:
                x, y = quit.popleft()

                col=[-1,1,0,0]
                row=[0,0,-1,1]
                

                safe = 0
                for k in range(4):
                    if (x + col[k]>-1) and (x + col[k]<len(matrixwalls)) and\
                        (y + row[k]>-1) and (y + row[k]<len(matrixwalls[0]))and \
                        not matrixwalls[x + col[k]][y + row[k]]!='w' and\
                        matrixwalls[x + col[k]][y + row[k]]:

                        
                        if col[k]==-1:
                            visited6[x-1][y] = False
                            quit.append((x-1, y))
                            #coordinates2.append([x-1, y])
                            safe+=1

                        if col[k]==1:
                            visited6[x+1][y] = False
                            quit.append((x+1, y))
                            #coordinates2.append([x+1, y])
                            safe+=1

                        if row[k]==-1:
                            visited6[x][y-1] = False
                            quit.append((x, y-1))
                            #coordinates2.append([x, y-1])
                            safe+=1
                            
                        if row[k]==1:
                            visited6[x][y+1] = False
                            quit.append((x, y+1))
                            #coordinates2.append([x, y+1])
                            safe+=1

                if safe>1:
                    quit.clear()

                    for x in coordinates2:
                        coordinates.append(x)
                else:
                    coordinates.append([x,y])
            



                # if safe>1:
                    
                #     del coordinates[-3:]                    

                #     for x in range(len(coordinates)):

                #         if coordinates[x][0] % 2 ==1 and coordinates[x][1] % 2 ==1:
                #             culdesacs3+=1

                #     if culdesacs3!=0:
                #         return culdesacs3
                
                # elif safe<1:
                #     return 0              

        def check_culdesac(i, j, matrixwalls): #finds culdesacs in accesible areas with multiple gates

            #visited6 = deepcopy(visited5) #used to find how deep the culdesac is / the size of the whole

            quit = deque()
            quit.append((i,j))

            culdesacs2 = 0
            matrixwalls[i][j] = False
            visited6[i][j] = False

            while quit:
                x, y = quit.popleft()

                col=[-1,1,0,0]
                row=[0,0,-1,1]


                no_of_walls = 0
                for k in range(4):
                    if (x + col[k]>-1) and (x + col[k]<len(matrixwalls)) and\
                         (y + row[k]>-1) and (y + row[k]<len(matrixwalls[0])):

                        if matrixwalls[x + col[k]][y + row[k]]!='w':

                            if check_visited4(matrixx, x + col[k], y + row[k], visited6):
                                
                                if col[k]==-1:
                                    visited6[x-1][y] = False
                                    quit.append((x-1, y))

                                if col[k]==1:
                                    visited6[x+1][y] = False
                                    quit.append((x+1, y))

                                if row[k]==-1:
                                    visited6[x][y-1] = False
                                    quit.append((x, y-1))
                                    
                                if row[k]==1:
                                    visited6[x][y+1] = False
                                    quit.append((x, y+1))

                        else:
                            no_of_walls+=1


                if no_of_walls==3 and x!=0 and x!=len(matrixwalls)-1 and y!=0 and y!=len(matrixwalls[0])-1:
            
                    culdesacs2+=1
                    find_the_size_of_the_culdesac(x, y, matrixwalls)

            if culdesacs2!=0:
                return culdesacs2
            else:
                return 0

        def accessible_areas(matrixx, i, j, visited4):

            quit = deque()
            quit.append((i,j))

            gates = 0
            global areas
            global inners
            global culdesacs
            global onepaths

            areas = 0
            inners = 0
            culdesacs = 0
            onepaths = 0
            coordinates3 = []
            

            if visited4[i][j]:

                points = 0
                coordinates3.append([i,j])
                visited4[i][j] = False
        
                while quit:

                    x,y = quit.popleft()

                    col=[-1,1,0,0]
                    row=[0,0,-1,1]

                    points+=1

                    for k in range(4):
                        if check_visited4(matrixx, x + col[k], y + row[k], visited4):
                            
                            if col[k]==-1:
                                visited4[x-1][y] = False
                                quit.append((x-1, y))
                                coordinates3.append([x-1, y])

                            if col[k]==1:
                                visited4[x+1][y] = False
                                quit.append((x+1, y))
                                coordinates3.append([x+1, y])

                            if row[k]==-1:
                                visited4[x][y-1] = False
                                quit.append((x, y-1))
                                coordinates3.append([x, y-1])
                                
                            if row[k]==1:
                                visited4[x][y+1] = False
                                quit.append((x, y+1))
                                coordinates3.append([x, y+1])

                for x in range(len(coordinates3)):
                        
                    if coordinates3[x][0] in [0, len(visited4)-1]\
                        or coordinates3[x][1] in [0, len(visited4[0])-1]:

                        gates+=1
                
                if gates==0:
                    
                    for x in range(len(coordinates3)):

                        if coordinates3[x][0] % 2 ==1 and coordinates3[x][1] % 2 ==1:
                            inners+=1

                    return inners
                
                elif gates>0:
                    if gates==1:

                        for x in coordinates3:

                            if x[0] % 2 ==1 and x[1] % 2 ==1:
                                
                                coordinates.append(x)

                        culdesacs+=1

                    elif gates>1:

                        culdesacs += check_culdesac(coordinates3[-1][0], coordinates3[-1][1], matrixwalls)


                    if gates==2 and onepaths>=0:
                        onepaths+=1

                    areas+=1
                    return areas

        matrixx = []
        for x in range(2*len(matrix)-1):
            matrixx.append([])
            for y in range(2*len(matrix[0])-1):
                matrixx[x].append(True)

        for x in range(len(matrix)):
            for y in range(len(matrix[0])):
                matrixx[2*x][2*y]=matrix[x][y]
        
        matrixwalls = deepcopy(matrixx)
        for x in range(len(matrixx)):
            for y in range(len(matrixx[0])):
                
                if str(matrixx[x][y])=='0':
                    matrixx[x][y]=False

                elif str(matrixx[x][y])=='1':
                    matrixx[x][y+1]=False
                    matrixx[x][y]=False

                elif matrixx[x][y]==2:
                    matrixx[x+1][y]=False
                    matrixx[x][y]=False

                elif matrixx[x][y]==3:
                    matrixx[x+1][y]=False
                    matrixx[x][y+1]=False
                    matrixx[x][y]=False  

        for x in range(len(matrixwalls)):
            for y in range(len(matrixwalls[0])):
                
                if str(matrixwalls[x][y])=='0':
                    matrixwalls[x][y]='w'

                elif str(matrixwalls[x][y])=='1':
                    matrixwalls[x][y+1]='w'
                    matrixwalls[x][y]='w'

                elif matrixwalls[x][y]==2:
                    matrixwalls[x+1][y]='w'
                    matrixwalls[x][y]='w'

                elif matrixwalls[x][y]==3:
                    matrixwalls[x+1][y]='w'
                    matrixwalls[x][y+1]='w'
                    matrixwalls[x][y]='w'

        area = 0
        inner = 0
        culdesac = 0
        onepath = 0
        visited4 = deepcopy(matrixx)
        visited5 = deepcopy(matrixx) #used in def check_culdesac function
        visited6 = deepcopy(visited5) #used to find how deep the culdesac is / the size of the whole
        
        global coordinates
        coordinates = []

        for i in range(len(matrixx)):
            for j in range(len(matrixx[0])):
                
                if matrixx[i][j]:
                    
                    a = accessible_areas(matrixx, i, j, visited4)

                    if areas!=0:
                        area+=a
                        culdesac+=culdesacs
                        onepath+=onepaths

                    elif inners!=0:
                        inner+=a

        
        print(Maze.analyse_messages(self, 'inner', inner))
        print(Maze.analyse_messages(self, 'accessible', area))
        print(Maze.analyse_messages(self, 'culdesac', culdesac))
        print(Maze.analyse_messages(self, 'path', onepath))






#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------





    def display(self):
          
        ################################################################
        #####################--------gates--------######################
        ################################################################
        top_gates=len([x for x in matrix[0][:-1] if x in [0, 2]])
        left_gates=len([matrix[x][0] for x in range(len(matrix)-1) if matrix[x][0] in [0, 1]])
        right_gates=len([matrix[x][-1] for x in range(len(matrix)-1) if matrix[x][-1]==0])
        bottom_gates=len([x for x in matrix[-1][:-1] if x==0])
        total_gates = top_gates + left_gates + right_gates + bottom_gates
        
        ################################################################
        #####################--------wales--------######################
        ################################################################
        def check_visited(matrix, x, y, visited): #checks if it was previously visited
            return (x>-1) and (x<len(visited)) and (y>-1) and (y<len(visited[0])) and (not visited[x][y])

        def check(matrix, i, j, visited, node):
            quit = deque()
            quit.append((i,j))

            visited[i][j] = True

            while quit:

                x,y = quit.popleft()
        
                node = matrix[x][y]

                if node==1:

                    col1=[0,0,-1]
                    row1=[1,-1,0]

                    for k in range(3):
                        if check_visited(matrix, x + col1[k], y + row1[k], visited):

                            if col1[k]==-1 and matrix[x + col1[k]][y + row1[k]] in [2,3]:
                                visited[x + col1[k]][y + row1[k]] = True
                                quit.append((x + col1[k], y + row1[k]))

                            if row1[k]==-1 and matrix[x + col1[k]][y + row1[k]] in [1,3]:
                                visited[x + col1[k]][y + row1[k]] = True
                                quit.append((x + col1[k], y + row1[k]))

                            if row1[k]==1:
                                visited[x + col1[k]][y + row1[k]] = True
                                quit.append((x + col1[k], y + row1[k]))

                elif node==2:

                    col2=[1,-1,0]
                    row2=[0,0,-1]

                    for k in range(3):     
                        if check_visited(matrix, x + col2[k], y + row2[k], visited):
                            
                            if col2[k]==-1 and matrix[x + col2[k]][y + row2[k]] in [2,3]:
                                visited[x + col2[k]][y + row2[k]] = True
                                quit.append((x + col2[k], y + row2[k]))

                            if row2[k]==-1 and matrix[x + col2[k]][y + row2[k]] in [1,3]:
                                visited[x + col2[k]][y + row2[k]] = True
                                quit.append((x + col2[k], y + row2[k]))

                            if col2[k]==1:
                                visited[x + col2[k]][y + row2[k]] = True
                                quit.append((x + col2[k], y + row2[k]))

                elif node==3:

                    col3=[1,-1,0,0]
                    row3=[0,0,-1,1]

                    for k in range(4):
                        if check_visited(matrix, x + col3[k], y + row3[k], visited):

                            if col3[k]==-1 and matrix[x + col3[k]][y + row3[k]] in [2,3]:
                                visited[x + col3[k]][y + row3[k]] = True
                                quit.append((x + col3[k], y + row3[k]))

                            if row3[k]==-1 and matrix[x + col3[k]][y + row3[k]] in [1,3]:
                                visited[x + col3[k]][y + row3[k]] = True
                                quit.append((x + col3[k], y + row3[k]))

                            if col3[k]==1:
                                visited[x + col3[k]][y + row3[k]] = True
                                quit.append((x + col3[k], y + row3[k]))
                                
                            if row3[k]==1:
                                visited[x + col3[k]][y + row3[k]] = True
                                quit.append((x + col3[k], y + row3[k]))

                elif node==0:

                    col0=[-1,0]
                    row0=[0,-1]

                    for k in range(2):     
                        if check_visited(matrix, x + col0[k], y + row0[k], visited):
                            
                            if col0[k]==-1 and matrix[x + col0[k]][y + row0[k]] in [2,3]:
                                visited[x + col0[k]][y + row0[k]] = True
                                quit.append((x + col0[k], y + row0[k]))

                            if row0[k]==-1 and matrix[x + col0[k]][y + row0[k]] in [1,3]:
                                visited[x + col0[k]][y + row0[k]] = True
                                quit.append((x + col0[k], y + row0[k]))
    
        visited = [[False for x in range(len(matrix[0]))] for y in range(len(matrix))]
        walls=0

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):

                if matrix[i][j]!=0 and not visited[i][j]:

                    check(matrix, i, j, visited, matrix[i][j])
                    walls +=1



        ###############################################################
        #######--------inner points & accessible areas--------#########
        ###############################################################
        def check_visited4(matrixx, x, y, visited4): #checks if it was previously visited
            return (x>-1) and (x<len(matrixx)) and (y>-1) and (y<len(matrixx[0])) and visited4[x][y]

        def find_the_size_of_the_culdesac(i, j, matrixwalls): #used to find how deep the culdesac is
                                
            quit = deque()
            quit.append((i,j))


            culdesacs3 = 0
            coordinates2 = []
            coordinates2.append([i,j])
            matrixwalls[i][j] = False

            while quit:
                x, y = quit.popleft()

                col=[-1,1,0,0]
                row=[0,0,-1,1]
                

                safe = 0
                for k in range(4):
                    if (x + col[k]>-1) and (x + col[k]<len(matrixwalls)) and\
                        (y + row[k]>-1) and (y + row[k]<len(matrixwalls[0]))and \
                        not matrixwalls[x + col[k]][y + row[k]]!='w' and\
                        matrixwalls[x + col[k]][y + row[k]]:

                        
                        if col[k]==-1:
                            visited6[x-1][y] = False
                            quit.append((x-1, y))
                            #coordinates2.append([x-1, y])
                            safe+=1

                        if col[k]==1:
                            visited6[x+1][y] = False
                            quit.append((x+1, y))
                            #coordinates2.append([x+1, y])
                            safe+=1

                        if row[k]==-1:
                            visited6[x][y-1] = False
                            quit.append((x, y-1))
                            #coordinates2.append([x, y-1])
                            safe+=1
                            
                        if row[k]==1:
                            visited6[x][y+1] = False
                            quit.append((x, y+1))
                            #coordinates2.append([x, y+1])
                            safe+=1

                if safe>1:
                    quit.clear()

                    for x in coordinates2:
                        coordinates.append(x)
                else:
                    coordinates.append([x,y])
            



                # if safe>1:
                    
                #     del coordinates[-3:]                    

                #     for x in range(len(coordinates)):

                #         if coordinates[x][0] % 2 ==1 and coordinates[x][1] % 2 ==1:
                #             culdesacs3+=1

                #     if culdesacs3!=0:
                #         return culdesacs3
                
                # elif safe<1:
                #     return 0              

        def check_culdesac(i, j, matrixwalls): #finds culdesacs in accesible areas with multiple gates

            #visited6 = deepcopy(visited5) #used to find how deep the culdesac is / the size of the whole

            quit = deque()
            quit.append((i,j))

            culdesacs2 = 0
            matrixwalls[i][j] = False
            visited6[i][j] = False

            while quit:
                x, y = quit.popleft()

                col=[-1,1,0,0]
                row=[0,0,-1,1]


                no_of_walls = 0
                for k in range(4):
                    if (x + col[k]>-1) and (x + col[k]<len(matrixwalls)) and\
                         (y + row[k]>-1) and (y + row[k]<len(matrixwalls[0])):

                        if matrixwalls[x + col[k]][y + row[k]]!='w':

                            if check_visited4(matrixx, x + col[k], y + row[k], visited6):
                                
                                if col[k]==-1:
                                    visited6[x-1][y] = False
                                    quit.append((x-1, y))

                                if col[k]==1:
                                    visited6[x+1][y] = False
                                    quit.append((x+1, y))

                                if row[k]==-1:
                                    visited6[x][y-1] = False
                                    quit.append((x, y-1))
                                    
                                if row[k]==1:
                                    visited6[x][y+1] = False
                                    quit.append((x, y+1))

                        else:
                            no_of_walls+=1


                if no_of_walls==3 and x!=0 and x!=len(matrixwalls)-1 and y!=0 and y!=len(matrixwalls[0])-1:
            
                    culdesacs2+=1
                    find_the_size_of_the_culdesac(x, y, matrixwalls)

            if culdesacs2!=0:
                return culdesacs2
            else:
                return 0

        def accessible_areas(matrixx, i, j, visited4):

            quit = deque()
            quit.append((i,j))

            gates = 0
            global areas
            global inners
            global culdesacs
            global onepaths

            areas = 0
            inners = 0
            culdesacs = 0
            onepaths = 0
            coordinates3 = []            

            if visited4[i][j]:

                points = 0
                coordinates3.append([i,j])
                visited4[i][j] = False
        
                while quit:

                    x,y = quit.popleft()

                    col=[-1,1,0,0]
                    row=[0,0,-1,1]

                    points+=1

                    for k in range(4):
                        if check_visited4(matrixx, x + col[k], y + row[k], visited4):
                            
                            if col[k]==-1:
                                visited4[x-1][y] = False
                                quit.append((x-1, y))
                                coordinates3.append([x-1, y])

                            if col[k]==1:
                                visited4[x+1][y] = False
                                quit.append((x+1, y))
                                coordinates3.append([x+1, y])

                            if row[k]==-1:
                                visited4[x][y-1] = False
                                quit.append((x, y-1))
                                coordinates3.append([x, y-1])
                                
                            if row[k]==1:
                                visited4[x][y+1] = False
                                quit.append((x, y+1))
                                coordinates3.append([x, y+1])

                for x in range(len(coordinates3)):
                        
                    if coordinates3[x][0] in [0, len(visited4)-1]\
                        or coordinates3[x][1] in [0, len(visited4[0])-1]:

                        gates+=1
                
                if gates==0:
                    
                    for x in range(len(coordinates3)):

                        if coordinates3[x][0] % 2 ==1 and coordinates3[x][1] % 2 ==1:
                            inners+=1

                    return inners
                
                elif gates>0:
                    if gates==1:

                        for x in coordinates3:

                            if x[0] % 2 ==1 and x[1] % 2 ==1:
                                
                                coordinates.append(x)

                        culdesacs+=1

                    elif gates>1:

                        culdesacs += check_culdesac(coordinates3[-1][0], coordinates3[-1][1], matrixwalls)


                    if gates==2 and onepaths>=0:
                    
                        for x in coordinates3:
                            if x[0] % 2 ==1 and x[1] % 2 ==1 or (x[0]==0 or x[1]==0) or\
                                (x[0]==len(coordinates3) or x[1]==len(coordinates3[0])):
                                coordinates4.append(x)
                            # elif x[0]==0 or x[1]==0:
                            #     coordinates5.append(x)

                        onepaths+=1

                    areas+=1
                    return areas

        matrixx = []
        for x in range(2*len(matrix)-1):
            matrixx.append([])
            for y in range(2*len(matrix[0])-1):
                matrixx[x].append(True)

        for x in range(len(matrix)):
            for y in range(len(matrix[0])):
                matrixx[2*x][2*y]=matrix[x][y]
        
        matrixwalls = deepcopy(matrixx)
        for x in range(len(matrixx)):
            for y in range(len(matrixx[0])):
                
                if str(matrixx[x][y])=='0':
                    matrixx[x][y]=False

                elif str(matrixx[x][y])=='1':
                    matrixx[x][y+1]=False
                    matrixx[x][y]=False

                elif matrixx[x][y]==2:
                    matrixx[x+1][y]=False
                    matrixx[x][y]=False

                elif matrixx[x][y]==3:
                    matrixx[x+1][y]=False
                    matrixx[x][y+1]=False
                    matrixx[x][y]=False  

        for x in range(len(matrixwalls)):
            for y in range(len(matrixwalls[0])):
                
                if str(matrixwalls[x][y])=='0':
                    matrixwalls[x][y]='w'

                elif str(matrixwalls[x][y])=='1':
                    matrixwalls[x][y+1]='w'
                    matrixwalls[x][y]='w'

                elif matrixwalls[x][y]==2:
                    matrixwalls[x+1][y]='w'
                    matrixwalls[x][y]='w'

                elif matrixwalls[x][y]==3:
                    matrixwalls[x+1][y]='w'
                    matrixwalls[x][y+1]='w'
                    matrixwalls[x][y]='w'

        area = 0
        inner = 0
        culdesac = 0
        onepath = 0
        visited4 = deepcopy(matrixx)
        visited5 = deepcopy(matrixx) #used in def check_culdesac function
        visited6 = deepcopy(visited5) #used to find how deep the culdesac is / the size of the whole
        
        global coordinates
        global coordinates4
        global coordinates5
        coordinates = []
        coordinates4 = []
        coordinates5 = []


        for i in range(len(matrixx)):
            for j in range(len(matrixx[0])):
                
                if matrixx[i][j]:
                    
                    a = accessible_areas(matrixx, i, j, visited4)

                    if areas!=0:
                        area+=a
                        culdesac+=culdesacs
                        onepath+=onepaths

                    elif inners!=0:
                        inner+=a


        ###############################################################
        #################--------draw walls--------####################
        ###############################################################

        hor = 0
        hor_list_1 = []
        hor_list_2 = []
        for x in range(len(matrix)):
            for y in range(len(matrix[0])):
                
                if matrix[x][y] in [1,3] and hor==0:
                    hor+=1
                    hor_list_1.append([y,x])

                elif not matrix[x][y] in [1,3] and hor!=0:
                    hor_list_2.append([y,x])
                    hor = 0

        ver = 0
        ver_list_1 = []
        ver_list_2 = []
        for y in range(len(matrix[0])):
            for x in range(len(matrix)):
                
                if matrix[x][y] in [2,3] and ver==0:
                    ver+=1
                    ver_list_1.append([y,x])

                elif not matrix[x][y] in [2,3] and ver!=0:
                    ver_list_2.append([y,x])
                    ver = 0

        ###############################################################
        ################--------draw pillars--------###################
        ###############################################################
        
        pillars = []
        for x in range(len(matrix)):
            for y in range(len(matrix[0])):

                if matrix[x][y]==0:
                    
                    if x==0 and y==0:
                        pillars.append([y,x])

                    elif x==0 and y!=0 and matrix[0][y-1]==2:
                        pillars.append([y,x])

                    elif x!=0 and y==0 and matrix[x-1][0]==1:
                        pillars.append([y,x])
                    
                    elif x!=0 and y!=0 and matrix[x-1][y] in [0,1] and matrix[x][y-1] in [0,2]:
                        pillars.append([y,x])
        


        ###############################################################
        ###############--------draw culdesacs--------##################
        ###############################################################

        for x in coordinates:
            i=x[0]
            j=x[1]
            x[0]=j/2
            x[1]=i/2

        coordinates.sort()

        global culdesac_nodes
        culdesac_nodes = coordinates

        ###############################################################
        #################--------draw path--------#####################
        ###############################################################

        for x in coordinates4:
            i=x[0]
            j=x[1]
            x[0]=j/2
            x[1]=i/2
        
        for x in coordinates5:
            i=x[0]
            j=x[1]
            x[0]=j/2
            x[1]=i/2

            if x[0]==0:
                x[0]=-0.5
            elif x[1]==0:
                x[1]=-0.5

        # for x in coordinates5:
        #     coordinates4.append(x)
        
        horizons = []
        verticals = []

        for index, x in enumerate(coordinates4):
            
            if index < len(coordinates4)-1:

                if x[0]==coordinates4[index+1][0]:
                    verticals.append([x,coordinates4[index+1]])

                    
                if x[1]==coordinates4[index+1][1]:
                    horizons.append([x,coordinates4[index+1]])

        
        horizons2=[]
        verticals2=[]
        for x in horizons:
            horizons2.append(x[0])
            horizons2.append(x[1])

        for x in verticals:
            verticals2.append(x[0])
            verticals2.append(x[1])

        horizons2.sort()
        verticals2.sort()

        verticals_0=[]

        for x in verticals2:
            verticals_0.append(x[0])

        for x in range(len(verticals_0)):
            y = verticals_0.count(verticals_0[x])
            if y>2:

                del verticals2[x+1:x+y-1]

        horizons_1=[]

        for x in horizons2:
            horizons_1.append(x[1])

        for x in range(len(horizons_1)):
            y = horizons_1.count(horizons_1[x])
            if y>2:
                del horizons2[x+1:x+y-1]    

        for x in horizons2:
            if x[0]==0:
                x[0]=-0.5
            elif x[1]==0:
                x[1]=-0.5

        for x in verticals2:
            if x[0]==0:
                x[0]=-0.5
            elif x[1]==0:
                x[1]=-0.5

        horizons2.sort()
        verticals2.sort()

        ff=open(texname, 'w')

        ff.write('\\documentclass[10pt]{article}\n'
        '\\usepackage{tikz}\n'
        '\\usetikzlibrary{shapes.misc}\n'
        '\\usepackage[margin=0cm]{geometry}\n'
        '\\pagestyle{empty}\n'
        '\\tikzstyle{every node}=[cross out, draw, red]\n'
        '\n'
        '\\begin{document}\n'
        '\n'
        '\\vspace*{\\fill}\n'
        '\\begin{center}\n'
        '\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n'
        '% Walls\n')

        for x in range(len(hor_list_1)):
            
            i = hor_list_1[x][0]
            ii = hor_list_1[x][1]
            j = hor_list_2[x][0]
            jj = hor_list_2[x][1]

            y = '    \\draw ({},{}) -- ({},{});\n'.format(i,ii,j,jj)
            
            ff.write(y)


        for x in range(len(ver_list_1)):
            
            i = ver_list_1[x][0]
            ii = ver_list_1[x][1]
            j = ver_list_2[x][0]
            jj = ver_list_2[x][1]

            y = '    \\draw ({},{}) -- ({},{});\n'.format(i,ii,j,jj)
            
            ff.write(y)

        ff.write('% Pillars\n')
        for x in pillars:

            i = x[0]
            ii = x[1]

            y = '    \\fill[green] ({},{}) circle(0.2);\n'.format(i,ii)

            ff.write(y)

        ff.write('% Inner points in accessible cul-de-sacs\n')

        for x in culdesac_nodes:

            i = x[0]
            ii = x[1]
    
            y = '    \\node at ({},{}) {{}};\n'.format(i,ii)

            ff.write(y)

        ff.write('% Entry-exit paths without intersections\n')

        for x in range(0,len(horizons2),2):
            
            i = horizons2[x][0]
            ii = horizons2[x][1]
            j = horizons2[x+1][0]
            jj = horizons2[x+1][1]

            y = '    \\draw[dashed, yellow] ({},{}) -- ({},{});\n'.format(i,ii,j,jj)

            ff.write(y)

        for x in range(0,len(verticals2),2):

            i = verticals2[x][0]
            ii = verticals2[x][1]
            j = verticals2[x+1][0]
            jj = verticals2[x+1][1]

            y = '    \\draw[dashed, yellow] ({},{}) -- ({},{});\n'.format(i,ii,j,jj)

            ff.write(y)

        ff.write('\\end{tikzpicture}\n'
        '\\end{center}\n'
        '\\vspace*{\\fill}\n'
        '\n'
        '\\end{document}\n')