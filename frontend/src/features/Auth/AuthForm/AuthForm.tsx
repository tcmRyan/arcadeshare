import React, { MouseEvent, useEffect } from "react";
import { Field, Form, Formik, FormikHelpers, FormikProps } from "formik";
import google_signin from "../img/btn_google_signin_dark_normal_web.png";
import ms_signin from "../img/ms-symbollockup_signin_dark.svg";
import { useAppDispatch } from "../../../app/hooks";
import { useSelector } from "react-redux";
import { RootState } from "../../../app/store";
import { useNavigate } from "react-router-dom";
import { basicLogin } from "../actions";
import classes from "../Auth.module.css";

interface FormValues {
  username: string;
  password: string;
}

const defaultValues: FormValues = {
  username: "",
  password: "",
};

const AuthForm = () => {
  const dispatch = useAppDispatch();
  const auth = useSelector((state: RootState) => state.auth);
  const navigate = useNavigate();
  useEffect(() => {
    if (auth.authenticated) {
      navigate("/");
    }
  });
  const onSubmit = (values: FormValues, actions: FormikHelpers<FormValues>) => {
    dispatch(basicLogin(values.username, values.password));
  };
  const sectionCls = `vh-100 ${classes.sectionBg}`;
  const cardCls = `card shadow-2-strong ${classes.cardBorder}`;
  const oauthHandler = (event: MouseEvent) => {
    event.preventDefault();
  };
  return (
    <Formik initialValues={defaultValues} onSubmit={onSubmit}>
      {(formikBag: FormikProps<FormValues>) => (
        <section className={sectionCls}>
          <div className="container py-5 h-100">
            <div className="row d-flex justify-content-center align-items-center h-100">
              <div className="col-12 col-md-8 col-lg-6 col-xl-5">
                <div className={cardCls}>
                  <Form className="card-body p-5 text-center">
                    <h3 className="mb-5">Sign in</h3>

                    <div className="form-outline mb-4">
                      <Field
                        id="typeEmailX-2"
                        className="form-control form-control-lg"
                        name="username"
                      />
                      <label className="form-label" htmlFor="typeEmailX-2">
                        Username or Email
                      </label>
                    </div>

                    <div className="form-outline mb-4">
                      <Field
                        name="password"
                        type="password"
                        id="typePasswordX-2"
                        className="form-control form-control-lg"
                      />
                      <label className="form-label" htmlFor="typePasswordX-2">
                        Password
                      </label>
                    </div>

                    <div className="form-check d-flex justify-content-start mb-4">
                      <input
                        className="form-check-input"
                        type="checkbox"
                        value=""
                        id="form1Example3"
                      />
                      <label
                        className="form-check-label"
                        htmlFor="form1Example3"
                      >
                        {" "}
                        Remember password{" "}
                      </label>
                    </div>

                    <button
                      className="btn btn-primary btn-lg btn-block"
                      type="submit"
                    >
                      Login
                    </button>

                    <hr className="my-4" />

                    <button onClick={oauthHandler} value="/login/google">
                      <img src={google_signin} alt={"Sign in with Google"} />
                    </button>
                    <button onClick={oauthHandler} value="/login/microsoft">
                      <img src={ms_signin} alt="Sign in with Microsoft" />
                    </button>
                  </Form>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}
    </Formik>
  );
};

export default AuthForm;
