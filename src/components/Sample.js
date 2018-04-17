import React from 'react';
import * as FontAwesome from 'react-icons/lib/fa'

export default class Grid extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        let url = '/api/image/test/' + (this.props.image_id);

        let icon, className;

        if (this.props.score === "1") {
            icon = <FontAwesome.FaCheckCircle />;
            className = "sample correct"
        } else if (this.props.score === "0") {
            icon = <FontAwesome.FaTimesCircle />;
            className = "sample incorrect"
        } else {
            icon = <FontAwesome.FaQuestionCircle />;
            className = "sample"
        }

        let label;
        if (this.props.label) {
            label = <div className="label">{this.props.label}</div>;
        } else {
            label = ''
        }

        return (

            <div className={className}>
                <div className="overlay" />
                {label}
                <div className="score">
                    {icon}
                </div>
                <img src={url} />
            </div>
        );
    }
}