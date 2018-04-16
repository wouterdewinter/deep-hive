import React from 'react';
import Sample from './Sample'

export default class Grid extends React.Component {

    constructor(props) {
        super(props);
    }

    createItems () {
        let items = [];
        for (let i = 0; i < 40; i++) {
            let score = this.props.test_scores[i] !== 'undefined' ? this.props.test_scores[i] : -1;
            let class_id = this.props.test_labels[i] !== 'undefined' ? this.props.test_labels[i] : -1;
            let label = this.props.labels[class_id];
            items.push(<Sample key={i} image_id={i} score={score} label={label} />);
        }
        return items
    }

    render() {
        return (
            <div className="grid">
               {this.createItems()}
            </div>
        );
    }

}