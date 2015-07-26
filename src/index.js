var express = require('express');
var PythonShell = require('python-shell');
var path = require('path');
var bodyParser = require('body-parser');

var app = express();

app.use(express.static('public'));
app.use(bodyParser.json());

app.post('/genetic', function (req, res) {
	var options = {
		mode: 'json',
		pythonOptions: ['-u'],
		scriptPath: path.resolve(__dirname) + '/python',
		args: [
			'-fn', req.body.fn.replace(/\^/g, '**'),
			'-min', req.body.min,
			'-max', req.body.max,
			'-s', req.body.step,
			'-p', req.body.popCount,
			'-st', req.body.selectionType
		]
	};

	PythonShell.run('genetic.py', options, function (err, results) {
		if (err) {
			res.status(500).send(err);
			throw err;
		}

		res.send(results[0]);

	});
});

var server = app.listen(3000, function () {
	var port = server.address().port;

	console.log('Server listening at http://localhost:%s', port);
});