import React from 'react';
import { QRCode } from 'react-qr-svg';

export default class Link extends React.Component {

    // Reset backend and clear model and metrics
    reset() {
        fetch('/api/reset')
    }

    render() {
        return (
            <div className="metric link">
                <div className="contents">
                    <div className="url">{this.props.url}</div>
                    <button onClick={this.reset}>Reset</button>
                </div>
                {/*<div className="qr"><QRCode
                    level="Q"
                    style={{ width:  150 }}
                    value={this.props.url}
                /></div>*/}
            </div>
        );
    }
}