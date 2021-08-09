import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import { check_authenticated, load_user, refresh } from '../actions/auth';
import Navbar from '../components/Navbar';
import { Redirect } from "react-router-dom";
import {
    get_items,
    get_item_total,
    get_total
} from '../actions/cart'

const Layout = ({
    check_authenticated,
    load_user,
    refresh,
    get_items,
    get_item_total,
    get_total,
    children
}) => {

    const [searchRedirect, setSearchRedirect] = useState(false);


    useEffect(() => {
        refresh();
        check_authenticated();
        load_user();
        get_items();
        get_item_total();
        get_total();
    }, []);

    if (searchRedirect){
        return (
            <div>
                <Navbar
                    setSearchRedirect={setSearchRedirect}
                    />
                <Redirect to='/search' />
            </div>
        )
    }


    return (
        <div>
            <Navbar
                setSearchRedirect={setSearchRedirect}
            />
            {children}
        </div>
    );
};

export default connect(null,
    {check_authenticated,
                     load_user,
                     refresh,
                     get_items,
                     get_item_total,
                     get_total
    })(Layout);