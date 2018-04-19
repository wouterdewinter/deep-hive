import React from 'react';

export default class Chart extends React.Component {

    constructor(props) {
        super(props);
    }

    componentDidMount() {
        let svg = d3.select("svg#" + this.props.id);
        let g = svg.append("g");

        g.append("path")
            .attr("fill", "none")
            .attr("stroke", "#408feb")
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("stroke-width", 3);

        this.update();
    }

    componentDidUpdate() {
        this.update();
    }

    update() {
        let svg = d3.select("svg#" + this.props.id);

        let rect = svg.node().getBoundingClientRect();

        let width = rect.width;
        let height = rect.height;


        let x = d3.scaleLinear()
            .rangeRound([width, 0]).domain([0,300]);

        let y = d3.scaleLinear()
            .rangeRound([height, 0]).domain([0,1]);

        let line = d3.line()
            .x(function(d, i) { return x(i); })
            .y(function(d) { return y(d); });

        let path = d3.select("path");
        path.attr("d", line(this.props.data));
    }

    render() {
        return (
            <svg className='chart' id={this.props.id}></svg>
        );
    }
}

Chart.defaultProps = {
    id: 'chart'
};

