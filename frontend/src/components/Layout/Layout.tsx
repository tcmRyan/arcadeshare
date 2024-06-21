import React, { Component, Fragment } from "react";

import ArcadeNav from "../ArcadeNav/ArcadeNav";
import {Spinner} from "react-bootstrap";

class Layout extends Component<any, any>{
    render() {
        let main = <main>{this.props.children}</main>
        if (this.props.loading){
            main = <Spinner animation="border" />
        }

        return (
            <Fragment>
                <ArcadeNav />
                {main}
            </Fragment>
        )

    }
}
export default Layout