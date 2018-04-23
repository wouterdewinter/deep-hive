import React from 'react';
import Grid from './Grid'
import Metric from './Metric'
import Link from './Link'

export default class Status extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            accuracy: 0,
            acc_history: [],
            test_scores: [],
            test_labels: [],
            annotation_count: 0,
            labels: []
        }
    }

    componentDidMount() {
        let intervalId = setInterval(this.timer.bind(this), 300);

        // store intervalId in the state so it can be accessed later:
        this.setState({intervalId: intervalId});
    }

    componentWillUnmount() {
        // use intervalId from the state to clear the interval
        clearInterval(this.state.intervalId);
    }

    updateAccHistory (acc) {
        let acc_history = this.state.acc_history.slice(0, 300);
        acc_history.unshift(acc);
        //acc_history.unshift( Math.random());
        this.setState({acc_history})
    }

    timer() {
        // workaround for undefined this
        let setter = this.setState.bind(this);
        let updateAccHistory = this.updateAccHistory.bind(this);


        fetch('/api/status')
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                updateAccHistory(data.accuracy);

                setter({
                    accuracy: data.accuracy,
                    test_scores: data.test_scores,
                    test_labels: data.test_labels,
                    annotation_count: data.annotation_count,
                    labels: data.labels
                });
            });

    }

    render() {
        return (
            <div className="status">
                <Metric id="accuracy" label="Accuracy" value={this.state.accuracy} type="percent" history={this.state.acc_history} />
                <Metric id="annotation_count" label="Annotation count" value={this.state.annotation_count} />
                <Link url="bit.ly/bfr18" />
                <Grid test_labels={this.state.test_labels} test_scores={this.state.test_scores} labels={this.state.labels} />
            </div>
        );
    }
}