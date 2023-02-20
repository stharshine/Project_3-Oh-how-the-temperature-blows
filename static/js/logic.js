console.log("logic.js")
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
        for (i=0; i < resultArray.length; i++) {
            let row = tbody.append("tr");
            Object.entries(resultArray[i]).forEach(([key, value]) => {
                // console.log(key + " " + value)
                let cell = row.append("td");
                cell.text(value);
            });
        }
    })
}