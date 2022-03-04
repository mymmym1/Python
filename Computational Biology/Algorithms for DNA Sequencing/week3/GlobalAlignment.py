alphabet = ['A', 'C', 'G', 'T']
score = [[0, 4, 2, 4, 8],
         [4, 0, 4, 2, 8],
         [2, 4, 0, 4, 8],
         [4, 2, 4, 0, 8],
         [8, 8, 8, 8, 8]]

def globalAlignment(x, y):  # x = [], y = []
    # Create distance matrix
    D = []
    for i in range(len(x) + 1):
        D.append([0] * (len(y) + 1))
    # Initialize first column
    for i in range(1, len(x) + 1):
        D[i][0] = D[i - 1][0] + score[alphabet.index(x[i - 1])][-1]  # (score)base:- => 8 highest penalty
    # Initialize first row
    for i in range(1, len(y) + 1):
        D[0][i] = D[0][i - 1] + score[-1][alphabet.index(y[i - 1])]  # (score)base:- => 8 highest penalty
    # Fill rest of the matrix
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            distHor = D[i][j - 1] + score[-1][alphabet.index(y[j - 1])]  # (score)base:- => 8 highest penalty
            distVer = D[i - 1][j] + score[alphabet.index(x[i - 1])][-1]  # (score)base:- => 8 highest penalty
            if x[i - 1] == y[j - 1]:
                distDiag = D[i - 1][j - 1]
            else:
                distDiag = D[i - 1][j - 1] + score[alphabet.index(x[i - 1])][alphabet.index(y[j - 1])]
            D[i][j] = min(distHor, distVer, distDiag)
    return D[-1][-1]  # return value in bottom right corner

x = 'TACCAGATTCGA'
y = 'TACCAATTCGA'
print(globalAlignment(x,y))  # 8 for skip penalty

x = 'TACCAGATTCGA'
y = 'TACCACATTCGA'
print(globalAlignment(x,y))  # 4 for transversion penalty

x = 'TACCAGATTCGA'
y = 'TACCAAATTCGA'
print(globalAlignment(x,y))  # 2 for transition penalty

x = 'TACCAGATTCGA'
y = 'TACCAAATTGA'
print(globalAlignment(x,y))  # 10 for a skip + a transition penalty