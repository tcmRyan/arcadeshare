import { useDispatch, useSelector } from "react-redux";
import { RootState } from "app/store";
import React, { useEffect, useState } from "react";
import { createFeed, updateFeed } from "features/Feeds/actions";
import { Field, Form, Formik, FormikHelpers, FormikProps } from "formik";

export interface FeedFormValues {
  id?: number;
  name: string;
  description: string;
  owner_id: number;
}

interface IFormDisplay {
  loaded: boolean;
}

const defaultValues: FeedFormValues = {
  name: "",
  description: "",
  owner_id: 0,
};

interface IFeedFormProps {
  onSubmit: Function;
}

const FeedForm = (props: IFeedFormProps) => {
  const authSlice = useSelector((state: RootState) => state.auth);
  const feedSlice = useSelector((state: RootState) => state.feed);
  const [formDisplay, setFormDisplay] = useState<IFormDisplay>();
  const dispatch = useDispatch();

  useEffect(() => {
    if (!formDisplay?.loaded) {
      setFormDisplay({
        loaded: true,
      });
      if (feedSlice.current) {
        if (feedSlice.current.id) {
          defaultValues.id = feedSlice.current.id;
        }
        defaultValues.name = feedSlice.current.name;
        defaultValues.description = feedSlice.current.description;
        defaultValues.owner_id = feedSlice.current.owner_id;
      }
    }
  }, [formDisplay, authSlice, dispatch, feedSlice]);

  const onSubmit = (
    values: FeedFormValues,
    actions: FormikHelpers<FeedFormValues>
  ) => {
    if (values.id) {
      if (feedSlice.current) {
        const feed = { ...values, games: feedSlice.current.games };
        dispatch(updateFeed(feed));
      }
    } else {
      dispatch(createFeed({ ...values, games: [] }));
    }
    props.onSubmit();
  };

  return (
    <div>
      <Formik initialValues={defaultValues} onSubmit={onSubmit}>
        {(formikBag: FormikProps<FeedFormValues>) => (
          <section className={"tbd"}>
            <div>
              <Form style={{ backgroundColor: "black" }}>
                <div>
                  <label htmlFor="feedName"> Feed Name </label>
                  <Field id="feedName" name="name" />
                </div>
                <div>
                  <label htmlFor="feedDescription">Description</label>
                  <Field id="feedDescription" name="description" />
                </div>
                <button
                  className="btn btn-primary btn-lg btn-block"
                  type="submit"
                >
                  Update Details
                </button>
              </Form>
            </div>
          </section>
        )}
      </Formik>
    </div>
  );
};

export default FeedForm;
