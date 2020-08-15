import React, { Component } from 'react';
import './DishSearch.scss';
import { Link } from 'react-router-dom';
import { ClientContext } from '../../../Context/ClientContext';
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import { ClientService } from '../../../Services/ClientService';

class DishSearch extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            counterVisible: false,
            addOns: []
        };
    }

    componentWillMount() {
        this.setState({ addOns: this.props.addOns });
    }

    componentDidMount() {
        this.setState({ counterVisible: this.props.presentInCart });
    }

    buttonHandler = () => {
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
                price: this.props.price,
                add_ons: []
            }

            ClientService.clientAddItemToCart(this.context.token, params).then((result) => {
                const contextParams = {
                    client: this.context.clientId,
                    restaurant: this.props.restaurant,
                    dish: this.props.data,
                    num_of_items: 1,
                    id: result.data.id,
                    price: this.props.price,
                    add_ons: []
                }
                this.context.addToCart(contextParams);
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
                        price: this.props.price,
                        add_ons: []
                    }

                    ClientService.clientAddItemToCart(this.context.token, params).then((result) => {
                        const contextParams = {
                            client: this.context.clientId,
                            restaurant: this.props.restaurant,
                            dish: this.props.data,
                            num_of_items: 1,
                            id: result.data.id,
                            price: this.props.price,
                            add_ons: []
                        }
                        this.context.addToCart(contextParams);
                        this.setState({ counterVisible: true });
                    });
                }
                else {
                    this.submit();
                }
            })
        }
    }

    buttonHandlerRemove = () => {
        const data = this.context.cartItems.filter(item => item.dish.id === this.props.id);
        console.log(data)
        ClientService.deleteItemFromCart(this.context.token, data[0].id).then(() => {
            this.setState({ counterVisible: false });
            this.context.removeFromCart(data[0].id);
        })
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
                            price: this.props.price,
                            add_ons: []
                        }

                        ClientService.clientAddItemToCart(this.context.token, params).then((result) => {
                            const contextParams = {
                                client: this.context.clientId,
                                restaurant: this.props.restaurant,
                                dish: this.props.data,
                                num_of_items: 1,
                                id: result.data.id,
                                price: this.props.price,
                                add_ons: []
                            }

                            this.context.addToCart(contextParams);
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

    render() {
        let color;
        if (this.props.restaurant.rating >= 0 && this.props.restaurant.rating < 2) {
            color = "#d9534f"
        }
        else if (this.props.restaurant.rating >= 2 && this.props.restaurant.rating < 3.5) {
            color = "#db7c38"
        }
        else {
            color = "#48c479"
        }
        const styles = {
            rating: {
                backgroundColor: color,     //#db7c38 
                width: "48px",
                padding: "0px 5px",
                fontWeight: 400,
                height: "22px",
                display: "inline-block",
                borderBottom: "1px solid #e9e9eb",
                borderRadius: "20px"
            }
        }
        return (
            <div className="dishsearch">
                <div className="restaurantsearch">
                    <Link to={`/restaurant/${this.props.restaurant.id}`}>
                        <p className="name">{this.props.restaurant.name}</p>
                    </Link>
                    <div className="features" style={{ display: "flex", justifyContent: "space-between", marginBottom: "10px" }}>
                        <div className="rating" style={styles.rating}>
                            <img src={require('../../../Assets/star-icon.png')} className="star-icon" alt="star" />
                            <h6 className="rating-value">{this.props.restaurant.rating}</h6>
                        </div>
                        <div style={{ display: "inline-block" }}>•</div>
                        <div className="distance">1km</div>
                        <div style={{ display: "inline-block" }}>•</div>
                        <div className="distance">32 min</div>
                    </div>
                    <div className="offers">
                        <img src={require('../../../Assets/discount.png')} className="discount" alt="discount" />
                        <h5 className="offer-content">20% on all orders</h5>
                    </div>
                </div>
                <div className="row dishsearch">
                    <div className="image">
                        <img className="image" src={this.props.image} alt="dish" />
                    </div>
                    <div className="details">
                        <h5 className="name">{this.props.name}</h5>
                        <h6 className="price">FCFA {this.props.price}</h6>
                    </div>
                    <div className="col-3 counter">
                        {this.state.counterVisible === false ?
                            <button className="button" onClick={this.buttonHandler}>
                                <span className="btncon">ADD</span>
                            </button> :
                            <button className="buttonRemove" onClick={this.buttonHandlerRemove}>
                                <span className="btncon">Remove</span>
                            </button>
                        }
                    </div>
                </div>
            </div>
        )
    }
}

export default DishSearch;