'use strict';

module.exports = function(app) {
    var pythonController = require('../controllers/pythonController');

    app.route('/python')
        .get(pythonController.executar);
};