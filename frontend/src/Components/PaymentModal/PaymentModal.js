import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import 'react-confirm-alert/src/react-confirm-alert.css';
import DialogTitle from '@material-ui/core/DialogTitle';
import Dialog from '@material-ui/core/Dialog';
import { blue } from '@material-ui/core/colors';
import CloseIcon from '@material-ui/icons/Close';
import IconButton from '@material-ui/core/IconButton';
import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import './PaymentModal.css';
import Axios from 'axios';
import { confirmAlert } from 'react-confirm-alert';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';

import { useClientContext } from '../../Context/ClientContext';



function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const useStyles = makeStyles((theme) => ({
    root: {
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    avatar: {
        backgroundColor: blue[100],
        color: blue[600],
    },
    closeButton: {
        position: 'absolute',
        right: theme.spacing(1),
        top: theme.spacing(1),
        color: theme.palette.grey[500],
        marginLeft: "100px"
    },
}));


function PaymentModal(props) {
    const classes = useStyles();

    //state variables
    const [error, setError] = React.useState(false);
    const [response, setResponse] = React.useState("");
    const [mobile, setMobile] = React.useState("");
    const [openSnackBar, setOpenSnackbar] = React.useState(false);
    const [snackbarText, setSnackbarText] = React.useState("");
    const [service, setService] = React.useState(null);
    const { onClose, open, finalPrice } = props;


    const handleClickSnackBar = () => {
        setOpenSnackbar(true);
    };


    const handleCloseSnackBar = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        setOpenSnackbar(false);
    };


    const submit = () => {
        confirmAlert({
            title: `Are you sure you want to pay FCFA ${finalPrice}`,
            message: '',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => {
                        const params = {
                            service: props.mode === "phone" ? service : props.service,
                            amount: finalPrice,
                            payer: "237" + mobile,
                            reference: 'For food order',
                            fees: true,
                            message: "MBOA services",
                            code: "6317afa1c5d4e73395d2e52ffc06eb4e5a9468a3"
                        }

                        Axios.post('https://mesomb.hachther.com/api/v1.0/payment/online/', params, {
                            headers: {
                                "X-MeSomb-Application": "6317afa1c5d4e73395d2e52ffc06eb4e5a9468a3",
                            }
                        }).then((result) => {
                            if (result.data.success === false) {
                                handleClickSnackBar();
                                setSnackbarText("Payment Unsuccessful!");
                            }
                            else {
                                props.createOrder();
                            }
                        }).catch((err) => {
                            console.log(err.response.data);
                            setSnackbarText(err.response.data.detail);
                            handleClickSnackBar();
                        })
                    }
                },
                {
                    label: 'No',
                    onClick: () => {
                        setSnackbarText("Payment Unsuccessful!");
                        handleClickSnackBar();
                    }
                }
            ]
        });
    };


    const handlePayment = () => {
        if (mobile === "") {
            setError(true);
            setResponse("*Please enter your mobile number");
        }
        onClose();
        submit();
    }

    const handleClose = () => { };




    return (
        <>
            <Dialog onClose={handleClose} aria-labelledby="simple-dialog-title" open={open}>
                <IconButton aria-label="close" className={classes.closeButton} onClick={onClose}>
                    <CloseIcon size={10} />
                </IconButton>
                <DialogTitle id="simple-dialog-title" style={{ fontWeight: "bold", marginRight: "30px" }}>Payment By {props.service}</DialogTitle>
                <Divider />
                <TextField
                    id="outlined-basic"
                    label="Enter your mobile number"
                    placeholder="Enter number after +237"
                    required={true}
                    variant="outlined"
                    style={{ margin: "20px" }}
                    onChange={(e) => { setMobile(e.target.value) }} />
                <div className="payment-modes">
                    <h4 className="price">Amount - FCFA <span style={{ color: "#52be80" }}>{finalPrice}</span></h4>
                </div>
                {props.mode === "phone" ?
                    <>
                        <h6 style={{ textAlign: "center" }}>Choose your payment method</h6>
                        <div className="payment-modes">
                            <Button className="mode1" onClick={() => { setService("ORANGE") }}>
                                <img src={require('../../Assets/orange_money.jpg')} alt="orange-money" className="payment-image" />
                            </Button>
                            <Button className="mode2" onClick={() => { setService("MTN") }}>
                                <img src={require('../../Assets/momo.jpg')} alt="mtn-money" className="payment-image" />
                            </Button>
                        </div>
                    </> : null}
                {error && <h6 style={{ textAlign: "center", color: "red" }}>{response}</h6>}
                <Button variant="contained" color="primary" onClick={handlePayment} style={{ height: 45 }}>
                    Pay
                </Button>
            </Dialog>
            <Snackbar open={openSnackBar} autoHideDuration={6000} onClose={handleCloseSnackBar}>
                <Alert onClose={handleCloseSnackBar} severity="error">{snackbarText}</Alert>
            </Snackbar>
        </>
    );
}

export default PaymentModal;