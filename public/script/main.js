$(function () {

	$('#caclBtn').click(function () {
		tClear();
		run();
	});

	function tClear() {
		$('#tables').empty();
	}

	function run() {

		var options = {
			fn: funct = "" + $("#f").val(),
			min: parseInt($("#min").val()),
			max: parseInt($("#max").val()),
			step: parseFloat($("#step").val()),
			popCount: parseInt($("#popCount").val()),
			selectionType: 'TOURNEY'

		};

		var data = [];

		for (var i = options['min']; i < options['max']; i += options['step']) {
			var scope = {
				x: i
			};
			data.push([i, math.eval(funct, scope)]);
		}

		$.plot("#placeholder", [data]);

		function renderPopTable(population) {
			var tData = "";

			population.individuals.sort(function (a, b) {
				if (a.fitness > b.fitness) return -1;
				else return 1;
			});


			for (var i = 0; i < population.individuals.length; i++) {
				tData += '<tr>' +
				'<td>' + i + '</td>' +
				'<td>' + (population.individuals[i].val * options['step']).toFixed(1) + '</td>' +
				'<td>' + population.individuals[i].fitness + '</td>' +
				'</tr>'
			}

			$('#tables').append(
				$('<table border="1px"><tr><td>№</td><td>Особи (10)</td><td>Приспособленость</td></tr>' + tData + '</table>')
			);
		}

		$.ajax({
			type: "POST",
			data: JSON.stringify(options),
			contentType: "application/json; charset=utf-8",
			dataType: 'json',
			url: "/genetic",
			success: function (result) {

				var $tables = $('#tables');

				$tables.append($('<div> First Population </div>'));
				renderPopTable(result.start_population);
				$tables.append($('<div> Last Population </div>'));
				renderPopTable(result.population);
				$tables.append($('<div> x = ' + result.x + ' </div>'));
			}
		});

	}
});
