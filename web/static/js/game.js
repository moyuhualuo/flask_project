document.addEventListener("DOMContentLoaded", () => {
  const gameBoard = document.getElementById("game-board");
  const restartButton = document.getElementById("restart-button");
  const scoreElement = document.getElementById("score");
  const bestScoreElement = document.getElementById("best-score");
  const timeElement = document.getElementById("survival-time");
  const bestTimeElement = document.getElementById("best-time");
  const statusElement = document.getElementById("game-status");

  if (!gameBoard) {
    console.error("Game board element not found");
    return;
  }

  const BEST_SCORE_KEY = "moyu-snake-best-score";
  const BEST_TIME_KEY = "moyu-snake-best-time";
  let gameLoop = null;
  let gameOver = false;
  let score = 0;
  let startedAt = Date.now();
  let elapsedSeconds = 0;

  function formatTime(seconds) {
    const minutes = String(Math.floor(seconds / 60)).padStart(2, "0");
    const restSeconds = String(seconds % 60).padStart(2, "0");
    return `${minutes}:${restSeconds}`;
  }

  function readBestScore() {
    return Number(localStorage.getItem(BEST_SCORE_KEY) || 0);
  }

  function readBestTime() {
    return Number(localStorage.getItem(BEST_TIME_KEY) || 0);
  }

  function saveBest() {
    if (score > readBestScore()) {
      localStorage.setItem(BEST_SCORE_KEY, String(score));
    }
    if (elapsedSeconds > readBestTime()) {
      localStorage.setItem(BEST_TIME_KEY, String(elapsedSeconds));
    }
  }

  function updateStats() {
    elapsedSeconds = Math.max(0, Math.floor((Date.now() - startedAt) / 1000));
    scoreElement.textContent = score;
    bestScoreElement.textContent = readBestScore();
    timeElement.textContent = formatTime(elapsedSeconds);
    bestTimeElement.textContent = formatTime(readBestTime());
  }

  function update() {
    updateSnake();
    if (updateFood()) {
      score += 10;
      statusElement.textContent = "吃到食物，继续保持。";
    }
    gameOver = isGameOver();
  }

  function draw() {
    gameBoard.innerHTML = "";
    drawSnake(gameBoard);
    drawFood(gameBoard);
  }

  function isGameOver() {
    return snakeOutofBounds() || snakeIntersectself();
  }

  function endGame() {
    clearInterval(gameLoop);
    saveBest();
    updateStats();
    statusElement.textContent = `游戏结束，最终得分 ${score}，坚持 ${formatTime(elapsedSeconds)}。`;
  }

  function tick() {
    update();
    draw();
    updateStats();
    if (gameOver) {
      endGame();
    }
  }

  function restartGame() {
    clearInterval(gameLoop);
    resetInputDirection();
    resetSnake();
    resetFood();
    score = 0;
    gameOver = false;
    startedAt = Date.now();
    elapsedSeconds = 0;
    statusElement.textContent = "方向键控制移动，吃到方块得分。";
    draw();
    updateStats();
    gameLoop = setInterval(tick, 1000 / SNAKE_SPEED);
  }

  restartButton.addEventListener("click", restartGame);
  window.addEventListener("keydown", (event) => {
    if (event.key === "r" || event.key === "R") {
      restartGame();
    }
  });

  restartGame();
});
