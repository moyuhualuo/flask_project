window.onload = () => {
  const gameBoard = document.getElementById("game-board");
  if (!gameBoard) {
    console.error("Game board element not found");
    return;
  }

  let gameOver = false;

  const main = () => {
    update();
    draw();
    if (gameOver) {
      alert("Game Over");
      clearInterval(gameLoop);
    }
  };

  let gameLoop = setInterval(main, 1000 / SNAKE_SPEED);

  const update = () => {
    console.log("Updating");
    updateSnake();
    updateFood();
    gameOver = isGameOver();
  };

  const draw = () => {
    gameBoard.innerHTML = "";
    drawSnake(gameBoard);
    drawFood(gameBoard);
  };

  const isGameOver = () => {
    return snakeOutofBounds() || snakeIntersectself();
  };
};
