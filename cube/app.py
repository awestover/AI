from flask import Flask, render_template, url_for, request
import json

app = Flask(__name__)

cube = []
# initialize the cube
COLORS = ['G', 'Y', 'B', 'W', 'R', 'O']
for color in COLORS:
    cube.append([[color, color],[color, color]])

# for every face on the cube, for every color on the side (2by2 matrix) what face and number of fold out does it correspond to?
facesToCubeColors = [
    [[[1,0],[1,3]], [[1,1],[1,2]]],
    [[[1,1],[1,2]], [[0,1],[0,2]]],
    [[[0,1],[0,2]], [[0,0],[0,3]]],
    [[[0,0],[0,3]], [[1,0],[1,3]]],
    [[[0,2],[1,2]], [[0,3],[1,3]]],
    [[[1,1],[0,1]], [[1,0],[0,0]]]
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cubeData', methods=('POST', 'GET'))
def cubeData():
    global cube
    if request.method == "POST": # alter the cube
        cube = request.json['cubeData'] # something like this
        return "thanks"
    elif request.method == "GET": # retreive the cube
        print(cube)
        tmpCube = [[['A' for k in range(6)] for i in range(4)] for j in range(2)]
        for f in range(len(cube)):
            for r in range(len(cube[f])):
                for c in range(len(cube[f][r])):
                    cIdx = facesToCubeColors[f][r][c]
                    tmpCube[cIdx[0]][cIdx[1]][f] = cube[f][r][c]
        return json.dumps(tmpCube)

if __name__ == "__main__":
    app.run(debug=True)
