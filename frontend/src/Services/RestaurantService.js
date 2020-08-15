import Axios from 'axios';

const getRestaurants = async (text) => {
    return await Axios.get(`/restaurant/get-restaurant-on-filter?search=${text}`);
}

const getRestaurantHomePage = async (token) => {
    return await Axios.get('/restaurant/get-restaurant-on-home-page', {
        headers: {
            'Authorization': "Bearer " + token
        }
    });
}

const getSpecificRestaurant = async (id) => {
    return await Axios.get(`/restaurant/get-restaurant/${id}`);
}

const getRestaurantPromoCodes = async (token, id) => {
    return await Axios.get(`/restaurant/get-promocode/${id}`, {
        headers: {
            'Authorization': "Bearer " + token
        }
    });
}

const giveRestaurantReview = async (token, params) => {
    return await Axios.post('/reviews/create-client-review', params, {
        headers: {
            'Authorization': "Bearer " + token
        }
    });
}



export const RestaurantService = {
    getRestaurants,
    getRestaurantHomePage,
    getSpecificRestaurant,
    getRestaurantPromoCodes,
    giveRestaurantReview
}