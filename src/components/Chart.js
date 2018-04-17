import React from 'react';

export default class Chart extends React.Component {

    constructor(props) {
        super(props);
    }

    componentDidMount() {
        let svg = d3.select("svg"),
            g = svg.append("g");

        let rect = svg.node().getBoundingClientRect();

        let width = rect.width;
        let height = rect.height;

        let x = d3.scaleLinear()
            .rangeRound([width, 0]).domain([0,100]);

        let y = d3.scaleLinear()
            .rangeRound([height, 0]).domain([0,1]);

        this.line = d3.line()
            .x(function(d, i) { return x(i); })
            .y(function(d) { return y(d); });

        g.append("path")
            .attr("fill", "none")
            .attr("stroke", "#fff")
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("stroke-width", 4.5);

        this.update();
    }

    componentDidUpdate() {
        this.update();
    }

    update() {
        let path = d3.select("path");
        path.attr("d", this.line(this.props.data));
    }

    render() {
        return (
            <svg id="chart"></svg>
        );
    }
}
