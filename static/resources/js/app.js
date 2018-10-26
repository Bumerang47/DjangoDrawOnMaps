var DEF_ZOOM = 11;
var MAP = Object;

$( document ).ready(function() {
	MAP = L.map('mapid');
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(MAP);
	reqCoordRoads();
});

function reqCoordRoads() {
    // Запрос кординат всех дорог
	fetch('/roads/')
		.then(function(response) { return response.json(); })
		.then(function(roads) {
			var roadsList = JSON.parse(roads);
			var indexCenterRoad = Math.floor(roadsList[1]['coordinates'].length/2);
			var startPoint = roadsList[1]['coordinates'][indexCenterRoad];
			MAP.setView(new L.LatLng(startPoint[1], startPoint[0]), DEF_ZOOM);
			drawRoads(roadsList);
			return;
		})
}

function getAzsOfRoad(code) {
    // Запрос и изображение АЗС соотведствующих коду дороге
	fetch('/roads/'+code+'/of_azs/')
		.then(function(response) {
            if (response.status == 200){
                return response.json();
            }
            throw new SyntaxError("Ошибка в данных");
		})
		.then(function(azses) {
			var azsList = JSON.parse(azses);
			var points_azs = []
			layerAzs.clearLayers();
            for(var i=azsList.length-1; i >= 0; i--){
                var azs = azsList[i];
                points_azs.push({
                    type:azs['geomtype'],
                    coordinates:azs['coordinates']
                })
            }
            layerAzs.addData(points_azs).addTo(MAP);
			return;
		})
		.catch(function(e){
		    layerAzs.clearLayers();
		})
}

function drawRoads(listRoads) {
    // Изображение дорог
	var roadLines = [];
	for ( var i=listRoads.length-1; (i >= 0); i-- ){
		var road = listRoads[i];

		var coordRoad = {
			type:road['geomtype'],
			coordinates:road['coordinates'],
			properties:{
                code:road['road_code'],
                name:road['name'],
                length_km:road['length_km'],
			}
		};
		L.geoJSON(coordRoad,{
                className: 'baseRoad',
                onEachFeature: onEachRoads
            }).bindTooltip(function (layer) {
                return (layer.feature.geometry.properties.name +
                    '<br>' +
                    layer.feature.geometry.properties.length_km + ' km');
            }).addTo(MAP);
	}
	
}

function onEachRoads(feature, layer) {
    // Обработчик событий для дорог
    layer.on('mouseover', function (e) {
        $(e.target.getElement()).addClass("active");
    });
    layer.on('mouseout', function (e) {
        $(e.target.getElement()).removeClass("active");
    });
    layer.on('click', function (e) {
        getAzsOfRoad(layer.feature.geometry.properties.code)
    });
}

// Инициализация иконки контейнера
var canisterIcon = L.icon({
        iconUrl: '/static/css/images/oil-canister-red-pointer.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41]
    });

// Инициализация geoJson для точек АСЗ к дороге
var layerAzs = L.geoJson([],{
    pointToLayer: function(feature, latlng) {
        // присвоение иконки к точке АЗС (options - {icon: Icon} не сработал)
        return L.marker(latlng, {icon: canisterIcon});
    }
});

