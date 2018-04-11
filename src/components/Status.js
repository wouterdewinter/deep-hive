import React from 'react';
import Grid from './Grid'

export default class Status extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            accuracy: 0,
            test_scores: [],
            test_labels: []
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
                console.log(3);
                return response.json();
            })
            .then(function (data) {
                console.log(data);
                setter({
                    accuracy: data.accuracy,
                    test_scores: data.test_scores,
                    test_labels: data.test_labels
                });
            });

    }

    render() {
        return (
            <div className="status">
                Accuracy {this.state.accuracy}
                <Grid test_labels={this.state.test_labels} test_scores={this.state.test_scores} />
            </div>
        );
    }
}