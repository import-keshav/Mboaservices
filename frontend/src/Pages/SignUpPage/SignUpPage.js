import React, { Component } from 'react';
import SignUp from '../../Components/SignUp/SignUp';

class SignUpPage extends Component {
    render() {
        return (
            <header className="App-header" >
                <SignUp {...this.props} />
            </header>
        )
    }
}

export default SignUpPage;