import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App'
import './style.css'
import Status from './components/Status'
import Config from './Config.json'

import { HashRouter, Route, Switch} from 'react-router-dom'

ReactDOM.render(
    <HashRouter>
        <Switch>
            <Route exact path='/' component={App}/>
            <Route path='/dashboard' render={() => <Status short_url={Config.short_url} />}/>
        </Switch>
    </HashRouter>,
    document.getElementById('app')
);

module.hot.accept();