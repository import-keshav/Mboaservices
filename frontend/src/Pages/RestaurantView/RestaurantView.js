import React, { Component, Fragment } from 'react';
import './RestaurantView.scss';
import Navbar from '../../Components/Navbar/Navbar';
import { GrFormSearch } from 'react-icons/all';
import Dish from '../../Components/Dish/Dish';
import { RestaurantService } from '../../Services/RestaurantService';
import { DishService } from '../../Services/DishService';
import CartComp from '../../Components/CartComp/CartComp';
import { ClientContext } from '../../Context/ClientContext';
import Rating from '../../Components/Rating/Rating';
import { apiUrl } from '../../config';
class RestaurantView extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            data: {},
            category: [],
            loading: false,
            selectedCategory: "",
            dishes: {},
            currentDishes: [],
            categoryToggle: false,
            cart: [],
            cartDishes: []
        };
    }


    async componentDidMount() {
        this.setState({ loading: true });
        let selectedCategory = ""
        await RestaurantService.getSpecificRestaurant(this.props.match.params.id).then((res) => {
            selectedCategory = res.data[0].category[0].name;
            this.setState({ data: res.data[0], category: res.data[0].category, selectedCategory: res.data[0].category[0].name, loading: false });
        });

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
            });
            const data = Array.from(cartDishes);
            return this.setState({ dishes: res.data, currentDishes: res.data[selectedCategory], cartDishes: data });
        })
    }

    onCategoryFilter = (name) => {
        this.setState({ currentDishes: this.state.dishes[name], selectedCategory: name, categoryToggle: true });
    }


    onSearchHandler = (event) => {
        this.setState({ categoryToggle: true })
        Object.entries(this.state.dishes).map((dishes) => {
            const currentList = dishes[1];
            const newList = currentList.filter(item => {
                const lc = item.name.toLowerCase();
                const filter = event.target.value.toLowerCase();
                return lc.includes(filter || dishes[0].toLowerCase());
            });
            if (newList.length > 0) {
                return this.setState({ currentDishes: this.state.dishes[dishes[0]], selectedCategory: dishes[0] })
            }
        })
    }

    render() {
        if (this.state.loading) {
            return null;
        }
        return (
            <div className="restaurant-view-desk">
                <Navbar {...this.props} name={this.state.data.name} />
                <div style={{ paddingTop: "100px" }}>
                    <div className="restaurant-info" >
                        <img className="restaurant-img" src={this.state.data.image} alt="restaurant" />
                        <div className="restaurant-details">
                            <h5 className="name">{this.state.data.name}</h5>
                            {this.state.data.is_open ? "" :
                                <div className="unservicable">Restaurant Unservicable</div>
                            }
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
                            <div className="features" style={{ display: "flex", justifyContent: "space-between", marginTop: "20px", marginBottom: "10px", marginLeft: "20px", marginRight: "20px" }}>
                                <div className="rating">
                                    <img src={require('../../Assets/star-icon.png')} className="star-icon" alt="star" />
                                    <h6 className="rating-value">{this.state.data.rating}</h6>
                                </div>
                                <div style={{ display: "inline-block", color: "white", paddingLeft: "50px", paddingRight: "50px" }}>•</div>
                                <div className="distance">
                                    1km
                            </div>
                                <div style={{ display: "inline-block", color: "white", paddingLeft: "50px", paddingRight: "50px" }}>•</div>
                                <div className="distance">32 min</div>
                            </div>
                            <div className="offersdesk">
                                <img src={require('../../Assets/discount.png')} className="discount" alt="discount" />
                                <h5 className="offer-content">20% on all orders</h5>
                            </div>
                            <div className="search-dish">
                                <input className="search" placeholder="Search for some good dish" onChange={this.onSearchHandler} />
                                <div className="search-icon">
                                    <GrFormSearch />
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="container">
                        <div className="row" >
                            <div className="categories col-2">
                                <div className="sidenav">
                                    <ul className="items">
                                        <>
                                            <li className="item" onClick={() => { this.setState({ categoryToggle: false }) }}>{"ALL"}</li>
                                            {
                                                Object.entries(this.state.dishes).map((dishes) => {
                                                    return <Fragment key={dishes[0]}>
                                                        <li key={dishes[0]} className="item" onClick={() => { this.onCategoryFilter(dishes[0]); }}>{dishes[0]}</li>
                                                    </Fragment>
                                                })
                                            }
                                        </>
                                    </ul>
                                </div>
                            </div>
                            {this.state.categoryToggle ?
                                <div className="dishes-view col-8">
                                    <h3 className="category-name">{this.state.selectedCategory} </h3>
                                    <h5 className="category-desc">{this.state.currentDishes ? this.state.currentDishes.length : "0"} dishes available</h5>
                                    <div className="dishes">
                                        {this.state.currentDishes ? this.state.currentDishes.map((indi) => {
                                            return <Dish restaurant={this.state.data} addOns={indi.add_ons} addOnPresent={true} presentInCart={this.state.cartDishes.includes(indi.id)} restId={this.props.match.params.id} data={indi} key={indi.id} id={indi.id} price={indi.price} name={indi.name} img={apiUrl + indi.image} description={indi.description} />
                                        }) : null}
                                    </div>
                                </div> :
                                <div className="dishes-view col-8">
                                    {Object.entries(this.state.dishes).map((dishes) => {
                                        return <Fragment key={dishes[0]}>
                                            <h3 className="category-name">{dishes[0]}</h3>
                                            <h5 className="category-desc">{dishes[1].length} dishes available</h5>
                                            <div className="dishes">
                                                {dishes[1].map((dish) => {
                                                    if (this.state.cart.includes(dish.id)) {
                                                        return <Dish restaurant={this.state.data} addOns={dish.add_ons} addOnPresent={true} presentInCart={this.state.cartDishes.includes(dish.id)} restId={this.props.match.params.id} data={dish} key={dish.id} {...this.props} price={dish.price} name={dish.name} id={dish.id} img={apiUrl + dish.image} description={dish.description} />
                                                    } else {
                                                        return <Dish restaurant={this.state.data} addOns={dish.add_ons} addOnPresent={true} presentInCart={this.state.cartDishes.includes(dish.id)} restId={this.props.match.params.id} data={dish} key={dish.id} {...this.props} price={dish.price} name={dish.name} id={dish.id} img={apiUrl + dish.image} description={dish.description} />
                                                    }
                                                })}
                                            </div>
                                        </Fragment>
                                    })}
                                </div>

                            }
                            <div className="dishes-view col-2">
                                <Rating id={this.props.match.params.id} />
                            </div>
                            {this.context.clientId ?
                                <CartComp {...this.props} cartItemsLength={this.context.cartItems.length} price={0} />
                                : null}
                        </div>
                    </div>
                </div>
            </div >
        )
    }
}

export default RestaurantView;