import React, { Component } from 'react';
import './SearchScreen.css';
import BottomNavPhone from '../../../Components/Mobile/BottomBar/BottomBar';
import { RestaurantService } from '../../../Services/RestaurantService';
import Restaurant from '../../../Components/Mobile/Restaurant/Restaurant';
import { DishService } from '../../../Services/DishService';
import DishSearch from '../../../Components/Mobile/DishSearch/DishSearch';
import { DebounceInput } from 'react-debounce-input';
import { ClientContext } from '../../../Context/ClientContext';

class SearchScreen extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            selectedTab: "Restaurant",
            restaurants: [],
            searched: false,
            dishes: []
        };

    }


    restaurantSearcHandler = (event) => {
        RestaurantService.getRestaurants(event.target.value).then((restaurants) => {
            this.setState({ restaurants: restaurants.data, searched: true });
        })
    }

    dishChangeHandler = (event) => {
        DishService.getDishBySearch(event.target.value).then((dishes) => {
            this.setState({ dishes: dishes.data, searched: true })
        })
    }

    render() {
        return (
            <div className="searchscreen">
                <h4 className="search-tab" onClick={() => { this.setState({ selectedTab: "Restaurant" }) }}>Restaurant</h4>
                <h4 className="search-tab" onClick={() => { this.setState({ selectedTab: "Dish" }) }}>Dish</h4>
                {this.state.selectedTab === "Restaurant" ?
                    <DebounceInput
                        minLength={2}
                        debounceTimeout={200}
                        placeholder="Search for Restaurant all around you"
                        onChange={this.restaurantSearcHandler} /> :
                    <DebounceInput
                        minLength={2}
                        debounceTimeout={200}
                        placeholder="Search for your favourite Dishes"
                        onChange={this.dishChangeHandler} />}
                <div className="content">
                    {this.state.selectedTab === "Restaurant" ?
                        (this.state.restaurants.length > 0 ? this.state.restaurants.map((item) => {
                            return <Restaurant key={item.id} {...this.props} id={item.id} name={item.name} categories={item.category} rating={item.rating} src={item.image} />
                        }) : <h6 style={{ textAlign: "center" }}>{this.state.searched ? "Sorry! No Restaurant available." : null}</h6>) :
                        (this.state.dishes.length > 0 ? this.state.dishes.map((item) => {
                            return <DishSearch presentInCart={this.context.cartItems.filter(item1 => item1.dish.id === item.id).length > 0 ? true : false} restId={item.restaurant.id} id={item.id} data={item} key={item.id} name={item.name} description={item.description} price={item.price} image={item.image} restaurant={item.restaurant} />
                        }) : <h6 style={{ textAlign: "center" }}>{this.state.searched ? "Sorry! No Dish available." : null}</h6>)
                    }
                </div>
                <BottomNavPhone {...this.props} />
            </div>
        )
    }
}

export default SearchScreen;