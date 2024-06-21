import RequireAuth from "../../components/RequireAuth/RequireAuth";
import { Link, Outlet } from "react-router-dom";

const Dashboard = () => {
  return (
    <div>
      <RequireAuth>
        <div>
          <Link to={"/dashboard/games"}>Games </Link>
          <Link to={"/dashboard/feeds"}>Feeds </Link>
          <Outlet />
        </div>
      </RequireAuth>
    </div>
  );
};

export default Dashboard;
