import React, { useEffect, useState } from 'react';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import Navbar from '../../Components/Navbar/Navbar';
import { useClientContext } from '../../Context/ClientContext';
import { ClientService } from '../../Services/ClientService';
import OrderTabs from '../../Components/OrderTabs/OrderTabs';
import { useAuthContext } from '../../Context/AuthContext';


const useStyles = makeStyles((theme) => ({
    icon: {
        marginRight: theme.spacing(2),
    },
    heroContent: {
        backgroundColor: theme.palette.primary.main,
        padding: theme.spacing(8, 0, 6),
    },
    heroButtons: {
        marginTop: theme.spacing(4),
    },
    cardGrid: {
        paddingTop: theme.spacing(8),
        paddingBottom: theme.spacing(8),

    },
    card: {
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
    },
    cardMedia: {
        paddingTop: '56.25%', // 16:9,
    },
    cardContent: {
        flexGrow: 1,
    },
    footer: {
        backgroundColor: theme.palette.background.paper,
        padding: theme.spacing(6),
    },
    search: {
        position: 'relative',
        borderRadius: theme.shape.borderRadius,
        marginLeft: 0,
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            marginLeft: theme.spacing(1),
            width: 'auto',
        },
        backgroundColor: "white",
        height: 40,
        marginBottom: 10,
        textIndent: 10,
        paddingTop: 4,
    },
    searchIcon: {
        height: '100%',
        position: 'absolute',
        right: "0px",
        pointerEvents: 'none',
        paddingTop: 5,
        paddingRight: 10

    },
    inputInput: {
        // vertical padding + font size from searchIcon
        paddingLeft: `calc(1em + ${theme.spacing(4)}px)`,
        transition: theme.transitions.create('width'),
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            width: '12ch',
            '&:focus': {
                width: '20ch',
            },
        },
    },
    inputRoot: {
        color: 'inherit',
    },
}));



export default function OrdersScreen(props) {
    const classes = useStyles();
    const [clientData, setClientData] = useState({});
    const { clientId } = useClientContext();
    const { token } = useAuthContext();

    useEffect(() => {
        ClientService.getSpecificClient(token, clientId).then((client) => {
            setClientData(client.data[0].user);
        });
    }, [clientId])

    return (
        <React.Fragment>
            <Navbar {...props} name="Orders" />

            <main style={{ backgroundColor: "white", paddingTop: "60px" }}>
                {/* Hero unit */}
                <div className={classes.heroContent}>
                    <Container maxWidth="sm">
                        <Typography component="h2" variant="h3" align="center" style={{ color: "white" }} gutterBottom>
                            {clientData.name}
                        </Typography>
                        <Typography variant="h5" align="center" color="textSecondary" style={{ color: "white" }} paragraph>
                            {clientData.mobile + " | " + clientData.email}
                        </Typography>
                    </Container>
                </div>
                <Container className={classes.cardGrid} maxWidth="lg">
                    {/* End hero unit */}
                    <Grid xs={12} sm={12} md={12} lg={12}>
                        <OrderTabs {...props} />
                    </Grid>
                </Container>
                {/* <ChatModal /> */}
            </main>
        </React.Fragment >
    );
}

