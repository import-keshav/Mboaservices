import React, { Component } from 'react';
import './CartItemDesk.css';
import CounterInput from "react-counter-input";

import { ClientContext } from '../../Context/ClientContext';
import { ClientService } from '../../Services/ClientService';
import AddOnModal from '../AddOnModal/AddonModal';

class CartItem extends Component {
    static contextType = ClientContext;

    constructor(props) {
        super(props);
        this.state = {
            count: 1,
            addOnVisible: false,
            addOns: [],
            finalPrice: null
        };
    }

    componentWillMount() {
        this.setState({ addOns: this.props.add_ons, finalPrice: this.props.finalPrice });
    }

    componentDidMount() {
        this.setState({ count: this.props.num_of_items });
    }


    handleAdd = (finalAddOn) => {
        ClientService.updateItemInCart(this.context.token, this.props.id, {
            add_ons: finalAddOn
        }).then((res) => {
            ClientService.getClientCartItemPrice(this.context.token, this.props.id).then((price) => {
                this.setState({ finalPrice: price.data.price });
                this.context.setProductAddOn(this.props.id, price.data.price);
            })
        })
    }

    removeFromCart = () => {
        ClientService.deleteItemFromCart(this.context.token, this.props.id).then((res) => {
            ClientService.getClientPrice(this.context.token, this.context.clientId).then((price) => {
                this.props.setFinalPriceData(price.data.total_price);
                this.context.removeFromCart(this.props.id);
            })
        })
    }

    handleClickOpen = () => {
        this.setState({ addOnVisible: true });
    };

    handleClose = (value) => {
        this.setState({ addOnVisible: false });
    };

    cartUpdateHandler = (count) => {
        const params = {
            num_of_items: count,
            price: this.props.price * count
        };

        ClientService.updateItemInCart(this.context.token, this.props.id, params).then((res) => {
            ClientService.getClientCartItemPrice(this.context.token, this.props.id).then((price) => {
                this.setState({ count: count, finalPrice: price.data.price });
                this.props.setFinalPriceData(price.data.price);
                this.context.setCartProductQuantity(this.props.id, count, price.data.price);
            })
        })
    }

    render() {
        return (
            <div className="cart-it">
                <div className="cart-item-desk">
                    <h5 className="name">{this.props.name}</h5>
                    <div className="counter">
                        <CounterInput
                            min={1}
                            max={10}
                            count={this.props.num_of_items}
                            onCountChange={count => {
                                if (count === 0) {
                                    this.removeFromCart();
                                }
                                this.cartUpdateHandler(count);
                            }}
                            inputStyle={{ color: '#52be80', fontWeight: "bold" }}
                            wrapperStyle={{ border: "2px solid #52be80", height: "43px", borderRadius: "10px", width: "108px", fontWeight: "bold", color: "#52be80" }}
                        />
                    </div>
                    <div className="price">FCFA {this.state.finalPrice}</div>
                    <div className="cross" onClick={this.removeFromCart}>x</div>
                    <AddOnModal handleAdd={this.handleAdd} {...this.props} cartItemId={this.props.id} addOnHandler={this.addOnHandler} addOns={this.state.addOns} open={this.state.addOnVisible} onClose={this.handleClose} />
                </div>

                {this.state.addOns.length > 0 ?
                    <button className="buttonCustomize" onClick={this.handleClickOpen}>
                        <span className="btncon">Customize</span>
                    </button> : null}
            </div>
        )
    }
}

export default CartItem;