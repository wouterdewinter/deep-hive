import React from 'react';

export default class Chart extends React.Component {

    constructor(props) {
        super(props);
    }

    componentDidUpdate() {
        //console.log(this.props.data)
        this.update();
    }
    componentDidMount() {
        this.update();
    }

    update() {
        let path = d3.select("path");
        path.datum(this.props.data);

        var svg = d3.select("svg"),
            //margin = {top: 20, right: 20, bottom: 30, left: 300},
            margin = {top: 0, right: 0, bottom: 0, left: 0},

            width = +svg.attr("width") - margin.left - margin.right,
            height = +svg.attr("height") - margin.top - margin.bottom,
            g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        console.log(width, height);

        var x = d3.scaleTime()
            .rangeRound([width, 0]);

        var y = d3.scaleLinear()
            .rangeRound([height, 0]);

        var line = d3.line()
            .x(function(d, i) { return x(i); })
            .y(function(d) { return y(d); });

        var data = this.props.data;

        x.domain(d3.extent(data, function(d, i) { return i; }));
        y.domain(d3.extent(data, function(d) { return d; }));

        // g.append("g")
        //     .attr("transform", "translate(0," + height + ")")
        //     .call(d3.axisBottom(x))
        //     .select(".domain")
        //     .remove();
        //
        // g.append("g")
        //     .call(d3.axisLeft(y))
        //     .append("text")
        //     .attr("fill", "#eee")
        //     .attr("transform", "rotate(-90)")
        //     .attr("y", 6)
        //     .attr("dy", "0.71em")
        //     .attr("text-anchor", "end")
        //     .text("Price ($)");

        g.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("stroke-width", 4.5)
            .attr("d", line);
    }

    render() {
        return (
            <svg id="chart" width="300" height="200"></svg>
        );
    }
}
