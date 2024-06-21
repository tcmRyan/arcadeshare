import React, { useEffect, useState } from "react";
import GameForm from "./GameForm/GameForm";
import Games from "./Games/Games";
import { RootState } from "../../app/store";
import { useDispatch, useSelector } from "react-redux";
import { Button, Container } from "react-bootstrap";
import { gameActions, IGame } from "./gameSlice";
import classes from "./Game.module.css";

const Game = () => {
  const [editView, setEditView] = useState<boolean>(false);
  const gameSlice = useSelector((state: RootState) => state.game);
  const dispatch = useDispatch();

  useEffect(() => {
    if (gameSlice.game) {
      setEditView(true);
    } else {
      setEditView(false);
    }
  }, [gameSlice.game]);

  const content = editView ? <GameForm toggleForm={setEditView} /> : <Games />;
  const createGameHandler = (
    event: React.MouseEvent<HTMLElement, MouseEvent>
  ) => {
    event.preventDefault();
    let newGame = {} as IGame;
    dispatch(gameActions.selectGame(newGame));
    setEditView(true);
  };

  return (
    <Container>
      <div className={classes.gamesHeader}>
        <h2 className={classes.title}>My Games</h2>
        <Button className={classes.button} onClick={createGameHandler}>
          Create Game
        </Button>
      </div>

      {content}
    </Container>
  );
};

export default Game;
