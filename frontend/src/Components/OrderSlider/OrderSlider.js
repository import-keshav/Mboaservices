import React, { Component } from 'react';
import './OrderSlider.css';
import { GrLocation } from 'react-icons/gr';
import { MdShoppingCart } from 'react-icons/md';
import moment from 'moment';
import { w3cwebsocket as W3CWebSocket } from 'websocket';

import { ClientContext } from '../../Context/ClientContext';
import { OrderService } from '../../Services/OrderService';
import ChatModal from '../ChatModal/ChatModal';
import { InvigilatorContext } from '../../Context/InvigilatorContext';
import { wsUrl } from '../../config';

class OrderSlider extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            data: {},
            loading: false,
            dishes: [],
            restaurant: {},
            status: "Will be Updated Soon",
            Client: null,
            currentId: null,
            invigilator: null
        };
    }

    componentWillMount() {
        this.setState({ Client: new W3CWebSocket(`${wsUrl}/orders/update-get-order-status/${this.props.currentId}`) });
    }

    componentDidMount() {
        const { Client } = this.state;
        this.setState({ loading: true, currentId: this.props.currentId });
        Client.onopen = () => {
            console.log('Hey i am interacting');
        }

        Client.onmessage = (message) => {
            this.setState({ status: message.data });
        }

        Client.onerror = (error) => {
            console.log("Connection error: " + error);
        }

        OrderService.getSpecificOrder(this.context.token, this.props.currentId).then((order) => {
            this.setState({
                data: order.data[0],
                dishes: order.data[0].dishes,
                restaurant: order.data[0].restaurant,
                invigilator: order.data[0].invigilator.id,
                loading: false
            });
        })
    }

    UNSAFE_componentWillReceiveProps(nextProps) {
        const { Client } = this.state;
        if (nextProps.currentId !== this.state.currentId) {
            this.setState({ loading: true });
            Client.onmessage = (message) => {
                this.setState({ status: message.data });
            }

            Client.onerror = (error) => {
                console.log("Connection error: " + error);
            }

            OrderService.getSpecificOrder(this.context.token, nextProps.currentId).then((order) => {
                this.setState({ data: order.data[0], dishes: order.data[0].dishes, restaurant: order.data[0].restaurant, loading: false });
            })
        }
    }

    componentWillUnmount() {
        const { Client } = this.state;
        Client.onclose = (data) => {
            console.log(data)
        }
    }

    setInvigilator = (data) => {
        this.setState({ invigilator: data });
    }

    render() {
        const showHideClassName = this.props.visible ? "order-slider show" : "order-slider hide";
        // let content = <Link to={`/restaurant/${this.context.cartItems[0].restaurant.id}`}>{this.context.cartItems[0].restaurant.name}</Link>;
        return (
            <InvigilatorContext.Provider
                value={{
                    invigilator: this.state.invigilator,
                    clientId: this.context.clientId,
                    setInvigilator: this.setInvigilator
                }}
            >
                <div className={showHideClassName}>
                    <div className="essential">
                        <MdShoppingCart size={20} />
                        <h5 className="number"><span style={{ color: '#212121' }}>Order Id</span> #{this.props.currentId} </h5>
                        <div className="close" onClick={this.props.handlerOpen}>x</div>
                    </div>
                    <div className="main-status">{this.state.status.toUpperCase()}</div>
                    <div className="restaurant-info">
                        <GrLocation size={25} />
                        <div className="info">
                            <h5 className="name">{this.state.restaurant.name}</h5>
                            <h6 className="address">{this.state.restaurant.address}</h6>
                        </div>
                    </div>
                    <div className="address-info">
                        <GrLocation style={{ height: 25, width: 25 }} />
                        <div className="info">
                            <h5 className="name">Address</h5>
                            <h6 className="address">{this.state.data.client_address_details}</h6>
                        </div>
                    </div>
                    <hr width={"90%"} height={"2px"} />
                    <div className="address">
                        <div className="info">
                            <h6 className="status">
                                {moment(this.state.data.delivered_time).format('ddd, MMM DD, YYYY, hh:mm A') === "Invalid Date" ?
                                    ("Delivered on " + moment(this.state.data.delivered_time).format('ddd, MMM DD, YYYY, hh:mm A')) === "Invalid Date"
                                    : "Will be delivered soon"}
                            </h6>
                        </div>
                    </div>
                    <hr width={"90%"} height={"2px"} />
                    <div className="items">
                        <h6 className="number">{this.state.dishes.length} items</h6>
                        <ul className="items-list">
                            {this.state.dishes.map((item) => {
                                return <li className="item">
                                    <h6 className="name">{item.dish.name} x {item.quantity} </h6>
                                    <h6 className="price">FCFA {item.dish.price * item.quantity}</h6>
                                </li>
                            })}
                        </ul>
                    </div>
                    <hr width={"90%"} height={"2px"} />
                    <div className="bill-details">
                        <h5 className="number">Bill Details</h5>
                        <div className="item-total">
                            <h6 className="heading">Item Total</h6>
                            <h6 className="price">FCFA {this.state.data.total_amount}</h6>
                        </div>
                        <div className="item-total">
                            <h6 className="heading">Coupon Discount</h6>
                            <h6 className="price">FCFA {this.state.data.total_amount}</h6>
                        </div>
                    </div>
                    <hr width={"90%"} height={"2px"} />
                    <div className="total-price">
                        <div>
                            <h6 className="heading-total">Total Price</h6>
                            <p className="mode">Paid via {this.state.data.payment_method}</p>
                        </div>
                        <h6 className="heading" style={{ color: '#52be80' }}>FCFA {this.state.data.total_amount}</h6>
                    </div>
                    {this.state.invigilator !== null ? <ChatModal order={this.props.currentId} /> : null}
                </div>
            </InvigilatorContext.Provider>
        )
    }
}

export default OrderSlider;