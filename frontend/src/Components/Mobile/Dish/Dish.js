import React, { Component } from 'react';
import './Dish.css';
import { ClientService } from '../../../Services/ClientService';
import { ClientContext } from '../../../Context/ClientContext';
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import AddOnModal from '../../AddOnModal/AddonModal';

class Dish extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            counterVisible: false,
            addOnVisible: false,
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

    handleClickOpen = () => {
        this.setState({ addOnVisible: true });
    };

    handleClose = (value) => {
        this.setState({ addOnVisible: false });
    }

    addOnHandler = (id) => {
        const data = [...this.state.finalAddOn];
        if (data.includes(id) !== true) {
            data.push(id);
        }
        else {
            const idx = data.findIndex(d => d === id);
            data.splice(idx, 1);
        }
        this.setState({ finalAddOn: data });
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
                            const contextParams = {
                                client: this.context.clientId,
                                restaurant: this.props.restaurant,
                                dish: this.props.data,
                                num_of_items: 1,
                                id: result.data.id,
                                add_ons: this.state.finalAddOn,
                                price: this.props.price
                            }
                            this.props.onToggle();

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
        if (this.context.clientId) {
            const checkParams = {
                client: this.context.clientId,
                restaurant: this.props.restId
            };
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
                    this.props.onToggle();
                    this.context.addToCart(contextParams);
                    // this.context.setFinalPrice(this.props.price, "add")
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
                            this.props.onToggle();
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
        } else {
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
            <div className="dishmob">
                <img className="image" src={this.props.img} alt="dish" />
                <h5 className="name">{this.props.name}</h5>
                <h6 className="description">{this.props.description}</h6>
                <h6 className="price">FCFA {this.props.price}</h6>
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
                <AddOnModal {...this.props} addOnHandler={this.addOnHandler} addOns={this.state.addOns} open={this.state.addOnVisible} onClose={this.handleClose} />
            </div>
        )
    }
}

export default Dish;