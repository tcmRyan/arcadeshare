import React, { useEffect } from "react";
import GameThumb from "./GameThumb/GameThumb";
import { useAppDispatch } from "../../../app/hooks";
import { useSelector } from "react-redux";
import { RootState } from "../../../app/store";
import { fetchGames, selectGame } from "../actions";
import { Col, Row } from "react-bootstrap";
import { IGame } from "../gameSlice";

const Games = () => {
  const dispatch = useAppDispatch();
  const gameState = useSelector((state: RootState) => state.game);
  const columnsPerRow = 4;

  useEffect(() => {
    if (!gameState.loading && !gameState.loaded) {
      dispatch(fetchGames());
    }
  });

  const editGame = (gameInfo: IGame) => {
    dispatch(selectGame(gameInfo));
  };

  const getColumnsForRow = () => {
    let items = gameState.games.map((game, index) => {
      return (
        <Col key={index}>
          <GameThumb gameInfo={game} index={index} onClick={editGame} />
        </Col>
      );
    });
    return items;
  };
  return (
    <Row xs={1} md={columnsPerRow}>
      {getColumnsForRow()}
    </Row>
  );
};

export default Games;
