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
    this.loc = data.loc;
    this.state = data.state;
    this.phone = data.phone;
    this.country = data.country;
    this.url = data.url;

    this.address = ko.pureComputed(function () {
        return self.loc + ", " + self.state + ", " + self.country;
    });

    this.marker = data.marker;
    this.visibleMarker = ko.observable(true);
    this.infoWindowContent = data.infoWindowContent;
};


/*
 * @description The ViewModel for the application.
 * */

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
            venues.forEach(function (venue) {
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
                    'loc': venue.location.address || "",
                    'state': venue.location.state || "",
                    'country': venue.location.country || "",
                    'url': venue.url || "",
                    'marker': marker
                });
                ModelVenue.infoWindowContent = createInfoWindow(ModelVenue);

                self.locations.push(ModelVenue);
            });

            // Load the markers on the map once the data arrives.
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

// Bind the view model to the View.
var viewModel = new AppViewModel();
ko.applyBindings(viewModel);


/*
 * @description Hides the markers for filtered-out locations.
 */

function editMap() {
    if (map == null)
        return;

    var bounds = new google.maps.LatLngBounds();
    viewModel.locations().forEach(function (location) {
        location.marker.setMap(location.visibleMarker() ? map : null);
        bounds.extend(location.marker.position);
    });
    map.fitBounds(bounds);
}

/*
 * @description Initializes the map object, and loads the location markers.
 * */
function initMap() {
    var bounds = new google.maps.LatLngBounds();

    infoWindow = new google.maps.InfoWindow();
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 30
    });


    viewModel.locations().forEach(function (currentLocation) {
        bounds.extend(currentLocation.marker.position);
        currentLocation.marker.setMap(map);
        currentLocation.marker.addListener('click', function (currentLocation) {
            return function () {
                infoWindow.setContent(currentLocation.infoWindowContent);
                infoWindow.open(map, currentLocation.marker);
                toggleBounce(currentLocation.marker);
            }
        }(currentLocation));
    });

    map.fitBounds(bounds);
}


/*
 *    HELPER FUNCTIONS
 */


/*
 * @description Adds a bounce animation to the marker when clicked,
 * stops after 1 sec.
 * */

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

/*
 * @description Creates HTML string to display in GMaps InfoWindow.
 * @returns {string} Formatted HTML string.
 * */

function createInfoWindow(location) {
    return "<div id='content'>" +
        "<h3 id='firstHeading' class='firstHeading'>" + location.name + "</h3>" +
        "<p>" + location.address() + "</p>" +
        "<a href='tel:" + location.phone + "'>" + location.phone + "</a><br />" +
        "<a href='" + location.url + "'>" + location.url + "</a>" +
        "</div>";
}


/*
 * UI HELPERS
 */
$('.clk').on('click', function (e) {
    e.stopPropagation();
    $('.main-container').toggleClass('sidebar_shown');
    $('.sidebar').toggleClass('sidebar_shown');
});

$(document).ready(function () {
    // run test on initial page load
    checkSize();

    // run test on resize of the window
    $(window).resize(checkSize);
});

//Function to the css rule
function checkSize() {
    if ($("nav").css("display") == 'none') {
        $('.main-container').removeClass('sidebar_shown');
        $('.sidebar').removeClass('sidebar_shown');
    }
}

/*
 * @description The Starting Point
 */
function startApp() {
    viewModel.loadLocations(FSQ_REQUEST_URL);

    // Subscribe to filteredLocations, change Map Items when it's changed.
    viewModel.filteredLocations.subscribe(function () {
        editMap();
    });
}

startApp();