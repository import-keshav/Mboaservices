import React, { Component } from 'react';
import './CouponScreen.css';
import CartNavbar from '../../../Components/Mobile/CartNavBar/CartNavbar';
import Coupon from '../../../Components/Mobile/Coupon/Coupon';
import { RestaurantService } from '../../../Services/RestaurantService';
import { ClientContext } from '../../../Context/ClientContext';

class CouponScreen extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            loading: false
        }
    }

    componentDidMount() {
        this.setState({ loading: true });
        RestaurantService.getRestaurantPromoCodes(this.context.token, this.props.match.params.id).then((res) => {
            this.setState({ data: res.data, loading: false });
        })
    }

    render() {
        return (
            <div className="couponscreen">
                <CartNavbar heading="Apply Coupons" onBack={() => { this.props.history.goBack() }} />
                <div className="text-input">
                    <input type="text" placeholder="Enter Coupon Code" className="input" />
                </div>
                <div className="coupon-list">
                    <h5 className="heading">Available Coupons</h5>
                    <div className="coupons">
                        {this.state.data.length > 0 ? this.state.data.map((coupon) => {
                            return <Coupon {...this.props} name={coupon.promocode} discount={coupon.discount_percentage} categories={coupon.category} />
                        }) : <h6 style={{ textAlign: "center" }}>Sorry!No coupons found</h6>}
                    </div>
                </div>
            </div>
        )
    }
}

export default CouponScreen;