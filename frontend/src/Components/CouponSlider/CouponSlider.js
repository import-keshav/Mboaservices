import React, { Component } from 'react';
import './CouponSlider.css';
import { RiCoupon2Line } from 'react-icons/ri';

import Coupon from '../../Components/Mobile/Coupon/Coupon';
import { ClientContext } from '../../Context/ClientContext';
import { RestaurantService } from '../../Services/RestaurantService';

class CouponSlider extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            loading: false,
        };
    }

    componentDidMount() {
        this.setState({ loading: true });

        RestaurantService.getRestaurantPromoCodes(this.context.token, this.props.restId).then((res) => {
            this.setState({ data: res.data, loading: false })
        })
    }

    render() {
        const showHideClassName = this.props.visible ? "coupon-slider show" : "coupon-slider hide";

        return (
            <div className={showHideClassName}>
                <div className="essential">
                    <RiCoupon2Line size={20} />
                    <h5 className="number">Coupons</h5>
                    <div className="close" onClick={this.props.handlerOpen}>x</div>
                </div>

                {this.state.data.length > 0 ? this.state.data.map((coupon) => {
                    return <Coupon
                        key={coupon.id}
                        {...this.props}
                        name={coupon.promocode}
                        discount={coupon.discount_percentage}
                        onApplyHandler={() => {
                            this.props.discountApply(coupon.discount_percentage)
                        }}
                        handlerOpen={this.props.handlerOpen}
                        categories={coupon.category} />
                }) : <h6 style={{ textAlign: "center" }}>Sorry!No coupons found</h6>}
            </div>
        )
    }
}

export default CouponSlider;