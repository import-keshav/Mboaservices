import React, { Component } from 'react';
import './Restaurant.css';

class Restaurant extends Component {
    // constructor(props) {
    //     super(props);
    // }
    render() {
        let color;
        if (this.props.rating >= 0 && this.props.rating < 2) {
            color = "#d9534f"
        }
        else if (this.props.rating >= 2 && this.props.rating < 3.5) {
            color = "#db7c38"
        }
        else {
            color = "#48c479"
        }
        const styles = {
            rating: {
                backgroundColor: color,     //#db7c38 
                width: "48px",
                padding: "0px 5px",
                fontWeight: 400,
                height: "22px",
                display: "inline-block",
                borderBottom: "1px solid #e9e9eb",
                borderRadius: "20px"
            }
        }
        return (
            <div className="restaurantmob" onClick={() => { this.props.history.push(`/restaurant/${this.props.id}`) }}>
                <img src={this.props.src} className="image ml-auto" alt="restaurant" />
                <div className="details">
                    <p className="name">{this.props.name}</p>
                    <p className="types">{this.props.categories.map((category, index) => {
                        if (index < 3) {
                            return category.name + ",";
                        }
                        if (index === 3) {
                            return category.name;
                        }
                    })}...</p>
                    <div className="features" style={{ display: "flex", justifyContent: "space-between", marginBottom: "10px" }}>
                        <div className="rating" style={styles.rating}>
                            <img src={require('../../../Assets/star-icon.png')} className="star-icon" alt="star" />
                            <h6 className="rating-value">{this.props.rating ? this.props.rating : 0}</h6>
                        </div>
                        <div style={{ display: "inline-block" }}>•</div>
                        <div className="distance">1km</div>
                        <div style={{ display: "inline-block" }}>•</div>
                        <div className="distance">32 min</div>
                    </div>
                    <div className="offers">
                        <img src={require('../../../Assets/discount.png')} className="discount" alt="discount" />
                        <h5 className="offer-content">20% on all orders</h5>
                    </div>
                </div>
            </div>
        )
    }
}

export default Restaurant;