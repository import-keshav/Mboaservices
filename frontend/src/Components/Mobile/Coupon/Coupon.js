import React, { Component } from 'react';
import './Coupon.css';
import { RiCouponLine } from 'react-icons/ri';

class Coupon extends Component {
    // constructor(props) {
    //     super(props);
    // }
    render() {
        return (
            <div className="coupon">
                <div className="nameview">
                    <RiCouponLine size={30} />
                    <h4 className="name">{this.props.name}</h4>
                    <h6 className="description">Get {this.props.discount}% discount on {this.props.categories.map((category, index) => {
                        if (index < this.props.categories.length - 1) {
                            return category.name + ",";
                        }
                        else {
                            return category.name;
                        }
                    })} for all orders in this category of the restaurant</h6>
                    <p className="tandc">*Terms and Conditions applied</p>
                </div>
                <button
                    className="apply-button"
                    onClick={() => {
                        this.props.onApplyHandler();
                    }}>
                    <span className="btncon">Apply</span>
                </button>
            </div>
        )
    }
}

export default Coupon;