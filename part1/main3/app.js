var mcs = require('mcsjs');
var SerialPort = require("serialport").SerialPort
var serialPort = new SerialPort("/dev/ttyS0",
{baudrate: 57600
});


var myApp = mcs.register({
        deviceId: 'D0RvxcCV',
        deviceKey: 'UoUukagjMzRMG71z',
});

console.log('Start Program!');

serialPort.on("open", function () {
        receivedData = "";
        serialPort.on('data',function(data)
        {
                receivedData = data.toString();
                console.log(receivedData);


                if(receivedData.indexOf('s') >= 0 ){
						type  = receivedData.substring(receivedData.indexOf('s')+1,receivedData.indexOf('g'));
                        myApp.emit('disaster','', 0);
                        myApp.emit('disaster_type','', type);
						console.log('Safe!');
                }
                else{
						type  = receivedData.substring(0,receivedData.indexOf('g'));
                        myApp.emit('disaster','', 1);
						myApp.emit('disaster_type','', type);
						console.log('Danger!');
						console.log(type);
                }
                if(receivedData.indexOf('g') >= 0 && receivedData.indexOf('f') >=0 && receivedData.indexOf('e') >= 0){
                        sensor[0] = receivedData.substring(receivedData.indexOf('g')+1,receivedData.indexOf('f'));
                        sensor[1] = receivedData.substring(receivedData.indexOf('f')+1, receivedData.indexOf('e'));
                        sensor[2] = receivedData.substring(receivedData.indexOf('e')+1, receivedData.indexOf('o'));
                        console.log(sensor[0]);
                        console.log(sensor[1]);
                        console.log(sensor[2]);

                        myApp.emit('gas_sensor','', sensor[0]);
                        myApp.emit('flame_sensor','', sensor[1]);
                        myApp.emit('earthquake_sensor','', sensor[2]);
                }
        });
});



