$(document).ready(function($) {
    var url = 'http://localhost:5000/api/sense';
    var cnt = 0;

    function init_plot() {
        Plotly.plot('temperature',[{
            y:[0],
            type:'line'
        }]);
        Plotly.plot('humidity',[{
            y:[0],
            type:'line'
        }]);
        Plotly.plot('pressure',[{
            y:[0],
            type:'line'
        }]);
    }

    function plot_data() {
        $.ajax({
            url:url,
            type:"GET",
            dataType:"json",
            success: function(result){
                update_plot(result);
            },
            error: function(error){
                console.log(error);
            }
        });
    }

    function update_plot(data) {
            Plotly.extendTraces('temperature',{ y:[[data.temperature]]}, [0]);
            if(cnt > 10) {
                Plotly.relayout('temperature',{
                    xaxis: {
                        range: [cnt-10,cnt]
                    }
                });
            }

            Plotly.extendTraces('humidity',{ y:[[data.humidity]]}, [0]);
            if(cnt > 20) {
                Plotly.relayout('humidity',{
                    xaxis: {
                        range: [cnt-10,cnt]
                    }
                });
            }

            Plotly.extendTraces('pressure',{ y:[[data.pressure]]}, [0]);
            if(cnt > 20) {
                Plotly.relayout('pressure',{
                    xaxis: {
                        range: [cnt-10,cnt]
                    }
                });
            }
            cnt++;
    }

    init_plot();
    setInterval(function(){
        plot_data();
    },1000);
});

