import React, { Component } from 'react';
import Restaurant from '../../Components/Restaurant/Restaurant';
import Navbar from '../../Components/Navbar/Navbar';
import './HomePage.css';
import { FaFilter } from 'react-icons/fa';
import { RestaurantService } from '../../Services/RestaurantService';
import CartComp from '../../Components/CartComp/CartComp';
import { ClientContext } from '../../Context/ClientContext';
import Skeleton from '@material-ui/lab/Skeleton';

const SkeletonStructure = () => {
    return (
        <div className="row">
            {
                Array(9)
                    .fill()
                    .map((item, index) => (
                        <div className="col-xs-12 col-sm-9 col-md-6 col-lg-3" key={index}>
                            <Skeleton height={180} />
                            <h4 className="card-title">
                                <Skeleton circle={true} height={50} width={50} /> &nbsp;
                            <Skeleton height={36} width={`80%`} />
                            </h4>
                            <p className="card-channel">
                                <Skeleton width={`60%`} />
                            </p>
                            <div className="card-metrics">
                                <Skeleton width={`90%`} />
                            </div>
                        </div>
                    ))
            }
        </div>
    )
}

class HomePage extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            filterData: [],
            loading: false
        }
    }

    componentDidMount() {
        this.setState({ loading: true });
        RestaurantService.getRestaurantHomePage(this.context.token).then((res) => {
            const data = [];
            res.data.map(item => {
                if (item.is_open) {
                    data.push(item);
                }
            })
            this.setState({ data: data, filterData: data, loading: false });
        });
    }

    sortBy = (name) => {
        if (name === "rating") {
            let sorted_data = this.state.data.sort((a, b) => {
                return new Date(a.rating).getTime() - new Date(b.rating).getTime()
            }).reverse();
            this.setState({ filterData: sorted_data });
        }
    }

    render() {
        return (
            <div className="homepage">
                <Navbar name="Home" {...this.props} />
                <div className="filters">
                    <h2 className="restaurant-count">{this.state.data.length} restaurants</h2>
                    <div className="filters-div">
                        <div className="filter">Relevance</div>
                        <div className="filter">Delivery Time</div>
                        <div className="filter" onClick={() => { this.sortBy("rating") }}>Rating</div>
                        <div className="filter"><FaFilter size={20} /> &nbsp;Filters</div>
                    </div>
                </div>
                <div className="container-fluid">
                    {this.state.loading && <SkeletonStructure />}
                    <div className="row cont">
                        {
                            this.state.filterData.map((item) => {
                                return <div key={item.id} className="col-xs-12 col-sm-9 col-md-6 col-lg-3 restaurant-card" onClick={() => { this.props.history.push(`/restaurant/${item.id}`) }}>
                                    <Restaurant {...this.props} src={item.image} id={item.id} name={item.name} categories={item.category} rating={item.rating} />
                                </div>
                            })
                        }
                    </div>
                </div>
                {this.context.clientId ?
                    <CartComp {...this.props} cartItemsLength={this.context.cartItems.length} price={0} />
                    : null}
            </div>
        )
    }
}

export default HomePage;