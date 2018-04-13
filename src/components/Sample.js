import React from 'react';
import * as FontAwesome from 'react-icons/lib/fa'

export default class Grid extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        let url = 'http://localhost:5000/image/test/' + this.props.image_id;

        let icon;

        if (this.props.score === "1") {
            icon = <div className="score correct"><FontAwesome.FaCheckCircle /></div>;
        } else {
            icon = <div className="score incorrect"><FontAwesome.FaTimesCircle /></div>;
        }

        return (
            <div className="sample">
                <img src={url} />
                {icon}
                <div className="label">{this.props.label}</div>
            </div>
        );
    }
}