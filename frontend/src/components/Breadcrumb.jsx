import React from 'react';

function BreadCrumb({ title, homeRoute }) {
    return (
        <nav aria-label="breadcrumb">
            <ol className="breadcrumb">
                <li className="breadcrumb-item">
                    <a href={homeRoute}>Home</a>
                </li>
                <li className="breadcrumb-item active" aria-current="page">
                    {title}
                </li>
            </ol>
        </nav>
    );
}

export default BreadCrumb;
