import React, { useEffect } from "react";
import RequireRole from "../../components/RequireRole/RequireRole";
import CollapseSection from "../../components/UI/CollapseSection/CollapseSection";
import CreateUserForm from "./CreateUserForm/CreateUserForm";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../app/store";
import { getRoles } from "./actions";

const Admin = () => {
  const auth = useSelector((root: RootState) => root.auth);
  const admin = useSelector((root: RootState) => root.admin);
  const dispatch = useDispatch();
  useEffect(() => {
    if (admin.roles.length === 0 && auth.authenticated) {
      dispatch(getRoles());
    }
  });
  let adminPage = null;
  if (admin.roles.length > 0) {
    adminPage = (
      <>
        <div>Admin Page</div>
        <CollapseSection title="Create User">
          <CreateUserForm />
        </CollapseSection>
      </>
    );
  }
  return <RequireRole role="admin">{adminPage}</RequireRole>;
};

export default Admin;
