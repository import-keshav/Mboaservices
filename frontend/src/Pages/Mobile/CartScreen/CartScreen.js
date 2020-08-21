import React, { Component } from 'react';
import './CartScreen.css';
import CartNavbar from '../../../Components/Mobile/CartNavBar/CartNavbar';
import CartItem from '../../../Components/Mobile/CartItem/CartItem';
import { AiOutlineRight } from 'react-icons/ai';
import { FcTodoList } from 'react-icons/fc';
import { IoIosRemoveCircleOutline } from 'react-icons/io';
import { ClientContext } from '../../../Context/ClientContext';
import CouponModal from '../../../Components/Mobile/CouponModal/CouponModal';
import { ClientService } from '../../../Services/ClientService';

class CartScreen extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            discount_applied: false,
            finalPrice: 0,
            modal_open: false,
            restaurantId: null,
            cartItems: []
        }
    }

    handleOpen = () => {
        this.setState({ modal_open: true });
    };

    handleClose = () => {
        this.setState({ modal_open: false });
    };

    componentDidMount() {
        ClientService.getClientCart(this.context.token, this.context.clientId).then((res) => {
            if (res.data.length > 0) {
                let finalPrice = 0;
                res.data.map((item) => {
                    finalPrice += item.price;
                })
                this.setState({
                    cartItems: res.data,
                    finalPrice: finalPrice,
                    restaurantId: res.data[0].restaurant.id
                });
            }
        }).then((res) => {
        })
    }

    setFinalPriceData = (data) => {
        this.setState({ finalPrice: data });
    }

    discountApply = (percentage) => {
        const { finalPrice } = this.state;
        this.setState({
            finalPrice: finalPrice - (percentage / 100 * finalPrice),
            discount_applied: true,
            modal_open: false
        });
    }

    removeCouponHandler = () => {
        const { finalPrice } = this.context;
        this.setState({
            finalPrice: finalPrice,
        });
    }

    render() {
        return (
            <div className="cartscreenmob" >
                <CartNavbar heading={this.context.restaurant.name + `${'(' + this.context.cartItems.length + ' items)'}`} items={2} onBack={() => { this.props.history.goBack() }} />
                <div className="cart-items">
                    {this.context.cartItems.length > 0 ? this.context.cartItems.map((item) => {
                        return <CartItem
                            key={item.id}
                            id={item.id}
                            add_ons={item.dish.add_ons}
                            name={item.dish.name}
                            finalPrice={item.price}
                            price={item.dish.price}
                            setFinalPriceData={this.setFinalPriceData}
                            num_of_items={item.num_of_items} />
                    }) : <h6 style={{ textAlign: "center" }}>No items found in cart</h6>}
                </div>
                {!this.state.discount_applied ?
                    <div className="apply-coupon" onClick={this.handleOpen}>
                        <img src={require('../../../Assets/discount.png')} className="discount" alt="discount" />
                        <h5 className="text">APPLY COUPON</h5>
                        <div className="arrow">
                            <AiOutlineRight />
                        </div>
                    </div> :
                    <div className="apply-coupon">
                        <img src={require('../../../Assets/discount.png')} className="discount" alt="discount" />
                        <h5 className="text">Discount Applied</h5>
                        <div className="arrow" onClick={this.removeCouponHandler}>
                            <IoIosRemoveCircleOutline />
                        </div>
                    </div>
                }
                {
                    this.state.restaurantId !== null ?
                        <CouponModal
                            restaurantId={this.state.restaurantId}
                            open={this.state.modal_open}
                            discountApply={this.discountApply}
                            onClose={this.handleClose} />
                        : null
                }
                <hr width="100%" color="grey" />
                <div className="payment-details">
                    <h6 className="main-text">Bill Details</h6>
                    <div className="price-details">
                        <h6 className="text">Item Total</h6>
                        <h6 className="price">FCFA {this.state.finalPrice}</h6>
                    </div>

                    <hr width="80%" color="grey" height="2px" />
                    <div className="price-details">
                        <h6 className="texttotal">Total Price</h6>
                        <h6 className="pricetotal">FCFA {this.state.finalPrice}</h6>
                    </div>
                </div>
                <div className="essential-details">
                    <div className="icon">
                        <FcTodoList size={25} />
                    </div>
                    <h6 className="text">
                        Please ensure your address and order details are correct. A cancellation fee will be applicable post 1 minute of placing your order.
                    </h6>
                </div>
                <button className="button" onClick={() => {
                    this.props.history.push('/address', {
                        finalPrice: this.state.finalPrice
                    });
                }}>
                    <span className="btncon">Add Address To Pay</span>
                </button>
            </div>
        )
    }
}

export default CartScreen;