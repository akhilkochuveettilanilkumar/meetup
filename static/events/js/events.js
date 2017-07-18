// Django csrf token handler
function csrfSafeMethod(method) {
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

function sameOrigin(url) {
      var host = document.location.host; // host + port
      var protocol = document.location.protocol;
      var sr_origin = '//' + host;
      var origin = protocol + sr_origin;

      return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
      (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
      !(/^(\/\/|http:|https:).*/.test(url));
    }

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
         xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
      }
    }
  });

// MAP Handler
function loadMap() {
    var map = new GMap2(document.getElementById("map"));
    map.addControl(new GLargeMapControl());
    map.addControl(new GMapTypeControl());
    //set map center (vienna)
    map.setCenter(new GLatLng(48.1985912972919, 16.367568969726562), 12);
    GEvent.addListener(map, "click", function(overlay, point) {
        map.clearOverlays();
        if (point) {
            map.addOverlay(new GMarker(point));
            map.panTo(point);

            document.getElementById("id_map_lat").value = point.lat(); //models field name 
            document.getElementById("id_map_lon").value = point.lng(); //models field name
        }
    });
}
// arrange for our onload handler to 'listen' for onload events
if (window.attachEvent) {
    window.attachEvent("onload", function() {
        loadMap(); // Internet Explorer
    });
} else {
    window.addEventListener("load", function() {
        loadMap(); // Firefox and standard browsers
    }, false);
}

// Event fetch handler
$("#submit").click(function() {
    $(".error").hide();
    $("#eventResult").empty();
    $(".loader").show();
    var lat = $("#id_map_lat").val();
    var lon = $("#id_map_lon").val();
    var start = $("#startingDate").val();
    var end = $("#endingDate").val();
    if ( (lat.length === 0 ) && 
         (lon.length === 0 ) ) {
        $(".loader").hide();
        $(".error").show();
    } else {
        $.ajax({
            url: '/events/',
            data: {
                'lat': lat,
                'lon': lon,
                'start_date': start,
                'end_date': end,
            },
            type: "POST",
            success: function(data) {
                $(".error").hide();
                $(".loader").hide();
                $("#eventResult").empty();
                data = data['events']
                inner = ''
                modals = ''
                for (i = 0; i < data.length; i++) {
                    var temp = ''
                    var init_modals = ''
                    temp = '<tr>';
                    temp = temp + '<td>' + data[i].name + '</td>';
                    temp = temp + '<td> <a data-toggle="modal" href="#' +
                                    data[i].event_id + '">View </a></td>';
                    temp = temp + '<td>' + data[i].link + '</td>';
                    temp = temp + '<td>' + data[i].start_time + '</td>';
                    temp = temp + '<td>' + data[i].duration + '</td>';
                    if (data[i].fee == null) {
                        temp = temp + '<td> Not Available </td>';
                    } else {
                        temp = temp + '<td>' + data[i].fee + '</td>';
                    }
                    temp = temp + '<td>' + data[i].status + '</td>';
                    temp = temp + '<td>' + data[i].group + '</td>';
                    temp = temp + '<td>' + data[i].address + '</td>';
                    temp = temp + '</tr>'
                    init_modals = `<!-- Modal -->
                        <div id="`+ data[i].event_id +`" class="modal fade" role="dialog">
                          <div class="modal-dialog">

                            <!-- Modal content-->
                            <div class="modal-content">
                              <div class="modal-header">
                                <button type="button" class="close"
                                 data-dismiss="modal">&times;</button>
                                <h4 class="modal-title">Event Description</h4>
                              </div>
                              <div class="modal-body">
                                <p>`+ data[i].description +`</p>
                              </div>
                              <div class="modal-footer">
                                <button type="button" class="btn btn-default close-button"
                                 data-dismiss="modal">Close</button>
                              </div>
                            </div>

                          </div>
                        </div>`
                    inner += temp
                    modals += init_modals
                }
                $("#eventResult").append(inner);
                $("#eventResult").append(modals);
            },
            error: function(data) {
                console.log("dddddddddd");
                $(".loader").hide();
                $(".error").show();
            }
        });
    }
});


$(function() {

    var start = moment().subtract(1, 'days');
    var end = moment();

    function cb(start, end) {
        $('#timerange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }

    $('#timerange').daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);

    cb(start, end);
    
});

$('#timerange').on('apply.daterangepicker' , function(ev, picker) {
      var startingDate = picker.startDate.format('YYYY-MM-DD');
      var endingDate = picker.endDate.format('YYYY-MM-DD');
      console.log(startingDate);
      console.log(endingDate);
      $("#startingDate").val(startingDate);
      $("#endingDate").val(endingDate);
      $( "#submit" ).trigger( "click" );
    });

