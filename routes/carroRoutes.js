'use strict';

module.exports = function(app) {
    var carroController = require('../controllers/carroController');

    app.route('/carros')
        .get(carroController.getAll);
    //     .post(carroController.post);

    // app.route('/carro/:id')
    //     .get(carroController.get)
    //     .put(carroController.update)
    //     .delete(carroController.delete);
};