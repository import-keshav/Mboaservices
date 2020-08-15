import Axios from 'axios';

const mobileCheckHandler = async (mobile) => {
    return await Axios.post('/user/check-mobile-number', {
        mobile_number: mobile
    })
}

const sendOtp = async (mobile) => {
    return await Axios.post('/user/send-otp', {
        mobile_number: mobile
    })
}

const verifyOtp = async (params) => {
    return await Axios.post('/user/verify-otp', params)
}

const signUp = async (params) => {
    return await Axios.post('/user/register', params);
}

export const AuthService = {
    mobileCheckHandler,
    sendOtp,
    verifyOtp,
    signUp
}