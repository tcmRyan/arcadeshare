import React, { useState } from "react";
import { Card, Collapse } from "react-bootstrap";
import classes from "./CollapseSection.module.css";
type CollapseSectionProps = {
  title: string;
  children: JSX.Element;
};
const CollapseSection = ({ title, children }: CollapseSectionProps) => {
  const [open, setOpen] = useState(false);

  return (
    <>
      <div className={classes.header} onClick={() => setOpen(!open)}>
        <div className={classes.title}>{title}</div>
        <i className={"fas fa-chevron-circle-" + (open ? "up" : "down")}></i>
      </div>
      <div style={{ minHeight: "150px" }}>
        <Collapse in={open}>
          <Card body>{children}</Card>
        </Collapse>
      </div>
    </>
  );
};

export default CollapseSection;
