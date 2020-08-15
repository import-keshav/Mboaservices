import React, { Component } from 'react';
import './SearchScreen.css';
import Navbar from '../../Components/Navbar/Navbar';
import { DishService } from '../../Services/DishService';
import { RestaurantService } from '../../Services/RestaurantService';
import { GrSearch } from 'react-icons/gr';
import Restaurant from '../../Components/Restaurant/Restaurant';
import { DebounceInput } from 'react-debounce-input';
import DishSearch from '../../Components/Mobile/DishSearch/DishSearch';
import CartComp from '../../Components/CartComp/CartComp';
import { ClientContext } from '../../Context/ClientContext';
import Skeleton from '@material-ui/lab/Skeleton';

const SkeletonStructure = () => {
    return (
        <div className="row">
            {
                Array(9)
                    .fill()
                    .map((item, index) => (
                        <div className="col-xs-12 col-sm-9 col-md-6 col-lg-4" key={index}>
                            <Skeleton height={180} />
                            <h4 className="card-title">
                                <Skeleton circle={true} height={50} width={50} /> &nbsp;
                            <Skeleton height={36} width={`80%`} />
                            </h4>
                            <p className="card-channel">
                                <Skeleton width={`60%`} />
                            </p>
                            <div className="card-metrics">
                                <Skeleton width={`90%`} />
                            </div>
                        </div>
                    ))
            }
        </div>
    )
}

const SkeletonStructure1 = () => {
    return (
        <>
            {
                Array(9)
                    .fill()
                    .map((item, index) => (
                        <>
                            <Skeleton height={180} width={"100%"} />
                            <Skeleton circle={true} height={50} width={"100%"} /> &nbsp;
                            <Skeleton height={36} width={`80%`} />
                            <Skeleton width={`100%`} />
                            <Skeleton width={`100%`} />
                        </>
                    ))
            }
        </>
    )
}


class SearchScreen extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            selectedTab: "Restaurant",
            restaurants: [],
            searched: false,
            dishes: [],
            responseText: "",
            loading: false
        };
    }

    restaurantSearcHandler = async (event) => {
        this.setState({ loading: true });
        await RestaurantService.getRestaurants(event.target.value).then((restaurants) => {
            this.setState({ restaurants: restaurants.data, searched: true, loading: false });
        })
    }

    dishChangeHandler = (event) => {
        this.setState({ loading: true });
        DishService.getDishBySearch(event.target.value).then((dishes) => {
            this.setState({ dishes: dishes.data, searched: true, loading: false })
        })
    }

    render() {
        let options = this.state.restaurants.map(item => {
            return <div className="col-xs-12 col-sm-9 col-md-6 col-lg-4 restaurant-card">
                <Restaurant key={item.id} {...this.props} id={item.id} name={item.name} categories={item.category} src={item.image} rating={item.rating} />
            </div>
        })

        let options1 = this.state.dishes.map(item => {
            return <DishSearch presentInCart={this.context.cartItems.filter(item1 => item1.dish.id === item.id).length > 0 ? true : false} restId={item.restaurant.id} addOns={item.add_ons} key={item.id} id={item.id} data={item} name={item.name} description={item.description} price={item.price} image={item.image} restaurant={item.restaurant} />
        })

        if (this.state.loading) {
            options = <SkeletonStructure />
            options1 = <SkeletonStructure1 />
        }



        let content;
        if (this.state.selectedTab === "Restaurant") {
            content = <>
                {this.state.searched ? <h5 style={{ textAlign: 'center', alignContent: "center" }}>{this.state.restaurants.length > 0 ? `${this.state.restaurants.length} restaurants found.` : "No restaurants found."}</h5> : null}
                <div className="row">
                    {options}
                </div>
            </>
        }
        else {
            content = <>
                {this.state.searched ? <h5 style={{ textAlign: 'center', alignContent: "center" }}>{this.state.dishes.length > 0 ? `${this.state.dishes.length} dishes found.` : "No dishes found."}</h5> : null}
                <div className="row">
                    {options1}
                </div>
            </>
        }
        return (
            <div className="search-screen-desk">
                <Navbar name="Search" {...this.props} />

                <div className="container">
                    <div className="search">
                        <div className="search-tabs">
                            <h4 className="search-tab1" onClick={() => { this.setState({ selectedTab: "Restaurant" }) }}>Restaurant</h4>
                            <h4 className="search-tab2" onClick={() => { this.setState({ selectedTab: "Dish" }) }}>Dish</h4>
                        </div>
                        <GrSearch size={35} className="searchicon" />
                        {this.state.selectedTab === "Restaurant" ?
                            <DebounceInput
                                className="search-desk"
                                minLength={2}
                                debounceTimeout={200}
                                placeholder="Search for Restaurant all around you"
                                onChange={this.restaurantSearcHandler} /> :
                            <DebounceInput
                                className="search-desk"
                                minLength={2}
                                debounceTimeout={200}
                                placeholder="Search for your favourite Dishes"
                                onChange={this.dishChangeHandler} />}

                        {content}
                    </div>
                </div>
                {this.context.clientId ?
                    <CartComp {...this.props} cartItemsLength={this.context.cartItems.length} price={0} />
                    : null}
            </div>
        )
    }
}

export default SearchScreen;