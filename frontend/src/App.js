import React, { useState, useEffect } from 'react';
import './App.css';
import {
    BrowserRouter,
    Route,
    Switch,
} from "react-router-dom";
import axios from 'axios';
import { createMuiTheme } from '@material-ui/core/styles';
import { ThemeProvider } from '@material-ui/core/styles';
import { CSSTransition, TransitionGroup } from 'react-transition-group';


//Desktop Views
import HomePage from './Pages/HomePage/HomePage';
import SignInPage from './Pages/SignInPage/SignInPage';
import SignUpPage from './Pages/SignUpPage/SignUpPage';
import RestaurantViewDesk from './Pages/RestaurantView/RestaurantView';
import CartScreenDesk from './Pages/CartScreen/CartScreen';
import SearchScreenDesk from './Pages/SearchScreen/SearchScreen';
import OrdersPage from './Pages/OrderScreen/OrderScreen';


//Mobile Views
import HomePageMobile from './Pages/Mobile/Homepage/Homepage';
import RestaurantView from './Pages/Mobile/RestaurantView/RestaurantView';
import CartScreen from './Pages/Mobile/CartScreen/CartScreen';
import CouponScreen from './Pages/Mobile/CouponScreen/CouponScreen';
import AddressScreen from './Pages/Mobile/AddressScreen/AddressScreen';
import SearchScreen from './Pages/Mobile/SearchScreen/SearchScreen';
import AccountScreen from './Pages/Mobile/AccountScreen/AccountScreen';
import OrderScreen from './Pages/Mobile/OrdersScreen/OrderScreen';
import OrderDetailsScreen from './Pages/Mobile/OrderDetailScreen/OrderDetailScreen';
// import PrivateRoute from './PrivateRoutes';

//Context
import { ClientContext } from './Context/ClientContext';
import { AuthContext } from './Context/AuthContext';

//Services
import { ClientService } from './Services/ClientService';
import { usePosition } from './Hooks/usePosition';

import PrivateRoute from './PrivateRoutes';


const theme = createMuiTheme({
    palette: {
        primary: {
            main: "#52be80",
            color: "white"
        },
        secondary: {
            main: '#f44336',
        },
    },
});

function App({ watch, settings }) {
    let tokens = localStorage.getItem("authToken");
    tokens = tokens === "null" ? JSON.parse(tokens) : tokens;
    let client = localStorage.getItem('clientId');
    client = client === "null" ? JSON.parse(client) : client;

    const [authToken, setAuthToken] = useState(tokens);
    const [clientId, setClientId] = useState(client);
    const [cartItems, setCartItems] = useState([]);
    const [finalPrice, setFinalPrice] = useState(0);
    const [restaurant, setRestaurant] = useState({});
    const { latitude, longitude, error } = usePosition(watch, settings);

    useEffect(() => {
        if (tokens) {
            axios.defaults.headers.common['Authorization'] = `Bearer ` + tokens;
            ClientService.getClientCart(tokens, clientId).then((cart) => {
                let finalPrice = 0;
                cart.data.map((cartItem) => {
                    return finalPrice += cartItem.price;
                });
                setCartItems(cart.data);
                setFinalPrice(finalPrice);
                setRestaurant(cart.data.length > 0 ? cart.data[0].restaurant : {});
            })
        }
        else {
            console.log(tokens);
            axios.defaults.headers.common['Authorization'] = null;
        }
    }, [tokens]);

    const setTokens = (data) => {
        localStorage.setItem("authToken", JSON.stringify(data));
        setAuthToken(data);
    }

    const setClient = (data) => {
        localStorage.setItem("clientId", JSON.stringify(data));
        setClientId(data);
        ClientService.getClientCart(tokens, data).then((cart) => {
            let finalPrice = 0;
            cart.data.map((cartItem) => {
                return finalPrice += cartItem.price;
            });
            setCartItems(cart.data);
            setFinalPrice(finalPrice);
            setRestaurant(cart.data.length > 0 ? cart.data[0].restaurant : {});
        })
    }

    const addToCart = (item) => {
        let data = [...cartItems];
        data.push(item);
        setCartItems(data);
        setRestaurant(item.restaurant);
        setFinalPriceHandler(item.price, "add");
    };

    const setFinalPriceHandler = (value, operation) => {
        let price = finalPrice;
        if (operation === "add") {
            price += value;
        }
        else if (operation === "sub") {
            price -= value;
        }
        else {
            price = value;
        }
        setFinalPrice(price);
    }

    const removeFromCart = (id) => {
        let data = [...cartItems];
        const index = data.findIndex(item => item.id === id);
        const filterData = data.filter(item => item.id === id);
        const price = filterData[0].price;
        data.splice(index, 1);
        setCartItems(data);
        setFinalPriceHandler(price, "sub");
    };

    const setProductCartQuantity = (id, quantity, price) => {
        let data = [...cartItems];
        const filterData = data.filter(item => item.id === id)[0];
        const index = data.findIndex(item => item.id === id);
        data[index] = { ...filterData, num_of_items: quantity, price: price };
        let finalPrice = 0;
        data.map((indi) => {
            return finalPrice += indi.price;
        });
        setCartItems(data);
        setFinalPrice(finalPrice);
    }

    const setProductAddOn = (id, price) => {
        let data = [...cartItems];
        const filterData = data.filter(item => item.id === id)[0];
        const index = data.findIndex(item => item.id === id);
        data[index] = { ...filterData, price: price };
        let finalPrice = 0;
        data.map((item) => {
            return finalPrice += item.price;
        });
        setCartItems(data);
        setFinalPrice(finalPrice);
    }

    return (
        <ThemeProvider theme={theme}>
            {/* Context Provider */}
            <AuthContext.Provider value={{ token: authToken, setToken: setTokens }}>
                <ClientContext.Provider value={{
                    token: authToken,
                    clientId: clientId,
                    latitude: latitude,
                    longitude: longitude,
                    cartItems: cartItems,
                    finalPrice: finalPrice,
                    restaurant: restaurant,
                    setToken: setTokens,
                    setClientId: setClient,
                    addToCart: addToCart,
                    removeFromCart: removeFromCart,
                    setFinalPrice: setFinalPrice,
                    setCartProductQuantity: setProductCartQuantity,
                    setProductCart: setCartItems,
                    setRestaurant: setRestaurant,
                    setProductAddOn: setProductAddOn
                }}>
                    <BrowserRouter>
                        <div className="App desktop-view">
                            <Route render={({ location }) => (
                                <TransitionGroup>
                                    <CSSTransition key={location.key} timeout={400} classNames="fade">
                                        <Switch>
                                            <Route exact path="/" component={HomePage} />
                                            <Route exact path="/search" component={SearchScreenDesk} />
                                            <Route exact path='/login' component={SignInPage} />
                                            <Route exact path='/signup' component={SignUpPage} />
                                            <Route exact path='/restaurant/:id' component={RestaurantViewDesk} />
                                            <PrivateRoute exact path='/cart' component={CartScreenDesk} />
                                            <PrivateRoute exact path='/orders' component={OrdersPage} />
                                        </Switch>
                                    </CSSTransition>
                                </TransitionGroup>
                            )} />
                        </div>
                        <div className="App phone-view">
                            <Route render={({ location }) => (
                                <TransitionGroup>
                                    <CSSTransition key={location.key} timeout={400} classNames="fade">
                                        <Switch>
                                            <Route exact path="/" component={HomePageMobile} />
                                            <Route exact path='/login' component={SignInPage} />
                                            <Route exact path='/signup' component={SignUpPage} />
                                            <Route exact path="/restaurant/:id" component={RestaurantView} />
                                            <Route exact path="/coupon/:id" component={CouponScreen} />
                                            <Route exact path="/search" component={SearchScreen} />
                                            <PrivateRoute exact path="/address" component={AddressScreen} />
                                            <PrivateRoute exact path="/cart" component={CartScreen} />
                                            <PrivateRoute exact path="/account" component={AccountScreen} />
                                            <PrivateRoute exact path="/orders" component={OrderScreen} />
                                            <PrivateRoute exact path="/order/:id" component={OrderDetailsScreen} />
                                        </Switch>
                                    </CSSTransition>
                                </TransitionGroup>
                            )} />
                        </div>
                    </BrowserRouter>
                </ClientContext.Provider >
            </AuthContext.Provider>
        </ThemeProvider >
    );
}

export default App;
