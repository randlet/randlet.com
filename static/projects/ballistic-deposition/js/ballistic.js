var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
canvas.width = canvas.parentNode.clientWidth;

var ncols = canvas.width;
var height = canvas.height;
var baseHeight = Math.floor(0.02*height);
var baseColor = "#000";
var colorA= "#FF0000";
var colorB= "#00FFFF";
var colorC= "#0000FF";
var colorD= "#FF00FF";

var heights = [];
heights.length = ncols;
for (var i=0; i < ncols; i++){
    heights[i]=0;
}

function drawBase(ctx){
    var col;
    var h;
    ctx.strokeStyle = baseColor;

    heights[0] = 0;

    for (col=1; col < ncols; col++){
        ctx.beginPath();
        ctx.moveTo(col, height-1);
        h = Math.floor(Math.random()*baseHeight);
        h = Math.max(0, heights[col-1] + 2*(Math.random()-0.5)*h);
        ctx.lineTo(col, height - h -1);
        heights[col] = h;
        ctx.stroke();
    }
}

drawBase(context);


function drawLine(){

    var col = Math.floor(Math.random()*ncols);
    var prev = col === 0 ? ncols - 1: col -1; // Math.max(0, col-1);
    var next = col === ncols - 1 ?  0: col + 1; // Math.min(col+1, ncols-1);

    var hc = heights[col];
    var hp = heights[prev];
    var hn = heights[next];

    var colHeight;
    var drawCol;

    if (hc >= hp && hc >= hn){
        bottom = hc;
        context.strokeStyle = colorA;
    }else{
        if (hp > hn){
            context.strokeStyle = colorB;
        }else if (hp==hn){
            context.strokeStyle = colorC;
        }else{
            context.strokeStyle = colorD;
        }

        bottom = Math.max(hp, hn)-1;
    }

    heights[col] = bottom + 1;
    context.beginPath();
    context.moveTo(col, height - bottom);
    context.lineTo(col, height - (bottom + 1));
    context.stroke();

    if (heights[col] >= 1.1*height){
        clearInterval(drawLoop);
    }

}


var drawLoop = setInterval(function(){for (var i=0; i<100; i++){drawLine()}}, 1);


