console.log('Iniciando');

let express = require('express');
let morgan = require('morgan');
let bodyParser = require('body-parser');
let xmlparser = require('express-xml-bodyparser');
let autorizarMiddleware = require('./middlewares/autorizarMiddeware');
let serializarMiddleware = require('./middlewares/serializarMiddeware');
let carroRoutes = require('./routes/carroRoutes');
let pythonRoutes = require('./routes/pythonRoutes');

let port = 3000;//process.env.PORT || 3000;
let app = express();
module.exports = app;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(xmlparser());
app.use(autorizarMiddleware.autorizar);
app.use(serializarMiddleware.serializar);
//app.use(morgan('combined'));

carroRoutes(app);
pythonRoutes(app);

app.listen(port);

console.log(`Escutando na porta:${port}`);
