import React from 'react';
import Sample from './Sample'

export default class Grid extends React.Component {

    constructor(props) {
        super(props);
    }

    createTable () {
        let table = [];

        // Outer loop to create parent
        let image_id = 0;
        for (let i = 0; i < 6; i++) {
            let children = [];
            //Inner loop to create children
            for (let j = 0; j < 6; j++) {
                let score = this.props.test_scores[image_id] !== 'undefined' ? this.props.test_scores[image_id] : -1;
                let class_id = this.props.test_labels[image_id] !== 'undefined' ? this.props.test_labels[image_id] : -1;
                let label = this.props.labels[class_id];
                children.push(<td key={j}><Sample image_id={image_id} score={score} label={label}/></td>);
                image_id++;
            }
            //Create the parent and add the children
            table.push(<tr>{children}</tr>)
        }
        return table
    }


    render() {
        console.log(this.props);

        return (
            <table className="grid">
                <tbody>{this.createTable()}</tbody>
            </table>
        );
    }
}