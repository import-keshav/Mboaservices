import React, { Component } from 'react';
import './AddressSlider.css';
import { TiLocation } from 'react-icons/ti';
import { ClientContext } from '../../Context/ClientContext';
import MapContainer from '../../Components/GoogleMap/GoogleMap';

class AddressSlider extends Component {
    static contextType = ClientContext;
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            loading: false,
            formfield: {
                door: "",
                landmark: ""
            },
            latitude: null,
            longitude: null
        };
    }


    inputChangeHandler = (e) => {
        let formfields = { ...this.state.formfield };
        formfields[e.target.name] = e.target.value;
        this.setState({ formfield: formfields });
    }


    onMarkerDrag = (one, two, three) => {
        const { latLng } = three;
        const lat = latLng.lat();
        const lng = latLng.lng();
        const formfield = { ...this.state.formfield };
        formfield["latitude"] = lat;
        formfield["longitude"] = lng;
        this.setState({ latitude: lat, longitude: lng, formfield: formfield });
    }


    render() {
        const { handlerOpen, addressHandler } = this.props;
        const showHideClassName = this.props.visible ? "address-slider show" : "address-slider hide";

        return (
            <div className={showHideClassName}>
                <div className="essential">
                    <TiLocation size={20} />
                    <h5 className="number">Add your location</h5>
                    <div className="close" onClick={handlerOpen}>x</div>
                </div>
                <MapContainer
                    latitude={this.context.latitude}
                    longitude={this.context.longitude}
                    onMarkerDrag={this.onMarkerDrag}
                />
                <div className="address-form">
                    <form className="form" method="POST">
                        <input
                            className="inputtext"
                            onChange={this.inputChangeHandler}
                            type="text"
                            name="door"
                            placeholder="Door/Flat No." />
                        <input
                            className="inputtext"
                            onChange={this.inputChangeHandler}
                            type="text"
                            name="landmark"
                            placeholder="Landmark" />
                    </form>
                </div>
                <div className="checkout" onClick={() => {
                    addressHandler(this.state.formfield);
                }}>
                    <span className="checkouttxt">
                        Add Address and Proceed
                    </span>
                </div>
            </div>
        )
    }
}

export default AddressSlider;