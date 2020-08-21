import React, { Component } from 'react';
import { FiArrowLeft } from 'react-icons/all';
import './BackNavbar.css';

class BackNavbar extends Component {
    // constructor(props) {
    //     super(props);
    // }
    render() {
        return (
            <div className="d-flex backnavbar">
                <button onClick={() => { this.props.onBack() }} className="backButton"><FiArrowLeft /></button>
                <h5 className="heading">{this.props.heading}</h5>
            </div>
        )
    }
}

export default BackNavbar;