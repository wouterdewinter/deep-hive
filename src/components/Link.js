import React from 'react';
import { QRCode } from 'react-qr-svg';

export default class Link extends React.Component {

    render() {
        return (
            <div className="metric link">
                <div className="url">{this.props.url}</div>
                {/*<div className="qr"><QRCode
                    level="Q"
                    style={{ width:  150 }}
                    value={this.props.url}
                /></div>*/}
            </div>
        );
    }
}