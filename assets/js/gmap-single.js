$(document).ready(function () {

    var map;
    var iterator = 0;
    var markers = [];
    var markerLatLng = [
        new google.maps.LatLng(43.26167, -79.9195)
    ];
    var contentString = [
        '<div class="infobox-inner"><img src="assets/img/icon-1.png" alt=""/><span>Sarkkara Apartment</span></div>'
    ];

    function initialize() {
        map = new google.maps.Map(document.getElementById('map-canvas'), {
            zoom: 15,
            center: new google.maps.LatLng(43.26167, -79.9195) //Berlin
        });
        setTimeout(function () {
            drop();
        }, 1000);
    }

    // animate markers
    function drop() {
        for (var i = 0; i < markerLatLng.length; i++) {
            setTimeout(function () {
                addMarker();
            }, i * 400);
        }
    }

    function addMarker() {
        var marker = new google.maps.Marker({
            position: markerLatLng[iterator],
            map: map,
            icon: 'assets/img/marker.png',
            draggable: false
            //,animation: google.maps.Animation.DROP
        });
        markers.push(marker);

        var infoBubble = new InfoBubble({
            map: map,
            content: contentString[iterator],
            position: markerLatLng[iterator],
            disableAutoPan: true,
            hideCloseButton: true,
            shadowStyle: 0,
            padding: 0,
            borderRadius: 3,
            borderWidth: 1,
            borderColor: '#74d2b2',
            backgroundColor: '#ffffff',
            backgroundClassName: 'infobox-bg',
            minHeight: 35,
            maxHeight: 230,
            minWidth: 200,
            maxWidth: 300,
            arrowSize: 5,
            arrowPosition: 50,
            arrowStyle: 0
        });

        setTimeout(function () {
            infoBubble.open(map, marker);
        }, 100);

        google.maps.event.addListener(marker, 'click', function () {
            if (!infoBubble.isOpen()) {
                infoBubble.open(map, marker);
            }
            else {
                infoBubble.close(map, marker);
            }
        });

        iterator++;
    }

    google.maps.event.addDomListener(window, 'load', initialize);

});
