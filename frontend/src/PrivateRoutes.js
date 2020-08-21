import React, { useEffect } from 'react';
import { Route, Redirect } from 'react-router-dom';
import { useAuthContext } from './Context/AuthContext';

function PrivateRoute({ component: Component, ...rest }, props) {
    const { token } = useAuthContext();
    useEffect(() => {
        console.log(token)
    }, [])
    return (
        <Route {...rest}
            render={(props) =>
                token !== null ?
                    (
                        <Component {...rest} {...props} />
                    ) :
                    (
                        <Redirect to={{ pathname: "/login", state: { referer: props.location } }} />
                    )
            }
        />
    )
}

export default PrivateRoute;