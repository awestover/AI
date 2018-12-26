let strategy5;

$.getJSON("strategy/strategy5.json", function(data){
  console.log(data);
  strategy5 = data;
  strategy5["frozenAllStates"] = [];
  for (var i = 0; i < strategy5["allStates"].length; i++) {
    strategy5["frozenAllStates"].push(freeze(strategy5["allStates"][i]));
  }
});

function handleUserInput() {
  let proposedMove = $("#userInput").val();
  let moveIdx = strategy5["frozenAllStates"].indexOf(proposedMove);// BUG: need to make sure this is a valid move!!!!!
  if (moveIdx != -1){
    $("body").append("<br>");
    $("body").append(proposedMove);
    $("body").append("<br>");
    let computerMoveIdx = strategy5["strategy"][moveIdx];
    let computerMove = strategy5["frozenAllStates"][computerMoveIdx];
    $("body").append(computerMove);
  }
}

function strToInt(arr) {
  let o =[];
  for (let a in arr) {
    o.push(parseInt(arr[a]));
  }
  return o;
}

function allGood(arr, mod) {
  for (let a in arr) {
    if (!arr[a] || arr[a] < 0 || arr[a] > mod) {
      return false;
    }
  }
  return true;
}

function freeze(arr) {
  return arr.join(" ");
}
