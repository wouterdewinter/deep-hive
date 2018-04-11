import React from 'react';

export default class Grid extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        let url = 'http://localhost:5000/image/train/' + this.props.image_id;
        let className = 'label ' + (this.props.score === "1" ? 'correct' : 'incorrect');
        return (
            <div className="sample">
                <img src={url} />
                <div className={className}>Rose</div>
            </div>
        );
    }
}