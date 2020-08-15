import { IoMdSearch, MdPersonOutline, TiHomeOutline, FaShoppingCart, FiShoppingBag } from "react-icons/all";
import React from "react";
import { Link } from 'react-router-dom';
import './BottomBar.scss';

const BottomNavPhone = (props) => {
    return <section className="bottom-navigation position-fixed">
        <div className="holder d-flex align-items-center justify-content-around">
            <div className="nav-option" onClick={() => { props.history.push('/') }}>
                <TiHomeOutline />
                <p className="nav-name">Home</p>
            </div>

            <div className="nav-option" onClick={() => { props.history.push('/cart') }}>
                <FaShoppingCart />
                <p className="nav-name">Cart</p>
            </div>

            <div className="nav-option center" onClick={() => { props.history.push('/search') }}>
                <div className="position-absolute">
                    <IoMdSearch className="search-icon" />
                    <p className="nav-name-search">Search</p>
                </div>
            </div>


            <div className="nav-option" onClick={() => { props.history.push('/orders') }}>
                <FiShoppingBag />
                <p className="nav-name">Orders</p>
            </div>

            <Link to='/account' onClick={() => { props.history.push('/account') }}>
                <div className="nav-option">
                    <MdPersonOutline />
                    <p className="nav-name">Profile</p>
                </div>
            </Link>
        </div>
    </section>
}

export default BottomNavPhone;
