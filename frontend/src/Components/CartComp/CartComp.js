import React, { Component } from 'react';
import './CartComp.css';
import { MdShoppingCart } from 'react-icons/md';
import CartSlider from './CartSlider';
import { ClientContext } from '../../Context/ClientContext';

class CartComp extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            active: false
        };
        this.handlerOpen = this.handlerOpen.bind(this);
    }


    handlerOpen = (e) => {
        e.stopPropagation();
        this.setState({ active: !this.state.active });
    }


    handlerOpen1 = () => {
        this.setState({ active: true })
    }


    render() {
        let content;
        if (this.state.active) {
            content = <CartSlider
                {...this.props}
                visible={this.state.active}
                handlerOpen1={this.handlerOpen1}
                handlerOpen={this.handlerOpen}
            />
        }
        return (
            <div className="cart-comp" onClick={() => { this.setState({ active: true }) }} >
                <div className="info">
                    <MdShoppingCart size={20} />
                    <h5 className="number">{this.context.cartItems.length} items</h5>
                </div>
                <div className="pricetag">
                    <h5 className="price">FCFA {this.context.finalPrice}</h5>
                </div>
                {content}
            </div>
        )
    }
}

export default CartComp;