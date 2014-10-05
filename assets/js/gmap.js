$(document).ready(function () {

    var placeSearch, autocomplete;
    var componentForm = {
        street_number: 'short_name',
        route: 'long_name',
        locality: 'long_name',
        administrative_area_level_1: 'short_name',
        country: 'long_name',
        postal_code: 'short_name'
    };

    function initialize() {
        var mapOptions = {
            center: new google.maps.LatLng(43.26167, -79.9195), //Hamilton
            zoom: 15
        };

        var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
        var defaultBounds = new google.maps.LatLngBounds(
            new google.maps.LatLng(43.24684388944852, -79.9451494216919),
            new google.maps.LatLng(43.26711256817906, -79.89468097686768));
        var input = /** @type {HTMLInputElement} */(
            document.getElementById('search-input'));
          
        var types = document.getElementById('type-selector');
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        // Create the autocomplete object, restricting the search
        // to geographical location types.
        autocomplete = new google.maps.places.Autocomplete((input),{ bounds: defaultBounds, types: ['geocode'] });
        // When the user selects an address from the dropdown,
        // populate the address fields in the form.   
        google.maps.event.addListener(autocomplete, 'place_changed', function() {
            fillInAddress();
        });
    }

    function fillInAddress() {
        // Get the place details from the autocomplete object.
        var place = autocomplete.getPlace();
        var temp = place.address_components[0].long_name + " " + place.address_components[1].long_name + ", " + place.address_components[3].long_name + ", " + place.address_components[5].short_name + ", " + place.address_components[6].long_name;
        
        console.log(temp);
        
        document.getElementById("hiddenField").value = temp;
        document.getElementById("searchForm").submit();
    
        /*      
        for (var component in componentForm) {
            document.getElementById(component).value = '';
            document.getElementById(component).disabled = false;
        }

        // Get each component of the address from the place details
        // and fill the corresponding field on the form.
        for (var i = 0; i < place.address_components.length; i++) {
            var addressType = place.address_components[i].types[0];
            if (componentForm[addressType]) {
                var val = place.address_components[i][componentForm[addressType]];
                document.getElementById(addressType).value = val;
            }
        }*/
    }
    google.maps.event.addDomListener(window, 'load', initialize);
});