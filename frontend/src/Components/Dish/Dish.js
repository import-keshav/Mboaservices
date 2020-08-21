import React, { Component } from 'react';
import './Dish.css';
import 'react-confirm-alert/src/react-confirm-alert.css';

import { ClientService } from '../../Services/ClientService';
import { ClientContext } from '../../Context/ClientContext';
import { confirmAlert } from 'react-confirm-alert';

class Dish extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            counterVisible: false,
            addOns: [],
            finalAddOn: []
        };
    }

    componentWillMount() {
        this.setState({ addOns: this.props.addOns });
    }

    componentDidMount() {
        this.setState({ counterVisible: this.props.presentInCart });
    }


    submit = () => {
        confirmAlert({
            title: 'Items already in cart',
            message: 'Your cart contains items from other restaurant. Would you like to reset your cart for adding items from this restaurant?',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => {
                        this.context.setProductCart([]);
                        this.context.setFinalPrice(0, "zero");
                        const params = {
                            client: this.context.clientId,
                            restaurant: this.props.restId,
                            dish: this.props.id,
                            num_of_items: 1,
                            add_ons: [],
                            price: this.props.price
                        }

                        ClientService.clientAddItemToCart(this.context.token, params).then((result) => {
                            console.log(result.data)
                            const contextParams = {
                                client: this.context.clientId,
                                restaurant: this.props.restaurant,
                                dish: this.props.data,
                                num_of_items: 1,
                                id: result.data.id,
                                add_ons: [],
                                price: this.props.price
                            }
                            this.context.addToCart(contextParams);
                            // this.context.setFinalPrice(this.props.price, "add")
                            this.setState({ counterVisible: true });
                        });
                    }
                },
                {
                    label: 'No',
                    onClick: () => console.log("No")
                }
            ]
        });
    };


    buttonHandler = () => {
        const checkParams = {
            client: this.context.clientId,
            restaurant: this.props.restId
        };

        if (this.context.clientId) {
            if (this.context.cartItems.length === 0) {
                const params = {
                    client: this.context.clientId,
                    restaurant: this.props.restId,
                    dish: this.props.id,
                    num_of_items: 1,
                    add_ons: [],
                    price: this.props.price
                }

                ClientService.clientAddItemToCart(this.context.token, params).then((result) => {
                    const contextParams = {
                        client: this.context.clientId,
                        restaurant: this.props.restaurant,
                        dish: this.props.data,
                        num_of_items: 1,
                        id: result.data.id,
                        add_ons: [],
                        price: this.props.price
                    }
                    this.context.addToCart(contextParams);
                    // this.context.setFinalPrice(this.props.price, "add");
                    this.setState({ counterVisible: true });
                });
            }
            else {
                ClientService.checkRestaurantCart(this.context.token, checkParams).then((res) => {
                    if (res.data.is_restaurant_same) {
                        const params = {
                            client: this.context.clientId,
                            restaurant: this.props.restId,
                            dish: this.props.id,
                            num_of_items: 1,
                            add_ons: [],
                            price: this.props.price
                        }

                        ClientService.clientAddItemToCart(this.context.token, params).then((result) => {
                            const contextParams = {
                                client: this.context.clientId,
                                restaurant: this.props.restaurant,
                                dish: this.props.data,
                                num_of_items: 1,
                                id: result.data.id,
                                add_ons: [],
                                price: this.props.price
                            }
                            this.context.addToCart(contextParams);
                            // this.context.setFinalPrice(this.props.price, "add")
                            this.setState({ counterVisible: true });
                        });
                    }
                    else {
                        this.submit();
                    }
                })
            }
        }
        else {
            return this.props.history.push('/login');
        }
    }

    buttonHandlerRemove = () => {
        const data = this.context.cartItems.filter(item => item.dish.id === this.props.id);

        ClientService.deleteItemFromCart(this.context.token, data[0].id).then(() => {
            this.setState({ counterVisible: false });
            this.context.removeFromCart(data[0].id);
        })
    }


    render() {
        return (
            <div className="dish">
                <img className="image" src={this.props.img} alt='dish' />
                <h5 className="name">{this.props.name}</h5>
                <h6 className="description">{this.props.description}</h6>
                <h5 className="price">FCFA {this.props.price}</h5>
                {this.state.counterVisible === false ?
                    <button className="button" onClick={this.buttonHandler}>
                        <span className="btncon">ADD</span>
                    </button> :
                    <>
                        <button className="buttonRemove" onClick={this.buttonHandlerRemove}>
                            <span className="btncon">Remove</span>
                        </button>

                    </>
                }

                {/* <CounterInput
                            min={1}
                            max={10}
                            count={1}
                            onCountChange={count => console.log(count)}
                            inputStyle={{ color: '#52be80', fontWeight: "bold" }}
                            wrapperStyle={{ border: "2px solid #52be80", height: "43px", borderRadius: "10px", width: "108px", fontWeight: "bold", color: "#52be80" }}
                        /> */}

            </div >
        )
    }
}

export default Dish;