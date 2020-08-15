import React, { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import DialogTitle from '@material-ui/core/DialogTitle';
import Dialog from '@material-ui/core/Dialog';
import { blue } from '@material-ui/core/colors';
import CloseIcon from '@material-ui/icons/Close';
import IconButton from '@material-ui/core/IconButton';
import Divider from '@material-ui/core/Divider';
import Checkbox from '@material-ui/core/Checkbox';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
    root: {
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    avatar: {
        backgroundColor: blue[100],
        color: blue[600],
    },
    closeButton: {
        position: 'absolute',
        right: theme.spacing(1),
        top: theme.spacing(1),
        color: theme.palette.grey[500],
        marginLeft: "100px"
    },
}));

function AddOnModal(props) {
    const classes = useStyles();
    const [addOns, setAddOns] = useState([]);
    const [finalAddOn, setFinalAddOn] = useState([]);
    const { onClose, open } = props;


    useEffect(() => {
        const data = props.addOns;
        setAddOns(data);
    }, [props.addOns])


    const handleAdd = () => {
        props.handleAdd(finalAddOn);
        onClose();
    }


    const handleClose = () => {

    }


    const addOnHandler = (event) => {
        addOnHandlerFinal(event.target.value);
    }


    const addOnHandlerFinal = (id) => {
        const data = [...finalAddOn];
        if (data.includes(id) !== true) {
            data.push(id);
        }
        else {
            const idx = data.findIndex(d => d === id);
            data.splice(idx, 1);
        }
        console.log(data);
        setFinalAddOn(data);
    }



    let content;

    content = addOns.map((addon) => (
        <ListItem button key={addon.id}>
            <Checkbox
                value={addon.id}
                onChange={(e) => { addOnHandler(e) }} />
            <ListItemText secondary={`FCFA ${addon.price}`} primary={`${addon.name}`} />
        </ListItem>
    ))

    return (
        <Dialog onClose={handleClose} aria-labelledby="simple-dialog-title" open={open}>
            <IconButton aria-label="close" className={classes.closeButton} onClick={onClose}>
                <CloseIcon size={10} />
            </IconButton>
            <DialogTitle
                id="simple-dialog-title"
                style={styles.dialogTitle}>
                Add Ons(Optional)
            </DialogTitle>
            <Divider />
            <List>
                {content}
            </List>
            <Button variant="contained" color="primary" onClick={handleAdd}>
                Add
            </Button>
        </Dialog>
    );
}

const styles = {
    dialogTitle: {
        fontWeight: "bold",
        marginLeft: "20px",
        marginRight: "20px"
    }
}

export default AddOnModal;