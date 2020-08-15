import React, { Component } from 'react';
import './SignUp.css';
import Checkbox from '@material-ui/core/Checkbox';
import { withStyles } from '@material-ui/core/styles';
import { red } from '@material-ui/core/colors';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import { Link } from 'react-router-dom';
import { AuthService } from '../../Services/AuthService';

const GreenCheckbox = withStyles({
    root: {
        color: red[300],
        '&$checked': {
            color: red[400],
        },
    },
    myLabel: {
        fontSize: "10px"
    },
    checked: {},
})((props) => <Checkbox color="default" {...props} />);



class SignUp extends Component {
    constructor(props) {
        super(props);
        this.state = {
            remember: false,
            passwordTypeText: false,
            formfields: {
                name: "",
                email: "",
                mobile: "",
                password: ""
            },
            checked: false
        };
    }

    handleChange = (event) => {
        this.setState({ ...this.state, [event.target.name]: event.target.checked });
    };

    passwordTypeHandler = () => {
        this.setState({ passwordTypeText: !this.state.passwordTypeText });
    }

    onChangeHandler = (event) => {
        const formfields = { ...this.state.formfields };
        formfields[event.target.name] = event.target.value;
        this.setState({ formfields: formfields })
    }

    handleCheckedChange = () => {
        this.setState({ checked: !this.state.checked })
    }

    onSubmitHandler = (e) => {
        e.preventDefault();
        let formfields = this.state.formfields;
        let mobile = "+237" + this.state.formfields.mobile;
        formfields['mobile'] = mobile;
        if (this.state.checked) {
            AuthService.signUp(formfields)
                .then((result) => {
                    if (result.status === 200) {
                        return this.props.history.push('/login');
                    }
                })
                .catch((err) => {
                    console.log(err);
                })
        }
        else {
            alert("Please confirm our privacy policy to proceed");
        }
    }


    render() {
        return (
            <div className="signup">
                <h2 className="header">Sign Up</h2>
                <form className="signup-form" method="post">
                    <input type="text" onChange={this.onChangeHandler} name="name" placeholder="Name" className="input" />
                    <input type="text" onChange={this.onChangeHandler} name="email" placeholder="Email" className="input" />
                    <input type="text" onChange={this.onChangeHandler} name="mobile" placeholder="Mobile" className="input" />

                    <div className="form-with-icon">
                        <input
                            placeholder="Password"
                            name="password"
                            className="signup-input"
                            onChange={this.onChangeHandler}
                            type={this.state.passwordTypeText ? "text" : "password"} />
                        <div className="icon" onClick={this.passwordTypeHandler}>
                            <img className="img-fluid lock-icon" src={require('../../Assets/lock-icon.png')} alt="lock" />
                        </div>
                    </div>
                    {/* <div className="form-with-icon">
                        <input placeholder="Confirm Password" className="signup-input" type={this.state.passwordTypeText ? "text" : "password"} />
                        <div className="icon" onClick={this.passwordTypeHandler}>
                            <img className="img-fluid lock-icon" src={require('../../Assets/lock-icon.png')} alt="lock" />
                        </div>
                    </div> */}
                    <FormControlLabel
                        control={<GreenCheckbox checked={this.state.checked} onChange={this.handleCheckedChange} name="remember" />}
                        label="You agree to our Terms of use"
                        classes={{ label: 'myLabel' }}
                    />
                    <br />
                    <button className="signup-button" onClick={this.onSubmitHandler}>
                        <span className="btncon">Sign Up</span>
                    </button>
                </form>
                <Link to={'/login'} className="link">
                    <h5 style={{ textAlign: 'center', fontWeight: "initial", marginTop: "0px" }}>Already Have an account? <span style={{ fontWeight: 'bold' }}>Sign In</span></h5>
                </Link>
            </div>
        )
    }
}

export default SignUp;