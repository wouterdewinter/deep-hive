import React from 'react';

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

        return (
            <div className={"metric metric-" + this.props.id}>
                <div className="label">{this.props.label}</div>
                <div className="value">{value}</div>
            </div>
        );
    }
}

Metric.defaultProps = {
    type: 'default'
};
