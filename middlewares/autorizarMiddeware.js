exports.autorizar = function (req, res, next) {
    let token = req.get('token');

    if (token !== '123') {
        res.status(403)
            .send('Acesso negado.')
            .end();
    } else {
        next();
    }
};