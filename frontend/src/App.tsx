import React, { useEffect } from "react";
import "./App.css";
import Home from "@features/Home/Home";
import Auth from "@features/Auth/Auth";
import Layout from "@components/Layout/Layout";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "@app/store";
import { checkState, oauthLogin } from "@features/Auth/actions";
import { Route, Routes } from "react-router-dom";
import Admin from "@features/Admin/Admin";
import Dashboard from "@features/Dashboard/Dashboard";
import Feeds from "@features/Feeds/Feeds";
import Feed from "@features/Feeds/Feed/Feed";
import Game from "@features/Game/Game";

function App() {
  const dispatch = useDispatch();
  const auth = useSelector((state: RootState) => state.auth);

  useEffect(() => {
    if (!auth.authenticated && !auth.checked) {
      dispatch(checkState());
    }

    if (auth.vendorUrl) {
      dispatch(oauthLogin(auth.vendorUrl));
    }
  });

  let routes = (
    <Routes>
      <Route index element={<Home />} />
      <Route path="auth" element={<Auth />} />
      <Route path="admin" element={<Admin />} />
      <Route path="dashboard" element={<Dashboard />}>
        <Route path="games" element={<Game />} />
        <Route path="feeds" element={<Feeds />}>
          <Route path="add" element={<Feed />} />
          <Route path=":feedId" element={<Feed />} />
        </Route>
      </Route>
    </Routes>
  );
  return (
    <div className="App">
      <Layout>{routes}</Layout>
      <p>TEST</p>
    </div>
  );
}

export default App;
