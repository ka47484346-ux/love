import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="🚀 우주선 피하기",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 우주선 피하기")
st.write("← → 방향키로 우주선을 움직여 운석을 피하세요!")

game = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
body {
    margin: 0;
    background: #050816;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 650px;
    overflow: hidden;
    font-family: Arial, sans-serif;
}

#game {
    text-align: center;
}

canvas {
    border: 3px solid #64748b;
    border-radius: 12px;
    background: #020617;
    box-shadow: 0 0 30px rgba(80,120,255,0.3);
}

#info {
    color: white;
    font-size: 19px;
    margin-bottom: 10px;
}

button {
    margin-top: 12px;
    padding: 10px 25px;
    border: none;
    border-radius: 8px;
    background: #2563eb;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

button:hover {
    background: #1d4ed8;
}
</style>
</head>

<body>

<div id="game">

    <div id="info">
        🚀 점수: <span id="score">0</span>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        ❤️ 목숨: <span id="lives">3</span>
    </div>

    <canvas id="canvas" width="500" height="580"></canvas>

    <br>

    <button onclick="restartGame()">🔄 다시 시작</button>

</div>


<script>

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const scoreText = document.getElementById("score");
const livesText = document.getElementById("lives");


// ======================
// 우주선
// ======================

let ship = {
    x: canvas.width / 2 - 22,
    y: canvas.height - 65,
    width: 44,
    height: 45,
    speed: 7
};


// ======================
// 게임 변수
// ======================

let score = 0;
let lives = 3;

let meteors = [];
let stars = [];

let leftPressed = false;
let rightPressed = false;

let gameOver = false;


// ======================
// 별 생성
// ======================

function createStars() {

    stars = [];

    for (let i = 0; i < 80; i++) {

        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 2 + 1,
            speed: Math.random() * 2 + 0.5
        });

    }
}


// ======================
// 별 그리기
// ======================

function drawStars() {

    ctx.fillStyle = "white";

    for (let star of stars) {

        ctx.fillRect(
            star.x,
            star.y,
            star.size,
            star.size
        );

        star.y += star.speed;

        if (star.y > canvas.height) {
            star.y = 0;
            star.x = Math.random() * canvas.width;
        }

    }
}


// ======================
// 우주선 그리기
// ======================

function drawShip() {

    ctx.save();

    ctx.translate(
        ship.x + ship.width / 2,
        ship.y + ship.height / 2
    );


    // 엔진 불꽃

    ctx.beginPath();

    ctx.moveTo(-10, 18);
    ctx.lineTo(0, 30 + Math.random() * 8);
    ctx.lineTo(10, 18);

    ctx.fillStyle = "#f59e0b";
    ctx.fill();


    // 우주선 몸체

    ctx.beginPath();

    ctx.moveTo(0, -22);
    ctx.lineTo(-22, 20);
    ctx.lineTo(0, 12);
    ctx.lineTo(22, 20);
    ctx.closePath();

    ctx.fillStyle = "#60a5fa";
    ctx.fill();

    ctx.strokeStyle = "#dbeafe";
    ctx.lineWidth = 2;
    ctx.stroke();


    // 창문

    ctx.beginPath();

    ctx.arc(0, -5, 7, 0, Math.PI * 2);

    ctx.fillStyle = "#e0f2fe";
    ctx.fill();

    ctx.strokeStyle = "#1e3a8a";
    ctx.stroke();


    ctx.restore();
}


// ======================
// 운석 생성
// ======================

function createMeteor() {

    let size = Math.random() * 22 + 18;

    meteors.push({

        x: Math.random() * (canvas.width - size),

        y: -size,

        size: size,

        speed:
            3 +
            Math.random() * 2 +
            score / 500

    });

}


// ======================
// 운석 그리기
// ======================

function drawMeteors() {

    for (let meteor of meteors) {

        ctx.beginPath();

        ctx.arc(
            meteor.x + meteor.size / 2,
            meteor.y + meteor.size / 2,
            meteor.size / 2,
            0,
            Math.PI * 2
        );

        ctx.fillStyle = "#78716c";
        ctx.fill();

        ctx.strokeStyle = "#a8a29e";
        ctx.lineWidth = 2;
        ctx.stroke();


        // 운석의 작은 구멍

        ctx.beginPath();

        ctx.arc(
            meteor.x + meteor.size * 0.35,
            meteor.y + meteor.size * 0.35,
            meteor.size * 0.12,
            0,
            Math.PI * 2
        );

        ctx.fillStyle = "#44403c";
        ctx.fill();


        ctx.beginPath();

        ctx.arc(
            meteor.x + meteor.size * 0.7,
            meteor.y + meteor.size * 0.65,
            meteor.size * 0.1,
            0,
            Math.PI * 2
        );

        ctx.fillStyle = "#44403c";
        ctx.fill();

    }
}


// ======================
// 운석 이동
// ======================

function moveMeteors() {

    for (let i = meteors.length - 1; i >= 0; i--) {

        let meteor = meteors[i];

        meteor.y += meteor.speed;


        // 화면 밖으로 나가면 점수 증가

        if (meteor.y > canvas.height) {

            meteors.splice(i, 1);

            score++;

            scoreText.textContent = score;
        }

    }

}


// ======================
// 충돌 검사
// ======================

function checkCollision() {

    for (let i = meteors.length - 1; i >= 0; i--) {

        let meteor = meteors[i];


        if (
            ship.x < meteor.x + meteor.size &&
            ship.x + ship.width > meteor.x &&
            ship.y < meteor.y + meteor.size &&
            ship.y + ship.height > meteor.y
        ) {

            meteors.splice(i, 1);

            lives--;

            livesText.textContent = lives;


            // 충돌 후 잠깐 무적 효과

            ship.x = canvas.width / 2 - ship.width / 2;


            if (lives <= 0) {

                gameOver = true;

            }

        }

    }

}


// ======================
// 우주선 이동
// ======================

function moveShip() {

    if (leftPressed) {
        ship.x -= ship.speed;
    }

    if (rightPressed) {
        ship.x += ship.speed;
    }


    // 화면 밖으로 못 나가게

    if (ship.x < 0) {
        ship.x = 0;
    }

    if (ship.x + ship.width > canvas.width) {
        ship.x = canvas.width - ship.width;
    }

}


// ======================
// 게임 오버 화면
// ======================

function drawGameOver() {

    if (!gameOver)
        return;


    ctx.fillStyle = "rgba(0,0,0,0.75)";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    ctx.textAlign = "center";

    ctx.fillStyle = "white";

    ctx.font = "bold 40px Arial";

    ctx.fillText(
        "GAME OVER",
        canvas.width / 2,
        canvas.height / 2 - 30
    );


    ctx.font = "22px Arial";

    ctx.fillText(
        "최종 점수: " + score,
        canvas.width / 2,
        canvas.height / 2 + 15
    );

}


// ======================
// 키보드 조작
// ======================

document.addEventListener("keydown", function(e) {

    if (e.key === "ArrowLeft") {

        leftPressed = true;

        e.preventDefault();

    }


    if (e.key === "ArrowRight") {

        rightPressed = true;

        e.preventDefault();

    }

});


document.addEventListener("keyup", function(e) {

    if (e.key === "ArrowLeft") {
        leftPressed = false;
    }

    if (e.key === "ArrowRight") {
        rightPressed = false;
    }

});


// ======================
// 게임 재시작
// ======================

function restartGame() {

    score = 0;

    lives = 3;

    meteors = [];

    gameOver = false;


    scoreText.textContent = score;

    livesText.textContent = lives;


    ship.x =
        canvas.width / 2 -
        ship.width / 2;

}


// ======================
// 메인 게임 루프
// ======================

let meteorTimer = 0;

function gameLoop() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    drawStars();


    if (!gameOver) {

        moveShip();

        drawShip();

        meteorTimer++;

        // 시간이 지날수록 운석이 자주 등장

        let spawnRate =
            Math.max(18, 55 - score / 2);


        if (meteorTimer >= spawnRate) {

            createMeteor();

            meteorTimer = 0;

        }


        moveMeteors();

        drawMeteors();

        checkCollision();

    } else {

        drawShip();

        drawMeteors();

    }


    drawGameOver();


    requestAnimationFrame(gameLoop);

}


// 시작

createStars();

gameLoop();

</script>

</body>
</html>
"""

components.html(game, height=650)
