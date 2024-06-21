import React from "react";
import { Card } from "react-bootstrap";
import { IGame } from "../../gameSlice";
import missing from "../GameThumb/static/missingThumbnail.jpg";

interface thumbProps {
  gameInfo: IGame;
  index: number;
  onClick?: Function;
  selectable?: boolean;
}

const GameThumb = (props: thumbProps) => {
  const onClickHandler = (event: React.MouseEvent<HTMLElement, MouseEvent>) => {
    event.preventDefault();
    if (props.onClick) {
      props.onClick(props.gameInfo);
    }
  };

  return (
    <Card key={props.index} onClick={onClickHandler}>
      <Card.Img
        variant="top"
        src={
          props.gameInfo.thumbnail_uri ? props.gameInfo.thumbnail_uri : missing
        }
      />
      <Card.Body>
        <Card.Title>{props.gameInfo.name}</Card.Title>
        <Card.Text>{props.gameInfo.description}</Card.Text>
      </Card.Body>
    </Card>
  );
};

export default GameThumb;
