# grid, grid size, how many in a row for a win
def whoWon(state, N, M):
    # horizontal
    # for each row
    for i in range(N):
        type = state[N*i]
        run = 1
        for j in range(1, N):
            if state[N*i+j] == type:
                run += 1
            else:
                type = state[N*i+j]
                run = 1
            if run == M and type != "E":
                return type

    # vertical
    # for each column
    for j in range(N):
        type = state[j]
        run = 1
        for i in range(1, N):
            if state[N*i+j] == type:
                run += 1
            else:
                type = state[N*i+j]
                run = 1
            if run == M and type != "E":
                return type

    # diagonal
    # right down
    # upper triangle
    # for each diagonal
    for j in range(0, N-M+1):
        type = state[j]
        run = 1
        for i in range(0, N-j): # check ERROR ERROR
            if state[N*i+j+i] == type:
                run += 1
            else:
                type = state[N*i+j+i]
                run = 1
            if run == M and type != "E":
                return type

    # right down
    # bottom triangle
    for i in range(1, N-M+1):
        type = state[N*i]
        run = 1
        for j in range(0, N-i): # check ERROR ERROR
            if state[N*(i+j)+j] == type:
                run += 1
            else:
                type = state[N*(i+j)+j]
                run = 1
            if run == M and type != "E":
                return type

    # left up
    # left triangle
    for i in range(M, N):
        type = state[N*i]
        run = 1
        for j in range(0, i):
            if state[N*(i-j)+j] == type:
                run += 1
            else:
                type = state[N*(i-j)+j]
                run = 1
            if run == M and type != "E":
                return type

    # down left
    # right triangle
    for j in range(1, N-M+1):
        type = state[N*j+N-1]
        run = 1
        for i in range(j, N):
            if state[N*i + N-(i-j+1)] == type:
                run += 1
            else:
                type = state[N*i + N-(i-j+1)]
                run = 1
            if run == M and type != "E":
                return type

    # is the game still going
    for i in range(N*N):
        if state[i] == "E":
            return "NoOne"

    return "Tie"


if __name__ == "__main__":
    N = 6
    M = 4
    board = "E"*N*N
    import random
    board = "".join([random.choice(["X", "E", "O"]) for i in range(N*N)])

    def printBoard(board, N):
        for i in range(N):
            print(board[i*N:(i+1)*N])

    board = "E"*N*N
    for i in range(0, M):
        idx = (i)*N+1+i+1
        board = board[:idx-1]+"X"+board[idx:]
    print(whoWon(board, N, M))
    printBoard(board, N)

    board = "E"*N*N
    for i in range(0, M):
        idx = (2+i)*N+1+i+1
        board = board[:idx-1]+"X"+board[idx:]
    print(whoWon(board, N, M))
    printBoard(board, N)

    board = "E"*N*N
    for i in range(0, M):
        idx = (N-1-i)*N+i+1
        board = board[:idx-1]+"O"+board[idx:]
    print(whoWon(board, N, M))
    printBoard(board, N)

    board = "E"*N*N
    for i in range(0, M):
        idx = (N-1-i)*N+i+1+2
        board = board[:idx-1]+"O"+board[idx:]
    print(whoWon(board, N, M))
    printBoard(board, N)
