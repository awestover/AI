let strategies = {};
let strategyName = "strategy5";
let mod = 5;

// "none", "split", or "hit"
let moveType = "none";
let hitInfo = {"from": -1, "to": -1};
let oldState = [1,1,1,1];

let state = [1,1,1,1];
function displayState() {
  $("#ch1").text(state[0]);
  $("#uh1").text(state[2]);
  $("#uh2").text(state[3]);
  $("#ch2").text(state[1]);
}

function loadStrategy(stratName){
  $.getJSON("strategy/"+stratName+".json", function(data){
    console.log(data);
    strategies[stratName] = data;
    strategies[stratName]["frozenAllStates"] = [];
    for (var i = 0; i < strategies[stratName]["allStates"].length; i++) {
      strategies[stratName]["frozenAllStates"].push(freeze(strategies[stratName]["allStates"][i]));
    }
  });
}
loadStrategy("strategy5");
loadStrategy("strategy6");

// function handleUserInput() {
//   let proposedMove = $("#userInput").val();
//   let moveIdx = strategies[strategyName]["frozenAllStates"].indexOf(proposedMove);// BUG: need to make sure this is a valid move!!!!!
//   if (moveIdx != -1){
//     $("body").append("<br>");
//     $("body").append(proposedMove);
//     $("body").append("<br>");
//     let computerMoveIdx = strategies[strategyName]["strategy"][moveIdx];
//     let computerMove = strategies[strategyName]["frozenAllStates"][computerMoveIdx];
//     $("body").append(computerMove);
//   }
// }
// function allGood(arr, mod) {
//   for (let a in arr) {
//     if (!arr[a] || arr[a] < 0 || arr[a] > mod) {
//       return false;
//     }
//   }
//   return true;
// }

function freeze(arr) {
  return arr.join(" ");
}

function unFreeze(arr) {
  let tmp = arr.split(" ");
  let out = [];
  for (let a in tmp) {
    out.push(parseInt(tmp[a]));
  }
  return out;
}

function quadType(quad) {
  if (quad == 1 || quad == 4) {
    return "computer";
  }
  else {
    return "user";
  }
}

function handleQuadrantHit(quad) {
  if (moveType == "hit") {
    if (quad == 1 && state[0] != 0) {
      hitInfo["to"] = 0;
    }
    else if (quad == 4 && state[1] != 0) {
      hitInfo["to"] = 1;
    }
    else if (quad == 2 && state[2] != 0) {
      hitInfo["from"] = 2;
    }
    else if(quad == 3 && state[3] != 0) {
      hitInfo["from"] = 3;
    }
  }
  else if (moveType == "split") {
    if (quad == 2) {
      if (state[2] > 0 && state[3] < mod) {
        state[2] -= 1;
        state[3] += 1;
      }
      else {
        alert("cant decrement any more");
      }
    }
    else if (quad == 3) {
      if (state[2] > 0 && state[3] < mod) {
        state[2] += 1;
        state[3] -= 1;
      }
      else {
        alert("cant decrement any more");
      }
    }
    displayState();
  }
  else {
    alert("Chose a move type!");
  }
}

function performReset() {
  moveType = 'none';
  state = oldState.slice();
  hitInfo["from"] = -1;
  hitInfo["to"] = -1;
}

function fixStateOrder(state) {
  let userA = Math.min(state[2], state[3]);
  let userB = Math.max(state[2], state[3]);
  let computerA = Math.min(state[0], state[1]);
  let computerB = Math.max(state[0], state[1]);
  return [computerA, computerB, userA, userB];
}

function performMove() {
  if (moveType == "none") {
    alert("Chose a move type!");
    return false;
  }
  if (moveType == "split") {
    console.log("Did split");
  }
  else if (moveType == "hit") {
    if (hitInfo["from"] == -1 || hitInfo["to"] == -1){
      alert("You did not correctly input a hit");
      return false;
    }
    else {
      state[hitInfo["to"]] = (state[hitInfo["from"]] + state[hitInfo["to"]]) % mod
      hitInfo["from"] = -1;
      hitInfo["to"] = -1;
    }
  }
  moveType = "none";
  state = fixStateOrder(state);
  // computer move
  let moveIdx = strategies[strategyName]["frozenAllStates"].indexOf(freeze(state));
  let computerMoveIdx = strategies[strategyName]["strategy"][moveIdx];
  let computerMove = strategies[strategyName]["frozenAllStates"][computerMoveIdx];
  state = unFreeze(computerMove);
  displayState();
}
