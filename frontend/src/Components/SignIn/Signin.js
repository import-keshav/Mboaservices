import React, { useState } from 'react';
import './Signin.css';
// import Checkbox from '@material-ui/core/Checkbox';
// import { withStyles } from '@material-ui/core/styles';
// import { red } from '@material-ui/core/colors';
import { Link } from 'react-router-dom';
import { AuthService } from '../../Services/AuthService';
import { useAuthContext } from '../../Context/AuthContext';
import { useClientContext } from '../../Context/ClientContext';

// const GreenCheckbox = withStyles({
//     root: {
//         color: red[300],
//         '&$checked': {
//             color: red[400],
//         },
//     },
//     checked: {},
// })((props) => <Checkbox color="default" {...props} />);


function SignIn(props) {
    const [remeber, setRemember] = useState(false);
    const [passwordTypeText, setPasswordTypeText] = useState(false);
    const [numberExists, setNumberExists] = useState(false);
    const [mobile, setMobile] = useState("");
    const [otp, setOtp] = useState("");
    const [otpSentMessage, setOtpSentMessage] = useState("");
    const { setToken } = useAuthContext();
    const { setClientId } = useClientContext();

    const onMobileChangeHandler = (event) => {
        setMobile(event.target.value);
    }

    const onOtpChangeHandler = (event) => {
        setOtp(event.target.value);
    }

    const passwordTypeHandler = () => {
        setPasswordTypeText(!passwordTypeText);
    }

    const numberExistHandler = (e) => {
        e.preventDefault();
        AuthService.mobileCheckHandler("+237" + mobile)
            .then((result) => {
                if (result.data.is_valid) {
                    setNumberExists(true);
                    AuthService.sendOtp(("+237" + mobile))
                        .then((res) => {
                            setOtpSentMessage("OTP sent successfully!");
                        })
                        .catch(err => {
                            console.log(err.response.data)
                        })
                }
            })
            .catch(err => {
                return props.history.push('/signup')
            })
    }

    const verifyOtp = (e) => {
        e.preventDefault();
        const params = {
            mobile_number: "+237" + mobile,
            otp: otp
        }
        AuthService.verifyOtp(params)
            .then((result) => {
                setToken(result.data.token);
                setClientId(result.data.client.id);
                localStorage.setItem('authToken', result.data.token);
                localStorage.setItem('clientId', result.data.client.id);
                props.history.push('/');
            })
            .catch((err) => {
                alert(err.response.data.message);
                console.log(err.response.data)
            })
    }

    let content;
    if (numberExists) {
        content = <>
            <h5 className="forgot-password" style={{ margin: "0px" }}>Sign In with OTP</h5>
            <div className="form-with-icon">
                <input
                    placeholder="OTP*"
                    name="otp"
                    onChange={onOtpChangeHandler}
                    className="signin-input"
                    type={passwordTypeText ? "text" : "password"} />
                <div className="icon" onClick={passwordTypeHandler}>
                    <img className="img-fluid lock-icon" src={require('../../Assets/lock-icon.png')} alt="lock" />
                </div>
            </div>
        </>
    }
    else {
        content = null
    }
    return (
        <div className="signin">
            <h2 className="header">Sign In</h2>

            <form className="signin-form">
                <img className="image" src={require('../../Assets/advertise.jpeg')} alt="advertise" />

                <input type="text" onChange={onMobileChangeHandler} name="mobile" placeholder="Mobile*" className="input" />

                {content}
                {/* <FormControlLabel
                        control={<GreenCheckbox checked={this.state.checked} onChange={this.handleChange} name="remember" />}
                        label="Remember Me"
                    /> */}
                <br />
                <button className="signin-button" onClick={numberExists ? verifyOtp : numberExistHandler}>
                    <span className="btncon">Log In</span>
                </button>
            </form>
            <Link to={'/signup'} className="link">
                <h5 style={{ textAlign: 'center', fontWeight: "initial", marginTop: "4px" }}>Don't Have an account? <span style={{ fontWeight: '600' }}>Sign Up</span></h5>
            </Link>
        </div>
    )
}

export default SignIn;