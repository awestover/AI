// code for the graphics

let camera, scene, renderer;
let matrices = {};  // external rotation matricies
let maxCt = 10;
let dth = Math.PI/(2*(maxCt+1));
let rotateIdxs, reindexIdxs;
let geometries = [];
let materials = [];
let meshes = [];
let dims = [2, 4];
let w = 0.3;
let meshInds = [
  [[0,0],[0,1],[0,2],[0,3]],
  [[1,0],[1,1],[1,2],[1,3]]
];
let translates = [[-w/2, -w/2, +w/2], [-w/2, w/2, +w/2], [w/2, w/2, +w/2], [w/2, -w/2, +w/2],
                  [-w/2, -w/2, -w/2], [-w/2, w/2, -w/2], [w/2, w/2, -w/2], [w/2, -w/2, -w/2]];
const COLORS = ['G', 'Y', 'B', 'W', 'O', 'R'];
const COLORWORDS = {
  "G": 0x04db2f,
  "Y": 0xeff707,
  "B": 0x4286f4,
  "W": 0xffffff,
  "O": 0xf78307,
  "R": 0xdb2f04,
  "A": 0x000000
}
const ORIGIN = new THREE.Vector3(0,0,0);
const faceIdxTransform = [5,2,4,3,0,1];
/*
their representation of a cube
   5
 1 2 0
   4
   3
mine:
   0
 5 1 4
   2
   3
*/
let rotationGoing = false;
/*


    |
    |
---------x
    |
    |
    y

  z is straight out of the screen
*/

$.get('/cubeData', function(colorData) {
  init(JSON.parse(colorData));
  animate();
});

function init(colorData) {
  camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.01, 10);
  camera.position.z = 1;

  scene = new THREE.Scene();

  for (let i = 0; i < dims[0]; i++)
  {
    geometries.push([]);
    materials.push([]);
    meshes.push([]);
    for (let k = 0; k < dims[1]; k++)
    {
      geometries[i].push(new THREE.BoxGeometry(0.95*w, 0.95*w, 0.95*w));
      for (let j = 0; j < faceIdxTransform.length; j++) {
        // each face has 2 triangles on it
        let jp = faceIdxTransform[j];
        geometries[i][k].faces[2*jp].color.setHex(COLORWORDS[colorData[i][k][j]]);
        geometries[i][k].faces[2*jp+1].color.setHex(COLORWORDS[colorData[i][k][j]]);
      }
      materials[i].push(new THREE.MeshBasicMaterial( { color: 0xffffff, vertexColors: THREE.FaceColors } ));

      meshes[i].push(new THREE.Mesh(geometries[i][k], materials[i][k]));
      meshes[i][k].translateX(translates[dims[1]*i+k][0]);
      meshes[i][k].translateY(translates[dims[1]*i+k][1]);
      meshes[i][k].translateZ(translates[dims[1]*i+k][2]);

      scene.add(meshes[i][k]);
    }
  }

  scene.rotateX(0.5);
  scene.rotateY(0.1);
  scene.rotateZ(0.1);

  matrices['F'] = new THREE.Matrix4();
  matrices['F'].set(
    Math.cos(-dth), -Math.sin(-dth), 0, 0,
    Math.sin(-dth), Math.cos(-dth), 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 1
  );

  matrices['Fi'] = new THREE.Matrix4();
  matrices['Fi'].set(
    Math.cos(dth), -Math.sin(dth), 0, 0,
    Math.sin(dth), Math.cos(dth), 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 1
  );

  matrices['B'] = matrices['Fi'];
  matrices['Bi'] = matrices['F'];

  matrices['U'] = new THREE.Matrix4();
  matrices['U'].set(
    Math.cos(dth), 0, -Math.sin(dth), 0,
    0, 1, 0, 0,
    Math.sin(dth), 0, Math.cos(dth), 0,
    0, 0, 0, 1
  );

  matrices['Ui'] = new THREE.Matrix4();
  matrices['Ui'].set(
    Math.cos(-dth), 0, -Math.sin(-dth), 0,
    0, 1, 0, 0,
    Math.sin(-dth), 0, Math.cos(-dth), 0,
    0, 0, 0, 1
  );

  matrices['D'] = matrices['Ui'];
  matrices['Di'] = matrices['U'];

  matrices['R'] = new THREE.Matrix4();
  matrices['R'].set(
    1, 0, 0, 0,
    0, Math.cos(-dth), -Math.sin(-dth), 0,
    0, Math.sin(-dth), Math.cos(-dth), 0,
    0, 0, 0, 1
  );

  matrices['Ri'] = new THREE.Matrix4();
  matrices['Ri'].set(
    1, 0, 0, 0,
    0, Math.cos(dth), -Math.sin(dth), 0,
    0, Math.sin(dth), Math.cos(dth), 0,
    0, 0, 0, 1
  );

  matrices['L'] = matrices['Ri'];
  matrices['Li'] = matrices['R'];


  rotateIdxs = {
    "R": [[0,3],[0,2],[1,2],[1,3]],
    "L": [[0,0],[1,0],[1,1],[0,1]],
    "U": [[0,1],[1,1],[1,2],[0,2]],
    "D": [[0,3],[1,3],[1,0],[0,0]],
    "F": [[0,0],[0,1],[0,2],[0,3]],
    "B": [[1,3],[1,2],[1,1],[1,0]]
  }

  for (let key in rotateIdxs) {
    if (key.indexOf('i')==-1)
    {
      rotateIdxs[key+"i"] = rotateIdxs[key].slice().reverse();
    }
  }

  renderer = new THREE.WebGLRenderer( { antialias: true } );
  renderer.setSize( window.innerWidth, window.innerHeight );
  document.body.appendChild( renderer.domElement );
}

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}

function maybeRotate(type, ct) {
  if (!rotationGoing) {
    rotation(type, ct);
  }
}

function getMeshIdxs(coordIdxs) {
  let meshIdxs = [];
  for (let i in coordIdxs) {
    meshIdxs.push(meshInds[coordIdxs[i][0]][coordIdxs[i][1]]);
  }
  return meshIdxs;
}

function rotation(type, ct, callback, params) {
  rotationGoing = true;
  if (ct > maxCt) {
    rotationGoing = false;
    let idxs = rotateIdxs[type];
    let midxs = getMeshIdxs(idxs);
    let tmpIdxs = [];
    let n = idxs.length;
    for (let i = 0; i < n; i++)
    {
      tmpIdxs.push(midxs[i].slice());
    }
    for (let i = 0; i < n; i++)
    {
      meshInds[idxs[(i+1)%n][0]][idxs[(i+1)%n][1]] = tmpIdxs[i];
    }
    if (callback) {
      callback(params);
    }
    return true;
  }
  let midxs = getMeshIdxs(rotateIdxs[type]);
  for (let i in midxs) {
    meshes[midxs[i][0]][midxs[i][1]].applyMatrix(matrices[type]);
  }
  setTimeout(rotation, 50, type, ct+1, callback, params);
}

function rotationQueue(types) {
  if (types.length > 0)
  {
    rotation(types[0], 0, rotationQueue, types.slice(1));
  }
}

document.addEventListener('keypress', (event) => {
  const keyName = event.key.toLowerCase();
  switch (keyName) {
    case 'w':
      scene.rotateX(-0.1);
      break;
    case 's':
      scene.rotateX(0.1);
      break;
    case 'a':
      scene.rotateY(-0.1);
      break;
    case 'd':
      scene.rotateY(0.1);
      break;
    case 'q':
      scene.rotateZ(-0.1);
      break;
    case 'e':
      scene.rotateZ(0.1);
      break;
  }
});

setTimeout(function() {
  let tmp = "";
  for (let key in rotateIdxs) {
    tmp += "<button class='btn btn-lg' onclick='maybeRotate(\""+key+"\",0);'>"+ key+"</button>"
  }
  $('#buttons').append(tmp);
}, 1000);
