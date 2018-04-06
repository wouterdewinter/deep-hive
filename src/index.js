import React from 'react';
import ReactDOM from 'react-dom';
import Task from './components/Task'

const title = 'My Minimal React Webpack Babel Setup';

fetch('http://localhost:5000/task', {mode: 'cors'})
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        ReactDOM.render(
            <Task image={data.image} image_id={data.image_id} labels={data.labels} />,
            document.getElementById('app')
        );
    });

module.hot.accept();