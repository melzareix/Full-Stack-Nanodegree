/*
 Foursquare API Constants.
 */
var CLIENT_ID = "BNM2EI5GCEEP4YXDFB3WB1DPB0Z3EKWJX5TGFWTYR0BRQ4OR";
var CLIENT_SECRET = "4X3YWTBFBOUQW31LE1TTRE2INBI0JLBEYGSSEXJMZPW2IOSY";
var SEARCH_LIMIT = 15;
var FSQ_REQUEST_URL = "https://api.foursquare.com/v2/venues/search?&client_id=" +
    CLIENT_ID + "&client_secret=" + CLIENT_SECRET +
    "&v=20170127&near=Dubai&limit=" + SEARCH_LIMIT;

/*
 GLOBAL Variables
 */

var map = null;
var infoWindow = null;

/*
 Map Data Model.
 */

/*
* @description Represent's a location in the neighbourhood.
* @constructor
* @param {dict} data - the information about the location.
* */
var MapModel = function (data) {
    var self = this;

    this.name = data.name;
    this.lng = data.lng;
    this.lat = data.lat;
    this.city = data.city;
    this.state = data.state;
    this.phone = data.phone;
    this.country = data.country;
    this.url = data.url;

    this.address = ko.pureComputed(function () {
        return self.city + " " + self.state + ", " + self.country;
    });

    this.marker = data.marker;
    this.visibleMarker = ko.observable(true);
    this.infoWindowContent = data.infoWindowContent;
};

var AppViewModel = function () {
    var self = this;

    this.locations = ko.observableArray();
    this.filterText = ko.observable("");

    /*
    @description Event handler for LocationList Item Click event.
    */
    this.showItemInfo = function (e) {
        infoWindow.setContent(e.infoWindowContent);
        infoWindow.open(map, e.marker);
        toggleBounce(e.marker);
    };

    this.loadLocations = function (req_url) {
        $.getJSON(req_url, function (data) {
            var venues = data.response.venues;
            for (var i = 0; i < venues.length; i++) {
                var venue = venues[i];
                var marker = new google.maps.Marker({
                    map: null,
                    animation: google.maps.Animation.DROP,
                    position: {lat: venue.location.lat, lng: venue.location.lng},
                    title: venue.name
                });
                var ModelVenue = new MapModel({
                    'name': venue.name,
                    'lat': venue.location.lat,
                    'lng': venue.location.lng,
                    'phone': venue.contact.phone || "",
                    'city': venue.location.city || "",
                    'state': venue.location.state || "",
                    'country': venue.location.country || "",
                    'url': venue.url || "",
                    'marker': marker
                });
                ModelVenue.infoWindowContent = createInfoWindow(ModelVenue);

                self.locations.push(ModelVenue);
            }
            initMap();
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alertify.error('An error occurred trying to fetch data. <br />' + errorThrown);
        });
    };

    this.filteredLocations = ko.computed(function () {
        var ans = [];
        for (var i = 0; i < self.locations().length; i++) {
            var currLoc = self.locations()[i];
            if (currLoc.name.toLowerCase().indexOf(self.filterText().toLowerCase()) !== -1) {
                currLoc.visibleMarker(true);
                ans.push(currLoc);
            } else {
                currLoc.visibleMarker(false);
            }
        }
        return ans;
    });
};

var vm = new AppViewModel();
ko.applyBindings(vm);
vm.loadLocations(FSQ_REQUEST_URL);
vm.filteredLocations.subscribe(function () {
    editMap();
});

$('.clk').on('click', function (e) {
    e.stopPropagation();
    $('.main-container').toggleClass('m_sidebar_shown');
    $('.sidebar').toggleClass('sidebar_shown');
});

function editMap() {
    if (map == null)
        return;
    var bounds = new google.maps.LatLngBounds();
    var locations = vm.locations();

    for (var x = 0; x < locations.length; x++) {
        var marker = locations[x].marker;
        marker.setMap(locations[x].visibleMarker() ? map : null);
        bounds.extend(marker.position);
    }
    map.fitBounds(bounds);
}

function initMap() {
    var bounds = new google.maps.LatLngBounds();

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 30
    });

    var locations = vm.locations();
    infoWindow = new google.maps.InfoWindow();

    for (var x = 0; x < locations.length; x++) {
        var currentLocation = locations[x];
        var marker = locations[x].marker;
        bounds.extend(marker.position);
        marker.setMap(map);
        marker.addListener('click', function (x, marker) {
            return function () {
                infoWindow.setContent(locations[x].infoWindowContent);
                infoWindow.open(map, marker);
                toggleBounce(marker);
            }
        }(x, marker));
    }
    map.fitBounds(bounds);
}

function setupInfoWindow(e){
    infoWindow.setContent(e.infoWindowContent);
    infoWindow.open(map, e.marker);
    toggleBounce(e.marker);
}

function toggleBounce(marker) {
    if (marker.getAnimation() !== null) {
        marker.setAnimation(null);
    } else {
        marker.setAnimation(google.maps.Animation.BOUNCE);
        setTimeout(function () {
            marker.setAnimation(null);
        }, 1000);
    }
}

function createInfoWindow(location) {
    return "<div id='content'>" +
        "<h3 id='firstHeading' class='firstHeading'>" + location.name + "</h3>" +
        "<p>" + location.address() + "</p>" +
        "<a href='tel:" + location.phone + "'>" + location.phone + "</a><br />" +
        "<a href='" + location.url + "'>" + location.url + "</a>" +
        "</div>";
}