import React, { Component } from 'react';
import './Navbar.css';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';
import { FaSearch } from 'react-icons/fa';
import { MdPersonOutline } from 'react-icons/md';
import { useAuthContext } from '../../Context/AuthContext';
import { useClientContext } from '../../Context/ClientContext';

function NavbarComponent(props) {
    const { token, setToken } = useAuthContext();
    const { clientId, setClientId } = useClientContext();

    const logoutHandler = async () => {
        await setToken(null);
        await setClientId(null);
        await localStorage.setItem('authToken', null);
        await localStorage.setItem('clientId', null);
        props.history.push('/login')
    }

    return (
        <Navbar bg="white" expand="lg" style={{ boxShadow: '0 15px 40px -30px' }}>
            <Navbar.Brand className="logo" onClick={() => { props.history.push('/'); }}>MBOA Services</Navbar.Brand>
            <Navbar.Brand>{props.name}</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse bg="white" id="basic-navbar-nav">
                <Nav className="ml-auto">
                    <Nav.Link className="navlink" onClick={() => { props.history.push('/search'); }}><FaSearch />&nbsp;Search</Nav.Link>
                    {/* <Nav.Link className="navlink" href="#link"><MdLocalOffer />&nbsp;Offers</Nav.Link> */}
                    {token !== null ?
                        <NavDropdown style={{ marginTop: "3px", color: "#52be80" }} title="Temporary User" id="basic-nav-dropdown">
                            {/* <NavDropdown.Item onClick={() => { this.props.history.push("/orders") }}><BsFillPersonFill />&nbsp;Profile</NavDropdown.Item> */}
                            <NavDropdown.Item onClick={() => { props.history.push("/orders") }}>Orders</NavDropdown.Item>
                            <NavDropdown.Item onClick={() => { props.history.push("/cart") }}>Cart</NavDropdown.Item>
                            <NavDropdown.Divider />
                            <NavDropdown.Item onClick={logoutHandler}>Logout</NavDropdown.Item>
                        </NavDropdown> :
                        <Nav.Link className="navlink" onClick={() => { props.history.push('/login') }}><MdPersonOutline size={20} />&nbsp;Login</Nav.Link>
                    }
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    )
}


export default NavbarComponent;