import React, { Component } from 'react';
import { BsFilter, FiShoppingCart, AiOutlineStar } from 'react-icons/all';
import BackNavbar from '../../../Components/Mobile/BackNavbar/BackNavbar';
import './RestaurantView.css';
import Dish from '../../../Components/Mobile/Dish/Dish';
import { RestaurantService } from '../../../Services/RestaurantService';
import { DishService } from '../../../Services/DishService';
import { Fragment } from 'react';
import { ClientContext } from '../../../Context/ClientContext';
import Rating from '../../../Components/Rating/Rating';
import { apiUrl } from '../../../config';

class BottomToggler extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {

        };
    }


    render() {
        return (
            <div className="bottomtogglebar">
                <div className="details">
                    <div className="text">{this.context.cartItems.length} items | FCFA {this.context.finalPrice}</div>
                </div>
                <div className="cartadd" onClick={() => { this.props.history.push('/cart') }}>View Cart &nbsp; <FiShoppingCart /> </div>
            </div>
        )
    }
}

class RestaurantView extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            visible: false,
            loading: false,
            data: {},
            category: [],
            selectedCategory: "",
            dishes: {},
            categoryToggle: false,
            ratingToggle: false,
            currentDishes: [],
            categoryChosen: false,
            cartItems: [],
            cartDishes: []
        }
    }

    async componentDidMount() {
        this.setState({ loading: true });
        let selectedCategory = ""
        await RestaurantService.getSpecificRestaurant(this.props.match.params.id).then((res) => {
            selectedCategory = res.data[0].category[0].name;
            this.setState({ data: res.data[0], category: res.data[0].category, selectedCategory: res.data[0].category[0].name, loading: false });
        })

        DishService.getDishesByRestaurant(this.props.match.params.id).then((res) => {
            const cartDishes = new Set();
            Object.entries(res.data).map((dishes) => {
                return dishes[1].map((dish) => {
                    return this.context.cartItems.map((cartItem) => {
                        if (cartItem.dish.id === dish.id) {
                            return cartDishes.add(dish.id);
                        }
                        else {
                            return;
                        }
                    })
                })
            })
            const data = Array.from(cartDishes);
            return this.setState({ dishes: res.data, currentDishes: res.data[selectedCategory], cartDishes: data, visible: data.length > 0 ? true : false });
        })
    }

    onToggle = () => {
        this.setState({ visible: true });
    }

    onCategoryFilter = (name) => {
        this.setState({ currentDishes: this.state.dishes[name], selectedCategory: name, categoryChosen: true });
    }

    addToCart = (id) => {
        const ids = [...this.state.cartItems];
        ids.push(id);
        this.setState({ cartItems: ids, visible: true });
    }

    render() {
        let content;
        let color;
        if (this.state.data.rating >= 0 && this.state.data.rating < 2) {
            color = "#d9534f"
        }
        else if (this.state.data.rating >= 2 && this.state.data.rating < 3.5) {
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
        if (this.state.categoryToggle) {
            content = <>
                <h5 className="filter-head">Categories</h5>
                <ul className="categories">
                    <>
                        <li className="item" onClick={() => { this.setState({ categoryChosen: false }) }}>All</li>
                        {
                            Object.keys(this.state.dishes).map((dishes) => {
                                return <li className="item" key={dishes} onClick={() => { this.onCategoryFilter(dishes) }}>{dishes}</li>
                            })
                        }
                    </>
                </ul>
            </>
        }

        if (this.state.ratingToggle) {
            content = <div style={{ marginLeft: "auto", marginRight: "auto" }}>
                <Rating />
            </div>
        }

        if (this.state.loading) {
            return null;
        }

        return (
            <div className="restaurant-view">
                <BackNavbar onBack={() => { this.props.history.goBack() }} heading={this.state.data.name} />
                <div className="restaurant-info">
                    <img src={this.state.data.image} className="image" alt="restaurant" />
                    <h4 className="name">{this.state.data.name}</h4>
                    <h6 className="types">{
                        this.state.category.map((category, index) => {
                            if (index < this.state.category.length - 1) {
                                return category.name + ",";
                            }
                            else {
                                return category.name;
                            }
                        })
                    }</h6>
                </div>
                <div className="features" style={{ display: "flex", justifyContent: "space-between", marginTop: "20px", marginBottom: "10px", marginLeft: "20px", marginRight: "20px" }}>
                    <div className="rating" style={styles.rating}>
                        <img src={require('../../../Assets/star-icon.png')} className="star-icon" alt="star" />
                        <h6 className="rating-value">{this.state.data.rating ? this.state.data.rating : 0}</h6>
                    </div>
                    <div style={{ display: "inline-block" }}>•</div>
                    <div className="distance">1km</div>
                    <div style={{ display: "inline-block" }}>•</div>
                    <div className="distance">32 min</div>
                </div>
                {this.state.data.is_open ? "" :
                    <div className="unservicable">Restaurant Unservicable</div>
                }
                <div className="offers">
                    <img src={require('../../../Assets/discount.png')} className="discount" alt="discount" />
                    <h5 className="offer-content">20% on all orders</h5>
                </div>
                <div className="dishes-view">
                    <div className="dishes-category">
                        <h6 className="dishes-cat" onClick={() => { this.setState({ categoryToggle: !this.state.categoryToggle }) }}><BsFilter size={25} />&nbsp; Sort/Filter </h6>
                        <h6 className="dishes-cat2" onClick={() => { this.setState({ ratingToggle: !this.state.ratingToggle }) }}><AiOutlineStar size={25} />&nbsp; Rate Us </h6>
                    </div>
                    {content}

                    <div className="dishes-list">
                        {!this.state.categoryChosen ? Object.entries(this.state.dishes).map((dishes) => {
                            return <Fragment key={dishes[0]}>
                                <div className="category-name">{dishes[0]}</div>
                                <div className="dishes">
                                    {dishes[1].map((dish) => {
                                        return <Dish restaurant={this.state.data} addOns={dish.add_ons} onToggle={this.onToggle} presentInCart={this.state.cartDishes.includes(dish.id)} restId={this.props.match.params.id} data={dish} key={dish.id} {...this.props} price={dish.price} name={dish.name} id={dish.id} addToCart={() => { this.addToCart(dish.id, dish.name, dish.price) }} img={apiUrl + dish.image} description={dish.description} />
                                    })}
                                </div>
                            </Fragment>
                        }) :
                            <Fragment>
                                <div className="category-name">{this.state.selectedCategory}</div>
                                <div className="dishes">
                                    {this.state.currentDishes.map((dish) => {
                                        return <Dish restaurant={this.state.data} addOns={dish.add_ons} onToggle={() => { this.onToggle() }} presentInCart={this.state.cartDishes.includes(dish.id)} restId={this.props.match.params.id} data={dish} key={dish.id} {...this.props} price={dish.price} name={dish.name} id={dish.id} addToCart={() => { this.addToCart(dish.id, dish.name, dish.price) }} img={apiUrl + dish.image} description={dish.description} />
                                    })}
                                </div>
                            </Fragment>
                        }

                    </div>
                </div>
                {this.state.visible ? <BottomToggler items={this.state.cartItems.length} {...this.props} /> : null}
            </div>
        )
    }
}

export default RestaurantView;