import React, { Component } from 'react';
import './AddressScreen.css';
import CartNavBar from '../../../Components/Mobile/CartNavBar/CartNavbar';
import { ClientContext } from '../../../Context/ClientContext';
import { OrderService } from '../../../Services/OrderService';
import 'react-confirm-alert/src/react-confirm-alert.css';
import PaymentModal from '../../../Components/PaymentModal/PaymentModal';
import MapContainer from '../../../Components/GoogleMap/GoogleMap';

class AddressScreen extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            loading: false,
            formfield: {
                door: "",
                landmark: "",
            },
            mainAddress: "Test Street",
            latitude: null,
            longitude: null,
            payment_modal: false,
        }
    }


    handleClickPaymentOpen = (e) => {
        e.preventDefault();
        this.setState({ payment_modal: true });
    };

    handlePaymentClose = (value) => {
        this.setState({ payment_modal: false });
    };

    inputChangeHandler = (e) => {
        let formfields = { ...this.state.formfield };
        formfields[e.target.name] = e.target.value;
        this.setState({ formfield: formfields });
    }

    createOrder = () => {
        const items = [];
        this.context.cartItems.map((item) => {
            return items.push({ dish: item.dish.id, quantity: item.num_of_items, add_ons: item.add_ons });
        });

        const params = {
            order: {
                restaurant: this.context.restaurant.id,
                client: this.context.clientId,
                payment_method: "Online Payment",
                total_amount: this.props.location.state.finalPrice,
                latitude: this.state.latitude,
                longitude: this.state.longitude,
                client_address_details: this.state.mainAddress + "," + this.state.formfield.door + "," + this.state.formfield.landmark
            },
            dishes: items
        }
        OrderService.createOrder(this.context.clientId, params).then((res) => {
            this.props.history.push('/orders');
            this.context.setProductCart([]);
            this.context.setFinalPrice(0);
        }).catch(err => {
            console.log(err);
        })
    }

    onMarkerDrag = (one, two, three) => {
        const { latLng } = three;
        const lat = latLng.lat();
        const lng = latLng.lng();
        this.setState({ latitude: lat, longitude: lng });
    }

    render() {
        return (
            <div className="addressscreen">
                <CartNavBar heading="Add Address" onBack={() => { this.props.history.goBack() }} />
                <div className="address-form">
                    <h5 className="heading">Save Address</h5>
                    <MapContainer
                        latitude={this.context.latitude}
                        longitude={this.context.longitude}
                        onMarkerDrag={this.onMarkerDrag}
                    />

                    <form className="form-address" onSubmit={this.handleClickPaymentOpen}>
                        <div className="input">
                            <label class="label">Door</label>
                            <input onChange={this.inputChangeHandler} name="door" type="text" className="input-text" placeholder="" />
                        </div>
                        <div className="input">
                            <label class="label">LANDMARK</label>
                            <input onChange={this.inputChangeHandler} name="landmark" type="text" className="input-text" placeholder="" />
                        </div>
                        <button type="submit" className="button">
                            <span className="btncon">Save and Continue</span>
                        </button>
                    </form>
                    <PaymentModal {...this.props} mode="phone" finalPrice={this.props.location.state.finalPrice} createOrder={this.createOrder} open={this.state.payment_modal} onClose={this.handlePaymentClose} />
                </div>
            </div>
        )
    }
}

export default AddressScreen;