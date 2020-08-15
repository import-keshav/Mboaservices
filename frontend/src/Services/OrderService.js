import Axios from 'axios';

const createOrder = async (token, params) => {
    return await Axios.post('/orders/create-order', params, {
        headers: {
            'Authorization': "Bearer " + token
        }
    });
}

const getClientOrders = async (token, clientId) => {
    return await Axios.get(`/orders/get-client-past-orders/${clientId}`, {
        headers: {
            'Authorization': "Bearer " + token
        }
    });
}

const getSpecificOrder = async (token, id) => {
    return await Axios.get(`/orders/get-specific-order/${id}`, {
        headers: {
            'Authorization': "Bearer " + token
        }
    });
}

export const OrderService = {
    createOrder,
    getClientOrders,
    getSpecificOrder
}