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
                children.push(<td><Sample image_id={image_id} /></td>);
                image_id++;
            }
            //Create the parent and add the children
            table.push(<tr>{children}</tr>)
        }
        return table
    }


    render() {
        return (
            <table className="grid">
                {this.createTable()}
            </table>
        );
    }
}