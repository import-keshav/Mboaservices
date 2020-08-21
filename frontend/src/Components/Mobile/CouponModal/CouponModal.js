import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Modal from '@material-ui/core/Modal';
import { RiCoupon2Line } from 'react-icons/ri';
import Coupon from '../Coupon/Coupon';
import { RestaurantService } from '../../../Services/RestaurantService';
import './CouponModal.css'
import { useAuthContext } from '../../../Context/AuthContext';

function rand() {
    return Math.round(Math.random() * 20) - 10;
}

function getModalStyle() {
    const top = 50 + rand();
    const left = 50 + rand();

    return {
        top: `${top}%`,
        left: `${left}%`,
        transform: `translate(-${top}%, -${left}%)`,
    };
}

const useStyles = makeStyles((theme) => ({
    paper: {
        position: 'absolute',
        width: '90%',
        marginLeft: "5%",
        marginRight: "5%",
        backgroundColor: theme.palette.background.paper,
        border: '2px solid #000',
        boxShadow: theme.shadows[5],
        marginTop: '40%',
        padding: "10%"
    },
}));

export default function CouponModal(props) {
    const classes = useStyles();
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const { token } = useAuthContext();

    useEffect(() => {
        RestaurantService.getRestaurantPromoCodes(token, props.restaurantId).then((res) => {
            setData(res.data)
        })
    }, [])

    const body = (
        <div className={classes.paper}>
            <div className="coupon-modal">
                <div className="position">
                    <div className="essential">
                        <RiCoupon2Line size={20} />
                        <h5 className="number">Coupons</h5>
                    </div>
                    <h6 className="cross" onClick={props.onClose}>x</h6>
                </div>


                {data.length > 0 ? data.map((coupon) => {
                    return <Coupon
                        key={coupon.id}
                        {...props}
                        name={coupon.promocode}
                        discount={coupon.discount_percentage}
                        onApplyHandler={() => {
                            props.discountApply(coupon.discount_percentage)
                        }}
                        categories={coupon.category} />
                }) : <h6 style={{ textAlign: "center" }}>Sorry!No coupons found</h6>}
            </div>
        </div>
    );

    return (
        <div>
            <Modal
                open={props.open}
                onClose={props.onClose}

                aria-labelledby="simple-modal-title"
                aria-describedby="simple-modal-description"
            >
                {body}
            </Modal>
        </div>
    );
}
