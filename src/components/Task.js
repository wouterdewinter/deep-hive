import React from 'react';

export default class Task extends React.Component {

    constructor(props) {
        super(props);

        // This binding is necessary to make `this` work in the callback
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(e) {
        let data = {
            class_id: e.target.dataset.id,
            image_id: this.props.image_id
        };

        let handleComplete = this.props.handleComplete;

        fetch('/api/label', {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }, method: 'POST', body: JSON.stringify(data)
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data.result == 'ok') {
                    handleComplete()
                }
            });
    }

    render() {
        let image = this.props.image;

        return (
            <div className="task">
                <img src={image}/>
                <ul>
                    {this.props.labels.map((item, i) => <li key={i}>
                        <button data-id={i} onClick={this.handleClick}>{item}</button>
                    </li>)}
                </ul>
            </div>
        );
    }
}