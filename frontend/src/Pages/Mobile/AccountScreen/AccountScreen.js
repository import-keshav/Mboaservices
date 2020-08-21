import React, { Component, useState, useEffect } from 'react';
import './AccountScreen.css';
import BottomNavPhone from '../../../Components/Mobile/BottomBar/BottomBar';
import { GoLocation, AiOutlineRight, MdLocalOffer, AiOutlineLogout } from 'react-icons/all';
import { ClientContext, useClientContext } from '../../../Context/ClientContext';
import { ClientService } from '../../../Services/ClientService';
import { useAuthContext } from '../../../Context/AuthContext';

function AccountScreen(props) {
    const [clientData, setClientData] = useState({});
    const { token, setToken } = useAuthContext();
    const { clientId, setClientId } = useClientContext();

    useEffect(() => {
        ClientService.getSpecificClient(token, clientId)
            .then((result) => {
                setClientData(result.data[0].user);
            })
    }, []);

    const logoutHandler = async () => {
        await setToken(null);
        await setClientId(null);
        await localStorage.setItem('authToken', null);
        await localStorage.setItem('clientId', null);
        props.history.push('/login');
    }

    const { name, mobile, email } = clientData;

    return (
        <div className="accountscreen" >
            <div className="account-info">
                <h3 className="name">{name}</h3>
                <div className="essential">
                    <h6 className="text-phone">{mobile}</h6>
                    <h6 className="text-email">{email}</h6>
                </div>
                <div className="options">
                    <div className="option">
                        <h6 className="option-text"><GoLocation />&nbsp; Manage Addresses</h6>
                        <div className="icon">
                            <AiOutlineRight />
                        </div>
                    </div>
                    <div className="option">
                        <h6 className="option-text"><MdLocalOffer />&nbsp; Offers</h6>
                        <div className="icon">
                            <AiOutlineRight />
                        </div>
                    </div>
                    <div className="option" onClick={logoutHandler}>
                        <h6 className="option-text"><AiOutlineLogout />&nbsp; Log Out</h6>
                        <div className="icon">
                            <AiOutlineRight />
                        </div>
                    </div>
                </div>
            </div>
            <BottomNavPhone {...props} />
        </div >
    )
}



export default AccountScreen;