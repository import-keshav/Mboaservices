import Axios from 'axios';

const getDishesByRestaurant = async (index) => {
    return await Axios.get(`/dish/list-restaurant-dishes/${index}`);
}

const getDishBySearch = async (input) => {
    return await Axios.get(`dish/get-dish-on-filter?search=${input}`);
}

export const DishService = {
    getDishesByRestaurant,
    getDishBySearch
}