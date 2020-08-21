import React, { Component } from 'react';
import BottomBar from '../../../Components/Mobile/BottomBar/BottomBar';
import { BsFilter } from 'react-icons/bs';
import './Homepage.css';
import Restaurant from '../../../Components/Mobile/Restaurant/Restaurant';
import { RestaurantService } from '../../../Services/RestaurantService';
import Skeleton from '@material-ui/lab/Skeleton';

const SkeletonStructure = () => {
    return (
        <>
            {
                Array(9)
                    .fill()
                    .map((item, index) => (
                        <div className="restaurantmob">
                            <Skeleton height={100} />
                            <div className="details">
                                <p className="name"> <Skeleton /></p>
                                <p className="types">
                                    <Skeleton />
                                </p>
                                <div className="features" style={{ display: "flex", justifyContent: "space-between", marginBottom: "10px" }}>
                                    <div className="rating">
                                        <Skeleton />
                                    </div>
                                    <div style={{ display: "inline-block" }}>•</div>
                                    <div className="distance"><Skeleton height={30} width={30} /></div>
                                    <div style={{ display: "inline-block" }}>•</div>
                                    <div className="distance"><Skeleton height={30} width={30} /></div>
                                </div>
                                <div className="offers">
                                    <Skeleton height={30} width={30} />
                                    <h5 className="offer-content"><Skeleton /></h5>
                                </div>
                            </div>
                        </div>
                    ))
            }
        </>
    )
}

class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            loading: false,
            filterData: [],
            filterOpen: false
        };
    }

    componentDidMount() {
        this.setState({ loading: true });
        RestaurantService.getRestaurantHomePage().then((res) => {
            const data = [];
            res.data.map(item => {
                if (item.is_open) {
                    data.push(item);
                }
            })
            this.setState({ data: data, loading: false });
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
        let content;
        let content1;
        if (this.state.loading) {
            content = null;
        } else {
            content = this.state.data.map((item) => {
                return <Restaurant key={item.id} {...this.props} id={item.id} name={item.name} rating={item.rating} categories={item.category} src={item.image} />
            })
        }

        if (this.state.filterOpen) {
            content1 = <>
                <h5 className="filter-head">Filters</h5>
                <ul className="categories">
                    <>
                        <li className="item" onClick={() => { this.sortBy("rating") }}>{"Relevance"}</li>
                        <li className="item" onClick={() => { this.sortBy("rating") }}>{"Rating"}</li>
                        <li className="item" onClick={() => { this.sortBy("rating") }}>{"Delivery Time"}</li>
                    </>
                </ul>
            </>
        }


        return (
            <div className="homepagemob">
                <div className="detailshome">
                    <h5 className="heading">All restaurants</h5>
                    <h6 className="sort mr-auto" onClick={() => { this.setState({ filterOpen: !this.state.filterOpen }) }}><BsFilter size={25} />&nbsp; Sort/Filter </h6>
                </div>
                {this.state.loading && <SkeletonStructure />}
                {content1}
                {content}
                <BottomBar {...this.props} />
            </div>
        )
    }
}

export default HomePage;