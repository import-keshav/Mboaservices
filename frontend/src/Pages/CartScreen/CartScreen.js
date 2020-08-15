import React, { Component } from 'react';
import './CartScreen.css';
import NavBar from '../../Components/Navbar/Navbar';
import { BsFillPersonFill, TiLocation, MdPayment, RiSecurePaymentLine, AiOutlineRight, IoIosRemoveCircleOutline } from 'react-icons/all';
import CartItem from '../../Components/CartItem/CartItemDesk';
import { ClientService } from '../../Services/ClientService';
import { ClientContext } from '../../Context/ClientContext';
import CouponSlider from '../../Components/CouponSlider/CouponSlider';
import AddressSlider from '../../Components/AddressSlider/AddressSlider';
import { OrderService } from '../../Services/OrderService';
import PaymentModal from '../../Components/PaymentModal/PaymentModal';
import Button from '@material-ui/core/Button';


class CartScreen extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            clientData: {},
            cartItems: [],
            coupon_active: false,
            restaurant: {},
            addressSlider: false,
            address: [],
            payment_modal: false,
            service: null,
            Client: null,
            finalPrice: null,
            discount_applied: false,
        };
    }

    componentWillMount() {
        this.setState({
            finalPrice: this.context.finalPrice
        })
    }


    handleClickPaymentOpenOrange = () => {
        this.setState({ payment_modal: true, service: "ORANGE" });
    };

    handleClickPaymentOpenMTN = () => {
        this.setState({ payment_modal: true, service: "MTN" });
    }

    handlePaymentClose = (value) => {
        this.setState({ payment_modal: false });
    };

    handlerOpen = (e) => {
        e.stopPropagation();
        this.setState({ coupon_active: !this.state.coupon_active });
    }

    handlerOpen1 = () => {
        this.setState({ coupon_active: true })
    }

    handlerOpenAddress = () => {
        this.setState({ addressSlider: !this.state.addressSlider });
    }

    handlerOpen1Address = () => {
        this.setState({ addressSlider: true })
    }

    addressHandler = (params) => {
        const data = [...this.state.address];
        data.push(params);

        this.setState({ address: data, addressSlider: false });
    }


    componentDidMount() {
        ClientService.getSpecificClient(this.context.token, this.context.clientId).then((client) => {
            this.setState({ clientData: client.data[0].user });
        });
        ClientService.getClientCart(this.context.token, this.context.clientId).then((res) => {
            if (res.data.length > 0) {
                let finalPrice = 0;
                res.data.map((item) => {
                    finalPrice += item.price;
                })
                this.setState({
                    cartItems: res.data,
                    finalPrice: finalPrice,
                });
            }
        }).then((res) => {
        })
    }

    setCoordinates = (lat, lng) => {
        this.setState({ latitude: lat, longitude: lng });
    }

    createOrder = () => {
        const items = [];
        this.context.cartItems.map((item) => {
            return items.push({ dish: item.dish.id, quantity: item.num_of_items, add_ons: item.add_ons });
        });

        if (this.state.address.length > 0) {
            const params = {
                order: {
                    restaurant: this.context.restaurant.id,
                    client: this.context.clientId,
                    payment_method: "Online Payment",
                    total_amount: this.state.finalPrice,
                    latitude: this.state.address[this.state.address.length - 1].latitude,
                    longitude: this.state.address[this.state.address.length - 1].longitude,
                    client_address_details: this.state.address[this.state.address.length - 1].door + "," + this.state.address[this.state.address.length - 1].landmark
                },
                dishes: items,
            }
            console.log(params)
            OrderService.createOrder(this.context.token, params)
                .then((res) => {
                    this.props.history.push('/orders');
                    this.context.setProductCart([]);
                    this.context.setFinalPrice(0);
                })
        }
        else {
            this.handlerOpenAddress();
        }
    }

    orangeMoney = () => {
    }

    mtnMoney = () => {
        this.setState({ service: "MTN" });
    }

    discountApply = (percentage) => {
        const { finalPrice } = this.state;
        this.setState({
            finalPrice: finalPrice - (percentage / 100 * finalPrice),
            discount_applied: true,
            coupon_active: false
        });
    }

    removeCouponHandler = () => {
        const { finalPrice } = this.context;
        this.setState({
            finalPrice: finalPrice,
            discount_applied: false,
        });
    }

    setFinalPriceData = (data) => {
        this.setState({ finalPrice: data });
    }

    render() {
        let content;
        if (this.state.coupon_active) {
            content = <CouponSlider
                {...this.props}
                restId={this.context.restaurant.id}
                visible={this.state.coupon_active}
                discountApply={this.discountApply}
                handlerOpen1={this.handlerOpen1}
                handlerOpen={this.handlerOpen} />
        }

        if (this.state.addressSlider) {
            content = <AddressSlider
                addressHandler={(data) => { this.addressHandler(data) }}
                {...this.props}
                restId={this.context.restaurant.id}
                visible={this.state.addressSlider}
                handlerOpen1={this.handlerOpen1Address}
                handlerOpen={this.handlerOpenAddress} />
        }
        return (
            <div className="cartscreen">
                <NavBar name="Cart" {...this.props} />
                <div className="App-header" style={{ paddingTop: "75px" }}>
                    <div className="container">
                        <div className="row" style={{ marginTop: '50px', marginBottom: '50px' }}>
                            <div className="col-8">
                                <div className="profile">
                                    <div className="profile-icon">
                                        <BsFillPersonFill />
                                    </div>
                                    <h4 className="name">{this.state.clientData.name}</h4>
                                    <h6 className="text">{this.state.clientData.mobile}</h6>
                                    <h6 className="text">{this.state.clientData.email}</h6>
                                </div>
                                <div className="delivery">
                                    <div className="profile-icon">
                                        <TiLocation />
                                    </div>
                                    <h4 className="heading">Add a delivery address</h4>
                                    <h6 className="text">We will try our best to serve you faster</h6>
                                    {this.state.address.length === 0 ?
                                        <div className="button-order" onClick={() => { this.setState({ addressSlider: true }) }}>
                                            <span className="btn-con">Add Address</span>
                                        </div> :
                                        <>
                                            <div className="address-data">
                                                <h6 className="main">Test Address</h6>
                                                <h6 className="door">{this.state.address[this.state.address.length - 1].door}</h6>
                                                <h6 className="landmark">{this.state.address[this.state.address.length - 1].landmark}</h6>
                                            </div>
                                            <div className="change" onClick={() => { this.setState({ addressSlider: true }) }}>Change</div>
                                        </>}
                                </div>
                                <div className="payment">
                                    <div className="profile-icon">
                                        <MdPayment />
                                    </div>
                                    <h4 className="heading">Payment</h4>
                                    <h5 className="pay-amount" style={{ color: "#52be80" }}>Pay {this.state.finalPrice}</h5>
                                    <h6>Choose your payment method</h6>
                                    <div className="payment-modes">
                                        <Button className="mode1" onClick={this.handleClickPaymentOpenOrange}>
                                            <img src={require('../../Assets/orange_money.jpg')} alt="orange-money" className="payment-image" />
                                        </Button>
                                        <Button className="mode2" onClick={this.handleClickPaymentOpenMTN}>
                                            <img src={require('../../Assets/momo.jpg')} alt="mtn-money" className="payment-image" />
                                        </Button>
                                    </div>
                                </div>
                                <PaymentModal {...this.props} service={this.state.service} finalPrice={this.state.finalPrice} createOrder={this.createOrder} open={this.state.payment_modal} onClose={this.handlePaymentClose} />
                                <div className="disclaimer">
                                    <div className="profile-icon">
                                        <RiSecurePaymentLine />
                                    </div>
                                    <h6 className="heading">Please ensure that your address and order details are correct. There can be a delivery charge to keep our delivery partners happy</h6>
                                </div>
                            </div>
                            <div className="col-4 cart-side">
                                <div className="rest-profile">
                                    <img src={this.context.restaurant.image} className="rest-img" alt="restaurant" />
                                    <h6 className="heading" onClick={() => { this.props.history.push(`/restaurant/${this.context.restaurant.id} `) }}>{this.context.restaurant.name}</h6>
                                    <h6 className="address">{this.context.restaurant.address}</h6>
                                </div>
                                <hr width="80%" />
                                <div className="cart-items">
                                    {this.context.cartItems.map((item) => {
                                        return <CartItem
                                            key={item.id}
                                            id={item.id}
                                            add_ons={item.dish.add_ons}
                                            setFinalPriceData={this.setFinalPriceData}
                                            name={item.dish.name}
                                            finalPrice={item.price}
                                            price={item.dish.price}
                                            num_of_items={item.num_of_items} />
                                    })}

                                </div>
                                {this.state.discount_applied ?
                                    <div className="apply-coupon">
                                        <img src={require('../../Assets/discount.png')} className="discount" alt="discount" />
                                        <h5 className="text">Discount Applied</h5>
                                        <div className="arrow" onClick={this.removeCouponHandler}>
                                            <IoIosRemoveCircleOutline />
                                        </div>
                                    </div> :
                                    <div className="apply-coupon" onClick={this.handlerOpen}>
                                        <img src={require('../../Assets/discount.png')} className="discount" alt="discount" />
                                        <h5 className="text">APPLY COUPON</h5>
                                        <div className="arrow" >
                                            <AiOutlineRight />
                                        </div>
                                    </div>}
                                {content}
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
                            </div>
                        </div>
                    </div>
                </div>
            </div >
        )
    }
}

export default CartScreen;