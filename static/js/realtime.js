var server = "127.0.0.1"
var last_plate = ""

$(document).ready(function(){


$.get( "/patentes/default/call/json/get_plates", function( data ) {

window.arrest = data

})

$.web2py.web2py_websocket('ws://'+ server +':8888/realtime/get_plates', function(e){

window.arrest = e.data

})

$.web2py.web2py_websocket('ws://'+ server +':8888/realtime/live_stream', function(e){
	var data = window.arrest

	var plate = JSON.parse(e.data)
	if (last_plate != plate.results[0].plate.toUpperCase()) {
		for (var i = 0; i < data.arrest.length; i++) {
			if (data.arrest[i].plate.toUpperCase() == plate.results[0].plate.toUpperCase()) {
				//Add to stream
				$("<tr class='danger'><td>"+  plate.site_id +"</td>"+
				"<td>"+  plate.camera_id +"</td>"+
				"<td><strong>"+  plate.results[0].plate +"</strong></td>"+
				"<td>"+  parseInt(plate.results[0].confidence) +"</td>"+
				"<td>"+  epoch(plate.epoch_time) +"</td>"+
				"<td> <img src='/patentes/static/plates/"+  plate.uuid + ".jpg' width='200px' height='100px'></td></tr>").prependTo("table > tbody")

				//Add to recent alerts
				$('<li class="list-group-item"><strong>'+ plate.results[0].plate + "</strong><br/>" +
				epoch(plate.epoch_time) + "<br/>" +
				plate.site_id + "<br/>" +
				"<strong>Delito: " + data.arrest[i].arrest_reason + "</strong><br/>" +
				"<strong>Conductor: " + data.arrest[i].driver_information + "</strong><br/>" +
				'</li>').prependTo(".list-group")
				var plate_hit = true;
				break
			}
		}
		if (!plate_hit) {
			$("<tr><td>"+  plate.site_id +"</td>"+
			"<td>"+  plate.camera_id +"</td>"+
			"<td><strong>"+  plate.results[0].plate +"</strong></td>"+
			"<td>"+  parseInt(plate.results[0].confidence) +"</td>"+
			"<td>"+  epoch(plate.epoch_time) +"</td>"+
			"<td> <img src='/patentes/static/plates/"+  plate.uuid + ".jpg' width='200px' height='100px'></td></tr>").prependTo("table > tbody")
		}
		last_plate = plate.results[0].plate.toUpperCase()
	}
})

})