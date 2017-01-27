var MapModel = function (data) {
    this.title = data.title;
    this.longitude = data.long;
    this.latitude = data.lat;
};

var AppViewModel = function () {
    var Locations = [new MapModel({'title': ''})]
};

$('.clk').on('click', function (e) {
    e.stopPropagation();
    $('.main-container').toggleClass('m_sidebar_shown');
    $('.sidebar').toggleClass('sidebar_shown');
});


function initMap() {
    var uluru = {lat: 30.062208, lng: 31.2157968};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: uluru
    });
    var marker = new google.maps.Marker({
        position: uluru,
        map: map
    });
}
