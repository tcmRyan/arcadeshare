import { FieldProps } from "formik";
import React, { ChangeEvent, useEffect, useState } from "react";
import formClasses from "../GameForm.module.css";
import missing from "../../Games/GameThumb/static/missingThumbnail.jpg";

interface IThumbnailProps extends FieldProps {
  thumbNailUri: string;
}

const Thumbnail = ({ form, field, thumbNailUri }: IThumbnailProps) => {
  const [selectedFile, setSelectedFile] = useState<File>();
  const [preview, setPreview] = useState<string>(missing);
  thumbNailUri = thumbNailUri ? thumbNailUri : missing;

  useEffect(() => {
    if (!selectedFile) {
      setPreview(thumbNailUri);
      return;
    }
    const objectUrl = URL.createObjectURL(selectedFile);
    setPreview(objectUrl);
    return () => URL.revokeObjectURL(objectUrl);
  }, [selectedFile, thumbNailUri]);

  const clickHandler = (event: ChangeEvent<HTMLInputElement>) => {
    const files = event.currentTarget.files;
    if (!files || files.length === 0) {
      form.setFieldValue(field.name, missing);
      return;
    }

    setSelectedFile(files[0]);
    form.setFieldValue(field.name, files[0]);
  };

  return (
    <div className={formClasses.wrapper}>
      <img
        src={preview}
        alt="Game Thumbnail"
        className={formClasses.uploadImg}
      />

      <input
        type="file"
        alt="Game Thumbnail"
        accept="image/*"
        onChange={clickHandler}
        className={formClasses.hidden}
      />
    </div>
  );
};

export default Thumbnail;
