function datedate(str) { 
    var d = new Date(str);
    var d2 = new Date(d.getTime() + 24*3600*1000);
    return [ 
        [d.getFullYear(), d.getMonth() + 1, d.getDate()], 
        [d2.getFullYear(), d2.getMonth() + 1, d2.getDate()]]; 
}

var rows = [];

require('csv')().from('timeline.csv').transform(function(row) { 
    rows.push(row); 

}).on('end', function() {
    var jsons = rows.map(function(row) { 
        var dd = datedate(row[0]); 
        return {
            startDate: dd[0].join(','), 
            endDate:dd[1].join(','), 
            headline: '',
            text: row[5],
            asset: {
                media: 'http://www.slobodensoftver.org.mk/files/garland_2s.mk_logo_0.png',
                credit:'',
                caption:''
            }
        }; 
    });
    jsons = jsons.slice(1, jsons.length - 2);
    var timeline = {
        headline: '2cmk timeline', 
        type:'default', 
        startDate:'1998', 
        date: jsons,
        text: '',
        asset: {
            media:"http://www.slobodensoftver.org.mk/files/garland_2s.mk_logo_0.png",
            credit:'',
            caption:''
        }
    };
    require('fs').writeFileSync('timeline.json', JSON.stringify({timeline:timeline}));
});
