'use strict';

exports.getAll = function (req, res, next) {
    res.sendData([{"name":"Palio"}]);

    next();
} ;