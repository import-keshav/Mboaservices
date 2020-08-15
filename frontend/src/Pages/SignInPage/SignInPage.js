import React, { Component } from 'react';
import './SignInPage.css';
import SignIn from '../../Components/SignIn/Signin';

class SignInPage extends Component {
    render() {
        return (
            <header className="App-header">
                <SignIn {...this.props} />
            </header>
        )
    }
}

export default SignInPage;