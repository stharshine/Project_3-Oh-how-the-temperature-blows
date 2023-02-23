//console.log("wind-table.js")

var selector = d3.select("#selCity");

d3.json("/cityList").then(function (cities) {
    // console.log("cities")
    // console.log(cities)
    selector
        .append("option")
        .text("Select a city")
        .property("value", "");
    cities.forEach((city) => {
        selector
            .append("option")
            .text(city)
            .property("value", city);
    });
})

function optionChanged(cityName) {
    d3.csv("/static/data/wind.csv").then(function (data) {
        // console.log("data")
        // console.log(data)

        var resultArray = data.filter(sampleObj => sampleObj.City == cityName);
        // console.log("resultArray")
        // console.log(resultArray)

        var tbody = d3.select("tbody");
        tbody.html("");

        timestamp_array = []
        y1_array = []
        y2_array = []

        for (i = 0; i < resultArray.length; i++) {

            let row = tbody.append("tr");

            Object.entries(resultArray[i]).forEach(([key, value]) => {

                let cell = row.append("td");
                cell.text(value);

                if (key == "Timestamp") {
                    // console.log("key= " + key + "  value=" + value)
                    timestamp_array.push(value)
                }
                else if (key == "Wind W-E") {
                    // console.log("key= " + key + "  value=" + value)
                    y1_array.push(value)
                }
                else if (key == "Wind E-W") {
                    //console.log("key= " + key + "  value=" + value)
                    y2_array.push(value)
                }
            });
        }

        var trace1 = {
            x: timestamp_array,
            y: y1_array,
            mode: 'lines+markers',
            name: 'Wind W-E'
        };

        var trace2 = {
            x: timestamp_array,
            y: y2_array,
            mode: 'lines+markers',
            name: 'Wind E-W'
        };

        var data = [trace1, trace2];

        var layout = {
            title: 'Line Plot of Timestamp and Wind'
        };

        Plotly.newPlot('myDiv', data, layout);
    })
}