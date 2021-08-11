import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';



const PrivateRoute = ({
    component: Component,
    auth: { isAuthenticated, loading },
    ...rest
}) => (
    <Route
         // ..rest의 내용은 exact, path='/checkout' props임
        {...rest}
        render={props => !isAuthenticated && !loading ? (
            // 만약 유저가 인증되지 않은 유저일경우 로그인 하도록 리다이렉트
            <Redirect to='/login' />
        ) : (
            // 인증된 경우 checkout page로 이동
            <Component {...props} />
        )}
    />
);

const mapStateToProps = state => ({
    auth: state.auth
});

export default connect(mapStateToProps, {})(PrivateRoute);