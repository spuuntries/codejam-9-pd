
const board = [];
const cells = document.getElementsByClassName("cell");


for (let i = 0; i < 4; i++) {
    board.push(Array(4).fill(0));
}

randomBoard();

let fixed = new Set();
let fixedCount = randint(6, 10); // adjust value if n

while (fixed.size < fixedCount) {
    fixed.add(`[${randint(0, 3)}, ${randint(0, 3)}]`);
}

for (let fix of fixed) {
    let [x, y] = eval(fix);
    let cell = cells[y * 4 + x];
    cell.classList.add("fixed");
    cell.innerHTML = board[y][x];
}

for (let [y, row] of board.entries()) {
    for (let [x, cell] of row.entries()) {
        if (!fixed.has(`[${x}, ${y}]`)) {
            board[y][x] = 0;
        }
    }
}

for (let cell of cells) {
    cell.addEventListener('click', () => {
        
        if (!cell.classList.contains('fixed')) {
            let f = +cell.id;
            let x = f % 4;
            let y = Math.floor(f / 4);
    
            let newVal = ((+cell.innerHTML || 0) + 1) % 5 || 1;
            cell.innerHTML = newVal;

            board[y][x] = 0;

            if (isValid(board, x, y, newVal)) {
                cell.classList.add("correct");
                cell.classList.remove("wrong")
            } else {
                cell.classList.add("wrong");
                cell.classList.remove("correct");
            }

            board[y][x] = newVal;
        }
    });
}





function randomBoard() {
    let [x, y] = findEmpty(board);

    if (x < 0) {
        return true;
    }

    for (let n of [1, 2, 3, 4].sort(() => Math.random() - .5)) {
        if (isValid(board, x, y, n)) {
            board[y][x] = n;

            if (randomBoard()) {
                return true;
            }

            board[y][x] = n;
        }
    }

    return false;
}


function findEmpty(board) {
    for (let y = 0; y < 4; y++) {
        for (let x = 0; x < 4; x++) {
            if (board[y][x] == 0) {
                return [x, y];
            }
        }
    }

    return [-1, -1];
}

function isValid(board, x, y, n) {
    if (board[y].includes(n)) {
        return false;
    }

    for (let row of board) {
        if (row[x] == n) {
            return false;
        }
    }

    for (let [i, j] of getBox(x, y)) {
        if (board[j][i] == n) {
            return false;
        }
    }

    return true;
}

function getBox(x, y) {
    let bx = 2 * Math.floor(x / 2);
    let by = 2 * Math.floor(y / 2);
    let res = [];

    for (let i = 0; i < 2; i++) {
        for (let j = 0; j < 2; j++) {
            res.push([bx + i, by + j]);
        }
    }

    return res;
}

function randint(min, max) {
    return Math.floor(Math.random()*(max-min+1)+min);
}


var solved = false;

setInterval(() => {
    if (!solved) {
        let tempBoard = JSON.parse(JSON.stringify(board));

        for (let y = 0; y < 4; y++) {
            for (let x = 0; x < 4; x++) {
                let n = tempBoard[y][x];
                tempBoard[y][x] = 0;

                if (!isValid(tempBoard, x, y, n)) {
                    return null;
                }

                tempBoard[y][x] = n;
            }
        }

        alert("Congrats u solved it!");
        solved = true;
    }

}, 1000);
