import React from 'react';
import Task from './Task'
import Grid from './Grid'
import Status from './Status'

export default class App extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            error: null,
            isLoaded: false,
            data: null
        };
    }

    componentDidMount() {
        this.newTask()
    }

    newTask() {
        fetch("http://localhost:5000/task")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        data: result
                    });
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    });
                }
            )
    }

    render() {
        const { error, isLoaded, data } = this.state;
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <div>
                    <Task image={data.image} image_id={data.image_id} labels={data.labels} handleComplete={this.newTask.bind(this)} />
                    <Status />
                    <Grid />
                </div>
            );
        }
    }
}