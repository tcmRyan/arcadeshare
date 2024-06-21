import React from "react";
import { Field, Form, Formik, FormikHelpers, FormikProps } from "formik";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../../app/store";
import { Card } from "react-bootstrap";
import { createUser } from "../actions";

interface FormValues {
  roles: number;
  email: string | null;
  username: string;
  password: string;
}

const CreateUserForm = () => {
  const dispatch = useDispatch();
  const admin = useSelector((state: RootState) => state.admin);
  const defaultValues: FormValues = {
    email: "",
    username: "",
    password: "",
    roles: admin.roles[0].id,
  };

  const onSubmit = (values: FormValues, actions: FormikHelpers<FormValues>) => {
    const role = admin.roles.find((role) => role.id === values.roles);
    if (role) {
      dispatch(createUser({ ...values, roles: [role] }));
    }
  };

  let form = null;
  form = (
    <Formik
      initialValues={defaultValues}
      enableReinitialize={true}
      onSubmit={onSubmit}
    >
      {(formikBag: FormikProps<FormValues>) => (
        <Card className="row d-flex justify-content-center align-items-center h-100">
          <Form className="card-body p-5">
            <div className="form-outline mb-4 col-md-6 row">
              <label className="form-label text text-start" htmlFor="username">
                Username
              </label>
              <Field
                id="username"
                className="form-control form-control-md col-md-6"
                name="username"
              />
            </div>
            <div className="form-outline mb-4 col-md-6 row">
              <label
                className="form-label text-start"
                htmlFor="typePasswordX-2"
              >
                Password
              </label>
              <Field
                name="password"
                type="password"
                id="typePasswordX-2"
                className="form-control form-control-md"
              />
            </div>
            <div className="form-outline mb-4 col-md-6 row">
              <label
                className="form-label align-content-md-start text-start"
                htmlFor="email"
              >
                Email
              </label>
              <Field
                id="email"
                className="form-control form-control-md"
                name="email"
                placeholder="Optional Email"
              />
              <div className="form-outline mb-4 col-md-6 row">
                <label
                  className="form-label align-content-md-start text-start"
                  htmlFor="roles"
                >
                  Roles
                </label>
                <Field
                  className="form-control form-control-md"
                  name="roles"
                  as="select"
                >
                  {admin.roles?.map((role, i) => (
                    <option value={role.id} key={i}>
                      {role.name}
                    </option>
                  ))}
                </Field>
              </div>
            </div>
            <button className="btn btn-primary btn-lg btn-block" type="submit">
              Create
            </button>
          </Form>
        </Card>
      )}
    </Formik>
  );

  return <>{form}</>;
};

export default CreateUserForm;
