$(document).ready(function () {

    var map;
    var iterator = 0;

    var contentString = [
        '<div class="infobox-inner"><a href="08_Properties_Single.html"><img src="assets/img/icon-1.png" alt=""/><span>Sarkkara Villa</span></a></div>',
        '<div class="infobox-inner"><a href="08_Properties_Single.html"><img src="assets/img/icon-2.png" alt=""/><span>Sarkkara Flat</span></div>',
        '<div class="infobox-inner"><a href="08_Properties_Single.html"><img src="assets/img/icon-3.png" alt=""/><span>Sarkkara Commercial</span></div>',
        '<div class="infobox-inner"><a href="08_Properties_Single.html"><img src="assets/img/icon-4.png" alt=""/><span>Sarkkara Appartment</span></a></div>'
    ];

    function initialize() {
        map = new google.maps.Map(document.getElementById('map-canvas'), {
            zoom: 15,
            center: new google.maps.LatLng(43.26167, -79.9195) //Hamilton
        });
        setTimeout(function () {
            drop();
        }, 1000);

    }

    function addMarker() {
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
        }, 200);

      /*  google.maps.event.addListener(marker, 'click', function () {
            if (!infoBubble.isOpen()) {
                infoBubble.open(map, marker);
            }
            else {
                infoBubble.close(map, marker);
            }
        });
*/
        iterator++;
    }

    google.maps.event.addDomListener(window, 'load', initialize);

});

//html shit
<script>
// This example displays an address form, using the autocomplete feature
// of the Google Places API to help users fill in the information.

function initialize() {
    var defaultBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(43.24684388944852, -79.9451494216919),

    var input = /** @type {HTMLInputElement} */(
        document.getElementById('search-input'));

        // Create the autocomplete object, restricting the search
        // to geographical location types.
    var autocomplete = new google.maps.places.Autocomplete((input),{ bounds: defaultBounds, types: ['geocode'] });

    var infowindow = new google.maps.InfoWindow();

    google.maps.event.addListener(search-input, 'place_changed', function() {
        infowindow.close();
        var place = autocomplete.getPlace();
        if (!place.geometry) {
          return;
        }

        var address = '';
        if (place.address_components) {
          address = [
            (place.address_components[0] && place.address_components[0].short_name || ''),
            (place.address_components[1] && place.address_components[1].short_name || ''),
            (place.address_components[2] && place.address_components[2].short_name || '')
          ].join(' ');
        }

        infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
        infowindow.open(map);
    });
}
google.maps.event.addDomListener(window, 'load', initialize)
</script>
<div class="google-maps">
        <div class="gmap-search">
            <input id="search-input" placeholder="Enter an address" type="text" name="streetADDR" value="{{streetADDR}}"></input>
        </div>
        
    </div>