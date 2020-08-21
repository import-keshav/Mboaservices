import React, { useContext } from 'react';

//Client Context
export const ClientContext = React.createContext({
    clientId: null,
    cartItems: [],
    finalPrice: 0,
    restaurant: {},
    latitude: null,
    longitude: null,
    setClientId: () => { },
    addToCart: (data) => { },
    removeFromCart: (data) => { },
    setProductCart: (data) => { },
    setFinalPrice: (data, operation) => { },
    setCartProductQuantity: (data) => { },
    setRestaurant: (data) => { },
    setProductAddOn: (data) => { },
})

//Use Client Context
export function useClientContext() {
    return useContext(ClientContext);
}
