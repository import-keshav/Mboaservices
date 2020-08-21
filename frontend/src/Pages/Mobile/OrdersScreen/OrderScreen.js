import React, { Component } from 'react';
import './OrderScreen.css';
import BottomBar from '../../../Components/Mobile/BottomBar/BottomBar';
import OrderItem from '../../../Components/Mobile/OrderItem/OrderItem';
import { OrderService } from '../../../Services/OrderService';
import { ClientContext } from '../../../Context/ClientContext';
import CircularProgress from '@material-ui/core/CircularProgress';


class OrderScreen extends Component {
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
        OrderService.getClientOrders(this.context.token, this.context.clientId).then((orders) => {
            this.setState({ data: orders.data, loading: false });
        });
    }

    render() {
        let content;
        if (this.state.loading) {
            content = <div style={{ marginLeft: "40%" }}>
                <CircularProgress />
            </div>
        }
        else {
            content = <div className="orders" >
                {this.state.data.length > 0 ? this.state.data.map((order) => {
                    return <OrderItem
                        {...this.props}
                        price={order.total_amount}
                        created={order.created}
                        id={order.id}
                        dishes={order.dishes}
                        delivered_time={order.delivered_time}
                        restaurant={order.restaurant}
                    />
                }) : <h5 style={{ textAlign: "center", color: "grey", marginTop: "20px" }}>No orders</h5>}
            </div>
        }
        return (
            <div className="ordersmob">
                <div className="detailshome">
                    <h5 className="heading">All Orders</h5>
                </div>
                {content}
                <BottomBar {...this.props} />
            </div>
        )
    }
}
export default OrderScreen;