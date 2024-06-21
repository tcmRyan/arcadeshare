import React, { useCallback, useEffect, useRef } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "app/store";
import * as actions from "features/Feeds/actions";
import { AgGridColumn, AgGridReact } from "ag-grid-react";
import { AgGridReact as AgGridReactType } from "ag-grid-react/lib/agGridReact";

const Feeds = () => {
  const navigate = useNavigate();
  const authSlice = useSelector((state: RootState) => state.auth);
  const feedSlice = useSelector((state: RootState) => state.feed);
  const dispatch = useDispatch();
  const gridApiRef = useRef<AgGridReactType>(null);
  let location = useLocation();

  useEffect(() => {
    if (location.pathname === "/dashboard/feeds" && feedSlice.current) {
      dispatch(actions.setCurrentFeed(null));
    }
    if (!feedSlice.loaded && !feedSlice.loading) {
      dispatch(actions.fetchFeeds());
    }
  });

  const DEFAULT_FEED_NAME = "My Feed";
  const DEFAULT_FEED_DESC = "A new game feed";

  const createGame = () => {
    if (authSlice.profile) {
      dispatch(
        actions.createFeed({
          description: DEFAULT_FEED_DESC,
          owner_id: authSlice.profile?.user.id,
          name: DEFAULT_FEED_NAME,
          games: [],
        })
      );
    }
    navigate("add");
  };

  let page = null;
  const onSelectionChanged = useCallback(() => {
    if (gridApiRef.current) {
      const selectedRows = gridApiRef.current.api.getSelectedRows();
      dispatch(actions.setCurrentFeed(selectedRows[0]));
      navigate(`${selectedRows[0].id}`);
    }
  }, [navigate, dispatch]);

  if (feedSlice.current) {
    page = <Outlet />;
  } else {
    page = (
      <div>
        <button onClick={createGame}>Create Feed</button>
        <div style={{ height: "400px" }}>
          <div className="ag-theme-alpine-dark" style={{ height: "400px" }}>
            <AgGridReact
              ref={gridApiRef}
              rowData={feedSlice.feeds}
              rowSelection="single"
              onSelectionChanged={onSelectionChanged}
            >
              <AgGridColumn field="name" />
              <AgGridColumn field="description" />
            </AgGridReact>
          </div>
        </div>
        <Outlet />
      </div>
    );
  }

  return <div>{page}</div>;
};

export default Feeds;
