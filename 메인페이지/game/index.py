<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lightning Dodger Game</title>
  <style>
    body { margin: 0; overflow: hidden; background: black; }
    canvas { display: block; margin: 0 auto; background: black; }
    #quizModal {
      position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
      background: white; padding: 20px; border-radius: 10px; z-index: 10;
      display: none; width: 300px; text-align: center;
    }
    .btn { margin-top: 10px; display: block; width: 100%; }
    #restartBtn { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 20px; padding: 10px; display: none; }
  </style>
</head>
<body>
  <canvas id="gameCanvas" width="800" height="600"></canvas>
  <div id="quizModal">
    <p><strong>퀴즈:</strong><br>전기는 어떤 입자의 이동으로 발생할까요?</p>
    <button class="btn" onclick="submitAnswer(true)">전자</button>
    <button class="btn" onclick="submitAnswer(false)">양성자</button>
    <button class="btn" onclick="submitAnswer(false)">중성자</button>
    <button class="btn" onclick="submitAnswer(false)">원자핵</button>
  </div>
  <button id="restartBtn" onclick="restartGame()">게임 재시작</button>

  <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const quizModal = document.getElementById("quizModal");
    const restartBtn = document.getElementById("restartBtn");

    const char = { x: 400, y: 300, size: 40 };
    const lightnings = [];
    const lightningCount = 9;
    const quizIcon = { x: Math.random() * 740 + 30, y: -100, size: 40 };
    let score = 0;
    let gameOver = false;
    let quizActive = false;
    let scoreHistory = [];

    document.addEventListener("mousemove", e => {
      const rect = canvas.getBoundingClientRect();
      char.x = e.clientX - rect.left;
      char.y = e.clientY - rect.top;
    });

    function spawnLightning() {
      for (let i = 0; i < lightningCount; i++) {
        lightnings.push({
          x: Math.random() * 740 + 30,
          y: -Math.random() * 600,
          size: 30
        });
      }
    }

    function drawCharacter() {
      ctx.fillStyle = "yellow";
      ctx.beginPath();
      ctx.arc(char.x, char.y, char.size / 2, 0, Math.PI * 2);
      ctx.fill();
    }

    function drawLightning(l) {
      ctx.fillStyle = "white";
      ctx.fillRect(l.x - l.size / 2, l.y, l.size, l.size * 2);
    }

    function drawQuizIcon() {
      ctx.fillStyle = "red";
      ctx.beginPath();
      ctx.arc(quizIcon.x, quizIcon.y, quizIcon.size / 2, 0, Math.PI * 2);
      ctx.fill();
    }

    function updateGame() {
      if (gameOver || quizActive) return;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      drawCharacter();
      drawQuizIcon();
      quizIcon.y += 4;

      if (quizIcon.y > 600) {
        quizIcon.x = Math.random() * 740 + 30;
        quizIcon.y = -100;
      }

      if (collision(char, quizIcon)) {
        showQuiz();
        return;
      }

      for (let l of lightnings) {
        l.y += 8;
        drawLightning(l);
        if (l.y > 600) {
          l.y = -60;
          l.x = Math.random() * 740 + 30;
          score++;
        }
        if (collision(char, l)) {
          endGame();
          return;
        }
      }

      requestAnimationFrame(updateGame);
    }

    function collision(a, b) {
      return Math.abs(a.x - b.x) < 30 && Math.abs(a.y - b.y) < 30;
    }

    function showQuiz() {
      quizActive = true;
      quizModal.style.display = "block";
      setTimeout(() => {
        if (quizActive) {
          quizModal.style.display = "none";
          endGame();
        }
      }, 60000);
    }

    function submitAnswer(correct) {
      quizModal.style.display = "none";
      if (correct) {
        quizActive = false;
        updateGame();
      } else {
        endGame();
      }
    }

    function endGame() {
      gameOver = true;
      scoreHistory.push(score);
      alert("게임 오버! 점수: " + score);
      restartBtn.style.display = "block";
    }

    function restartGame() {
      score = 0;
      gameOver = false;
      quizActive = false;
      lightnings.length = 0;
      quizIcon.y = -100;
      spawnLightning();
      restartBtn.style.display = "none";
      updateGame();
    }

    spawnLightning();
    updateGame();
  </script>
</body>
</html>
