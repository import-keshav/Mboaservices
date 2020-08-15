import React, { Component } from 'react';
import { GrLocation } from 'react-icons/gr';
import { MdShoppingCart } from 'react-icons/md';
import './OrderDetailScreen.css';
import BackNavbar from '../../../Components/Mobile/BackNavbar/BackNavbar';
import { OrderService } from '../../../Services/OrderService';
import moment from 'moment';
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import ChatModal from '../../../Components/ChatModal/ChatModal';
import { ClientContext } from '../../../Context/ClientContext';
import { InvigilatorContext } from '../../../Context/InvigilatorContext';
import { wsUrl } from '../../../config';

export default class OrderDetailsScreen extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            dishes: [],
            loading: false,
            Client: null,
            restaurant: {},
            invigilator: null,
            status: "Will be updated soon"
        };
    }

    componentWillMount() {
        this.setState({ Client: new W3CWebSocket(`${wsUrl}/orders/get-order-status/${this.props.match.params.id}`) });
    }

    componentDidMount() {
        const { Client } = this.state;
        this.setState({ loading: true });

        Client.onopen = () => {
            console.log('Hey i am interacting');
        }

        Client.onmessage = (message) => {
            this.setState({ status: message.data });
        }

        Client.onerror = (error) => {
            console.log("Connection error: " + error);
        }

        OrderService.getSpecificOrder(this.context.token, this.props.match.params.id)
            .then((order) => {
                this.setState({
                    data: order.data[0],
                    dishes: order.data[0].dishes,
                    restaurant: order.data[0].restaurant,
                    invigilator: order.data[0].invigilator.id,
                    loading: false
                });
            })
    }

    componentWillUnmount() {
        const { Client } = this.state;

        Client.onclose = (data) => {
            console.log(data)
        }
    }

    render() {
        return (
            <InvigilatorContext.Provider
                value={{
                    invigilator: this.state.invigilator,
                    clientId: this.context.clientId,
                    setInvigilator: this.setInvigilator
                }}
            >
                <div className="order-detail-screen" >
                    <BackNavbar {...this.props} onBack={() => { this.props.history.goBack() }} heading={"# " + this.state.data.id} />
                    <div className="essential">
                        <MdShoppingCart size={20} />
                        <h5 className="number"><span style={{ color: '#212121' }}>Order Id</span> #{this.state.data.id}</h5>
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
                                {moment(this.props.delivered_time).format('ddd, MMM DD, YYYY, hh:mm A') === "Invalid Date" ?
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
                        <h6 className="heading" style={{ color: '#52be80', position: "absolute", right: '40px' }}>FCFA {this.state.data.total_amount}</h6>
                    </div>
                    {this.state.invigilator !== null ? <ChatModal order={this.props.match.params.id} /> : null}

                </div >
            </InvigilatorContext.Provider>
        );
    }
}
