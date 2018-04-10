import React from 'react';

export default class Status extends React.Component {
    constructor(props) {
        super(props);
        this.state = {accuracy: 0}
    }

    componentDidMount() {
        let intervalId = setInterval(this.timer.bind(this), 1000);

        // store intervalId in the state so it can be accessed later:
        this.setState({intervalId: intervalId});
    }

    componentWillUnmount() {
        // use intervalId from the state to clear the interval
        clearInterval(this.state.intervalId);
    }

    timer() {
        // workaround for undefined this
        let setter = this.setState.bind(this);


        fetch('http://localhost:5000/status')
            .then(function (response) {
                console.log(3);
                return response.json();
            })
            .then(function (data) {
                console.log(data);
                setter({accuracy: data.accuracy});
            });

    }

    render() {
        return (
            <div className="status">
                Accuracy {this.state.accuracy}
            </div>
        );
    }
}