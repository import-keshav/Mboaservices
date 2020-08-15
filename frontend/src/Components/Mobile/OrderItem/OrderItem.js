import React, { Component } from 'react';
import './OrderItem.css';
import moment from 'moment';

class OrderItem extends Component {

    render() {
        return (
            <div className="order-item-mob">
                <div className="essential-info">
                    <div className="restaurant-info">
                        <img className="image" src={this.props.restaurant.image} alt="restaurantimage" />
                        <div className="info">
                            <h5 className="name">{this.props.restaurant.name}</h5>
                            <h6 className="address">{this.props.restaurant.address}</h6>
                            <h6 className="order">ORDER #{this.props.id} |  {moment(this.props.created).format('ddd, MMM DD, YYYY,  hh:mm A')}</h6>
                            <h5 className="view-details" onClick={() => { this.props.history.push(`/order/${this.props.id}`) }}>View Details</h5>
                        </div>
                    </div>
                    <div className="status">
                        {moment(this.props.delivered_time).format('ddd, MMM DD, YYYY, hh:mm A') === "Invalid Date" ?
                            ("Delivered on " + moment(this.state.data.delivered_time).format('ddd, MMM DD, YYYY, hh:mm A')) === "Invalid Date"
                            : "Will be delivered soon"}
                    </div>
                </div>
                <hr width={"90%"} height={2} striped />
                <div className="items-info">
                    <div className="items">
                        <h6 style={{ fontSize: "16px" }}>{this.props.dishes.map((item, index) => {
                            if (index < this.props.dishes.length - 1) {
                                return (item.dish.name + " x " + item.quantity + ",")
                            }
                            else {
                                return (item.dish.name + " x " + item.quantity)
                            }
                        })}</h6>
                    </div>
                    <div className="paid">
                        Total Paid: <strong>FCFA {this.props.price}</strong>
                    </div>
                </div>
                <h6 style={{ color: '#52be80' }}>* To view order status click on View Details</h6>
            </div>
        )
    }
}

export default OrderItem;