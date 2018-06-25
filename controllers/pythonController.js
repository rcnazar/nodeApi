'use strict';

let PythonShell = require('python-shell');
let AsyncLock = require('async-lock');

let lock = new AsyncLock();
let contador = 0;
let pyshell = new PythonShell('./externa/Simples.py', {
  mode: 'text',
  pythonOptions: ['-u'],
});
let resGlobal = null;

pyshell.on('message', function (message) {
  if (!message) return;

  //console.log(contador + ": evento python");
  resGlobal.res.sendData(message);
  resGlobal.next();
  resGlobal.done();
});

exports.executar = function (req, res, next) {
  lock.acquire("Simples.py", function(done) {
    contador++;
    //console.log(contador + ": lock enter")

    resGlobal = {
      res : res,
      next : next,
      done : done,
    };
 
    pyshell.send("rua " + contador);  
  }, function(err, ret) {
      //console.log(contador + ": lock release")
  }, {});

};


// let funcRemove = function () {
//   pyshell.removeListener('message', func);
// };

// var PythonShell = require('python-shell');
// PythonShell.run("./externa/Simples.py", function (err) {
//   if (err) throw err;
//   console.log('finished');
// });

// var spawn = require("child_process").spawn;
// var process = spawn('python', [
//     "./externa/Simples.py",
//     "primasdadheiro",
//     "segundo"]);

// process.stdout.on('data', function(data) {
//     console.log(data.toString());
// });

// pyshell.end(function (err,code,signal) {
//   if (err) throw err;
//   console.log('The exit code was: ' + code);
//   console.log('The exit signal was: ' + signal);
//   console.log('finished');
//   console.log('finished');
// });