import React, { Component } from 'react';
import Card from '@material-ui/core/Card';
import { Map, GoogleApiWrapper, Marker } from 'google-maps-react';

const styles = {
    card: {
        border: 'solid 2px #52be80',
        flex: 1,
        height: '19em',
        width: '19em'
    },
    map: {
        height: '18em',
        width: '18em',
        margin: "0.5em"
    }
};


export class MapContainer extends Component {
    onDragend = (one, two, three) => {
        const { latLng } = three;
        const lat = latLng.lat();
        const lng = latLng.lng();
        console.log(lat);
        console.log(lng);
    }
    render() {
        return (
            <Card style={styles.card} >
                <Map
                    google={this.props.google}
                    zoom={17}
                    containerStyle={{ height: '19rem', width: "19rem" }}
                    initialCenter={{
                        lat: this.props.latitude,
                        lng: this.props.longitude
                    }}
                    style={styles.map}>
                    <Marker
                        onClick={this.onMarkerClick}
                        draggable={true}
                        onDragend={this.props.onMarkerDrag}
                        name={'Current location'} />
                </Map>
            </Card>
        );
    }
}

export default GoogleApiWrapper({
    apiKey: "AIzaSyD3O7PvN7LlKEXJ0QxOEmXPR3GYAjaS8t0",
})(MapContainer);