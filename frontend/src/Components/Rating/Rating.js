import React from 'react';
import Rating from '@material-ui/lab/Rating';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import TextareaAutosize from '@material-ui/core/TextareaAutosize/TextareaAutosize';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import MuiAlert from '@material-ui/lab/Alert';
import Snackbar from '@material-ui/core/Snackbar';

import { useClientContext } from '../../Context/ClientContext';
import { RestaurantService } from '../../Services/RestaurantService';
import { useAuthContext } from '../../Context/AuthContext';

function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
}


export default function SimpleRating(props) {
    //state variables
    const [value, setValue] = React.useState(0);
    const [text, setText] = React.useState("");
    const [loading, setLoading] = React.useState(false);
    const { clientId } = useClientContext();
    const { token } = useAuthContext();
    const [open, setOpen] = React.useState(false);
    const [error, setError] = React.useState(false);


    const handleClick = () => {
        setOpen(true);
    };

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }

        setOpen(false);
    };



    function submitHandler(e) {
        e.preventDefault();
        const params = {
            client: clientId,
            restaurant: props.id,
            points: value,
            comment: text
        }
        setLoading(true);
        RestaurantService.giveRestaurantReview(token, params).then(() => {
            setLoading(false);
            handleClick();
        }).catch(() => {
            setError(true);
            setLoading(false);
        })
    }

    return (
        <div>
            <Box component="fieldset" mb={3} borderColor="transparent">
                <Typography component="legend">Rating</Typography>
                <br />
                <Rating
                    name="simple-controlled"
                    value={value}
                    onChange={(event, newValue) => {
                        setValue(newValue);
                    }}
                />
                <br />
                <TextareaAutosize
                    aria-label="minimum height"
                    rowsMin={3}
                    placeholder="Enter your reviews here"
                    onChange={(e) => { setText(e.target.value) }}
                />
                <br />
                <Button variant="contained" color="primary" onClick={submitHandler}>
                    Rate Us
                </Button>
                <br />
                {loading ? <CircularProgress style={{ marginTop: "10px" }} /> : null}
                <Snackbar open={open} autoHideDuration={4000} onClose={handleClose}>
                    <Alert onClose={handleClose} severity="success">
                        Thanks for Reviewing us
                    </Alert>
                </Snackbar>
                <Snackbar open={error} autoHideDuration={4000} onClose={() => { setError(false) }}>
                    <Alert onClose={() => { setError(false) }} severity="error">
                        You have already reviewed us. Thanks!
                    </Alert>
                </Snackbar>
            </Box>
        </div>
    );
}