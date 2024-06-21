import { useDispatch, useSelector } from "react-redux";
import { RootState } from "app/store";
import FeedForm from "features/Feeds/Feed/FeedForm/FeedForm";
import GameSearch from "features/Feeds/Feed/GameSearch/GameSearch";
import { AgGridColumn, AgGridReact } from "ag-grid-react";
import { ICellRendererParams } from "ag-grid-community";
import * as actions from "features/Feeds/actions";
import { MouseEvent, useEffect, useState } from "react";
import { Modal } from "react-bootstrap";
import classes from "./Feed.module.css";
import { useParams } from "react-router-dom";

const FeedGameGrid = () => {
  const feedSlice = useSelector((state: RootState) => state.feed);
  const dispatch = useDispatch();
  const BtnCellRenderer = (params: ICellRendererParams) => {
    const btnHandler = () => {
      if (feedSlice.current) {
        let tempFeed = { ...feedSlice.current };
        const games = tempFeed.games.filter(
          (value, index, array) => value.id !== params.data.id
        );
        tempFeed.games = games;
        dispatch(actions.updateFeed(tempFeed));
      }
    };
    return <button onClick={btnHandler}>Remove</button>;
  };
  const frameworkComponents = {
    BtnCellRenderer: BtnCellRenderer,
  };

  return (
    <div style={{ height: "400px" }}>
      <div className="ag-theme-alpine-dark" style={{ height: "400px" }}>
        <AgGridReact
          rowData={feedSlice.current?.games}
          frameworkComponents={frameworkComponents}
        >
          <AgGridColumn field="name" />
          <AgGridColumn field="description" />
          <AgGridColumn field="version" />
          <AgGridColumn field="remove" cellRenderer="BtnCellRenderer" />
        </AgGridReact>
      </div>
    </div>
  );
};
const Feed = () => {
  const feedSlice = useSelector((state: RootState) => state.feed);
  const [showModal, setShowModal] = useState<boolean>(false);
  let { feedId } = useParams();

  useEffect(() => {
    if (feedId && feedSlice.current === null) {
      //fetch data
    }
  }, [feedSlice, feedId]);

  const detailClickHandler = (event: MouseEvent<HTMLDivElement>) => {
    event.preventDefault();
    setShowModal(true);
  };

  const handleClose = () => {
    setShowModal(false);
  };

  let feedPage = <div>BadState</div>;

  if (!feedSlice.loading && feedSlice.current) {
    feedPage = (
      <div>
        <div onClick={detailClickHandler} className={classes.details}>
          <h2>{feedSlice.current.name}</h2>
          <p>{feedSlice.current.description}</p>
        </div>
        <Modal show={showModal} onHide={handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>Edit Details</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <FeedForm onSubmit={handleClose} />
          </Modal.Body>
        </Modal>

        <FeedGameGrid />
        <GameSearch />
      </div>
    );
  }

  return <div>{feedPage}</div>;
};

export default Feed;
