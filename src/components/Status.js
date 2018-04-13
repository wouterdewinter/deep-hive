import React from 'react';
import Grid from './Grid'

export default class Status extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            accuracy: 0,
            test_scores: [],
            test_labels: [],
            labels: []
        }
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
                return response.json();
            })
            .then(function (data) {
                setter({
                    accuracy: data.accuracy,
                    test_scores: data.test_scores,
                    test_labels: data.test_labels,
                    labels: data.labels
                });
            });

    }

    render() {
        return (
            <div className="status">
                <div className="accuracy">Accuracy: {(this.state.accuracy * 100).toFixed(1)} %</div>
                <Grid test_labels={this.state.test_labels} test_scores={this.state.test_scores} labels={this.state.labels} />
            </div>
        );
    }
}