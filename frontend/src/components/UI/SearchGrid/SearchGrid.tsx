import { IGame } from "features/Game/gameSlice";
import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine-dark.css";
import { AgGridColumn, AgGridReact } from "ag-grid-react";
import { ICellRendererParams } from "ag-grid-community";
import { useDispatch, useSelector } from "react-redux";
import { addToFeed, updateFeed } from "features/Feeds/actions";
import { RootState } from "app/store";

interface ISearchGrid {
  games: IGame[];
}

const SearchGrid = (props: ISearchGrid) => {
  const dispatch = useDispatch();
  const feedSlice = useSelector((state: RootState) => state.feed);
  const BtnCellRenderer = (params: ICellRendererParams) => {
    const btnHandler = () => {
      if (feedSlice.current) {
        let tempFeed = { ...feedSlice.current };
        let games = [...tempFeed.games];
        games.push(params.data);
        tempFeed.games = games;
        dispatch(updateFeed(tempFeed));
      }
    };
    return <button onClick={btnHandler}>Add</button>;
  };

  const frameworkComponents = {
    BtnCellRenderer: BtnCellRenderer,
  };

  return (
    <div style={{ height: "400px" }}>
      <div className="ag-theme-alpine-dark" style={{ height: "400px" }}>
        <AgGridReact
          rowData={props.games}
          frameworkComponents={frameworkComponents}
        >
          <AgGridColumn field="name" />
          <AgGridColumn field="description" />
          <AgGridColumn field="version" />
          <AgGridColumn
            field="game_uri"
            headerName="Add"
            cellRenderer="BtnCellRenderer"
          />
        </AgGridReact>
      </div>
    </div>
  );
};

export default SearchGrid;
