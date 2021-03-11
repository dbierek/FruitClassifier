function getNext() {
    let div = document.getElementById('fruit-image-div');
    document.getElementById('next-button').disabled = true;
    fetch('/next')
        .then(response => {
            console.log("next/ response")
            console.log(response)
            return response.json()
        })
        .then(data => {
            console.log(data)
            console.log("Next Pressed")
            div.innerHTML = data.text;
            showFruitImageFeatures(data.features);
            document.getElementById('next-button').disabled = false;
        });
}
function showFruitImageFeatures(allFeatures) {
    for (let i = 0; i < allFeatures.length; i += 3) {
        var size = allFeatures[i].length;
        let squareSize = Math.floor(200 / size);
        dataset = [];
        for (var y = 0; y < size; y++) {
            var tempData = [size];
            for (var x = 0; x < size; x++) {
                colorR = 255 * allFeatures[i][y][x]
                colorG = 255 * allFeatures[i + 1][y][x]
                colorB = 255 * allFeatures[i + 2][y][x]
                tempData[x] = { x: x, y: y, color: "rgb(" + colorR + ", " + colorG + "," + colorB + ")" };
            };
            dataset.push(tempData);
        };

        d3.select("#fruit-image-div").append("svg")
            .attr("width", size * squareSize)
            .attr("height", size * squareSize)
            .selectAll("rect")
            .data(dataset)
            .enter()
            .append("g")
            .selectAll("rect")
            .data(function (d, i) { return d; })
            .enter()
            .append("rect")
            .attr("x", function (d) {
                return d.x * squareSize;
            })
            .attr("y", function (d) {
                return d.y * squareSize;
            })
            .attr("height", squareSize)
            .attr("width", squareSize)
            .attr("fill", function (d) {
                return d.color
            });
    }
    document.getElementById("next-button").addEventListener("click=", getNext);
}
getNext();