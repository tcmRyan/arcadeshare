import React from "react";
import {Container, Nav, Navbar, NavDropdown} from "react-bootstrap";
import NavbarToggle from "react-bootstrap/NavbarToggle";
import {useDispatch, useSelector} from "react-redux";
import {RootState} from "../../app/store";
import {logout} from "../../features/Auth/actions";
import {Link, useNavigate} from "react-router-dom";

const ArcadeNav = () => {
    const auth = useSelector((state: RootState) => state.auth)
    const dispatch = useDispatch()
    const navigate = useNavigate()

    const logoutHandler = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        event.preventDefault()
        dispatch(logout())
    }

    const adminHandler = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        event.preventDefault()
        navigate("/admin")
    }

    let userItem = null

    if (auth.profile) {
        let adminItem = null
        if (auth.profile.user.roles.map(role => role.name).indexOf("admin") >= 0){
            adminItem = (
                <NavDropdown.Item onClick={adminHandler}>Settings</NavDropdown.Item>
            )
        }
        userItem = (
            <NavDropdown title={auth.profile.user.username} id="basic-nav-dropdown">
                {adminItem}
                <NavDropdown.Item onClick={logoutHandler} >Log Out</NavDropdown.Item>
            </NavDropdown>
        )
    } else {
        userItem = <Nav.Link as={Link} to="/auth">Sign In</Nav.Link>
    }

    return (
        <Navbar bg="dark" variant="dark" expand="lg" sticky="top">
            <Container>
                <Navbar.Brand as={Link} to="/">ArcadeShare</Navbar.Brand>
                <NavbarToggle aria-controls="basic-nav-bar-nav"/>
                <Navbar.Collapse id="basic-navbar-nav" >
                </Navbar.Collapse>
                <Nav>
                    {userItem}
                </Nav>
            </Container>
        </Navbar>
    )
}

export default ArcadeNav;