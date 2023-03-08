// console.log("hello");
document.body.onload = function() {
    let elem = document.getElementById('algo-type');
    // console.log(elem);
    eel.get_algo_names_python()((result) => {
        // console.log(result)
        Object.keys(result).forEach(element => {
            let d = document.createElement('option');
            d.value = result[element];
            d.innerText = element;
            elem.appendChild(d);
        });
    });
    let form = document.getElementById('entry');
    form.addEventListener('submit', validate, false)
    form = document.getElementById("inputform");
    form.addEventListener('submit', validateCalculation, false)
    // debugger;
}

window.onresize = function() {
    let h = calcHeight(gchart)
    setChartdim(window.innerWidth, h)
    drawGChart(gchart);
}

processes = {}

function getRow(...args) {
    let tr = document.createElement('tr');
    // console.log("here")
    let i = 0;
    while (i < 8) {
        let td = document.createElement('td');
        td.innerText = i < args.length? args[i]: "";
        tr.appendChild(td);
        i++;
    }
    let td = document.createElement('td');
    let button = document.createElement('button');
    button.classList.add('button', '**is-large', 'is-success', 'is-rounded')
    button.onclick = (e) => {
        delete processes[tr.children[0].innerText];
        tr.parentElement.removeChild(tr);
    }
    button.value = 'x';
    button.innerText = 'x';
    td.appendChild(button);
    tr.classList.add('active')
    tr.appendChild(td);
    return tr;
}

function validate(e) {
    e.preventDefault()
    e.returnValue = false;
    // debugger;
    let elem = document.getElementById('outtable');
    let data = new FormData(e.target);
    let p = {};
    let name = data.get('p-name');
    p['priority'] = data.get('p-pri');
    p['arrival_time'] = data.get('p-at');
    p['burst_time'] = data.get('p-bt');
    if (! (name in processes)) {
        processes[name] = p;
        let tr = getRow(name, p['priority'], p['arrival_time'], p['burst_time'])
        p['row'] = tr;
        // let tr = document.createElement('tr');
        elem.appendChild(tr);
    } else {
        let tr = getRow(name, p['priority'], p['arrival_time'], p['burst_time'])
        // console.log(processes[name].row);
        elem.insertBefore(tr, processes[name].row)
        elem.removeChild(processes[name].row)
        p['row'] = tr;
        processes[name] = p;
    }
    // console.log("hmmm")
    // debugger;

    return false;
}

function validateCalculation(e) {
    e.preventDefault();
    e.returnValue = false;
    calculateScheduling()
    return false;
}

function calculateScheduling() {
    let s = "True "
    
    let tq = document.getElementById('time_quantum').value
    if (Number(tq) == NaN) {
        s += "False\n"
    } else {
        s += tq + '\n';
    }
    
    Object.keys(processes).forEach(key1 => {
        let obj = processes[key1]
        s += [key1, obj.priority, obj.arrival_time, 'c' + obj.burst_time].join(" ")
        s += '\n'
    })
    s =s.slice(0,-1);

    let sel = document.getElementById('algo-type');

    eel.calculate_scheduling_python(s, sel.value)(function (result) {
        drawGChart(result['gant_chart']);
        // console.log(result);
        setRows(4, result['ct_list'])
        setRows(5, result['tat_list'])
        setRows(6, result['wt_list'])
        setRows(7, result['rt_list'])
    })
}

function setRows(num, ct_list) {
    // debugger;
    let table = document.getElementById('outtable');
    for (key in ct_list) {
        for (l of table.children) {
            if (l.children[0].innerText == key) {
                l.children[num].innerText = ct_list[key]
            }
        }
    }
}

colorMap = new Map()

function getColor(name) {
    if (colorMap.has(name)) return colorMap.get(name)
    rint = Math.floor(Math.random() * 360);
    let val;
    if (name === null) val =  [`#000000`, 'black']
    else val = [`hsl(${rint}, 90%, 50%)`, `hsl(${rint}, 90%, 20%)`]
    colorMap.set(name, val)
    return val
}

var gchart = []

function calcHeight(chart) {
    let can_elem = document.querySelector('#chart > canvas');
    let ctx = can_elem.getContext("2d");
    let m = 50;
    let cw = 0;
    let ch = m + 60;
    let nr = 1;
    for (key in chart) {
        let x = chart[key]
        let dim = ctx.measureText(x[1])
        let t = dim.width <= 60 || x[1] == null ? 60 : dim.width;
        if ((cw + t + 2 *m) > can_elem.width) {
            nr++;
            cw = 0
        } else {
            cw += t;
        }
    }
    nr++;
    ch = nr * 60 + (nr + 1) * 50;
    console.log("number of rows: " ,nr)
    console.log('calculated height:', ch);

    return ch;

}

function setChartdim(width, height) {
    let chartdiv = document.getElementById('chart');
    let canv = document.querySelector('#chart > canvas');
    canv.width = chartdiv.clientWidth
    canv.height = height
}

function drawGChart(chart) {
    gchart = chart
    let calh = calcHeight(gchart);
    let can_elem = document.querySelector('#chart > canvas');
    setChartdim(window.innerWidth, calh)
    let ctx = can_elem.getContext('2d');
    // console.log(ctx.fillStyle)
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, can_elem.width, can_elem.height);
    let pos = [50, 50];
    for (key in chart) {
        let box_size_x = 60
        let box_size_y = 60
        let x = chart[key]
        // console.log(pos)
        colr = getColor(x[1])
        ctx.fillStyle = colr[0];
        // console.log('HSL: ', colr)
        ctx.font = "30px Arial";
        let dim = ctx.measureText(x[1])
        // console.log(x[1])
        // console.log( pos[0] + (box_size_x-dim.width) / 2, pos[1] + box_size_y/2 )
        if (x[1] != null) {
            // console.log("Box size: ", box_size_x);
            // console.log("Dimension Text: ", dim.width);
            if (dim.width > box_size_x) box_size_x = dim.width;
            // console.log("Box size: ", box_size_x);
            // console.log("Dimension Text: ", dim.width);
            if (pos[0] + box_size_x + 50 > can_elem.width) {
                pos[0] = 50;
                pos[1] += 50 + box_size_y;
            }
            ctx.textBaseline = "center";
            ctx.fillRect(pos[0], pos[1], box_size_x, box_size_y)
            ctx.fillStyle = colr[1]
            ctx.fillText(x[1], pos[0] + (box_size_x-dim.width) / 2, pos[1] + (box_size_y)/2)
        } else {
            if (pos[0] + box_size_x + 50 > can_elem.width) {
                pos[0] = 50;
                pos[1] += 50 + box_size_y;
            }
            ctx.fillRect(pos[0], pos[1], box_size_x, box_size_y);
        }
        ctx.beginPath();
        ctx.rect(pos[0], pos[1], box_size_x, box_size_y);
        ctx.stroke();
        ctx.closePath();
        ctx.font = "20px Arial";
        ctx.fillStyle = "black";
        ctx.fillText(x[0], pos[0], pos[1] + box_size_y + 25)
        ctx.fillText(x[2], pos[0] + box_size_x, pos[1] + box_size_y + 25)
        // ctx.fillText("hello", 0 , 0)
        pos[0] += box_size_x;
    }
}