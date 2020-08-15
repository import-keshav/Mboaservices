import Axios from 'axios';

const getSpecificClient = async (token, id) => {
    return await Axios.get(`/client/get-client/${id}`, {
        headers: {
            'Authorization': "Bearer " + token
        }
    });
}

const getClientCart = async (token, id) => {
    return await Axios.get(`/client/get-client-cart/${id}`, {
        headers: {
            'Authorization': "Bearer " + token
        }
    });
}

const clientAddItemToCart = async (token, params) => {
    return await Axios.post('/client/add-item-in-client-cart', params, {
        headers: {
            'Authorization': "Bearer " + token
        }
    });
}

const deleteItemFromCart = async (token, params) => {
    return await Axios.delete(`/client/delete-item-in-client-cart/${params}`, {
        headers: {
            'Authorization': "Bearer " + token
        }
    });
}

const updateItemInCart = async (token, id, params) => {
    return await Axios.put(`/client/update-item-in-client-cart/${id}`, params, {
        headers: {
            'Authorization': "Bearer " + token
        }
    });
}

const checkRestaurantCart = async (token, params) => {
    return await Axios.post(`/client/verify-restraurant-with-client-cart`, params, {
        headers: {
            'Authorization': "Bearer " + token
        }
    });
}

const getClientCartItemPrice = async (token, id) => {
    return await Axios.get(`/client/get-client-cart-item-price/${id}`, {
        headers: {
            'Authorization': "Bearer " + token
        }
    });
}

const getClientPrice = async (token, id) => {
    return await Axios.get(`/client/get-client-total-cart-price/${id}`, {
        headers: {
            'Authorization': "Bearer " + token
        }
    })
}

export const ClientService = {
    getSpecificClient,
    getClientCart,
    clientAddItemToCart,
    deleteItemFromCart,
    updateItemInCart,
    checkRestaurantCart,
    getClientCartItemPrice,
    getClientPrice
}