import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import MoonLoader from 'react-spinners/MoonLoader';

import OrderItem from '../OrderItem/OrderItem';
import OrderSlider from '../OrderSlider/OrderSlider';
import { OrderService } from '../../Services/OrderService';
import { useClientContext } from '../../Context/ClientContext';
import { useAuthContext } from '../../Context/AuthContext';

function TabPanel(props) {
    const { children, value, index, ...other } = props;
    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`vertical-tabpanel-${index}`}
            aria-labelledby={`vertical-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box p={3}>
                    <Typography>{children}</Typography>
                </Box>
            )}
        </div>
    );
}

TabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.any.isRequired,
    value: PropTypes.any.isRequired,
};

function a11yProps(index) {
    return {
        id: `vertical-tab-${index}`,
        'aria-controls': `vertical-tabpanel-${index}`,
    };
}

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
        backgroundColor: theme.palette.background.paper,
        display: 'flex',
        height: 'auto',
    },
    tabs: {
        borderRight: `1px solid ${theme.palette.divider}`,
    },

}));

export default function OrderTabs(props) {
    const classes = useStyles();

    //state variables
    const [value, setValue] = React.useState(0);
    const [active, setActive] = React.useState(false);
    const [data, setData] = React.useState([]);
    const [loading, setLoading] = React.useState(false);
    const [currentId, setCurrentId] = React.useState(null);
    const { clientId } = useClientContext();
    const { token } = useAuthContext();


    const handleChange = (event, newValue) => {
        setValue(newValue);
    };


    useEffect(() => {
        setLoading(true);
        OrderService.getClientOrders(token, clientId).then((orders) => {
            setData(orders.data);
            setLoading(false);
        });
    }, [clientId]);


    const handlerOpen = (e) => {
        e.stopPropagation();
        setActive(false);
    }


    const handlerOpen1 = () => {
        setActive(false);
    }


    let content;
    if (active) {
        content = <OrderSlider {...props} currentId={currentId} visible={active} handlerOpen1={handlerOpen1} handlerOpen={handlerOpen} />
    }

    let main_content;
    if (loading) {
        main_content = <MoonLoader color="#52be80" />
    }

    else {
        main_content = <div className="orders">
            {data.map((order) => {
                return <OrderItem
                    price={order.total_amount}
                    created={order.created}
                    id={order.id}
                    dishes={order.dishes}
                    restaurant={order.restaurant}
                    delivered_time={order.created}
                    handleClick={() => {
                        setCurrentId(order.id);
                        setActive(true);
                    }} />
            })}
        </div>
    }

    return (
        <div className={classes.root}>
            <Tabs
                orientation="vertical"
                variant="scrollable"
                value={value}
                onChange={handleChange}
                aria-label="Vertical tabs example"
                className={classes.tabs}
            >
                <Tab className={classes.tab} label="Orders" {...a11yProps(0)} />
                <Tab className={classes.tab} label="Addresses" {...a11yProps(1)} />
            </Tabs>
            {content}
            <TabPanel value={value} index={0}>
                <Typography component="h4" variant="h4">
                    Orders
                </Typography>
                {main_content}
            </TabPanel>

            <TabPanel value={value} index={2}>
                <Typography component="h4" variant="h4">
                    Addresses
                </Typography>
            </TabPanel>
        </div>
    );
}
