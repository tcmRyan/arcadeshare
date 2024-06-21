import React from "react";
import { RootState } from "../../app/store";
import { Navigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { useLocation } from "react-router-dom";

type RequireRoleProps = {
  role: string;
  children: JSX.Element | null;
};

const RequireRole = ({ role, children }: RequireRoleProps) => {
  const auth = useSelector((state: RootState) => state.auth);
  let location = useLocation();

  if (!auth.profile) {
    return <Navigate to={"/auth"} state={{ from: location }} replace />;
  }

  if (auth.profile.user.roles.map((role) => role.name).indexOf(role) === -1) {
    return <Navigate to={"/home"} state={{ from: location }} replace />;
  }

  return children;
};

export default RequireRole;
