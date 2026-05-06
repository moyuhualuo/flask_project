const SNAKE_SPEED = 7;
const START_SNAKE = [
  { x: 11, y: 11 },
  { x: 11, y: 10 },
  { x: 11, y: 9 },
];
const snakeBody = [
  ...START_SNAKE.map((segment) => ({ ...segment })),
];

const updateSnake = () => {
  snakeBody.pop();

  const newHead = { ...snakeBody[0] };
  const snakeDirection = getInputDirection();

  newHead.x += snakeDirection.x;
  newHead.y += snakeDirection.y;

  snakeBody.unshift(newHead);
};

const drawSnake = (gameBoard) => {
  for (let i = 0; i < snakeBody.length; i++) {
    const segment = snakeBody[i];
    const snakeElement = document.createElement("div");
    snakeElement.style.gridRowStart = segment.y;
    snakeElement.style.gridColumnStart = segment.x;
    snakeElement.classList.add("snake");
    if (i === 0) {
      snakeElement.classList.add("snake-head");
    }
    gameBoard.appendChild(snakeElement);
  }
};

const resetSnake = () => {
  snakeBody.splice(0, snakeBody.length, ...START_SNAKE.map((segment) => ({ ...segment })));
};
