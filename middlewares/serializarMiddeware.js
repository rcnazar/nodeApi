var easyxml = require('easyxml');

let xmlSerializer = new easyxml({
    singularize: true,
    rootElement: 'response',
    dateFormat: 'ISO',
    manifest: true
});

exports.serializar = function(req, res, next) {
    res.sendData = function(obj) {
        if (req.accepts('json') || req.accepts('text/html')) {
            res.header('Content-Type', 'application/json');
            res.send(obj);
        } else { //req.accepts('application/xml')
            res.header('Content-Type', 'text/xml');
            var xml = xmlSerializer.render(obj);
            res.send(xml);
        }
    };

    next();
};