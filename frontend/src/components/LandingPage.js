import React from 'react';
import { Link } from 'react-router-dom';
import Card from './Card'

const landingPage = ({
    products_arrival,
    products_sold
}) => (
    <div className='container'>
        <div className='jumbotron mt-5'>
            <h1 className='display-4'>This is jumbotron mt-5's display-4</h1>
            <p className='lead'>This is p class, 'lead'</p>
            <hr className='my-4' />
            <p>Hello</p>
            <Link className='btn btn-primary btn-lg' to='/shop'>Shop</Link>
        </div>

        <section>
            <h2 className='mt-5 mb-5 display-4'>Newest Arrival</h2>
            <div className='row'>
                {
                    products_arrival &&
                    products_arrival !== null &&
                    products_arrival !== undefined &&
                    products_arrival.map((product, index) => (
                        <div key={index} className='col-4'>
                            <Card
                                product={product}
                            />
                        </div>
                    ))
                }
            </div>
        </section>

        <section>
            <h2 className='mt-5 mb-5 display-4'>Top Selling</h2>
            <div className='row'>
                {
                    products_sold &&
                    products_sold !== null &&
                    products_sold !== undefined &&
                    products_sold.map((product, index) => (
                        <div key={index} className='col-4'>
                            <Card
                                product={product}
                            />
                        </div>
                    ))
                }
            </div>


        </section>



    </div>

);

export default landingPage;