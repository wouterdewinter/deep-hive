import React from 'react';
import Chart from './Chart'

export default class Metric extends React.Component {

    render() {
        let value = Number(this.props.value);

        if (value === undefined) {
            value = '-'
        } else if (this.props.type === 'percent') {
            value = (value * 100).toFixed(1) + '%'
        } else {
            value = Math.round(value)
        }

        let chart_id = 'chart-' + this.props.id;
        let chart = this.props.history ? <Chart data={this.props.history} id={chart_id} /> : '';

        return (
            <div className={"metric metric-" + this.props.id}>
                {chart}
                <div className="contents">
                    <div className="label">{this.props.label}</div>
                    <div className="value">{value}</div>
                </div>
            </div>
        );
    }
}

Metric.defaultProps = {
    type: 'default'
};
