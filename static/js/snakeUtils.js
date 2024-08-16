const GRID_SIZE = 21;

const onSnake = (position) => {
  for (let i = 0; i < snakeBody.length; i++) {
    if (equalPositions(position, snakeBody[i])) {
      return true;
    }
  }
  return false;
};

const equalPositions = (pos1, pos2) => {
  return pos1.x === pos2.x && pos1.y === pos2.y;
};

const growSnake = () => {
  snakeBody.push({ ...snakeBody[snakeBody.length - 1] });
};

const getNewFoodPosition = () => {
  let randowFoodPosition = randomGridPosition();
  while (onSnake(randowFoodPosition)) {
    randowFoodPosition = randomGridPosition();
  }
  return randowFoodPosition;
};

const randomGridPosition = () => {
  return {
    x: Math.floor(Math.random() * GRID_SIZE) + 1,
    y: Math.floor(Math.random() * GRID_SIZE) + 1,
  };
};

const OutofBounds = (position) => {
  return (
    position.x < 1 ||
    position.x > GRID_SIZE ||
    position.y < 1 ||
    position.y > GRID_SIZE
  );
};

const snakeOutofBounds = (position) => {
  return OutofBounds(snakeBody[0]);
};

const snakeIntersectself = () => {
  for (let i = 1; i < snakeBody.length; i++) {
    if (equalPositions(snakeBody[0], snakeBody[i])) {
      return true;
    }
  }
  return false;
};
