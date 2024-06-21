import React, { useEffect, useState } from "react";
import {
  Field,
  Form,
  FieldProps,
  Formik,
  FormikHelpers,
  FormikProps,
} from "formik";
import classes from "../../Auth/Auth.module.css";
import formClasses from "./GameForm.module.css";
import { useAppDispatch } from "../../../app/hooks";
import { cleanGame, createGame, updateGame } from "../actions";
import { useSelector } from "react-redux";
import { RootState } from "../../../app/store";
import missing from "../Games/GameThumb/static/missingThumbnail.jpg";
import Thumbnail from "./Thumbnail/Thumbnail";

export interface GameFormValues {
  id?: number;
  name: string;
  description: string;
  upload?: File | null;
  thumbnail?: File | null;
}

interface GameFormProps {
  toggleForm: Function;
}

const defaultValues: GameFormValues = {
  name: "",
  description: "",
  upload: undefined,
};

interface IFormDisplay {
  title: string;
  submitName: string;
}

const GameForm = (props: GameFormProps) => {
  const [preview, setPreview] = useState<string>(missing);
  const [formDisplay, setFormTitle] = useState<IFormDisplay>();
  const gameSlice = useSelector((state: RootState) => state.game);

  useEffect(() => {
    let thumbnailUri = missing;
    if (gameSlice.game?.id) {
      setFormTitle({ title: "Update Game", submitName: "Update" });
      defaultValues.name = gameSlice.game.name;
      defaultValues.description = gameSlice.game.description;
      defaultValues.id = gameSlice.game.id;
      thumbnailUri = gameSlice.game.thumbnail_uri
        ? gameSlice.game.thumbnail_uri
        : missing;
    } else {
      setFormTitle({ title: "Create Game", submitName: "Create" });
    }
    setPreview(thumbnailUri);
  }, [gameSlice]);

  const dispatch = useAppDispatch();
  const onSubmit = (
    values: GameFormValues,
    actions: FormikHelpers<GameFormValues>
  ) => {
    if (values.id) {
      dispatch(updateGame(values));
    } else {
      dispatch(createGame(values));
    }
    props.toggleForm(false);
  };

  const sectionCls = `vh-100 ${classes.sectionBg}`;
  const cardCls = `card shadow-2-strong ${classes.cardBorder}`;
  const uploadComponent = ({ field, form }: FieldProps) => {
    return (
      <input
        name={field.name}
        type="file"
        onChange={(event) => {
          const files = event.currentTarget.files;
          if (files) {
            form.setFieldValue(field.name, files[0]);
          }
        }}
      />
    );
  };

  const handleCancel = (event: React.MouseEvent<HTMLElement, MouseEvent>) => {
    event.preventDefault();
    dispatch(cleanGame());
  };

  return (
    <div>
      <Formik initialValues={defaultValues} onSubmit={onSubmit}>
        {(formikBag: FormikProps<GameFormValues>) => (
          <section className={sectionCls}>
            <div className={cardCls}>
              <Form className="card-body p-5 text-center">
                <h3 className="mb-5">{formDisplay?.title}</h3>
                <div className="form-outline mb-4">
                  <Field
                    id="thumbnail"
                    name="thumbnail"
                    component={Thumbnail}
                    thumbNailUri={preview}
                  />
                </div>

                <span style={{ minHeight: "20px" }} />

                <div className="form-outline mb-4">
                  <Field
                    id="gameName"
                    className="form-control form-control-lg"
                    name="name"
                  />
                  <label className="form-label" htmlFor="gameName">
                    Game Name
                  </label>
                </div>
                <div className="form-outline mb-4">
                  <Field
                    id="gameDescription"
                    className="form-control form-control-lg"
                    name="description"
                    as="textarea"
                  />
                  <label className="form-label" htmlFor="gameDescription">
                    Description
                  </label>
                </div>
                <div className={formClasses.wrapper}>
                  <div className="form-outline mb-4">
                    <Field
                      id="gameFile"
                      className="form-control form-control-lg"
                      name="upload"
                      component={uploadComponent}
                    />
                    <label className="form-label" htmlFor="gameFile">
                      Game Upload
                    </label>
                  </div>
                </div>

                <div>
                  <button
                    className="btn btn-primary btn-lg btn-block"
                    type="submit"
                  >
                    {formDisplay?.submitName}
                  </button>
                  <button
                    type="button"
                    className="btn btn-lg btn-danger"
                    onClick={handleCancel}
                  >
                    Cancel
                  </button>
                </div>
              </Form>
            </div>
          </section>
        )}
      </Formik>
    </div>
  );
};

export default GameForm;
