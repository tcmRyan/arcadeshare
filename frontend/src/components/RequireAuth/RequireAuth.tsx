import React from "react";
import { RootState } from "../../app/store";
import { Navigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { useLocation } from "react-router-dom";

const RequireAuth = ({ children }: { children: JSX.Element }) => {
    const auth = useSelector((state: RootState) => state.auth);
    let location = useLocation()

    if(!auth.profile) {
        return <Navigate to={"/auth"} state={{from: location}} replace />
    }

    return children;
}

export default RequireAuth