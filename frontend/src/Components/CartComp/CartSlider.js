import React, { Component } from 'react';
import './CartSlider.css';
import { MdShoppingCart } from 'react-icons/md';
import { ClientContext } from '../../Context/ClientContext';
import { Link } from 'react-router-dom';

import CartItem from '../../Components/CartItem/CartItemDesk';


class CartSlider extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            loading: false,
        };
    }


    render() {
        const showHideClassName = this.props.visible ? "cart-slider show" : "cart-slider hide";

        return (
            <div className={showHideClassName}>
                <div className="essential">
                    <MdShoppingCart size={20} />
                    <h5 className="number">{this.props.cartItemsLength} items {this.context.cartItems.length > 0 ? <Link to={`/restaurant/${this.context.cartItems[0].restaurant.id}`}>{"from " + this.context.cartItems[0].restaurant.name}</Link> : ""} </h5>
                    <div className="close" onClick={this.props.handlerOpen}>x</div>
                </div>

                {
                    this.context.cartItems.map((item) => {
                        return <CartItem key={item.id} id={item.id} add_ons={item.dish.add_ons} name={item.dish.name} price={item.dish.price} finalPrice={item.price} num_of_items={item.num_of_items} />
                    })
                }

                {this.context.finalPrice !== 0 ?
                    <div className="checkout" onClick={() => { this.props.history.push('/cart') }}>
                        <span className="checkouttxt">Checkout</span>
                        <div className="checkout-btn">
                            <span className="checkout-btntxt">FCFA {this.context.finalPrice}</span>
                        </div>
                    </div> : null}
            </div>
        )
    }
}

export default CartSlider;