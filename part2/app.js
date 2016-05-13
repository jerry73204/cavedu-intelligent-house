var mcs = require('mcsjs');
var SerialPort = require("serialport").SerialPort
var serialPort = new SerialPort("/dev/ttyS0",
{baudrate: 57600
});


var myApp = mcs.register({
        deviceId: 'D7YhDuc0',
        deviceKey: 'YkAZ68cFpKXK0HAv',
});

console.log('Start Program!');

serialPort.on("open", function () {
        receivedData ="";
        var sensor = new Array(4);
        serialPort.on('data',function(data)
        {
                receivedData =data.toString();
                console.log(receivedData);

		if(receivedData.indexOf('R')>=0 ){
                        myApp.emit('auto','',1);
                        myApp.emit('room','',0);
                        myApp.emit('Inside_degree','',0);
                        myApp.emit('outside_degree','',0);
                        myApp.emit('blackout','',0);
                        myApp.emit('living_color','',16777215);
                        myApp.emit('livingroom','',0);
                        myApp.emit('disaster','',0);
                }
                if(receivedData.indexOf('S')>=0 ){
                        myApp.emit('disaster','', 0);
                        console.log('Safe!');
                }
                else if(receivedData.indexOf('D')>=0){
                        myApp.emit('disaster','', 1);
                        console.log('Danger!');
                }
                else if(receivedData.indexOf('l')>=0 && receivedData.indexOf('i')>=0 && receivedData.indexOf('p')>=0 && receivedData.indexOf('s')>=0){
                        sensor[0] = receivedData.substring(receivedData.indexOf('l')+1,receivedData.indexOf('i'));
                        sensor[1] = receivedData.substring(receivedData.indexOf('i')+1, receivedData.indexOf('p'));
                        sensor[2] = receivedData.substring(receivedData.indexOf('p')+1, receivedData.indexOf('s'));
			sensor[3] = receivedData.substring(receivedData.indexOf('s')+1, receivedData.indexOf('e'));
                        console.log(sensor[0]);
                        console.log(sensor[1]);
                        console.log(sensor[2]);
			console.log(sensor[3]);

                        myApp.emit('blackout','', sensor[0]);
                        myApp.emit('outside_degree','', sensor[1]);
                        myApp.emit('inside_degree','', sensor[2]);
			myApp.emit('solar','',sensor[3]);
                }
        });
});

myApp.on('auto',function(data,time){

        if(Number(data)){
                console.log('auto');
        }
        else{
                console.log('manual');
        }

});

myApp.on('room',function(data,time){

        if(Number(data)){
                console.log('room on');
                serialPort.write("ro\r");
        }
        else{
                console.log('room off');
                meg = "rc";
                serialPort.write("rc\r");
        }
});
myApp.on('livingroom',function(data,time){

        if(Number(data)){
                console.log('livingroom on');
                serialPort.write("lo\r");
        }
        else{
                console.log('livingroom off');
                serialPort.write("lc\r");
        }


});

myApp.on('living_color',function(data,time){
        serialPort.write("c"+data);
        console.log('change color!');

});